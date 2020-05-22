from reader import gettingData
from normal_parser import parsing, printingParseSentence
from copy import deepcopy
from sent_tokenizer import sentSeparatorsFinding, sentGramBasisVarsFinding, gramBasisFinding, gramBasisFiltering


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
    },
    {
    "ID правила": 33,
    "Название": "ПОДЛ",
    "Приоритет": 9,
    "Флаг согласования рода": False,
    "Флаг согласования падежа": False,
    "Флаг согласования числа": False,
    "ВИД ПЕРВОЙ СГ": None,
    "ВИД ВТОРОЙ СГ": None,
    "ТИП ПЕРВОЙ СГ": 1,
    "ТИП ВТОРОЙ СГ": None,
    "ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ": 2
    },
    {
    "ID правила": 34,
    "Название": "СКАЗ",
    "Приоритет": 9,
    "Флаг согласования рода": False,
    "Флаг согласования падежа": False,
    "Флаг согласования числа": False,
    "ВИД ПЕРВОЙ СГ": None,
    "ВИД ВТОРОЙ СГ": None,
    "ТИП ПЕРВОЙ СГ": 1,
    "ТИП ВТОРОЙ СГ": None,
    "ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ": 3
    },
    {
    "ID правила": 35,
    "Название": "ПОДЛ+СКАЗ/СКАЗ+ПОДЛ",
    "Приоритет": 10,
    "Флаг согласования рода": False,
    "Флаг согласования падежа": False,
    "Флаг согласования числа": False,
    "ВИД ПЕРВОЙ СГ": None,
    "ВИД ВТОРОЙ СГ": None,
    "ТИП ПЕРВОЙ СГ": 1,
    "ТИП ВТОРОЙ СГ": 1,
    "ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ": 1
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


def analyzeVarsForming(inputSentence, separators, sent_number, prgf_number, gbVars):
    last_lex = inputSentence["lexems"][-1]
    start = 0
    finish = 0
    sent_atba = []
    atba_flags = [True for i in range(len(separators)-1)]
    res_flags = []
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
        pre_vars_coefs = []
        for li in range(lexems_count):
            # коэффициенты для вычисления номера рассматриваемого варианта
            pre_vars_coefs.append(res_vars_count//preVarsCount(lexems, li))
        # перед возвратом данная функция будет иметь все варианты цепочек слов
        rfs = [[True] for i in range(res_vars_count)]
        resPartVarForming(lexems, part_gb_vars, 0, pre_vars_coefs, 0, [], i-1, sent_number, prgf_number, separators, atba_flags, rfs)
        res_flags.append(rfs)
        start = separators[i]
    return atba_flags, res_flags


def resPartVarForming(lexems, part_gb_vars, li, pre_vars_coefs, var_number, part_var, part_number, sent_number, prgf_number, separators, atba_flags, res_flags):
    if li == len(lexems):
        res_mains = []
        res_subs = []
        # print(part_number, var_number)
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
        if part_gb_vars and part_gb_vars[0][0] and part_gb_vars[0][1]:
            full_gb = True
        # если только подлежащее
        elif part_gb_vars and part_gb_vars[0][0]:
            subj_gb = True
        # если только сказуемое
        elif part_gb_vars:
            pred_gb = True
        else:
            atba_flags[part_number] = False
            return
        res_flag_had_been = False
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
            for i in range(len(res_flags)):
                if i == var_number:
                    for j in range(1, len(current_part_gb_vars)):
                        res_flags[var_number].append(res_flags[var_number][0])
            idx = -1
            for gb_var in current_part_gb_vars:
                idx += 1
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
                print("prgf_number = ", prgf_number, ", sent_number = ", sent_number, ", part_number = ", part_number, ", var_number = ", var_number, ", subj_idx = ", subj_idx, ", pred_idx = ", pred_idx, sep="")
                res_flag_idx = current_part_gb_vars.index(gb_var)
                res_mains, res_subs = syntaxAnalysis(words, part_var, subj_idx, pred_idx, var_number, part_number, sent_number, prgf_number, gb_priority, res_flags[var_number], res_flag_idx)
                # ТУТ вызвать функцию переделки в метаграфы





                
                # print(res_mains)
                # print(res_subs)
        return
    vars_count = len(lexems[li]["variants"])
    lex_coef = pre_vars_coefs[li]
    for vi in range(vars_count):
        resPartVarForming(lexems, part_gb_vars, li+1, pre_vars_coefs, var_number+lex_coef*vi, part_var + [lexems[li]["variants"][vi]], part_number, sent_number, prgf_number, separators, atba_flags, res_flags)
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
            if subj_idx and subj_idx > i:
                subj_idx -= 1
            if pred_idx and pred_idx > i:
                pred_idx -= 1
    return actual_part_lexems, actual_part_words, subj_idx, pred_idx


def syntaxAnalysis(words, part_lexems, subj_idx, pred_idx, var_number, part_number, sent_number, prgf_number, gb_priority, res_flags, res_flag_idx):
    # print("subj_idx = ", subj_idx, ", pred_idx = ", pred_idx, ", gb_priority = ", gb_priority, sep="")
    # если из неразобранных слов осталась только грамм основа,
    # то действуем по отдельному алгоритму после всего остального
    # проходимся по всем приоритетам. сначала 1. потом 2 и т.д.
    # правила, необходимые для примера:
    part_vars, part_words, subj_idx, pred_idx = conjEjecting(words, part_lexems, subj_idx, pred_idx)
    # print("subj_idx = ", subj_idx, ", pred_idx = ", pred_idx, sep="")
    lexems_count = len(part_words)
    words_flags = [False for i in range(lexems_count)]
    rules_applying_flag = False
    gb_processing_flag = False
    main_words = []
    subordinate_words = []
    prior = 1
    while prior < RULES_PRIORITY_COUNT:
        while True:
            rules_applying_flag = False
            l_count = len(part_vars)
            for i in range(l_count-2):
                # print(part_vars[i])
                # цикл для ситуаций: зпт1+зпт2 -> зпт2 и т.п.
                if {"PNCT"} in part_lexems[i] and not words_flags[i]:
                    for j in range(i+1, l_count-2):
                        if not words_flags[i]:
                            if {"PNCT"} in part_lexems[j]:
                                words_flags[i] = True
                # непосредственно поиск лексем для правил
                if part_vars[i].POS not in POS_to_SG_KIND.keys() or words_flags[i]:
                    continue
                this_circle_lex_rules = []
                for rule in rules:
                    if rule["ВИД ПЕРВОЙ СГ"] == POS_to_SG_KIND[part_vars[i].POS] and rule["Приоритет"] == prior:
                        this_circle_lex_rules.append(rule)
                if not this_circle_lex_rules:
                    continue
                # поиск второго слова
                si = i+1
                si_flag = False
                pnct_flag = True
                first_lexem_is_main = False
                pnct_lexem = ""
                while True:
                    if not words_flags[si]:
                        if {"PNCT"} not in part_lexems[si]:
                            if pnct_flag:
                                ignore_flag = False
                                for j in range(si, l_count-1):
                                    if not words_flags[j] and {"PNCT"} not in part_lexems[j]:
                                        ignore_flag = True
                                        break
                                if not ignore_flag:
                                    if pnct_lexem in [";", ","]:
                                        first_lexem_is_main = True
                                        si_flag = True
                                        break
                                    if pnct_lexem == ":":
                                        if part_vars[si].case == part_vars[i].case:
                                            si_flag = True
                                            break
                            si_flag = True
                            break
                        else:
                            pnct_flag = True
                            pnct_lexem = part_words[si]
                    si += 1
                    if si > l_count-1:
                        break
                if not si_flag:
                    break
                # print(part_vars[i], part_vars[si])
                # поиск нужного правила для i-го и si-го слов
                actual_rule = dict()
                for rule in this_circle_lex_rules:
                    # если за данной идёт часть речи, про которую нет правил
                    if part_vars[si].POS not in POS_to_SG_KIND.keys():
                        break
                    # если нет правил для данных двух частей речи
                    if POS_to_SG_KIND[part_vars[si].POS] != rule["ВИД ВТОРОЙ СГ"]:
                        continue
                    # иначе - нашли нужное правило. ВСЕГДА ЕДИНСТВЕННОЕ
                    actual_rule = rule
                    break
                # если нет правил
                if not actual_rule:
                    continue
                # если ГРУППА+сущ, и сущ в им падеже () - break
                if rule["ТИП ПЕРВОЙ СГ"] < rule["ТИП ВТОРОЙ СГ"]:
                    if part_vars[si].case == "nomn" and part_vars[i].case != "nomn":
                        continue
                else:
                    if part_vars[i].case == "nomn" and part_vars[si].case != "nomn":
                        continue
                # если одно из слов - грамматическая основа
                if (i == subj_idx or i == pred_idx or si == subj_idx or si == pred_idx) and not gb_processing_flag:
                    if (part_vars[i].POS == "VERB" or part_vars[si].POS == "VERB") and prior == 1:
                        # Главная синтаксическая группа (ГСГ)
                        # (ID ГСГ, содержание, номер предложения, номер части,
                        # номер в части, ВИД СГ, ПРАВИЛО):
                        # запись слова
                        rules_applying_flag = wordsAppending(part_vars, part_words, i, si, prgf_number, sent_number, part_number, var_number, actual_rule, rules.index(actual_rule), words_flags, main_words, subordinate_words, subj_idx, pred_idx)
                    continue
                # тут обработка обычных слов
                rules_applying_flag = wordsAppending(part_vars, part_words, i, si, prgf_number, sent_number, part_number, var_number, actual_rule, rules.index(actual_rule), words_flags, main_words, subordinate_words, subj_idx, pred_idx)
            if not rules_applying_flag:
                priority_workoff_flag = True
                break
        if priority_workoff_flag:
            prior += 1
            if prior == RULES_PRIORITY_COUNT and not gb_processing_flag:
                gb_processing_flag = True
                prior = 1
        else:
            prior = 1
    # выкидывание если не оработали слова (кроме ГРАММ.ОСНОВЫ)
    for i in range(lexems_count):
        if {"PNCT"} in part_vars[i]:
            words_flags[i] = True
        if not words_flags[i]:
            if (subj_idx != None and i != subj_idx or subj_idx == None) \
                    and (pred_idx != None and i != pred_idx or pred_idx == None):
                res_flags[res_flag_idx] = False
                return main_words, subordinate_words
    # print("main_words")
    # for i in main_words:
    #     print(i)
    # print("sub_words")
    # for i in subordinate_words:
    #     print(i)
    # обработка ГРАММ.ОСНОВЫ
    sent_word = ""
    if subj_idx != None:
        sent_word = part_words[subj_idx]
        # print(part_words[subj_idx])
        subj_rule = dict()
        for rule in rules:
            if rule["Название"] == "ПОДЛ":
                subj_rule = rule
        # слово; тэг; номер параграфа, предложения, части, варианта; номер в части; ID вид СГ, ID член предложения, ID правила, ID главного слова
        subordinate_word = [part_words[subj_idx], part_vars[subj_idx], prgf_number, sent_number, part_number, var_number, subj_idx, None, subj_rule["ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ"], rules.index(subj_rule), None]
        subordinate_words.append(subordinate_word)
    sent_word += "_"
    if pred_idx != None:
        sent_word += part_words[pred_idx]
        # print(part_words[pred_idx])
        pred_rule = dict()
        for rule in rules:
            if rule["Название"] == "СКАЗ":
                pred_rule = rule
        # слово; тэг; номер параграфа, предложения, части, варианта; номер в части; ID вид СГ, ID член предложения, ID правила, ID главного слова
        subordinate_word = [part_words[pred_idx], part_vars[pred_idx], prgf_number, sent_number, part_number, var_number, pred_idx, POS_to_SG_KIND[part_vars[pred_idx].POS], pred_rule["ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ"], rules.index(pred_rule), None]
        subordinate_words.append(subordinate_word)
    sent_rule = dict()
    for rule in rules:
        if rule["Название"] == "ПОДЛ+СКАЗ/СКАЗ+ПОДЛ":
            sent_rule = rule
    # слово; тэг; номер параграфа, предложения, части, варианта; номер в части; ID вид СГ, ID член предложения, ID правила, ID главного слова
    subordinate_word = [sent_word, None, prgf_number, sent_number, part_number, var_number, None, None, sent_rule["ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ"], rules.index(sent_rule), None]
    subordinate_words.append(subordinate_word)
    for i in subordinate_words:
        print(i)
    return main_words, subordinate_words


def wordsAppending(part_vars, part_words, i, si, prgf_number, sent_number, part_number, var_number, actual_rule, ar_number, words_flags, main_words, subordinate_words, subj_idx, pred_idx):
    if actual_rule["ТИП ПЕРВОЙ СГ"] == 1:
        if si == pred_idx or si == subj_idx:
            return False
        mw_idx = mainWordAppending(main_words, part_vars[i], part_words[i], prgf_number, sent_number, part_number, var_number, i, actual_rule["ВИД ПЕРВОЙ СГ"])
        subWordAppending(subordinate_words, part_vars[si], part_words[si], prgf_number, sent_number, part_number, var_number, si, actual_rule["ВИД ВТОРОЙ СГ"], actual_rule["ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ"], ar_number, mw_idx)
        words_flags[si] = True
    else:
        if i == pred_idx or i == subj_idx:
            return False
        mw_idx = mainWordAppending(main_words, part_vars[si], part_words[si], prgf_number, sent_number, part_number, var_number, si, actual_rule["ВИД ВТОРОЙ СГ"])
        subWordAppending(subordinate_words, part_vars[i], part_words[i], prgf_number, sent_number, part_number, var_number, i, actual_rule["ВИД ПЕРВОЙ СГ"], actual_rule["ПОДЧИНЕННЫЙ ЧЛЕН ПРЕДЛОЖЕНИЯ"], ar_number, mw_idx)
        words_flags[i] = True
    return True


def mainWordAppending(main_words, var, word, prgf_number, sent_number, part_number, var_number, i, sg_kind):
    # слово; тэг; номер параграфа, предложения, части, варианта; номер в части; вид СГ
    mw_idx = len(main_words)
    if [word, var, prgf_number, sent_number, part_number, var_number, i, sg_kind] not in main_words:
        main_words.append([word, var, prgf_number, sent_number, part_number, var_number, i, sg_kind])
    else:
        mw_idx = main_words.index([word, var, prgf_number, sent_number, part_number, var_number, i, sg_kind])
    return mw_idx


def subWordAppending(subordinate_words, var, word, prgf_number, sent_number, part_number, var_number, si, sg_kind, attribute, ar_number, mw_idx):
    # слово; тэг; номер параграфа, предложения, части, варианта; номер в части; ID вид СГ, ID член предложения, ID правила, ID главного слова
    subordinate_words.append([word, var, prgf_number, sent_number, part_number, var_number, si, sg_kind, attribute, ar_number, mw_idx])
    return