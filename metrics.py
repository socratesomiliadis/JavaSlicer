MAX_SIZE_DIFF = 0.2
MIN_OVERLAP = 0.1

def not_similar_size(cluster1, cluster2):
    loc_1 = cluster1[1] - cluster1[0] + 1
    loc_2 = cluster2[1] - cluster2[0] + 1
    size_diff = abs(loc_1 - loc_2) / min(loc_1, loc_2)

    return size_diff > MAX_SIZE_DIFF

def significantly_overlapping(cluster1, cluster2):
    overlap = None
    start_1, end_1 = cluster1
    start_2, end_2 = cluster2
    loc_1 = end_1 - start_1 + 1
    loc_2 = end_2 - start_2 + 1

    if start_1 <= start_2 and end_1 >= end_2:
        # cluster2 is fully contained within cluster1
        overlap = abs(end_2 - start_2 + 1)
    elif start_1 >= start_2 and end_1 <= end_2:
        # cluster1 is fully contained within cluster2
        overlap = abs(end_1 - start_1 + 1)
    elif start_1 <= start_2 <= end_1 <= end_2:
        # cluster1 overlaps with cluster2 on the left
        overlap = abs(end_1 - start_2 + 1)
    elif start_2 <= start_1 <= end_2 <= end_1:
        # cluster1 overlaps with cluster2 on the right
        overlap = abs(end_2 - start_1 + 1)
    else:
        overlap = 0

    return overlap / max(loc_1, loc_2) >= MIN_OVERLAP


if __name__ == '__main__':
    pass
