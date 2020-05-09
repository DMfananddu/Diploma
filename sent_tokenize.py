from normal_parser import parsing, printingParseResult
from conj_finding import sentenceConjFinding, conjCheking
from reader import gettingData
from copy import deepcopy

# приоритеты существит., местоим., числит., прил., причастия, инфинитива, наречия
SUBJECT_PRIORITY_COUNT = 7
NOUN_SUBJECT_PRIORITY = 0
NPRO_SUBJECT_PRIORITY = 1
ADJF_SUBJECT_PRIORITY = 2
PRTF_SUBJECT_PRIORITY = 3
NUMR_SUBJECT_PRIORITY = 4
INFN_SUBJECT_PRIORITY = 5
ADVB_SUBJECT_PRIORITY = 6

# приоритеты существит., местоим., числит., прил., причастия, наречия, инфинитива
PREDICATE_PRIORITY_COUNT = 11
VERB_PREDICATE_PRIORITY = 0
INFN_PREDICATE_PRIORITY = 1
ADJF_PREDICATE_PRIORITY = 2
PRTF_PREDICATE_PRIORITY = 3
NOUN_PREDICATE_PRIORITY = 4
ADJS_PREDICATE_PRIORITY = 5
PRTS_PREDICATE_PRIORITY = 6
ADVB_PREDICATE_PRIORITY = 7
COMP_PREDICATE_PRIORITY = 8
NUMR_PREDICATE_PRIORITY = 9
NPRO_PREDICATE_PRIORITY = 10


def sentGramBasisVarsFinding(inputSentence, separators_positions):
    allSubjectForms = []
    allPredicateForms = []
    partSubjectForms = []
    partPredicateForms = []
    sep_count = len(separators_positions)
    start = 0
    finish = 0
    separators_positions.append(len(inputSentence["lexems"]))
    for i in range(sep_count+1):
        start = finish
        finish = separators_positions[i]
        flag_part_existing = False
        for lexIndex in range(start, finish):
            if lexIndex not in separators:
                part_subj_vars = subjectFormFinding(inputSentence["lexems"][lexIndex]["variants"], lexIndex)
                part_subj_vars.sort()
                partSubjectForms.append(part_subj_vars)
                part_pred_vars = predicateFormFinding(inputSentence["lexems"][lexIndex]["variants"], lexIndex)
                part_pred_vars.sort()
                partPredicateForms.append(part_pred_vars)
                if partSubjectForms[-1] or partPredicateForms[-1]:
                    flag_part_existing = True
        if not flag_part_existing:
            allSubjectForms[-1].extend(partSubjectForms)
            allPredicateForms[-1].extend(partPredicateForms)
        else:
            allSubjectForms.append(partSubjectForms)
            allPredicateForms.append(partPredicateForms)
        partSubjectForms = []
        partPredicateForms = []
    # parts_count = len(allSubjectForms)
    # for part in range(parts_count):
    #     print(part, "Subjectes")
    #     subjs_part_count = len(allSubjectForms[part])
    #     for subj in range(subjs_part_count):
    #         print("\t", subj)
    #         vars_count = len(allSubjectForms[part][subj])
    #         for var in range(vars_count):
    #             print("\t\t", allSubjectForms[part][subj][var])
    #     print(part, "Predicates")
    #     subjs_part_count = len(allPredicateForms[part])
    #     for subj in range(subjs_part_count):
    #         print("\t", subj)
    #         vars_count = len(allPredicateForms[part][subj])
    #         for var in range(vars_count):
    #             print("\t\t", allPredicateForms[part][subj][var])
    return allSubjectForms, allPredicateForms


def sentSeparatorsFinding(inputSentence):
    conjs = sentenceConjFinding(inputSentence)
    separators_indexes = []
    print("Союзы:")
    for conj in conjs:
        print(conj)
        for lex in conj:
            vars_count = len(inputSentence["lexems"][lex[0]]["variants"])
            for varIdx in range(vars_count):
                if inputSentence["lexems"][lex[0]]["variants"][varIdx].tag.POS == "CONJ":
                    inputSentence["lexems"][lex[0]]["variants"] = [inputSentence["lexems"][lex[0]]["variants"][varIdx]]
                    break
        if conj[0][1] == "Сочинительный" and conj[0][0] != 0 and inputSentence["lexems"][conj[0][0] - 1] != ",":
            continue
        for lex in conj:
            if lex[0] != 0:
                separators_indexes.append(lex[0])
    print("sep_indexes:", separators_indexes)
    return separators_indexes


def gramBasisFinding(inputSentence, subjes, predes):
    parts_count = len(subjes)
    gram_basis_vars = []
    s_flag = False
    p_flag = False
    for s_part in subjes:
        part_len = len(s_part)
        s_flag = False
        p_flag = False
        for s_priority_idx in range(SUBJECT_PRIORITY_COUNT):
            for s_lex_idx in range(part_len):
                s_vars_count = len(s_part[s_lex_idx])
                for s_var_idx in range(s_vars_count):
                    s_flag = True
                    if s_part[s_lex_idx][s_var_idx][0] == s_priority_idx:
                        for p_part in predes:
                            if predes.index(p_part) == subjes.index(s_part):
                                for p_priority_idx in range(PREDICATE_PRIORITY_COUNT):
                                    for p_lex_idx in range(part_len):
                                        p_vars_count = len(p_part[p_lex_idx])
                                        if p_lex_idx == s_lex_idx:
                                            continue
                                        for p_var_idx in range(p_vars_count):
                                            # тире
                                            p_flag = True
                                            dash_hyphen_flag = dashHyphenFinding(inputSentence, s_part[s_lex_idx][s_var_idx][2], p_part[p_lex_idx][p_var_idx][2])
                                            # это, вот, значит
                                            this_that_means_flag = thisThatMeansFinding(inputSentence, s_part[s_lex_idx][s_var_idx][2], p_part[p_lex_idx][p_var_idx][2])
                                            # не
                                            not_flag = notFinding(inputSentence, s_part[s_lex_idx][s_var_idx][2], p_part[p_lex_idx][p_var_idx][2])
                                            # как, словно, будто
                                            as_flag = asAs_ifAs_though(inputSentence, s_part[s_lex_idx][s_var_idx][2], p_part[p_lex_idx][p_var_idx][2])
                                            # союз, частица, обстоятельство ИЛИ вводное слово, оборот
                                            conj_prcl_advb_parenthesis_flag = parenthesisFinding(inputSentence, s_part[s_lex_idx][s_var_idx][2], p_part[p_lex_idx][p_var_idx][2]) or conjPrclAdvbFinding(inputSentence, s_part[s_lex_idx][s_var_idx][2], p_part[p_lex_idx][p_var_idx][2])
                                            if p_part[p_lex_idx][p_var_idx][0] == p_priority_idx and (dash_hyphen_flag or not this_that_means_flag):
                                                if p_part[p_lex_idx][p_var_idx][0] == VERB_PREDICATE_PRIORITY:
                                                    if s_part[s_lex_idx][s_var_idx][0] <= PRTF_SUBJECT_PRIORITY:
                                                        if not (s_part[s_lex_idx][s_var_idx][3].number == "plur" and p_part[p_lex_idx][p_var_idx][3].number == "sing"):
                                                            gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    elif s_part[s_lex_idx][s_var_idx][0] == ADVB_SUBJECT_PRIORITY:
                                                        if p_part[p_lex_idx][p_var_idx][3].number == "sing" and p_part[p_lex_idx][p_var_idx][3].gender in ["masc", "neut"]:
                                                            gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                elif p_part[p_lex_idx][p_var_idx][0] == INFN_PREDICATE_PRIORITY:
                                                    if s_part[s_lex_idx][s_var_idx][0] <= PRTF_SUBJECT_PRIORITY:
                                                        if dash_hyphen_flag and not as_flag:
                                                            gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                        elif as_flag and not dash_hyphen_flag:
                                                            gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    elif s_part[s_lex_idx][s_var_idx][0] == INFN_SUBJECT_PRIORITY and dash_hyphen_flag:
                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                elif p_part[p_lex_idx][p_var_idx][0] == NOUN_PREDICATE_PRIORITY:
                                                    if s_part[s_lex_idx][s_var_idx][0] == NOUN_SUBJECT_PRIORITY:
                                                        if p_part[p_lex_idx][p_var_idx][3].number == s_part[s_lex_idx][s_var_idx][3].number:
                                                            if dash_hyphen_flag and not conj_prcl_advb_parenthesis_flag:
                                                                if this_that_means_flag:
                                                                    gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                                elif not (not_flag or as_flag):
                                                                    gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                            elif not dash_hyphen_flag and ((not_flag or as_flag) and not this_that_means_flag) or conj_prcl_advb_parenthesis_flag:
                                                                gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    elif s_part[s_lex_idx][s_var_idx][0] in [NPRO_SUBJECT_PRIORITY, PRTF_SUBJECT_PRIORITY, ADJF_SUBJECT_PRIORITY]:
                                                        if s_part[s_lex_idx][s_var_idx][3].number == p_part[p_lex_idx][p_var_idx][3].number:
                                                            if s_part[s_lex_idx][s_var_idx][3].number == "plur" or s_part[s_lex_idx][s_var_idx][3].number == "sing" and s_part[s_lex_idx][s_var_idx][3].gender == p_part[p_lex_idx][p_var_idx][3].gender:
                                                                gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    elif s_part[s_lex_idx][s_var_idx][0] == NUMR_SUBJECT_PRIORITY:
                                                        if s_part[s_lex_idx][s_var_idx][3].number == p_part[p_lex_idx][p_var_idx][3].number:
                                                            if s_part[s_lex_idx][s_var_idx][3].number == "plur" or s_part[s_lex_idx][s_var_idx][3].number == "sing" and s_part[s_lex_idx][s_var_idx][3].gender == p_part[p_lex_idx][p_var_idx][3].gender:
                                                                if dash_hyphen_flag and not conj_prcl_advb_parenthesis_flag:
                                                                    if this_that_means_flag:
                                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                                    elif not (not_flag or as_flag):
                                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                                elif not dash_hyphen_flag and ((not_flag or as_flag) and not this_that_means_flag) or conj_prcl_advb_parenthesis_flag:
                                                                    gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    elif s_part[s_lex_idx][s_var_idx][0] == INFN_SUBJECT_PRIORITY:
                                                        if p_part[p_lex_idx][p_var_idx][3].number == "sing" and (p_part[p_lex_idx][p_var_idx][3].gender == "masc" or p_part[p_lex_idx][p_var_idx][3].gender == "neut"):
                                                            if dash_hyphen_flag and not conj_prcl_advb_parenthesis_flag:
                                                                if this_that_means_flag:
                                                                    gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                                elif not (not_flag or as_flag):
                                                                    gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                            elif not dash_hyphen_flag and ((not_flag or as_flag) and not this_that_means_flag) or conj_prcl_advb_parenthesis_flag:
                                                                gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    else:
                                                        if p_part[p_lex_idx][p_var_idx][3].number == "sing" and (p_part[p_lex_idx][p_var_idx][3].gender == "masc" or p_part[p_lex_idx][p_var_idx][3].gender == "neut"):
                                                            gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                elif p_part[p_lex_idx][p_var_idx][0] in [ADJF_PREDICATE_PRIORITY, ADJS_PREDICATE_PRIORITY, PRTF_PREDICATE_PRIORITY, PRTS_PREDICATE_PRIORITY]:
                                                    if p_part[p_lex_idx][p_var_idx][3].number == "sing":
                                                        if s_part[s_lex_idx][s_var_idx][0] in [INFN_SUBJECT_PRIORITY, ADVB_SUBJECT_PRIORITY]:
                                                            if dash_hyphen_flag and p_part[p_lex_idx][p_var_idx][3].gender in ["masc", "neut"]:
                                                                gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                        elif s_part[s_lex_idx][s_var_idx][3].number == "sing":
                                                            if s_part[s_lex_idx][s_var_idx][3].gender == p_part[p_lex_idx][p_var_idx][3].gender:
                                                                gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                            elif s_part[s_lex_idx][s_var_idx][3].gender == "neut":
                                                                gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    else:
                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                elif p_part[p_lex_idx][p_var_idx][0] in [ADVB_PREDICATE_PRIORITY, COMP_PREDICATE_PRIORITY]:
                                                    if s_part[s_lex_idx][s_var_idx][0] == INFN_SUBJECT_PRIORITY:
                                                        if dash_hyphen_flag:
                                                            gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    else:
                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                elif p_part[p_lex_idx][p_var_idx][0] == NUMR_PREDICATE_PRIORITY:
                                                    if s_part[s_lex_idx][s_var_idx][0] in [NOUN_SUBJECT_PRIORITY, NUMR_SUBJECT_PRIORITY]:
                                                        if s_part[s_lex_idx][s_var_idx][3].number == p_part[p_lex_idx][p_var_idx][3].number:
                                                            if s_part[s_lex_idx][s_var_idx][3].number == "plur" or s_part[s_lex_idx][s_var_idx][3].number == "sing" and s_part[s_lex_idx][s_var_idx][3].gender == p_part[p_lex_idx][p_var_idx][3].gender:
                                                                if dash_hyphen_flag:
                                                                    if this_that_means_flag:
                                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                                    elif not (not_flag or as_flag):
                                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                                elif (not_flag or as_flag) and not this_that_means_flag:
                                                                    gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    elif s_part[s_lex_idx][s_var_idx][0] in [NPRO_SUBJECT_PRIORITY, ADJF_SUBJECT_PRIORITY, PRTF_SUBJECT_PRIORITY]:
                                                        if s_part[s_lex_idx][s_var_idx][3].number == p_part[p_lex_idx][p_var_idx][3].number:
                                                            if s_part[s_lex_idx][s_var_idx][3].number == "plur" or s_part[s_lex_idx][s_var_idx][3].number == "sing" and s_part[s_lex_idx][s_var_idx][3].gender == p_part[p_lex_idx][p_var_idx][3].gender:
                                                                gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                    else:
                                                        if p_part[p_lex_idx][p_var_idx][3].number == "sing" and s_part[s_lex_idx][s_var_idx][3].gender in ["masc", "neut"]:
                                                            if s_part[s_lex_idx][s_var_idx][0] == INFN_SUBJECT_PRIORITY:
                                                                if dash_hyphen_flag:
                                                                    if this_that_means_flag:
                                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                                    elif not (not_flag or as_flag):
                                                                        gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                                elif (not_flag or as_flag) and not this_that_means_flag:
                                                                    gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                            gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                                else:
                                                    if s_part[s_lex_idx][s_var_idx][0] <= PRTF_SUBJECT_PRIORITY:
                                                        if s_part[s_lex_idx][s_var_idx][3].number == p_part[p_lex_idx][p_var_idx][3].number:
                                                            if s_part[s_lex_idx][s_var_idx][3].number == "plur" or s_part[s_lex_idx][s_var_idx][3].number == "sing" and s_part[s_lex_idx][s_var_idx][3].gender == p_part[p_lex_idx][p_var_idx][3].gender:
                                                                gram_basis_vars.append([predes.index(p_part), s_part[s_lex_idx][s_var_idx][3::-1], p_part[p_lex_idx][p_var_idx][3::-1]])
                                if not p_flag:
                                    for s_lex_idx in range(part_len):
                                        s_vars_count = len(s_part[s_lex_idx])
                                        for s_var_idx in range(s_vars_count):
                                            gram_basis_vars.append([subjes.index(s_part), s_part[s_lex_idx][s_var_idx][3::-1], []])
        if not s_flag:
            p_part = predes[subjes.index(s_part)]
            part_len = len(p_part)
            for p_lex_idx in range(part_len):
                p_vars_count = len(predes[subjes.index(s_part)][p_lex_idx])
                for p_var_idx in range(p_vars_count):
                    gram_basis_vars.append([predes.index(p_part), [], p_part[p_lex_idx][p_var_idx][3::-1]])
    return gram_basis_vars


def subjectFormFinding(inputWordForms, lexIndex):
    allWordSubjectForms = []
    varCount = len(inputWordForms)
    for varIdx in range(varCount):
        # существительное в им. падеже
        if inputWordForms[varIdx].tag.POS == 'NOUN' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([NOUN_SUBJECT_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # местоимение-существительное в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'NPRO' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([NPRO_SUBJECT_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # числительное в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'NUMR' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([NUMR_SUBJECT_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # инфинитив
        elif inputWordForms[varIdx].tag.POS == 'INFN':
            allWordSubjectForms.append([INFN_SUBJECT_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # прилагательное в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'ADJF' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([ADJF_SUBJECT_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # причастие в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'PRTF' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([PRTF_SUBJECT_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # наречие
        elif inputWordForms[varIdx].tag.POS == 'ADVB':
            allWordSubjectForms.append([ADVB_SUBJECT_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
    return allWordSubjectForms


def predicateFormFinding(inputWordForms, lexIndex):
    allWordPredicateForms = []
    varCount = len(inputWordForms)
    for varIdx in range(varCount):
        # глагол в любой форме
        if inputWordForms[varIdx].tag.POS == 'VERB':
            allWordPredicateForms.append([VERB_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # инфинитив
        elif inputWordForms[varIdx].tag.POS == 'INFN':
            allWordPredicateForms.append([INFN_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # наречие
        elif inputWordForms[varIdx].tag.POS == 'ADVB':
            allWordPredicateForms.append([ADVB_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # существительное в им. падеже
        if inputWordForms[varIdx].tag.POS == 'NOUN' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordPredicateForms.append([NOUN_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # компаратив
        elif inputWordForms[varIdx].tag.POS == 'COMP':
            allWordPredicateForms.append([COMP_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # прилагательное в им. падеже падеже
        elif inputWordForms[varIdx].tag.POS == 'ADJF' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordPredicateForms.append([ADJF_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # краткое прилагательное
        elif inputWordForms[varIdx].tag.POS == 'ADJS':
            allWordPredicateForms.append([ADJS_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # местоимение-существительное в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'NPRO' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordPredicateForms.append([NPRO_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # числительное в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'NUMR' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordPredicateForms.append([NUMR_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # причастие в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'PRTF' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordPredicateForms.append([PRTF_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # краткое причастие
        elif inputWordForms[varIdx].tag.POS == 'PRTS':
            allWordPredicateForms.append([PRTS_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
    return allWordPredicateForms

def thisThatMeansFinding(inputSentence, subj_position, pred_position):
    this_flag = False # это
    that_flag = False # вот
    means_flag = False # значит
    for lexemIdx in range(subj_position + 1, pred_position):
        if inputSentence["lexems"][lexemIdx]["lexem"] == "это":
            this_flag = True
        elif inputSentence["lexems"][lexemIdx]["lexem"] == "вот":
            that_flag = True
        elif inputSentence["lexems"][lexemIdx]["lexem"] == "вот":
            means_flag = True
    return this_flag or that_flag or means_flag


def asAs_ifAs_though(inputSentence, subj_position, pred_position):
    as_flag = False # как
    as_if_flag = False # словно
    as_though_flag = False # будто
    for lexemIdx in range(subj_position + 1, pred_position):
        if inputSentence["lexems"][lexemIdx]["lexem"] == "как":
            as_flag = True
        elif inputSentence["lexems"][lexemIdx]["lexem"] == "словно":
            as_if_flag = True
        elif inputSentence["lexems"][lexemIdx]["lexem"] == "будто":
            as_though_flag = True
    return as_flag or as_if_flag or as_though_flag


def notFinding(inputSentence, subj_position, pred_position):
    not_flag = False # это
    for lexemIdx in range(subj_position + 1, pred_position):
        if inputSentence["lexems"][lexemIdx]["lexem"] == "не":
            this_flag = True
    return not_flag


def parenthesisFinding(inputSentence, subj_position, pred_position):
    first_flag = False # вводное слово ограничивается всегда 2-мя запятыми
    second_flag = False
    for lexemIdx in range(subj_position + 1, pred_position):
        if inputSentence["lexems"][lexemIdx]["lexem"] == ",":
            if first_flag:
                second_flag = True
            else:
                first_flag = True
    return second_flag


def dashHyphenFinding(inputSentence, subj_position, pred_position):
    dash_flag = False # тире
    hyphen_flag = False # дефис
    for lexemIdx in range(subj_position + 1, pred_position):
        if inputSentence["lexems"][lexemIdx]["lexem"] in ["-", "–"]:
            if hyphen_flag:
                hyphen_flag = False
            else:
                hyphen_flag = True
        elif inputSentence["lexems"][lexemIdx]["lexem"] == "—":
            if dash_flag:
                dash_flag = False
            else:
                dash_flag = True                                                    
    return dash_flag or hyphen_flag


def conjPrclAdvbFinding(inputSentence, subj_position, pred_position):
    conj_flag = False # союз
    prcl_flag = False # частица
    advb_flag = False# наречие
    for lexemIdx in range(subj_position + 1, pred_position):
        variants = inputSentence["lexems"][lexemIdx]["variants"]
        for var in variants:
            if {"CONJ"} in var.tag:
                conj_flag = True
            if {"PRCL"} in var.tag:
                prcl_flag = True
            if {"ADVB"} in var.tag:
                advb_flag = True
    return conj_flag or prcl_flag or advb_flag


def gramBasisFiltering(inputSentence, gram_basis_vars, parts_count):
    res_gb = []
    # по частям предложения
    # for i in gram_basis_vars:
    #     print(i)
    for partIdx in range(parts_count):
        # по вариантам в частях
        part_var_scores = []
        for var in gram_basis_vars:
            var_score = 0
            subj_POS = None
            pred_POS = None
            # если вариант не принадлежит текущей части, проходим мимо него
            if var[0] != partIdx:
                continue
            # счёт вариантов подлежащего и сказуемого для выбора наилучшего
            subj_score, pred_score = 0, 0
            # если есть подлежащее
            if var[1]:
                subj_score = var[1][-1]
                subj_POS = var[1][0].POS
            else:
                subj_score = 0
            # если есть сказуемое
            if var[2]:
                pred_score = var[2][-1]
                pred_POS = var[2][0].POS
            else:
                pred_score = 0
            # считаем счёт
            var_score = subj_score + pred_score
            if subj_POS and pred_POS and var[1][1] > var[2][1]:
                if subj_POS in ["NOUN", "ADJF", "PRTF", "NPRO"] and pred_POS in ["VERB", "COMP", "NPRO", "ADJS", "PRTS"]:
                    part_var_scores.append([var_score, var])
            else:
                part_var_scores.append([var_score, var])
        part_var_scores.sort()
        for i in part_var_scores:
            res_gb.append(i[1])
    for i in res_gb:
        print(i)
    return res_gb

# testing
parsedTestText = parsing(gettingData())
# printingParseResult(parsedTestText)
testInputSentence = parsedTestText["paragraphs"][0]["sentences"][0]
separators = sentSeparatorsFinding(testInputSentence)
# функции для примера ниже перенести в другой файл
subj_vars, pred_vars = sentGramBasisVarsFinding(testInputSentence, separators)
gram_basis = gramBasisFiltering(testInputSentence, gramBasisFinding(testInputSentence, subj_vars, pred_vars), len(separators))
# printingParseResult(parsedTestText)
                                            # lexems_count = len(inputSentence["lexems"])
                                            # hyphen_flag = False
                                            # dash_flag = False
                                            # for lexemIdx in range(s_part[s_lex_idx][2] + 1, p_part[p_lex_idx][2]):
                                            #     if inputSentence["lexems"][lexemIdx]["lexem"] == "-":
                                            #         if hyphen_flag:
                                            #             hyphen_flag = False
                                            #         else:
                                            #             hyphen_flag = True
                                            #     if inputSentence["lexems"][lexemIdx]["lexem"] == "—":
                                            #         if dash_flag:
                                            #             dash_flag = False
                                            #         else:
                                            #             dash_flag = True
                                            # if hyphen_flag or dash_flag:
                                            #     continue
                            # lexems_count = len(inputSentence["lexems"])
                            # for lexemIdx in range(lexems_count):
                            #     if {"PNKT"} in inputSentence["lexems"][lexemIdx]["variants"][0].tag and \
                            #             inputSentence["lexems"][lexemIdx]["lexem"] == ":" or \
                            #             inputSentence["lexems"][lexemIdx]["lexem"] == "-" or \
                            #             inputSentence["lexems"][lexemIdx]["lexem"] == "—":
                            #         separators_indexes.append(lexemIdx)
                            