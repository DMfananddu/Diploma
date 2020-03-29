import nltk_parser

class Tree:
	def __init__(self, kids, nextVar=None, pm=None):
		self.kids = self.val = kids
		self.next = nextVar
        self.punctuation_mark = pm

test_sentence = ['Паша', ',', 'Саша', 'и', 'Вася', 'пошли', 'гулять', '.']

def MPT_forming(sentence):
    t = Tree(Tree)