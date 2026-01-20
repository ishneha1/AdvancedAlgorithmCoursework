"""
Minimum Service Centers - Procedural Greedy DFS

This implementation uses a post-order traversal (bottom-up) with three states:
- 0: Node is NOT covered
- 1: Node HAS a service center
- 2: Node is covered (by child or parent) but HAS NO center

Algorithm runs in O(N) time and O(H) space (recursion depth).
"""

from collections import deque


class TreeNode:
    """Binary tree node."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree_from_level_list(level_list):
    """
    Build binary tree from level-order list where `None` indicates missing node.
    Returns root TreeNode or None.
    """
    if not level_list:
        return None
    it = iter(level_list)
    root_val = next(it)
    if root_val is None:
        return None
    root = TreeNode(root_val)
    queue = deque([root])
    for val in it:
        node = queue.popleft()
        # left child
        if val is not None:
            node.left = TreeNode(val)
            queue.append(node.left)
        # right child
        try:
            val = next(it)
        except StopIteration:
            break
        if val is not None:
            node.right = TreeNode(val)
            queue.append(node.right)
    return root


def min_service_centers(root):
    """
    Return minimum number of service centers so that every node is covered.

    Uses greedy DFS with states 0/1/2 defined above. We do post-order traversal
    and decide placement based on children's states:
      - If any child is 0 (not covered) -> we must place center here (state 1)
      - Else if any child is 1 (has center) -> this node is covered (state 2)
      - Else -> node is not covered (state 0)

    After DFS, if root is 0, add one center.
    """
    SERVICE = 1  # node has a center
    NOT_COVERED = 0
    COVERED = 2

    service_centers_count = 0

    def dfs(node):
        nonlocal service_centers_count
        if node is None:
            # Null nodes are considered covered to avoid placing centers on parents of absent children
            return COVERED
        left_child_state = dfs(node.left)
        right_child_state = dfs(node.right)

        # If any child is not covered, we must place a center here
        if left_child_state == NOT_COVERED or right_child_state == NOT_COVERED:
            service_centers_count += 1
            return SERVICE

        # If any child has a center, this node is covered
        if left_child_state == SERVICE or right_child_state == SERVICE:
            return COVERED

        # Otherwise, this node is not covered
        return NOT_COVERED

    root_state = dfs(root)
    if root_state == NOT_COVERED:
        service_centers_count += 1
    return service_centers_count


if __name__ == "__main__":
    # Test tree: {0, 0, null, 0, null, 0, null, null, 0}
    # Interpreted as level-order list: [0,0,None,0,None,0,None,None,0]
    level_order = [0, 0, None, 0, None, 0, None, None, 0]
    root = build_tree_from_level_list(level_order)
    result = min_service_centers(root)
    print("Procedural Greedy Result:", result)
    print("Expected: 2")

    print("Test Case 2 (Balanced tree):")
    level_order2 = [0, 1, 2, 3, 4, 5, 6]
    root2 = build_tree_from_level_list(level_order2)
    result2 = min_service_centers(root2)
    print("Procedural Greedy Result:", result2)
    print("Expected: 2")
    print("Explanation: Centers at nodes 1 and 2 cover all nodes")
    print("  - Node 1 covers: 0, 1, 3, 4")
    print("  - Node 2 covers: 2, 5, 6")


