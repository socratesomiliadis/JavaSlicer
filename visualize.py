import pandas as pd
from cluster import cluster_statements

def visualize_matrix(usage_table, total_lines):
    unique_keywords = []  # Use a list to maintain order

    # Iterate through the dictionary to maintain the order of insertion
    for keywords in usage_table.values():
        for keyword in keywords:
            if keyword not in unique_keywords:
                unique_keywords.append(keyword)  # Add only if it's not already in the list

    # Create an empty DataFrame with unique keywords as rows and line numbers as columns
    matrix = pd.DataFrame(index=unique_keywords, columns=range(1, total_lines + 1))

    # Fill the DataFrame: mark 'X' where a keyword is found on a specific line
    for line, keywords in usage_table.items():
        for keyword in keywords:
            matrix.at[keyword, line] = 1

    # Replace NaNs with empty strings for better visualization
    matrix.fillna(0, inplace=True)

    # matrix.to_csv('./output/usage_matrix.csv')  # Save as CSV
    # matrix.to_excel('./output/usage_matrix.xlsx')  # Save as Excel
    cluster_statements(matrix, True)
