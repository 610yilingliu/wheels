# Binary Search Tree
from py_wheels.BinaryTree import TreeNode


class bst:
    def __init__(self):
        self.root = None
    
    def Search(self, root, val):
        """
        :type val: int
        :rtype: (bool, TreeNode node, TreeNode parent)
        """
        if not root:
            return False
        if root.val == val:
            return True
        if val < root.val:
            return self.Search(root.left, val)
        return self.Search(root.right, val)
        
    def InsertNode(self, val):
        """
        :type val: int
        :rtype: None
        """
        if not self.root:
            self.root = TreeNode(val)
            return
        r = self.root
        def helper(root, val):
            if root == None:
                root = TreeNode(val)
            elif val < root.val:
                root.left = helper(root.left, val)
            elif val > root.val:
                root.right = helper(root.right, val)
            return root
        self.root = helper(r, val)

    def FindMin(self, node):
        if node.left:
            return self.FindMin(node.left)
        return node.val
    
    def FindMax(self, node):
        if node.right:
            return self.FindMax(node.right)
        return node.val
    
    def DeleteNode(self, val):
        def del_node(root, val):
            if not root:
                return None
            if root.val == val:
                if not root.right:
                    return root.left
                right = root.right
                while right.left:
                    right = right.left
                root.val, right.val = right.val, root.val
            root.left = del_node(root.left, val)
            root.right = del_node(root.right, val)
            return root
            
        r = self.root
        self.root = del_node(r,val)

        