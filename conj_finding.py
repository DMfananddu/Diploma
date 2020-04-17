from reader import gettingData
from nltk_parser import parsing
from copy import deepcopy

testText = gettingData()
parsedTestText = parsing(testText)


# получение списка союзов из специального файла в удобочитаемом виде
all_conjs = []

f = open("Conjunction_kinds.TXT", encoding="UTF-8").readlines()
conj_kinds = []
conj_kind_flag = False
for line in f:
    elem = line.strip("\n").strip("\t")
    if elem == "Подчинительные:":
        conj_kind_flag = True
    if elem[-1] != ":":
        all_conjs.append(elem)
    if not conj_kind_flag:
        conj_kinds.append("Сочинительный")
    else:
        conj_kinds.append("Подчинительный")
raw_conjs = deepcopy(all_conjs)
all_conjs.sort()
conj_count = len(all_conjs)

for i in range(conj_count):
    conj_kind = conj_kinds[raw_conjs.index(all_conjs[i])]
    if "...," in all_conjs[i]:
        conj1 = all_conjs[i].split("..., ")[0]
        conj2 = all_conjs[i].split("..., ")[1]
        all_conjs[i] = [conj1.split(), conj2.split(), conj_kind]
    else:
        all_conjs[i] = [all_conjs[i].split(), "", conj_kind]

# print(all_conjs)

def conjFinding(parsedText):
    whole_text_pc = []
    for p in parsedText["paragraphs"]:
        for s in p["sentences"]:
            # список всех возможных вариантов любых союзов, 
            # которые могут начинаться на какой-либо лексеме
            curr_conjs = []
            for l in s["lexems"]:
                # все лексемы к нижнему регистру, чтобы "Чем" и "чем" были одинаковыми лексемами 
                wanted_lexem = l["lexem"].lower()
                # все союзы, которые могут начинаться на данной лексеме
                possible_conjs = []
                for conj in all_conjs:
                    if conj[0][0] == wanted_lexem:
                        possible_conjs.append(conj)
                curr_conjs.append(possible_conjs)
            # кол-во лексем в предложении
            lexem_count = len(curr_conjs)
            # список вариантов данного союза
            # он должен заполнятсья только теми видами союзов, союзами и
            # индексами начала этих союзов в предложении,
            # которые реально есть в данном предложении
            possible_conjs = []
            for i in range(lexem_count):
                if len(curr_conjs[i]) != 0:
                    # длина списка вариантов
                    len_сvl = len(curr_conjs[i])
                    # первая лексема союза в предложении
                    wanted_lexem = s["lexems"][i]["lexem"]
                    # проход по всем вариантам
                    for j in range (len_сvl):
                        # рассматриваемый вариант союза
                        wanted_conj = curr_conjs[i][j][0]
                        # рассматриваемый вид союза
                        wanted_conj_kind = curr_conjs[i][j][2]
                        # длина союза в лексемах
                        len_wanted_conj1 = len(wanted_conj)
                        # если длина предполагаемого союза не выводит за пределы предложения, 
                        if i + len_wanted_conj1 < lexem_count: 
                            # мы рассматриваем j-й вариант
                            for k in range(1, len_wanted_conj1):
                                if s["lexems"][i+k]["lexem"] != wanted_conj[k]:
                                    break
                            else: # нашли нужный союз
                                possible_conjs.append([i, wanted_conj_kind, wanted_conj])
                                # отдельный поиск второй части раздельно-составного союза по тому же плану
                                if curr_conjs[i][j][1] != '':
                                    # разыскиваемая в предложении вторая часть составного союза
                                    wanted_conj = curr_conjs[i][j][1]
                                    # ее длина
                                    len_wanted_conj2 = len(wanted_conj)
                                    # точка отсчёта - следующий элемент после окончания первой части составного союза
                                    k = i + len_wanted_conj1
                                    while True:
                                        # после 1-й части должна быть лексема, поэтому наращиваем счётчик перед шагом
                                        k += 1
                                        # если после предполагаемого союза не уместится лексем, break
                                        if k + len_wanted_conj2 >= lexem_count:
                                            break
                                        # ключевое: перед 1-й лексемой 2-й части союза дб запятая!
                                        if s["lexems"][k]["lexem"] == wanted_conj[0] and s["lexems"][k-1]["lexem"] == ",":
                                            # проход по нужным лексемам до тех пор, пока совпадения есть
                                            for m in range(1, len_wanted_conj2):
                                                # m запоминать не надо, т.к. она дает лишь len(союз)
                                                if s["lexems"][k+m]["lexem"] != wanted_conj[m]:
                                                    break
                                            else:
                                                # если мы не прошли ни одной инструкции в for, союз найден
                                                possible_conjs[-1].append([k, wanted_conj_kind, wanted_conj])
                                                # следующий после него должен располагаться минимум через лексему
                                                k += 1
            # не забываем запомнить list возможных союзов для данного предложения
            whole_text_pc.append(possible_conjs)
    return whole_text_pc

# testing
print(conjFinding(parsedTestText))
