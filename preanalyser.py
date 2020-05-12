from reader import gettingData
from normal_parser import parsing
from copy import deepcopy
from conj_finding import sentenceConjFinding
from sent_tokenizer import sentSeparatorsFinding, sentGramBasisVarsFinding, gramBasisFinding, gramBasisFiltering


# testing
parsedTestText = parsing(gettingData())
# printingParseResult(parsedTestText)
testInputSentence = parsedTestText["paragraphs"][0]["sentences"][0]
separators, conjs = sentSeparatorsFinding(testInputSentence)
# printingParseResult(parsedTestText)
subj_vars, pred_vars = sentGramBasisVarsFinding(testInputSentence, separators)
gbVars = gramBasisFiltering(testInputSentence, gramBasisFinding(testInputSentence, subj_vars, pred_vars), len(separators))


def analyzeVarsForming(inputSentence):
    lexems_count = len(inputSentence["lexems"])
    res_count = 1
    for li in range(lexems_count):
        vars_count = len(inputSentence["lexems"][li]["variants"])
        res_count *= vars_count
    res = [[] for i in range(res_count)]
    res1 = [[] for i in range(res_count)]
    repeat_count = 1
    for li in range(lexems_count):        
        vars_count = len(inputSentence["lexems"][li]["variants"])
        for j in range(repeat_count):
            reVar_count = res_count // vars_count
            for vi in range(vars_count):
                for i in range(reVar_count):
                    res1[(i+vi*reVar_count)+j*res_count].append([li, vi])
                    res[(i+vi*reVar_count)+j*res_count].append(inputSentence["lexems"][li]["variants"][vi])
        repeat_count *= vars_count
        res_count //= vars_count
    return res

res_an_vars = analyzeVarsForming(testInputSentence)