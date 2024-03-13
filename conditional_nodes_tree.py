import javalang


class ConditionalNode:
    def __init__(self, line, statement_type, hierarchy_level, parent=None):
        self.line = line  # The line number where this statement starts
        self.statement_type = statement_type  # 'if', 'else-if', or 'else'
        self.parent = parent  # The parent node
        self.children = []  # A list of child nodes
        self.hierarchy_level = hierarchy_level  # The level of this node in the tree

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"{self.statement_type} (level {self.hierarchy_level} | line {self.line})"


def find_conditional_nodes(node, current_node, hierarchy_level, is_part_of_else=False):
    if isinstance(node, javalang.tree.IfStatement):
        # Determine the type of the statement: 'if', 'else-if'
        statement_type = 'else-if' if is_part_of_else else 'if'
        new_node = ConditionalNode(node.position.line, statement_type, hierarchy_level, parent=current_node)

        if current_node:
            current_node.add_child(new_node)

        # Recursively process the 'then' part of the if statement
        find_conditional_nodes(node.then_statement, new_node, hierarchy_level + 1)

        # Process 'else' part if it exists
        if node.else_statement:
            if isinstance(node.else_statement, javalang.tree.IfStatement):
                # It's an 'else if'. Process it as a new if statement but keep the same parent.
                # Pass True for is_part_of_else because it's part of an 'else' clause.
                find_conditional_nodes(node.else_statement, current_node, hierarchy_level, is_part_of_else=True)
            else:
                # It's an 'else'. Create a new node for this else statement.
                else_node = ConditionalNode(node.else_statement.position.line, 'else', hierarchy_level,
                                            parent=current_node)
                current_node.add_child(else_node)
                find_conditional_nodes(node.else_statement, else_node, hierarchy_level + 1)
    else:
        # General case for traversing the AST: handle lists of nodes and single nodes
        if isinstance(node, javalang.ast.Node):
            for child in node.children:
                if isinstance(child, javalang.ast.Node):
                    find_conditional_nodes(child, current_node, hierarchy_level)
                elif isinstance(child, list) or isinstance(child, set):
                    for subchild in child:
                        find_conditional_nodes(subchild, current_node, hierarchy_level)
        elif isinstance(node, list) or isinstance(node, set):
            for child in node:
                find_conditional_nodes(child, current_node, hierarchy_level)


# Function to update the usage table with conditional context
# "if" statement context is propagated to "else-if" and "else" statements and their children
def update_usage_table_with_conditional_context(node, usage_table):
    context_stack = []

    def traverse(node):
        if not node:
            return

        # Retrieve the current line's context from the usage table
        current_vars_methods = usage_table.get(node.line, set())

        if node.statement_type == 'if':
            # If it's an 'if' node and while's condition is true, we've reached a new if block and should
            # pop the stack until we reach the 'if' node's hierarchy level, thus removing the context of
            # the previous neighboring if/else-if/else blocks
            while len(context_stack) >= node.hierarchy_level:
                context_stack.pop()
            if context_stack:
                usage_table[node.line] = current_vars_methods.union(*context_stack)
            context_stack.append(current_vars_methods)
        elif node.statement_type == 'else-if':
            # If it's an 'else-if' node, retrieve the top of the stack and add its context to the current line's context
            if context_stack:
                usage_table[node.line] = current_vars_methods.union(*context_stack)
            # Augment the top of the stack with the current line's context
            context_stack[-1] = context_stack[-1].union(current_vars_methods)
        elif node.statement_type in ['else']:
            # If it's an 'else' node, add the parent's context to the current line's context
            if context_stack:
                usage_table[node.line] = current_vars_methods.union(*context_stack)

        # Iterate through the children of the current node recursively
        for child in node.children:
            traverse(child)

    traverse(node)  # Start the traversal with the root node
