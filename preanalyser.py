from reader import gettingData
from normal_parser import parsing, printingParseSentence
from copy import deepcopy
from sent_tokenizer import sentSeparatorsFinding, sentGramBasisVarsFinding, gramBasisFinding, gramBasisFiltering


def analyzeVarsForming(inputSentence, separators):
    if 0 not in separators:
        seps_posses = [0]
        seps_posses.extend(separators)
        separators = seps_posses
    res = []
    start = 0
    finish = 0
    for i in range(1, len(separators)):
        finish = separators[i]
        lexems_count = len(inputSentence["lexems"][start:finish])
        res_count = 1
        for li in range(start, lexems_count):
            vars_count = len(inputSentence["lexems"][li]["variants"])
            res_count *= vars_count
        printingParseSentence(inputSentence)
        print(separators)
        print(lexems_count, res_count)
        part_res = [[] for i in range(res_count)]
        repeat_count = 1
        for li in range(start, lexems_count):        
            vars_count = len(inputSentence["lexems"][li]["variants"])
            for j in range(repeat_count):
                reVar_count = res_count // vars_count
                for vi in range(vars_count):
                    for i in range(reVar_count):
                        # res1[(i+vi*reVar_count)+j*res_count].append([li, vi])
                        if (i+vi*reVar_count)+j*res_count > 576:
                            print((i+vi*reVar_count)+j*res_count)
                        # res[(i+vi*reVar_count)+j*res_count].append(inputSentence["lexems"][li]["variants"][vi])
            repeat_count *= vars_count
            res_count //= vars_count
        # for i in part_res:
        #     print(i)
        # res.append(part_res)
        start = separators[i]
    return res


# testing
parsedTestText = parsing(gettingData())
# printingParseResult(parsedTestText)
testInputSentence = parsedTestText["paragraphs"][0]["sentences"][0]
separators, conjs = sentSeparatorsFinding(testInputSentence)
# printingParseResult(parsedTestText)
subj_vars, pred_vars = sentGramBasisVarsFinding(testInputSentence, separators)
gbVars = gramBasisFiltering(testInputSentence, gramBasisFinding(testInputSentence, subj_vars, pred_vars), len(separators))
res_an_vars = analyzeVarsForming(testInputSentence, separators)