import pandas as pd

def merge_clusters_horizontally(clusters, step):
    if not clusters:
        return []

    merged_clusters = [clusters[0]]
    for current in clusters[1:]:
        last = merged_clusters[-1]
        # Check if the current cluster can be merged with the last one based on the step size
        if current[0] - last[1] <= step:
            # Merge the current cluster with the last one
            merged_clusters[-1] = (last[0], current[1])
        else:
            merged_clusters.append(current)

    # Discard single cell clusters
    merged_clusters = [cluster for cluster in merged_clusters if cluster[0] != cluster[1]]

    # Convert list to set to remove duplicates
    merged_clusters = set(merged_clusters)

    return merged_clusters

def merge_clusters_vertically(clusters):
    # Sort the clusters by their starting points
    clusters_sorted = sorted(clusters, key=lambda x: x[0])

    # Initialize the list for merged clusters
    merged = []

    for cluster in clusters_sorted:
        # If the list is empty or there is no overlap with the last cluster in the list, add the current cluster
        if not merged or merged[-1][1] < cluster[0]:
            merged.append(cluster)
        else:
            # There is an overlap, so we merge the current cluster with the last one in the list
            merged[-1] = (merged[-1][0], max(merged[-1][1], cluster[1]))

    return merged

def find_and_merge_clusters(matrix):
    row_clusters = []
    seen_clusters = set()  # Initialize a set to keep track of all previously seen clusters

    for step in range(1, len(matrix.columns)):
        aggregated_clusters = set()
        for row_idx, row in matrix.iterrows():
            clusters = []
            start = None
            for i, cell in enumerate(row):
                if cell == 1:
                    if start is None:
                        start = i
                else:
                    if start is not None:
                        clusters.append((start, i - 1))
                        start = None
            if start is not None:  # For a cluster that ends at the last cell
                clusters.append((start, len(row) - 1))

            # Merge clusters horizontally based on the step condition
            merged_clusters = merge_clusters_horizontally(clusters, step)
            # Append only if it's not an empty list
            if merged_clusters:
                aggregated_clusters.update(merged_clusters)

        # Merge overlapping clusters vertically to form larger clusters
        merged_clusters = merge_clusters_vertically(aggregated_clusters)
        # Append only if it's not an empty list
        if merged_clusters:
            aggregated_clusters.update(merged_clusters)

        if row_clusters:
            # Remove clusters that have been seen in previous sets
            new_clusters = aggregated_clusters.difference(seen_clusters)
            row_clusters.append(new_clusters)

            # Update the set of all previously seen clusters with the new clusters
            seen_clusters.update(new_clusters)
        else:
            # For the first set, just add it directly since there are no previous clusters to compare with
            row_clusters.append(aggregated_clusters)
            seen_clusters.update(aggregated_clusters)

    return row_clusters

def cluster_statements(matrix, output=False):
    clusters = find_and_merge_clusters(matrix)
    if output:
        for row_idx, row in enumerate(clusters):
            if row:
                print(f"Step = {row_idx + 1}: {row}")
            else:
                print(f"Step = {row_idx + 1}: No new clusters found")


if __name__ == '__main__':
    data = pd.read_csv('./output/usage_matrix.csv', index_col=0)
    cluster_statements(data, True)
