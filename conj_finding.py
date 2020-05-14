from reader import gettingData
from normal_parser import parsing
from copy import deepcopy


# получение списка союзов из специального файла в удобочитаемом виде
all_conjs = []

f = open("Conjunction_kinds.TXT", encoding="UTF-8").readlines()
conj_kinds = []
conj_kind_flag = False
for line in f:
    elem = line.strip("\n").strip("\t")
    if elem == "Подчинительные:":
        conj_kind_flag = True
    elif elem[-1] != ":":
        new_elem = [elem]
        if not conj_kind_flag:
            new_elem.append("Сочинительный")
        else:
            new_elem.append("Подчинительный")
        if new_elem not in all_conjs:
            all_conjs.append(new_elem)

all_conjs.sort()
conj_count = len(all_conjs)
for i in range(conj_count):
    if "...," in all_conjs[i][0]:
        conj1 = all_conjs[i][0].split("..., ")[0]
        conj2 = all_conjs[i][0].split("..., ")[1]
        all_conjs[i] = [conj1.split(), conj2.split(), all_conjs[i][1]]
    else:
        all_conjs[i] = [all_conjs[i][0].split(), "", all_conjs[i][1]]

all_unique_conjs = []
for i in range(conj_count):
    if all_conjs[i] != all_conjs[i-1]:
        all_unique_conjs.append(all_conjs[i])
        # print(all_conjs[i])

def sentenceConjFinding(inputSentence):
    # список всех возможных вариантов любых союзов, 
    # которые могут начинаться на какой-либо лексеме входного предложения
    possible_conjs = []
    # список вариантов союзов предложения
    # он должен заполнятсья только теми видами союзов, союзами и
    # индексами начала этих союзов в предложении,
    # которые реально есть в данном предложении
    curr_conjs = []
    for l in inputSentence["lexems"]:
        # все лексемы к нижнему регистру, чтобы "Чем" и "чем" были одинаковыми лексемами 
        wanted_lexem = l["lexem"].lower()
        # все союзы, которые могут начинаться на данной лексеме
        lexem_conjs = []
        for conj in all_conjs:
            if conj[0][0] == wanted_lexem:
                lexem_conjs.append(conj)
        possible_conjs.append(lexem_conjs)
    # кол-во лексем в предложении
    lexem_count = len(possible_conjs)
    for i in range(lexem_count):
        if len(possible_conjs[i]) != 0:
            # длина списка вариантов
            len_сvl = len(possible_conjs[i])
            # первая лексема союза в предложении
            wanted_lexem = inputSentence["lexems"][i]["lexem"]
            # проход по всем вариантам
            for j in range (len_сvl):
                # рассматриваемый вариант союза
                wanted_conj = possible_conjs[i][j][0]
                # рассматриваемый вид союза
                wanted_conj_kind = possible_conjs[i][j][2]
                # длина союза в лексемах
                len_wanted_conj1 = len(wanted_conj)
                # если длина предполагаемого союза не выводит за пределы предложения, 
                if i + len_wanted_conj1 < lexem_count:
                    # мы рассматриваем j-й вариант
                    for k in range(1, len_wanted_conj1):
                        if inputSentence["lexems"][i+k]["lexem"] != wanted_conj[k]:
                            break
                    else: # нашли нужный союз
                        # который и т.п. союзы - исключение - рассматриваем отдельно
                        if wanted_conj[0][:5] != "котор" and i != 0 and inputSentence["lexems"][i-1]["lexem"] != "," and wanted_conj_kind == "Подчинительный" and possible_conjs[i][j][1] == '':
                            continue
                        curr_conjs.append([[i, wanted_conj_kind, wanted_conj]])
                        second_conj_part_accepted = False
                        # отдельный поиск второй части раздельно-составного союза по тому же плану
                        if possible_conjs[i][j][1] != '' and (i == 0 or inputSentence["lexems"][i-1]["lexem"] == ","):
                            # разыскиваемая в предложении вторая часть составного союза
                            wanted_conj = possible_conjs[i][j][1]
                            # ее длина
                            len_wanted_conj2 = len(wanted_conj)
                            # точка отсчёта - следующий элемент после окончания первой части составного союза
                            k = i + len_wanted_conj1 + 1
                            while True:
                                # после 1-й части должна быть лексема, поэтому наращиваем счётчик перед шагом
                                k += 1
                                # если после предполагаемого союза не уместится лексем, break
                                if k + len_wanted_conj2 >= lexem_count:
                                    break
                                # ключевое: перед 1-й лексемой 2-й части союза дб запятая!
                                if inputSentence["lexems"][k]["lexem"] == wanted_conj[0] and inputSentence["lexems"][k-1]["lexem"] == ",":
                                    # проход по нужным лексемам до тех пор, пока совпадения есть
                                    for m in range(1, len_wanted_conj2):
                                        # m запоминать не надо, т.к. она дает лишь len(союз)
                                        if inputSentence["lexems"][k+m]["lexem"] != wanted_conj[m]:
                                            break
                                    else:
                                        # если мы не прошли в for, союз найден
                                        second_conj_part_accepted = True
                                        curr_conjs[-1].append([k, wanted_conj_kind, wanted_conj])
                        # если второй части союза нет, а союз составной,
                        # то первую принятую его часть удаляем
                        if (not second_conj_part_accepted) and possible_conjs[i][j][1] != '' and len(curr_conjs[-1]) == 1:
                            curr_conjs.pop()
    return conjCheking(inputSentence, curr_conjs)

def conjCheking(inputSentence, possible_conjs):
    output_conjs = deepcopy(possible_conjs)
    conjs_count = len(possible_conjs)
    flag_conj_reality = [True for i in range(conjs_count)]
    for conjIdx in range(conjs_count):
        conj_len = len(possible_conjs[conjIdx])
        for prevConjIdx in range(conjIdx):
            prevConj_len = len(possible_conjs[prevConjIdx])
            if flag_conj_reality[prevConjIdx]:
                if possible_conjs[conjIdx][0][2] > possible_conjs[prevConjIdx][0][2]:
                    if possible_conjs[conjIdx][0][0] == possible_conjs[prevConjIdx][0][0]:
                        flag_conj_reality[prevConjIdx] = False
                    elif possible_conjs[conjIdx][0][2][0] in possible_conjs[prevConjIdx][0][2]:
                        if (possible_conjs[prevConjIdx][0][2].index(possible_conjs[conjIdx][0][2][0])) + \
                                possible_conjs[prevConjIdx][0][0] == possible_conjs[conjIdx][0][0]:
                            flag_conj_reality[conjIdx] = False
                # попытка выкинуть односложный союз, когда есть двусложный с таким в составе
                # выкидывание происходит при условии, что 2 часть двусложного не мб самостоятельным союзом
                # работает для союзов, 2-я часть которых не присутствует в таких союзах, как "то..., то"
                elif prevConj_len == 1 and possible_conjs[prevConjIdx][0] in possible_conjs[conjIdx]:
                    prevConjCut_start = possible_conjs[conjIdx].index(possible_conjs[prevConjIdx][0])
                    l_poss_conjs = possible_conjs[conjIdx][:prevConjCut_start]
                    r_poss_conjs = possible_conjs[conjIdx][prevConjCut_start+1:]
                    if l_poss_conjs:
                        if [l_poss_conjs[0][2], '', l_poss_conjs[0][1]] not in all_unique_conjs:
                            flag_conj_reality[prevConjIdx] = False
                    if r_poss_conjs:
                        if [r_poss_conjs[0][2], '', r_poss_conjs[0][1]] not in all_unique_conjs:
                            flag_conj_reality[prevConjIdx] = False
                elif prevConj_len >= 2 and prevConj_len < conj_len:
                    if possible_conjs[prevConjIdx][0] in possible_conjs[conjIdx]:
                        if possible_conjs[conjIdx][1:] == possible_conjs[prevConjIdx]:
                            flag_conj_reality[prevConjIdx] = False
                    else:
                        for k in range(1, prevConj_len):
                            if possible_conjs[prevConjIdx][k] in possible_conjs[conjIdx]:
                                prevConj_cut = possible_conjs[conjIdx].index(possible_conjs[prevConjIdx][k])
                                output_conjs[conjIdx] = output_conjs[conjIdx][:prevConj_cut]
        possible_conjs = deepcopy(output_conjs)
    for conjIdx in range(conjs_count-1, -1, -1):
        conj_len = len(possible_conjs[conjIdx])
        for prevConjIdx in range(conjs_count-1, conjIdx, -1):
            prevConj_len = len(possible_conjs[prevConjIdx])
            if flag_conj_reality[prevConjIdx]:
                if possible_conjs[conjIdx][0][2] > possible_conjs[prevConjIdx][0][2]:
                    if possible_conjs[conjIdx][0][0] == possible_conjs[prevConjIdx][0][0]:
                        flag_conj_reality[prevConjIdx] = False
                    elif len(possible_conjs[prevConjIdx][0][2]) == 1 and \
                            possible_conjs[prevConjIdx][0][2][0] in possible_conjs[conjIdx][0][2]:
                        if (possible_conjs[conjIdx][0][2].index(possible_conjs[prevConjIdx][0][2][0])) + \
                                possible_conjs[conjIdx][0][0] == possible_conjs[prevConjIdx][0][0]:
                            flag_conj_reality[prevConjIdx] = False
                # попытка выкинуть односложный союз, когда есть двусложный с таким в составе
                # выкидывание происходит при условии, что 2 часть двусложного не мб самостоятельным союзом
                # работает для союзов, 2-я часть которых не присутствует в таких союзах, как "то..., то"
                elif prevConj_len == 1 and possible_conjs[prevConjIdx][0] in possible_conjs[conjIdx]:
                    prevConjCut_start = possible_conjs[conjIdx].index(possible_conjs[prevConjIdx][0])
                    l_poss_conjs = possible_conjs[conjIdx][:prevConjCut_start]
                    r_poss_conjs = possible_conjs[conjIdx][prevConjCut_start+1:]
                    if l_poss_conjs:
                        if [l_poss_conjs[0][2], '', l_poss_conjs[0][1]] not in all_unique_conjs:
                            flag_conj_reality[prevConjIdx] = False
                    if r_poss_conjs:
                        if [r_poss_conjs[0][2], '', r_poss_conjs[0][1]] not in all_unique_conjs:
                            flag_conj_reality[prevConjIdx] = False
                elif prevConj_len >= 2 and prevConj_len < conj_len:
                    if possible_conjs[prevConjIdx][0] in possible_conjs[conjIdx]:
                        if possible_conjs[conjIdx][1:] == possible_conjs[prevConjIdx]:
                            flag_conj_reality[prevConjIdx] = False
                    else:
                        for k in range(1, prevConj_len):
                            if possible_conjs[prevConjIdx][k] in possible_conjs[conjIdx]:
                                prevConj_cut = possible_conjs[conjIdx].index(possible_conjs[prevConjIdx][k])
                                output_conjs[conjIdx] = output_conjs[conjIdx][:prevConj_cut]
        possible_conjs = deepcopy(output_conjs)
    output_conjs = []
    for i in range(conjs_count):
        # print(flag_conj_reality[i], possible_conjs[i])
        if flag_conj_reality[i]:
            output_conjs.append(possible_conjs[i])
    conjFiltering(inputSentence, output_conjs)
    return output_conjs


def conjFiltering(inputSentence, conjs):
    conjs_posses = []
    for conj in conjs:
        for el_conj in conj:
            conjs_posses.append(el_conj[0])
            # lexem_vars = inputSentence["lexems"][el_conj[0]]["variants"]
    lexem_idx = 0
    out_vars = []
    for lexem in inputSentence["lexems"]:
        for var in lexem["variants"]:
            if var.POS == "CONJ" and lexem_idx not in conjs_posses:
                continue
            else:
                out_vars.append(var)
        lexem["variants"] = out_vars
        out_vars = []
        lexem_idx += 1
    return 0


def fullTextConjFinding(parsedText):
    whole_text_pc = []
    for p in parsedText["paragraphs"]:
        paragraph_possible_conjs = []
        for s in p["sentences"]:
            paragraph_possible_conjs.append(sentenceConjFinding(s))
        whole_text_pc.append(paragraph_possible_conjs)
    return whole_text_pc

# testing
# fullTextConjFinding(parsing(gettingData()))

# test1 = "Для примера, в качестве синтаксического объекта возьмем предложение, семантическим элементом тогда будет являться слово или его нормализованная версия, а в качестве рассматриваемой части текста выберем абзац, так как и предложения, и абзац являются формами завершенной мысли."
# test2 = "Если не перестанешь орать, то я тебе врежу, и твоя рожа будет то болеть, то очень болеть, то не болеть, то очень болеть."
# test3 = "Чем больше я о ней думаю, тем сильнее влюбляюсь."
# test4 = "Основная описанного метода состоит в том, что, используя частоту вхождения слова в синтаксические конструкции (предложение, абзац, текст), позицию слова в тексте, а также применение различных эвристик по определению семантических весовых коэффициентов для элементов текста, можно определить основные дескрипторные конструкции (ключевые слова, словосочетания, предложения) и описать семантический «скелет» текста, который можно использовать, например, в задачах классификации."