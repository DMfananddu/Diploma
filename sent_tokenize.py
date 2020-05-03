from normal_parser import parsing, printingParseResult
from conj_finding import sentenceConjFinding, conjCheking
from reader import gettingData
from copy import deepcopy

# приоритеты существит., местоим., числит., прил., причастия, инфинитива, наречия
SUBJECT_PRIORITY_COUNT = 7
NOUN_SUBJECT_PRIORITY = 0
NPRO_SUBJECT_PRIORITY = 1
NUMR_SUBJECT_PRIORITY = 2
ADJF_SUBJECT_PRIORITY = 3
PRTF_SUBJECT_PRIORITY = 4
INFN_SUBJECT_PRIORITY = 5
ADVB_SUBJECT_PRIORITY = 6

# приоритеты существит., местоим., числит., прил., причастия, наречия, инфинитива
PREDICATE_PRIORITY_COUNT = 11
VERB_PREDICATE_PRIORITY = 0
INFN_PREDICATE_PRIORITY = 1
NOUN_PREDICATE_PRIORITY = 2
ADJF_PREDICATE_PRIORITY = 3
PRTF_PREDICATE_PRIORITY = 4
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
    parts_count = len(allSubjectForms)
    for part in range(parts_count):
        print(part, "Subjectes")
        subjs_part_count = len(allSubjectForms[part])
        for subj in range(subjs_part_count):
            print("\t", subj)
            vars_count = len(allSubjectForms[part][subj])
            for var in range(vars_count):
                print("\t\t", allSubjectForms[part][subj][var])
        print(part, "Predicates")
        subjs_part_count = len(allPredicateForms[part])
        for subj in range(subjs_part_count):
            print("\t", subj)
            vars_count = len(allPredicateForms[part][subj])
            for var in range(vars_count):
                print("\t\t", allPredicateForms[part][subj][var])
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

# testing
parsedTestText = parsing(gettingData())
testInputSentence = parsedTestText["paragraphs"][0]["sentences"][0]
separators = sentSeparatorsFinding(testInputSentence)
subj_vars, pred_vars = sentGramBasisVarsFinding(testInputSentence, separators)


def gramBasisFinding(inputSentence, subj_vars, pred_vars):
    parts_count = len(subj_vars)
    gram_basis_vars = []
    for s_part in subj_vars:
        part_len = len(s_part)
        for s_priority_idx in range(SUBJECT_PRIORITY_COUNT):
            for s_var_idx in range(part_len):
                if s_part[s_var_idx][0] == s_priority_idx:
                    if s_part[s_var_idx][0] <= 4:
                        # if s_var[0] == 0:
                        #     break
                        # elif s_var[0] == 1:
                        #     break
                        # elif s_var[0] == 2:
                        #     break
                        # elif s_var[0] == 3:
                        #     break
                        # else:
                        #     break
                        # lexems_count = len(inputSentence["lexems"])
                        # for lexemIdx in range(lexems_count):
                        #     if {"PNKT"} in inputSentence["lexems"][lexemIdx]["variants"][0].tag and \
                        #             inputSentence["lexems"][lexemIdx]["lexem"] == ":" or \
                        #             inputSentence["lexems"][lexemIdx]["lexem"] == "-" or \
                        #             inputSentence["lexems"][lexemIdx]["lexem"] == "—":
                        #         separators_indexes.append(lexemIdx)
                        
                        for p_part in pred_vars:
                            for p_priority_idx in range(PREDICATE_PRIORITY_COUNT):
                                for p_var_idx in range(part_len):
                                    if p_part[p_var_idx][0] == p_priority_idx:
                                        if p_part[p_var_idx][0] == VERB_PREDICATE_PRIORITY:
                                            lexems_count = len(inputSentence["lexems"])
                                            hyphen_flag = False
                                            dash_flag = False
                                            for lexemIdx in range(s_part[s_var_idx][2] + 1, p_part[p_var_idx][2]):
                                                if inputSentence["lexems"][lexemIdx]["lexem"] == "-":
                                                    if hyphen_flag:
                                                        hyphen_flag = False
                                                    else:
                                                        hyphen_flag = True
                                                if inputSentence["lexems"][lexemIdx]["lexem"] == "—":
                                                    if dash_flag:
                                                        dash_flag = False
                                                    else:
                                                        dash_flag = True
                                            if hyphen_flag or dash_flag:
                                                continue
                                            if s_part[s_var_idx][3].number == "sing":
                                                if p_part[p_var_idx][3].number == "sing":
                                                    if s_part[s_var_idx][3].gender == p_part[p_var_idx][3].gender:
                                                        gram_basis_vars.append([s_part[s_var_idx][2]], [s_part[s_var_idx][1]], [p_part[p_var_idx][2]], [p_part[p_var_idx][1]])
                                            else:
                                                gram_basis_vars.append([s_part[s_var_idx][2]], [s_part[s_var_idx][1]], [p_part[p_var_idx][2]], [p_part[p_var_idx][1]])
    return 0


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
        # существительное в им. и тв. падеже
        if inputWordForms[varIdx].tag.POS == 'NOUN' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([NOUN_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # компаратив
        elif inputWordForms[varIdx].tag.POS == 'COMP':
            allWordPredicateForms.append([COMP_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # прилагательное в им. падеже и тв. падеже
        elif inputWordForms[varIdx].tag.POS == 'ADJF' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([ADJF_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # краткое прилагательное
        elif inputWordForms[varIdx].tag.POS == 'ADJS':
            allWordPredicateForms.append([ADJS_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # местоимение-существительное в им. и тв. падеже
        elif inputWordForms[varIdx].tag.POS == 'NPRO' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([NPRO_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # числительное в им. и тв. падеже
        elif inputWordForms[varIdx].tag.POS == 'NUMR' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([NUMR_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # причастие в им. и тв. падеже
        elif inputWordForms[varIdx].tag.POS == 'PRTF' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([PRTF_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
        # краткое причастие
        elif inputWordForms[varIdx].tag.POS == 'PRTS' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([PRTS_PREDICATE_PRIORITY, varIdx, lexIndex, inputWordForms[varIdx].tag])
    return allWordPredicateForms
