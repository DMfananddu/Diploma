from reader import gettingData
from normal_parser import parsing, printingParseSentence
from copy import deepcopy
from sent_tokenizer import sentSeparatorsFinding, sentGramBasisVarsFinding, gramBasisFinding, gramBasisFiltering


def analyzeVarsForming(inputSentence, separators):
    if 0 not in separators:
        seps_posses = [0]
        seps_posses.extend(separators)
        separators = seps_posses
    res_vars = []
    last_lex = inputSentence["lexems"][-1]
    start = 0
    finish = 0
    for i in range(1, len(separators)):
        finish = separators[i]
        lexems_count = len(inputSentence["lexems"][start:finish])
        lexems = inputSentence["lexems"][start:finish]
        res_vars_count = 1
        for li in range(lexems_count):
            res_vars_count *= len(lexems[li]["variants"])
            # print(lexems[li]["lexem"])
            # for vi in range(len(lexems[li]["variants"])):
            #     print("\t", lexems[li]["variants"][vi])
        part_vars = [i for i in range(res_vars_count)]
        pre_vars_coefs = []
        for li in range(lexems_count):
            pre_vars_coefs.append(res_vars_count//preVarsCount(lexems, li))
        resPartVarForming(lexems, 0, pre_vars_coefs, 0, [])
        start = separators[i]
        res_vars.append(part_vars)
    return res_vars


def resPartVarForming(lexems, li, pre_vars_coefs, var_numb, part_var):
    if li == len(lexems):
        print(var_numb)
        # ЗДЕСЬ ВЫЗЫВАТЬ ФУНКЦИЮ ПРОВЕРКИ ПО ПРАВИЛАМ, которая вернет ТРУ
        # ТОГДА МОЖНО БУДЕТ ДОБАВИТЬ ЭТОТ part_var в ответ! дааааа
        for i in part_var:
            print("\t", i)
        return
    vars_count = len(lexems[li]["variants"])
    lex_coef = pre_vars_coefs[li]
    for vi in range(vars_count):
        resPartVarForming(lexems, li+1, pre_vars_coefs, var_numb+lex_coef*vi, part_var + [lexems[li]["variants"][vi]])
    return


def preVarsCount(lexems, li):
    res = 1
    for i in range(li+1):
        res *= len(lexems[i]["variants"])
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