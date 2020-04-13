from reader import gettingData
from nltk_parser import parsing

testText = gettingData()
parsedTestText = parsing(testText)

all_conjs = []

f = open("Conjunction_kinds.TXT", encoding="UTF-8").readlines()
for line in f:
    elem = line.strip("\n").strip("\t")
    if elem[-1] != ":":
        all_conjs.append(elem)
all_conjs.sort()
conj_count = len(all_conjs)

for i in range(conj_count):
    if "...," in all_conjs[i]:
        conj1 = all_conjs[i].split("..., ")[0]
        conj2 = all_conjs[i].split("..., ")[1]
        all_conjs[i] = [conj1.split(), conj2.split()]
    else:
        all_conjs[i] = [all_conjs[i].split(), ""]

# print(all_conjs)

def conjFinding(parsedText):
    for p in parsedText["paragraphs"]:
        for s in p["sentences"]:
            curr_conjs = []
            for l in s["lexems"]:
                wanted_lexem = l["lexem"].lower()
                possible_conjs = []
                for conj in all_conjs:
                    if conj[0][0] == wanted_lexem:
                        possible_conjs.append(conj)
                curr_conjs.append(possible_conjs)
            lexem_count = len(curr_conjs) # кол-во лексем в предложении
            # список вариантов данного союза
            # он должен заполнятсья только теми составными союзами
            # и индексами начала этих союзов в предложении,
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
                        # длина союза в лексемах
                        len_wanted_conj1 = len(wanted_conj)
                        # если длина предполагаемого союза не выводит за пределы предложения, 
                        if i + len_wanted_conj1 < lexem_count: 
                            # мы рассматриваем j-й вариант
                            for k in range(1, len_wanted_conj1):
                                if s["lexems"][i+k]["lexem"] != wanted_conj[k]:
                                    break
                            else:
                                possible_conjs.append([[i, wanted_conj]])
                                if curr_conjs[i][j][1] != '':
                                    wanted_conj = curr_conjs[i][j][1]
                                    len_wanted_conj2 = len(wanted_conj)
                                    k = i + len_wanted_conj1
                                    while True:
                                        k += 1
                                        if k + len_wanted_conj2 >= lexem_count:
                                            break
                                        if s["lexems"][k]["lexem"] == wanted_conj[0] and s["lexems"][k-1]["lexem"] == ",":
                                            for m in range(1, len_wanted_conj2):
                                                if s["lexems"][k+m]["lexem"] != wanted_conj[m]:
                                                    break
                                            else:
                                                possible_conjs[-1].append([k, wanted_conj])
                                                k += 1
                                print(possible_conjs)
                            
                            
# testing
conjFinding(parsedTestText)
