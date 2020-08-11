import unittest
from py_wheels.BinaryTree import *

class TreesTests(unittest.TestCase):
    def setUp(self):
        self.ls = [1, 2, 3, None, None, None, 4]
        self.tree = LevelOrderGenerator(self.ls)

    def test_LevelOrder(self):
        converted_ls = LevelOrderTraversal(self.tree)
        self.assertEqual(self.ls, converted_ls)
    
    def test_preorder(self):
        converted_ls = PreOrderTraversal(self.tree)
        self.assertEqual([1,2,3,4], converted_ls)

    def test_inorder(self):
        converted_ls = InOrderTraversal(self.tree)
        self.assertEqual([2,1,3,4], converted_ls)

    def test_postorder(self):
        converted_ls = PostOrderTraversal(self.tree)
        self.assertEqual([2,4,3,1], converted_ls)

if __name__ == '__main__':
    unittest.main()