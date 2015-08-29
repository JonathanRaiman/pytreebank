cdef dict get_depth_sorted_children(list children):
    cdef dict branch_with_depth = {}
    cdef int i = 0
    cdef int children_len = len(children)
    cdef int max_depth = 0
    for i in range(children_len):
        if children[i].depth in branch_with_depth:
            branch_with_depth[children[i].depth].append(children[i])
        else:
            branch_with_depth[children[i].depth] = [children[i]]
        if max_depth < children[i].depth:
            max_depth = children[i].depth
    branch_with_depth[-1] = max_depth
    return branch_with_depth

def depth_sorted_children(tree):
    return get_depth_sorted_children(tree.general_children)
