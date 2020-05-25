attributes_names = {
    1: "Предложение",
    2: "Подлежащие",
    3: "Сказуемое",
    4: "Дополнение",
    5: "Определение",
    6: "Обстоятельство",
    7: "Служебное"
}


class Vertex:
    def __init__(self, word=None, tag=None, attribute=None):
        # атрибуты
        self.word = word # само слово (оштрафован)
        self.attribute = attribute # название члена предложения
        self.tag = tag # ТЭГ (OpencorporaTag('PRTS,perf,past,pssv masc,sing'))

    def __str__(self):
        return f"Слово: {self.word}\tЧлен предложения: {self.attribute}\tТэг слова: {self.tag}\n"


class MetaVertex:
    def __init__(self, word=None, tag=None, attribute=None, vertices=None, meta_vertices=None, edges=None, meta_edges=None):
        # атрибуты
        self.word = word # само слово (оштрафован)
        self.attribute = attribute # название члена предложения
        self.tag = tag # ТЭГ (OpencorporaTag('PRTS,perf,past,pssv masc,sing'))
        # внутренние элементы
        self.vertices = vertices # набор вершин метавершины (list адресов)
        self.meta_vertices = meta_vertices # набор метавершин метавершины (list адресов)
        self.edges = edges # набор ребер метавершины (list адресов)
        self.meta_edges = meta_edges # набор метаребер метавершины (list адресов)
    
    def __str__(self):
        res_str = f"Слово: {self.word}\tЧлен предложения: {self.attribute}\nТэг слова: {self.tag}\n"
        # res_str += f"Содержимое рёбер метавершины:\n"
        # for key in self.edges:
            # res_str += f"Ребро связывает {key[0]} и {key[1]} слова предложения.\n"
            # res_str += f"Содержимое ребра Метавершины:\n{self.edges[key]}\n"
        for key in sorted(self.vertices):
            res_str += f"{key}-е слово имеет содержимое:\n"
            res_str += f"{self.vertices[key]}\n"
        return res_str


class Edge:
    def __init__(self, start_vertex=None, end_vertex=None, conjuction=None, punctuation_mark=None):
        self.start_vertex = start_vertex # адрес исходной вершины
        self.end_vertex = end_vertex # адрес конечной вершины
        self.edge_orientation = False # направленность вершины
        # attributes
        self.conjuction = conjuction # союз (в неизменном виде элемента поступившего массива)
        self.punctuation_mark = punctuation_mark # знак препинания (просто лексема)
    
    def __str__(self):
        res_str = f"Ребро содержит следующий подчинительный союз: {self.conjuction}\n"
        res_str += f"Ребро содержит следующий знак препинания: {self.punctuation_mark}\n"
        # res_str += f"Главная вершина:\n{self.start_vertex}\nПодчинённая вершина:\n{self.end_vertex}\n"
        return res_str


class MetaGraph:
    def __init__(self, sentence=None, paragraph_number=None, sentence_number=None, vertices=None, meta_vertices=None, edges=None, meta_edges=None):
        # атрибуты
        self.sentence = sentence # текст предложения
        self.paragraph_number = paragraph_number # номер параграфа в тексте
        self.sentence_number = sentence_number # номер предложения в параграфе
        # внутренние элементы
        self.vertices = vertices # набор вершин метаграфа (list адресов)
        self.meta_vertices = meta_vertices # набор метавершин метаграфа (list адресов)
        self.edges = edges # набор ребер метаграфа (list адресов)
        self.meta_edges = meta_edges # набор метаребер метаграфа (list адресов)

    def __str__(self):
        res_str = f"Проанализировано {self.sentence_number}-е предложение {self.paragraph_number}-го параграфа.\n"
        res_str += f"Текст предложения: {self.sentence}\n\n"
        for key in self.edges:
            res_str += f"Ребро связывает {key[0]} и {key[1]} части предложения, их {key[2]} и {key[3]} варианты.\n"
            res_str += f"Содержимое ребра Метаграфа:\n{self.edges[key]}\n"
        for key in self.meta_vertices:
            res_str += f"{key}-я часть предложения имеет содержимое:\n"
            for i in range(len(self.meta_vertices[key])):
                res_str += f"{self.meta_vertices[key][i]}\n"
        return res_str


def metagraphMaker(sent_metagraph, to_MM, pncts, prgf_number, sent_number, parts_count, sent_parts_vars_count):
    # to_MM: res_mains, res_subs, conjs, separators, inputSentence
    # res_subs: слово; тэг; номер параграфа, предложения, части, варианта; номер в части; ID вид СГ, ID член предложения, ID правила, ID главного слова
    sent_metavertexes = dict()
    sent_edges = dict()
    for part_idx in range(parts_count):
        part_metavertexes = []
        for i in range(len(to_MM)):
            if to_MM[i][1][0][4] == part_idx:
                words_count = len(to_MM[i][1])
                words = dict()
                edges = dict()
                # создаем вершины
                for sw_idx in range(words_count):
                    sub_word = to_MM[i][1][sw_idx]
                    if sub_word[1]:
                        # добавление вершины в словарь сершин
                        words[sub_word[6]] = Vertex(sub_word[0], sub_word[1], attributes_names[sub_word[8]])
                # создаем ребра, а затем метавершину варианта
                for sw_idx in range(words_count):
                    sub_word = to_MM[i][1][sw_idx]
                    if sub_word[1]:
                        # sub_word_number, main_word_number
                        sub_word_number = sub_word[6]
                        main_word_number = None
                        if sub_word[10] is not None:
                            main_word_number = to_MM[i][0][sub_word[10]][6]
                            # добавление ребра в словарь рёбер
                            edges[(main_word_number, sub_word_number)] = makeEdge(to_MM[i], main_word_number, sub_word_number, words[main_word_number], words[sub_word_number], pncts)
                    else:
                        # метавершина грамматической основы == метавершина части
                        part_metavertexes.append(MetaVertex(sub_word[0], None, attributes_names[sub_word[8]], words, None, edges, None))
        # запоминание всех вариантов части в виде элемента словаря по ключу
        sent_metavertexes[part_idx] = part_metavertexes
        # соединение метавершин частей предложения посредством рёбер
        conjs = to_MM[0][2] # союзы, остались только подчинительные межчастные
        separators = to_MM[0][3] # положения разделителей, подч. союзов
        if part_idx != 0:
            for curr_part_var_idx in range(len(sent_metavertexes[part_idx])):
                edge_conj, edge_pnct, main_part_number = mgEdgeConjPnctFinding(conjs, pncts, part_idx, separators)
                for prev_part_var_idx in range(len(sent_metavertexes[main_part_number])):
                    # ключ словаря: номер 1й и 2й частей, номер вара из 1й и 2й частей
                    sent_edges[(main_part_number, curr_part_var_idx, prev_part_var_idx, curr_part_var_idx)] = Edge(sent_metavertexes[main_part_number][prev_part_var_idx], sent_metavertexes[part_idx][curr_part_var_idx], edge_conj, edge_pnct)
    sent_metagraph = MetaGraph(to_MM[0][4]["sentence"], prgf_number, sent_number, None, sent_metavertexes, sent_edges, None)
    print(sent_metagraph)
    return sent_metagraph


def mgEdgeConjPnctFinding(conjs, pncts, sub_part_number, separators):
    edge_conj = []
    edge_pnct = []
    finish = separators[sub_part_number]
    for conj in conjs:
        if len(conj) > 1:
            for el in conj:
                if el[0] == finish:
                    edge_conj = [conj[0], el]
                    main_part_number = separators.index(conj[0][0])
        else:
            if conj[0][0] == finish:
                edge_conj = conj[0]
                main_part_number = sub_part_number - 1
    start = separators[main_part_number]
    for i in range(len(pncts)):
        # print("sent", pncts[i], start, finish)
        if start < pncts[i][0] < finish:
            edge_pnct = pncts[i]
            pncts.pop(i)
            break
    return edge_conj, edge_pnct, main_part_number


def makeEdge(to_MM, main_word_number, sub_word_number, mainV, subV, pncts):
    # to_MM: res_mains, res_subs, conjs, separators, inputSentence
    start = min(main_word_number, sub_word_number)
    finish = max(main_word_number, sub_word_number)
    edge_conj = None
    edge_pnct = None
    for conj in to_MM[2]:
        for el in conj:
            if start < el[0] < finish:
                edge_conj = el
                conj.pop(conj.index(el))
                if conj == []:
                    to_MM[2].pop(to_MM[2].index(conj))
                break
    for pnct in pncts:
        # print("part", pnct, start, finish)
        if start < pnct[0] < finish:
            edge_pnct = pnct
            pncts.pop(pncts.index(pnct))
            break
    edge = Edge(mainV, subV, edge_conj, edge_pnct)
    return edge


""" НЕ ИСПОЛЬЗУЕТСЯ
class MetaEdge(Edge):
    def __init__(self):
        super().__init__()
        # внутренние элементы
        self.vertices = None # набор вершин метаребра (list адресов)
        self.meta_vertices = None # набор метавершин метаребра (list адресов)
        self.edges = None # набор ребер метаребра (list адресов)
        self.meta_edges = None # набор метаребер метаребра (list адресов)
"""
