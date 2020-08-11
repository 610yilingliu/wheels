import unittest
from py_wheels.bst import *
from py_wheels.BinaryTree import *

class bstTest(unittest.TestCase):
    def setUp(self):
        self.btree = bst()
        ls = [90,50,150,20,75,5,66,80,68]
        for num in ls:
            self.btree.InsertNode(num)
    
    def test_Insert(self):
        converted_ls = LevelOrderTraversal(self.btree.root)
        print(converted_ls)

    def test_Delete(self):
        self.btree.DeleteNode(50)
        converted_ls = LevelOrderTraversal(self.btree.root)
        print(converted_ls)