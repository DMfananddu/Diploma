class Vertex:
    def __init__(self, word=None, tag=None, attribute=None):
        # атрибуты
        self.word = word # само слово
        self.attribute = attribute # название члена предложения
        self.tag = tag # ТЭГ (OpencorporaTag('PRTS,perf,past,pssv masc,sing'))

class MetaVertex:
    def __init__(self, word=None, tag=None, attribute=None,
                 vertices=None, meta_vertices=None, edges=None, meta_edges=None):
        # атрибуты
        self.word = word # само слово
        self.attribute = attribute # название члена предложения
        self.tag = tag # ТЭГ (OpencorporaTag('PRTS,perf,past,pssv masc,sing'))
        # внутренние элементы
        self.vertices = vertices # набор вершин метавершины (list адресов)
        self.meta_vertices = meta_vertices # набор метавершин метавершины (list адресов)
        self.edges = edges # набор ребер метавершины (list адресов)
        self.meta_edges = meta_edges # набор метаребер метаграфа (list адресов)

class Edge:
    def __init__(self, start_vertex=None, end_vertex=None, conjuction=None, punctuation_mark=None):
        self.start_vertex = start_vertex # адрес исходной вершины
        self.end_vertex = end_vertex # адрес конечной вершины
        self.edge_orientation = False # направленность вершины
        # attributes
        self.conjuction = conjuction # союз (в неизменном виде элемента поступившего массива)
        self.punctuation_mark = punctuation_mark # знак препинания (просто лексема)

class MetaGraph:
    def __init__(self, sentence=None, paragraph_number=None, sentence_number=None,
                 vertices=None, meta_vertices=None, edges=None, meta_edges=None):
        # атрибуты
        self.sentence = sentence # текст предложения
        self.paragraph_number = paragraph_number # номер параграфа в тексте
        self.sentence_number = sentence_number # номер предложения в параграфе
        # внутренние элементы
        self.vertices = vertices # набор вершин метаграфа (list адресов)
        self.meta_vertices = meta_vertices # набор метавершин метаграфа (list адресов)
        self.edges = edges # набор ребер метаграфа (list адресов)
        self.meta_edges = meta_edges # набор метаребер метаграфа (list адресов)





































from nltk import tokenize
from rusenttokenize import ru_sent_tokenize
testText = "Я: она, ты."

# sent = tokenize.sent_tokenize(testText, language="russian")
# print(sent)
# sent = ru_sent_tokenize(testText)
# print(sent)
# words = tokenize.word_tokenize(sent[0], language="russian")
# print(words)
# print(ord("—"), ord("-"), ord(":"))

import MySQLdb

conn = MySQLdb.connect("localhost", "root", "SO08051897fya", "syntax_analyze", charset="utf8", init_command="SET NAMES UTF8")
cursor = conn.cursor()

cursor.execute("SELECT * FROM rule")

# Получаем данные.
row = cursor.fetchone()
while True:
    row = cursor.fetchone()
    if row is None:
        break
    print(row)

 
# Разрываем подключение.
conn.close()
