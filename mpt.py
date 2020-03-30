# import nltk_parser

class Tree:
	def __init__(self, value=None, nextVariant=None, kids=None):
		self.value = value
		self.brother = nextVariant
		self.kids = kids
        
test_sentence = [['Павел', 'Павлуша'], [','], ['Александр', 'Алекс'], ['и', 'а', 'о'], ['Василий'], ['пошли'], ['гулять'], ['.']]

def MPT_forming(sentence):
	sl = len(sentence)
	globalTree = Tree()
	globalTree.kids = MPT_hierarchy_forming(globalTree.kids, sentence, 0)
	return globalTree

def MPT_hierarchy_forming(tree, sentence, idx):
	tree = Tree()
	tree.kids = Tree()
	var_count = len(sentence[idx])
	bufLevelTree = Tree(sentence[idx][-1], None, tree.kids)
	for j in range(var_count-2, -1, -1):
		bufLevelTree = Tree(sentence[idx][j], bufLevelTree, tree.kids)
	tree = bufLevelTree
	if idx != len(sentence)-1:
		MPT_hierarchy_forming(tree.kids, sentence, idx+1)
	return tree

test_tree = MPT_forming(test_sentence)
print(test_tree.kids.value, test_tree.kids.kids, test_tree.kids.brother)