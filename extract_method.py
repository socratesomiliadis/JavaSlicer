import javalang
import conditional_nodes_tree as cnt
from visualize import visualize_matrix as vm


# Simple class holding information about variables and method calls
class CodeElement:
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def __hash__(self):
        return hash((self.name, self.line))

    def __eq__(self, other):
        return self.name == other.name and self.line == other.line


def read_java_code_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def count_lines_in_string(s):
    return s.count('\n') + 1 if s else 0


def process_expression(expression, line):
    # Yield the full expression as is
    yield CodeElement(expression, line)

    # Find the index of the first dot
    dot_index = expression.find('.')

    # If there's a dot, split the expression at this dot and process recursively
    if dot_index != -1:
        first_part = expression[:dot_index]
        remainder = expression[dot_index + 1:]  # The rest of the expression after the dot

        # Yield the first part before the dot
        yield CodeElement(first_part, line)

        # Recursively process the remainder of the expression
        yield from process_expression(remainder, line)
    else:
        # If there's no dot, it's the final word, so just yield it
        yield CodeElement(expression, line)


# Handles cases like 'rec[0][j].getName().replace' where array selectors are involved
def build_member_chain(selectors, start_chain):
    member_chain = start_chain

    for selector in selectors:
        if isinstance(selector, javalang.tree.ArraySelector):
            continue  # Skip ArraySelectors
        elif isinstance(selector, (javalang.tree.MemberReference, javalang.tree.MethodInvocation)):
            # When a MemberReference or MethodInvocation follows an ArraySelector
            member_chain += '.' + selector.member  # Append the member to the chain

    return member_chain


# Enhanced function to capture both parts and the whole of member references
def find_nodes(node, node_type):
    line = node.position.line if node.position else None

    if line is not None:
        if isinstance(node, (javalang.tree.MemberReference, javalang.tree.MethodInvocation)):
            if node.selectors:
                yield from process_expression(build_member_chain(node.selectors, node.member), line)
            elif node.qualifier:
                expression = f"{node.qualifier}.{node.member}"
                yield from process_expression(expression, line)
            else:
                yield CodeElement(node.member, line)

        # Handle LocalVariableDeclaration nodes
        if isinstance(node, javalang.tree.LocalVariableDeclaration):
            for declarator in node.declarators:
                yield CodeElement(declarator.name, line)

        # Handle VariableDeclarator nodes (for other types of variable declarations)
        if isinstance(node, javalang.tree.VariableDeclarator):
            yield CodeElement(node.name, line)

    # Recursively process child nodes
    for child in node.children:
        if isinstance(child, (list, set)):
            for subchild in child:
                if isinstance(subchild, javalang.ast.Node):
                    yield from find_nodes(subchild, node_type)
        elif isinstance(child, javalang.ast.Node):
            yield from find_nodes(child, node_type)


# Main function to parse Java method code and output the usage table
def main(java_file_path):
    # Read the Java method code from a file
    java_code = read_java_code_from_file(java_file_path)
    number_of_lines = count_lines_in_string(java_code)

    # Tokenize the Java source code
    tokens = list(javalang.tokenizer.tokenize(java_code))

    # Find the index where the method body begins (after the first '{')
    method_body_start_index = next((index for index, token in enumerate(tokens) if
                                    isinstance(token, javalang.tokenizer.Separator) and token.value == '{'), None)

    # If we found the beginning of a method body
    if method_body_start_index is not None:
        # Adjust the tokens to start from the method body
        tokens = tokens[method_body_start_index:]
        parser = javalang.parser.Parser(tokens)

        try:
            # Attempt to parse the method body
            block_statement = parser.parse_block_statement()

            # Find variable references and method calls within the method body
            nodes = list(find_nodes(block_statement, javalang.tree.MemberReference))

            # Create a dictionary to store where each variable/method (context) is used
            usage_table = {}

            # Populate the usage_table
            for element in nodes:
                if element.line not in usage_table:
                    usage_table[element.line] = set()
                usage_table[element.line].add(element.name)

            # Create the conditional tree
            root_node = cnt.ConditionalNode(-1, 'root', -1)
            # Find the root of the method body and start building the conditional tree
            cnt.find_conditional_nodes(block_statement, root_node, 1)
            # Update the usage table with conditional context
            cnt.update_usage_table_with_conditional_context(root_node, usage_table)

            # Print the result as a simple table
            print(f"{'Line':<5}{'Variables/Methods Accessed/Called':<35}")
            print('-' * 40)
            for line, items in sorted(usage_table.items()):
                print(f"{line:<5}{', '.join(items):<35}")

            # Visualize the result as a matrix
            vm(usage_table, number_of_lines)

        except javalang.parser.JavaSyntaxError as e:
            print("Failed to parse the method body:", e)
        else:
            print("Parsing completed successfully.")


if __name__ == '__main__':
    java_file_path = 'extract_method_sample.java'
    main(java_file_path)
