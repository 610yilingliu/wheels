import unittest
from py_wheels.Trie import * 

class Trietest(unittest.TestCase):
    def setUp(self):
        self.words = ["words","word", "wire", "abcd", "wife"]
        self.t = Trie()
        for w in self.words:
            self.t.insert(w)

    def test_findword(self):
        self.assertTrue(self.t.search("wife"))
        self.assertFalse(self.t.search("w"))
        self.assertFalse(self.t.search("wifi"))