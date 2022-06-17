"""
Some community detection algorithms output the community number based on a semantical meaning defined by it
But in order to construct our intra and inter graphs with overlapping and non-overlapping nodes, we need to
organize our community number ordering from 0 to n-1 communities

For example, SLPA algorithm outputs dictionary communities c, like partition dictionary where:
        1. Key = community number
        2. Value = nodes within that community
        But, the community numbering is unordederd
        --> So we organize the ordering in dictionary `partition`
"""


def orderCommunities(c):
    # We index each community starting from 0 and put them in list keys_partition
    # So, if we have 11 communities, then the indexing list keys_partition = [0,1,2,3,4,5,6,7,8,9,10]
    # Use `j` to move till the length of c and iterate `i` = i+1 to organize the community numbering
    # say it is #20, as index 0 and the second community, say #49 as index 1, etc...
    i = 0
    keys_partition = list()
    for j in c:
        keys_partition.append(i)
        i = i + 1

    # Then for each index i aka for each community, we will create a dictionary partition where i is the key
    partition = dict()
    for i in keys_partition:
        partition[i] = []

    # Now we have to fill the partition dictionary
    i = 0
    for j in c:  # for each community j in c
        for k in c[j]:  # for each node in community c
            partition[i].append(k)  # for partition i (organized), append the nodes in this community
        i = i + 1

    return partition


def communityInfo(c, partition):
    print('Number of partitions: ', len(partition))
    l = list()
    for i in c:  # for all communities i in c
        for j in c[i]:  # for all nodes in communities c[i]
            l.append(j)  # add the nodes to l

    print('Number of nodes in the communities detected: ', len(l))

    s = set(l)  # removes repetitive nodes since set() involves only unique inputs
    print('Number of repetitions: ', len(l) - len(s))
    print()
    print()


