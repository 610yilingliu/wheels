# Convert a list to tree structure in level-order traversal
# Example:
# in: 
#       [1, 2, 3, None, None, None, 4]
# out:
#       1
#      / \
#     2   3
#          \
#           4
import collections

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def LevelOrderGenerator(ls):
    """
    :type ls:List[object]
    :rtype TreeNode
    """
    if not ls:
        return None
    root = TreeNode(ls[0])
    q = collections.deque([root])
    l = len(ls)
    pos = 1
    while pos < l:
        node = q.popleft()
        # if node is None, do not connect it with anything
        if node:
            node.left = TreeNode(ls[pos]) if ls[pos] is not None else None
            q.append(node.left)
            if pos + 1 < l:
                node.right = TreeNode(ls[pos + 1]) if ls[pos + 1] is not None else None
                q.append(node.right)
                pos += 1
            pos += 1
    return root
        

def LevelOrderTraversal(root):
    """
    :type root: TreeNode
    :rtype List[object]
    """
    if not root:
        return []
    ls = []
    q = collections.deque([root])
    while q:
        curroot = q.popleft()
        if curroot == None:
            ls.append(curroot)
            continue
        ls.append(curroot.val)
        q.append(curroot.left)
        q.append(curroot.right)
    while ls[-1] == None:
        ls.pop()
    return ls
    

def PreOrderTraversal(root):
    """
    :type root: TreeNode
    :rtype List[object]
    """
    if not root:
        return []
    ans = []
    def helper(root):
        if not root:
            return
        ans.append(root.val)
        helper(root.left)
        helper(root.right)
    helper(root)
    return ans

def InOrderTraversal(root):
    """
    :type root: TreeNode
    :rtype List[object]
    """
    if not root:
        return []
    ans = []
    def helper(root):
        if not root:
            return
        helper(root.left)
        ans.append(root.val)
        helper(root.right)
    helper(root)
    return ans

def PostOrderTraversal(root):
    """
    :type root: TreeNode
    :rtype List[object]
    """
    if not root:
        return []
    ans = []
    def helper(root):
        if not root:
            return
        helper(root.left)
        helper(root.right)
        ans.append(root.val)
    helper(root)
    return ans
