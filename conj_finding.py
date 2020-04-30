from reader import gettingData
from normal_parser import parsing
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
for i in all_conjs:
    if i in all_unique_conjs:
        continue
    else:
        all_unique_conjs.append(i)

for i in all_conjs:
    print(i)

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
                print(possible_conjs[i][j])
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
                        print(i, wanted_conj_kind, wanted_conj)
                        
                        curr_conjs.append([[i, wanted_conj_kind, wanted_conj]])
                        second_conj_part_accepted = False
                        # отдельный поиск второй части раздельно-составного союза по тому же плану
                        if possible_conjs[i][j][1] != '':
                            # разыскиваемая в предложении вторая часть составного союза
                            wanted_conj = possible_conjs[i][j][1]
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
                                if inputSentence["lexems"][k]["lexem"] == wanted_conj[0] and inputSentence["lexems"][k-1]["lexem"] == ",":
                                    # проход по нужным лексемам до тех пор, пока совпадения есть
                                    for m in range(1, len_wanted_conj2):
                                        # m запоминать не надо, т.к. она дает лишь len(союз)
                                        if inputSentence["lexems"][k+m]["lexem"] != wanted_conj[m]:
                                            break
                                    else:
                                        # если мы не прошли ни одной инструкции в for, союз найден
                                        second_conj_part_accepted = True
                                        curr_conjs[-1].append([k, wanted_conj_kind, wanted_conj])
                                        # следующий после него должен располагаться минимум через лексему
                                k += 1
                        # если второй части союза нет, а союз составной,
                        # то первую принятую его часть удаляем
                        if (not second_conj_part_accepted) and possible_conjs[i][j][1] != '':
                            curr_conjs.pop()

    return curr_conjs

def fullTextConjFinding(parsedText):
    whole_text_pc = []
    for p in parsedText["paragraphs"]:
        for s in p["sentences"]:
            whole_text_pc.append(sentenceConjFinding(s))
    return whole_text_pc

# testing
print(fullTextConjFinding(parsedTestText))
