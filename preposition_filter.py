from reader import gettingData
from normal_parser import parsing
from sent_tokenizer import sentSeparatorsFinding

# получение списка союзов из специального файла в удобочитаемом виде
all_preps = []

f = open("Preposition_cases.TXT", encoding="UTF-8").readlines()
for line in f:
    elem = line.strip("\n").strip("\t").split(" — ")
    elem = [elem[0].split(), sorted(elem[1].split())]
    for i in range(len(elem[1])):
        if elem[1][i] == "род.":
            elem[1][i] = "gent"
            elem[1].append("gen1")
            elem[1].append("gen2")
        elif elem[1][i] == "вин.":
            elem[1][i] = "accs"
            elem[1].append("acc2")
        elif elem[1][i] == "твор.":
            elem[1][i] = "ablt"
        elif elem[1][i] == "дат.":
            elem[1][i] = "datv"
        else:
            elem[1][i] = "loct"
            elem[1].append("loc1")
            elem[1].append("loc2")
    all_preps.append(elem)
all_preps.sort()
all_preps.reverse()
# for i in all_preps:
#     print(i)


def prepositionFiltering(inputSentence):
    lexems = []
    for lexem in inputSentence["lexems"]:
        lexems.append(lexem["lexem"].lower())
    prep_count = len(all_preps)
    captured_prep_posses = []
    captured_preps = []
    for i in range(prep_count):
        poss_prep_idx = -1
        try:
            poss_prep_idx = lexems.index(all_preps[i][0][0])
        except:
            continue
        if poss_prep_idx != -1 and poss_prep_idx not in captured_prep_posses:
            for j in range(len(all_preps[i][0])):
                if lexems[poss_prep_idx+j] != all_preps[i][0][j]:
                    break
            else:
                captured_prep_posses.append(poss_prep_idx)
                captured_preps.append([poss_prep_idx, all_preps[i][0]])
                lex_idx = poss_prep_idx
                break_flag = False
                while True and not break_flag:
                    lex_idx += 1
                    if {"PNCT"} in inputSentence["lexems"][lex_idx]["variants"][0].tag:
                        break
                    true_vars = []
                    # for g in inputSentence["lexems"][lex_idx]["variants"]:
                    #     print(g)
                    for var in inputSentence["lexems"][lex_idx]["variants"]:
                        if var.tag.POS == "NOUN":
                            if var.tag.case in all_preps[i][1]:
                                true_vars.append(var)
                        elif var.tag.POS == "NPRO":
                            if var.tag.case in all_preps[i][1]:
                                true_vars.append(var)
                        elif var.tag.POS == "PRTF":
                            if var.tag.case in all_preps[i][1]:
                                true_vars.append(var)
                        elif var.tag.POS == "ADJF":
                            if var.tag.case in all_preps[i][1]:
                                true_vars.append(var)
                        elif var.tag.POS == "NUMR":
                            if var.tag.case in all_preps[i][1]:
                                true_vars.append(var)
                        elif var.tag.POS != "VERB":
                            true_vars.append(var)
                        else:
                            true_vars.append(var)
                            break_flag = True
                    inputSentence["lexems"][lex_idx]["variants"] = true_vars
                    # print(0)
                    # for g in inputSentence["lexems"][lex_idx]["variants"]:
                    #     print(g)
    for i in captured_preps:
        print(i)
    return captured_preps

# # testing
# parsedTestText = parsing(gettingData())
# # printingParseResult(parsedTestText)
# testInputSentence = parsedTestText["paragraphs"][0]["sentences"][0]
# separators, conjs = sentSeparatorsFinding(testInputSentence)
# preps = prepositionFiltering(testInputSentence)