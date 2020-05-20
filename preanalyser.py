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


def analyzeVarsForming(inputSentence, separators, sent_number):
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
                part_gb_vars.append([gb_var[1], gb_var[2]])
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
        resPartVarForming(lexems, part_gb_vars, 0, pre_vars_coefs, 0, [], i-1, sent_number)
        start = separators[i]
    return


def resPartVarForming(lexems, part_gb_vars, li, pre_vars_coefs, var_numb, part_var, part_number, sent_number):
    if li == len(lexems):
        # print(part_number, var_numb)
        # список всех слов части
        words = []
        for l in lexems:
            words.append(l["lexem"])
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
                    gb_priority = gb_var[0][3] * gb_var[1][3]
                elif subj_gb:
                    subj_idx = gb_var[0][1]
                    gb_priority = gb_var[0][3]
                else:
                    pred_idx = gb_var[1][1]
                    gb_priority = gb_var[1][3]
                print("part_number = ", part_number, ", var_numb = ", var_numb, sep="")
                res, res_flag = syntaxAnalysis(words, part_var, subj_idx, pred_idx, part_number, sent_number, gb_priority)
        return
    vars_count = len(lexems[li]["variants"])
    lex_coef = pre_vars_coefs[li]
    for vi in range(vars_count):
        resPartVarForming(lexems, part_gb_vars, li+1, pre_vars_coefs, var_numb+lex_coef*vi, part_var + [lexems[li]["variants"][vi]], part_number, sent_number)
    return


def preVarsCount(lexems, li):
    res = 1
    for i in range(li+1):
        res *= len(lexems[i]["variants"])
    return res


def conjEjecting(words, part_lexems, subj_idx, pred_idx):
    actual_part_lexems = []
    actual_part_words = []
    for i in range(len(part_lexems)):
        if part_lexems[i].POS != "CONJ":
            actual_part_words.append(words[i])
            actual_part_lexems.append(part_lexems[i])
            # print("\t", i, actual_part_lexems[i])
        else:
            if subj_idx > i:
                subj_idx -= 1
            if pred_idx > i:
                pred_idx -= 1
    return actual_part_lexems, actual_part_words, subj_idx, pred_idx
"""
    Правило (ID правила, Название, Приоритет,
    Флаг согласования рода, Флаг согласования падежа, Флаг согласования числа,
    ВИД ПЕРВОЙ СГ, ВИД ВТОРОЙ СГ, ТИП ПЕРВОЙ СГ, ТИП ВТОРОЙ СГ):
    2, предл+СУЩ, 1, нет, нет, нет, 14, 1, 2, 1, 7
    16, ГЛ+кр.прич, 1, да, нет, да, 7, 10, 1, 2, 3
	30, нареч+ГЛ, 2, нет, нет, нет, 12, 7, 2, 1, 6
	31, прил+СУЩ, 3, да, да, да, 2, 1, 2, 1, 5
	32, ГЛ+сущ, 8, нет, нет, нет, 7, 1, 1, 2, 4
	"""
    
rules = [
    {
    "ID правила": 2,
    "Название": "предл+СУЩ",
    "Приоритет": 1,
    "Флаг согласования рода": False,
    "Флаг согласования падежа": False,
    "Флаг согласования числа": False,
    "ВИД ПЕРВОЙ СГ": 14,
    "ВИД ВТОРОЙ СГ": 1,
    "ТИП ПЕРВОЙ СГ": 2,
    "ТИП ВТОРОЙ СГ": 1,
    "ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ": 7
    },
    {
    "ID правила": 16,
    "Название": "ГЛ+кр.прич",
    "Приоритет": 1,
    "Флаг согласования рода": True,
    "Флаг согласования падежа": False,
    "Флаг согласования числа": True,
    "ВИД ПЕРВОЙ СГ": 7,
    "ВИД ВТОРОЙ СГ": 10,
    "ТИП ПЕРВОЙ СГ": 1,
    "ТИП ВТОРОЙ СГ": 2,
    "ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ": 3
    },
    {
    "ID правила": 30,
    "Название": "нареч+ГЛ",
    "Приоритет": 2,
    "Флаг согласования рода": False,
    "Флаг согласования падежа": False,
    "Флаг согласования числа": False,
    "ВИД ПЕРВОЙ СГ": 12,
    "ВИД ВТОРОЙ СГ": 7,
    "ТИП ПЕРВОЙ СГ": 2,
    "ТИП ВТОРОЙ СГ": 1,
    "ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ": 6
    },
    {
    "ID правила": 31,
    "Название": "прил+СУЩ",
    "Приоритет": 3,
    "Флаг согласования рода": True,
    "Флаг согласования падежа": True,
    "Флаг согласования числа": True,
    "ВИД ПЕРВОЙ СГ": 2,
    "ВИД ВТОРОЙ СГ": 1,
    "ТИП ПЕРВОЙ СГ": 2,
    "ТИП ВТОРОЙ СГ": 1,
    "ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ": 5
    },
    {
    "ID правила": 32,
    "Название": "ГЛ+сущ",
    "Приоритет": 8,
    "Флаг согласования рода": False,
    "Флаг согласования падежа": False,
    "Флаг согласования числа": False,
    "ВИД ПЕРВОЙ СГ": 7,
    "ВИД ВТОРОЙ СГ": 1,
    "ТИП ПЕРВОЙ СГ": 1,
    "ТИП ВТОРОЙ СГ": 2,
    "ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ": 4
    }
    ]

RULES_PRIORITY_COUNT = 9

POS_to_SG_KIND = {
    "NOUN": 1,
    "ADJF": 2,
    "ADJS": 3,
    "COMP": 4,
    "NUMB": 5,
    "NPRO": 6,
    "VERB": 7,
    "INFN": 8,
    "PRTF": 9,
    "PRTS": 10,
    "GRND": 11,
    "ADVB": 12,
    "PRCL": 13,
    "PREP": 14
}

def syntaxAnalysis(words, part_lexems, subj_idx, pred_idx, part_number, sent_number, gb_priority):
    print("subj_idx = ", subj_idx, ", pred_idx = ", pred_idx, ", gb_priority = ", gb_priority, sep="")
    # если из неразобранных слов осталась только грамм основа,
    # то действуем по отдельному алгоритму после всего остального
    # проходимся по всем приоритетам. сначала 1. потом 2 и т.д.
    # правила, необходимые для примера:
    actual_part_lexems, words, subj_idx, pred_idx = conjEjecting(words, part_lexems, subj_idx, pred_idx)
    rules_applying_flag = False
    main_words = []
    subordinate_words = []
    for prior in range(RULES_PRIORITY_COUNT):
        while True:
            l_count = len(actual_part_lexems)
            new_apl = deepcopy(actual_part_lexems)
            for i in range(l_count-2):
                print(actual_part_lexems[i])
                if actual_part_lexems[i].POS not in POS_to_SG_KIND.keys():
                    continue
                this_circle_lex_rules = []
                for rule in rules:
                    if rule["ВИД ПЕРВОЙ СГ"] == POS_to_SG_KIND[actual_part_lexems[i].POS] and rule["Приоритет"] == prior:
                        this_circle_lex_rules.append(rule)
                else:
                    continue
                # поиск нужного правила
                actual_rule = dict()
                for rule in this_circle_lex_rules:
                    # если за данной идёт часть речи, про которую нет правил
                    if actual_part_lexems[i+1].POS not in POS_to_SG_KIND.keys():
                        break
                    # если нет правил для данных двух частей речи
                    if POS_to_SG_KIND[actual_part_lexems[i+1].POS] != rule["ВИД ВТОРОЙ СГ"]:
                        continue
                    actual_rule = rule
                    break
                # если одно из слов НЕ грамматическая основа
                if i == subj_idx or i == pred_idx or i+1 == subj_idx or i+1 == pred_idx:
                    if (actual_part_lexems[i].POS == "VERB" or actual_part_lexems[i+1].POS == "VERB") and prior == 0:
                        rules_applying_flag = True
                        # Главная синтаксическая группа (ГСГ)
                        # (ID ГСГ, содержание, номер предложения, номер части,
                        # номер в части, ВИД СГ, ПРАВИЛО):
                        # 4, был, 1, 1, 1, 7, 3, 16
                        # 4, оштрафован, 1, 1, 2, 3, 16, 4
                        # запись слова
                        if actual_rule["ТИП ПЕРВОЙ СГ"] == 1:
                            main_word = [words[i], sent_number, part_number, i, actual_rule["ВИД ПЕРВОЙ СГ"]]
                            subordinate_word = [words[i+1], sent_number, part_number, i+1, actual_rule["ВИД ПЕРВОЙ СГ"], actual_rule["ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ"], rules.index(actual_rule)]
                        else:
                            main_word = [words[i+1], sent_number, part_number, i+1, actual_rule["ВИД ПЕРВОЙ СГ"]]
                            subordinate_word = [words[i], sent_number, part_number, i, actual_rule["ВИД ПЕРВОЙ СГ"], actual_rule["ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ"], rules.index(actual_rule)]
                        main_words.append(main_word)
                        subordinate_words.append(subordinate_word)
            # обновляем список необслужанных лексем
            actual_part_lexems = new_apl
            if not rules_applying_flag:
                break
    return part_lexems, True

# testing
analyzeVarsForming(testInputSentence, separators, 0)