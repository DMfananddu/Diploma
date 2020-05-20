from reader import gettingData
from normal_parser import parsing, printingParseSentence
from copy import deepcopy
from sent_tokenizer import sentSeparatorsFinding, sentGramBasisVarsFinding, gramBasisFinding, gramBasisFiltering


# testing
parsedTestText = parsing(gettingData())
# printingParseResult(parsedTestText)
testInputSentence = parsedTestText["paragraphs"][0]["sentences"][0]
separators, conjs = sentSeparatorsFinding(testInputSentence)
# printingParseResult(parsedTestText)
subj_vars, pred_vars = sentGramBasisVarsFinding(testInputSentence, separators)
gbVars = gramBasisFiltering(testInputSentence, gramBasisFinding(testInputSentence, subj_vars, pred_vars), len(separators))
if separators[0] != 0:
    new_separators = [0]
    new_separators.extend(separators)
    separators = new_separators


def analyzeVarsForming(inputSentence, separators):
    res_vars = []
    last_lex = inputSentence["lexems"][-1]
    start = 0
    finish = 0
    for i in range(1, len(separators)):
        finish = separators[i]
        lexems_count = len(inputSentence["lexems"][start:finish])
        # лексемы части
        lexems = inputSentence["lexems"][start:finish]
        # список вариантов грамм основ данного предложения
        part_gb_vars = []
        for gb_var in gbVars:
            if gb_var[0] == i-1:
                # у грамм.основы: тэг, номер лексемы, номер варианта, приоритет
                subj = []
                pred = []
                if gb_var[1]:
                    subj = gb_var[1][:3]
                if gb_var[2]:
                    pred = gb_var[2][:3]
                part_gb_vars.append([subj, pred])
        res_vars_count = 1
        for li in range(lexems_count):
            res_vars_count *= len(lexems[li]["variants"])
            # print(lexems[li]["lexem"])
            # for vi in range(len(lexems[li]["variants"])):
            #     print("\t", lexems[li]["variants"][vi])
        # part_vars = [i for i in range(res_vars_count)]
        pre_vars_coefs = []
        for li in range(lexems_count):
            # коэффициенты для вычисления номера рассматриваемого варианта
            pre_vars_coefs.append(res_vars_count//preVarsCount(lexems, li))
        # перед возвратом данная функция будет иметь все варианты цепочек слов
        resPartVarForming(lexems, part_gb_vars, 0, pre_vars_coefs, 0, [], i-1)
        start = separators[i]
    return


def resPartVarForming(lexems, part_gb_vars, li, pre_vars_coefs, var_numb, part_var, part_number):
    if li == len(lexems):
        # print(part_number, var_numb)
        # ЗДЕСЬ ВЫЗЫВАТЬ ФУНКЦИЮ ПРОВЕРКИ ПО ПРАВИЛАМ, которая вернет ТРУ
        # ТОГДА МОЖНО БУДЕТ ДОБАВИТЬ ЭТОТ part_var в ответ! дааааа
        # у грамм.основы: тэг, номер лексемы, номер варианта морфологии лексемы
        current_part_gb_vars = []
        # флаги грамм.основ (должна ли быть у нас в варианте full_gb/pred_gb/subj_gb)
        full_gb = False
        subj_gb = False
        pred_gb = False
        # если полноценна грамм.основа
        if part_gb_vars[0][0] and part_gb_vars[0][1]:
            full_gb = True
        # если только подлежащее
        elif part_gb_vars[0][0]:
            subj_gb = True
        # если только сказуемое
        else:
            pred_gb = True
        for gb_var in part_gb_vars:
            if full_gb and (gb_var[0] and part_var[gb_var[0][1]-separators[part_number]] == gb_var[0][0]) and \
                    (gb_var[1] and part_var[gb_var[1][1]-separators[part_number]] == gb_var[1][0]):
                current_part_gb_vars.append(gb_var)
                current_part_gb_vars[-1][0][1] -= separators[part_number]
                current_part_gb_vars[-1][1][1] -= separators[part_number]
            elif pred_gb and not gb_var[0] and \
                    (gb_var[1] and part_var[gb_var[1][1]-separators[part_number]] == gb_var[1][0]):
                current_part_gb_vars.append(gb_var)
                current_part_gb_vars[-1][1][1] -= separators[part_number]
            elif subj_gb and not gb_var[1] and \
                    (gb_var[0] and part_var[gb_var[0][1]-separators[part_number]] == gb_var[0][0]):
                current_part_gb_vars.append(gb_var)
                current_part_gb_vars[-1][0][1] -= separators[part_number]
        # если для данного варианта есть нужная (полная или односложная) грамм.основа
        if current_part_gb_vars:
            for gb_var in current_part_gb_vars:
                subj_idx = None
                pred_idx = None
                if full_gb:
                    subj_idx = gb_var[0][1]
                    pred_idx = gb_var[1][1]
                elif subj_gb:
                    subj_idx = gb_var[0][1]
                else:
                    pred_idx = gb_var[1][1]
                print("part_number = ", part_number, ", var_numb = ", var_numb, sep="")
                res, res_flag = syntaxAnalysis(part_var, subj_idx, pred_idx)
        return
    vars_count = len(lexems[li]["variants"])
    lex_coef = pre_vars_coefs[li]
    for vi in range(vars_count):
        resPartVarForming(lexems, part_gb_vars, li+1, pre_vars_coefs, var_numb+lex_coef*vi, part_var + [lexems[li]["variants"][vi]], part_number)
    return


def preVarsCount(lexems, li):
    res = 1
    for i in range(li+1):
        res *= len(lexems[i]["variants"])
    return res


def syntaxAnalysis(part_lexems, subj_idx, pred_idx):
    print("subj_idx = ", subj_idx, ", pred_idx = ", pred_idx, sep="")
    for i in range(len(part_lexems)):
        if part_lexems[i].POS != "CONJ":
            print("\t", i, part_lexems[i])
    return part_lexems, True

# testing
analyzeVarsForming(testInputSentence, separators)