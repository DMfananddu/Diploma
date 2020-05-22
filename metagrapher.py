"""
Виды синтаксических группы
1, Существительная группа
2, Прилагательная группа
3, Кратко-прилагательная группа
4, Компаративная группа
5, Числительная группа
6, Местоименная группа
7, Глагольная группа
8, Инфинитивная группа
9, Причастная группа
10, Кратко-причастная группа
11, Деепричастная группа
12, Наречная группа
13, Частичная группа
14, Предложная группа

Члены предложения
1, Предложение
2, Подлежащее
3, Сказуемое
4, Дополнение
5, Определение
6, Обстоятельство
7, Служебное
"""


"""
Наступило лето.
mains
subs
['лето', OpencorporaTag('NOUN,inan,neut,Sgtm sing,nomn'), 0, 0, 0, 1, 1, None, 2, 5, None]
['Наступило', OpencorporaTag('VERB,perf,intr neut,sing,past,indc'), 0, 0, 0, 1, 0, 7, 3, 6, None]
['лето_Наступило', None, 0, 0, 0, 1, None, None, 1, 7, None]

Сегодня лил сильный дождь.
mains
слово; тэг; номер параграфа, предложения, части, варианта; номер в части; вид СГ
['дождь', OpencorporaTag('NOUN,inan,masc sing,accs'), 0, 0, 0, 3, 3, 1]
['лил', OpencorporaTag('VERB,impf,tran masc,sing,past,indc'), 0, 0, 0, 3, 1, 7]
subs
слово; тэг; номер параграфа, предложения, части, варианта; номер в части; ID вид СГ, ID член предложения, ID правила, ID главного слова
['сильный', OpencorporaTag('ADJF,Qual inan,masc,sing,accs'), 0, 0, 0, 3, 2, 2, 5, 3, 0]
['дождь', OpencorporaTag('NOUN,inan,masc sing,accs'), 0, 0, 0, 3, 3, 1, 4, 4, 1]
['Сегодня', OpencorporaTag('ADVB'), 0, 0, 0, 3, 0, None, 2, 5, None]
['лил', OpencorporaTag('VERB,impf,tran masc,sing,past,indc'), 0, 0, 0, 3, 1, 7, 3, 6, None]
['Сегодня_лил', None, 0, 0, 0, 3, None, None, 1, 7, None]

Отдыхающий насорил на пляже, поэтому был оштрафован.
Отдыхающий насорил на пляже,
mains
слово; тэг; номер параграфа, предложения, части, варианта; номер в части; вид СГ
['пляже', OpencorporaTag('NOUN,inan,masc sing,loct'), 0, 0, 0, 0, 3, 1]
['насорил', OpencorporaTag('VERB,perf,intr masc,sing,past,indc'), 0, 0, 0, 0, 1, 7]
subs
слово; тэг; номер параграфа, предложения, части, варианта; номер в части; ID вид СГ, ID член предложения, ID правила, ID главного слова
['на', OpencorporaTag('PREP'), 0, 0, 0, 0, 2, 14, 7, 0, 0]
['пляже', OpencorporaTag('NOUN,inan,masc sing,loct'), 0, 0, 0, 0, 3, 1, 4, 4, 1]
['Отдыхающий', OpencorporaTag('PRTF,Subx,impf,intr,pres,actv masc,sing,nomn'), 0, 0, 0, 0, 0, None, 2, 5, None]
['насорил', OpencorporaTag('VERB,perf,intr masc,sing,past,indc'), 0, 0, 0, 0, 1, 7, 3, 6, None]
['Отдыхающий_насорил', None, 0, 0, 0, 0, None, None, 1, 7, None]
поэтому был оштрафован.
mains
слово; тэг; номер параграфа, предложения, части, варианта; номер в части; вид СГ
['был', OpencorporaTag('VERB,impf,intr masc,sing,past,indc'), 0, 0, 1, 0, 1, 7]
subs
слово; тэг; номер параграфа, предложения, части, варианта; номер в части; ID вид СГ, ID член предложения, ID правила, ID главного слова
['оштрафован', OpencorporaTag('PRTS,perf,past,pssv masc,sing'), 0, 0, 1, 0, 2, 10, 3, 1, 0]
['поэтому', OpencorporaTag('ADVB'), 0, 0, 1, 0, 0, 12, 6, 2, 0]
['был', OpencorporaTag('VERB,impf,intr masc,sing,past,indc'), 0, 0, 1, 0, 1, 7, 3, 6, None]
['_был', None, 0, 0, 1, 0, None, None, 1, 7, None]
"""


class MetaVertex(Vertex):
    def __init__(self):
        super().__init__()
        self.paragraph_number = None # номер параграфа в тексте
        self.sentence_number = None # номер предложения в параграфе
        self.sp_number = None # номер части в предложении
        self.vertices = None # набор вершин метаграфа (list адресов)
        self.meta_vertices = None # набор вметаершин метаграфа (list адресов)
        self.edges = None # набор ребер метаграфа (list адресов)
        self.meta_edges = None # набор метаребер метаграфа (list адресов)


class Vertex:
    def __init__(self):
        self.word = None # само слово (оштрафован)
        self.tag = None # ТЭГ (OpencorporaTag('PRTS,perf,past,pssv masc,sing'))
        self.number_in_sp = None # номер в части предложения
        self.sg_kind_id = None # вид синтаксической группы (1 - ID Существительнрй группы)
        self.attribute_name = None # название члена предложения
        self.rule_id = None


def metagraphMaker(res_mains, res_subs, conjs, inputSentence):
    # print(inputSentence)
    # print("mains")
    # for i in res_mains:
    #     print(i)
    # print("subs")
    # for i in res_subs:
    #     print(i)
    # print(conjs)
    return