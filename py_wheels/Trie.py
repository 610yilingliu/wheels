import collections

class CharNode:
    def __init__(self):
        self.children = collections.defaultdict(CharNode)
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = CharNode()
    
    def insert(self, word):
        """
        :type word: string
        :rtype: None
        """
        cur = self.root
        for c in word:
            cur = cur.children[c]
        cur.is_word = True
    
    def search(self, word):
        """
        :type word: string
        :rtype: None
        """
        cur = self.root
        for c in word:
            cur = cur.children.get(c)
            if cur is None:
                return False
        return cur.is_word