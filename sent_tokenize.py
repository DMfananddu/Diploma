from normal_parser import parsing, printingParseResult
from conj_finding import sentenceConjFinding, conjCheking
from reader import gettingData
from copy import deepcopy

def sentGramBasisVarsFinding(inputSentence, separators_positions):
    allSubjectForms = []
    allPredicateForms = []
    partSubjectForms = []
    partPredicateForms = []
    sep_count = len(separators_positions)
    start = 0
    finish = 0
    separators_positions.append(len(inputSentence["lexems"]) - 1)
    for i in range(sep_count+1):
        start = finish
        finish = separators_positions[i]+1
        for lexIndex in range(start, finish):
            partSubjectForms.append(subjectFormFinding(inputSentence["lexems"][lexIndex]["variants"]))
            partPredicateForms.append(predicateFormFinding(inputSentence["lexems"][lexIndex]["variants"]))
        allSubjectForms.append(partSubjectForms)
        partSubjectForms = []
        allPredicateForms.append(partPredicateForms)
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

# приоритеты существит., местоим., числит., прил., причастия, инфинитива, наречия
NOUN_SUBJECT_PRIORITY = 1
NPRO_SUBJECT_PRIORITY = 2
NUMR_SUBJECT_PRIORITY = 3
ADJF_SUBJECT_PRIORITY = 4
PRTF_SUBJECT_PRIORITY = 5
INFN_SUBJECT_PRIORITY = 6
ADVB_SUBJECT_PRIORITY = 7

# приоритеты существит., местоим., числит., прил., причастия, наречия, инфинитива
VERB_PREDICATE_PRIORITY = 1
INFN_PREDICATE_PRIORITY = 2
NOUN_PREDICATE_PRIORITY = 3
ADJF_PREDICATE_PRIORITY = 4
PRTF_PREDICATE_PRIORITY = 5
ADJS_PREDICATE_PRIORITY = 6
PRTS_PREDICATE_PRIORITY = 7
ADVB_PREDICATE_PRIORITY = 8
COMP_PREDICATE_PRIORITY = 9
NUMR_PREDICATE_PRIORITY = 10
NPRO_PREDICATE_PRIORITY = 11


def subjectFormFinding(inputWordForms):
    allWordSubjectForms = []
    varCount = len(inputWordForms)
    for varIdx in range(varCount):
        # существительное в им. падеже
        if inputWordForms[varIdx].tag.POS == 'NOUN' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([NOUN_SUBJECT_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # местоимение-существительное в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'NPRO' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([NPRO_SUBJECT_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # числительное в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'NUMR' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([NUMR_SUBJECT_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # инфинитив
        elif inputWordForms[varIdx].tag.POS == 'INFN':
            allWordSubjectForms.append([INFN_SUBJECT_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # прилагательное в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'ADJF' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([ADJF_SUBJECT_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # причастие в им. падеже
        elif inputWordForms[varIdx].tag.POS == 'PRTF' and inputWordForms[varIdx].tag.case == 'nomn':
            allWordSubjectForms.append([PRTF_SUBJECT_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # наречие
        elif inputWordForms[varIdx].tag.POS == 'ADVB':
            allWordSubjectForms.append([ADVB_SUBJECT_PRIORITY, varIdx, inputWordForms[varIdx].tag])
    return allWordSubjectForms


def predicateFormFinding(inputWordForms):
    allWordPredicateForms = []
    varCount = len(inputWordForms)
    for varIdx in range(varCount):
        # глагол в любой форме
        if inputWordForms[varIdx].tag.POS == 'VERB':
            allWordPredicateForms.append([VERB_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # инфинитив
        elif inputWordForms[varIdx].tag.POS == 'INFN':
            allWordPredicateForms.append([INFN_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # наречие
        elif inputWordForms[varIdx].tag.POS == 'ADVB':
            allWordPredicateForms.append([ADVB_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # существительное в им. и тв. падеже
        if inputWordForms[varIdx].tag.POS == 'NOUN' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([NOUN_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # компаратив
        elif inputWordForms[varIdx].tag.POS == 'COMP':
            allWordPredicateForms.append([COMP_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # прилагательное в им. падеже и тв. падеже
        elif inputWordForms[varIdx].tag.POS == 'ADJF' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([ADJF_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # краткое прилагательное
        elif inputWordForms[varIdx].tag.POS == 'ADJS':
            allWordPredicateForms.append([ADJS_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # местоимение-существительное в им. и тв. падеже
        elif inputWordForms[varIdx].tag.POS == 'NPRO' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([NPRO_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # числительное в им. и тв. падеже
        elif inputWordForms[varIdx].tag.POS == 'NUMR' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([NUMR_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # причастие в им. и тв. падеже
        elif inputWordForms[varIdx].tag.POS == 'PRTF' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([PRTF_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
        # краткое причастие
        elif inputWordForms[varIdx].tag.POS == 'PRTS' and (inputWordForms[varIdx].tag.case == 'nomn' or inputWordForms[varIdx].tag.case == 'ablt'):
            allWordPredicateForms.append([PRTS_PREDICATE_PRIORITY, varIdx, inputWordForms[varIdx].tag])
    return allWordPredicateForms

# testing
# testSentence = ["В знакомой сакле огонёк то трепетал, то снова гас."]
# printingParseResult(parsing(testSentence))
# resSub, resPred = sentTokenize(parsing(testSentence)["paragraphs"][-1]["sentences"][-1])
# for i in range(len(resSub)):
#     print(i)
#     for j in range(len(resSub[i])):
#         print("\t", resSub[i][j])
# for i in range(len(resPred)):
#     print(i)
#     for j in range(len(resPred[i])):
#         print("\t", resPred[i][j])


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
separators = sentSeparatorsFinding(parsedTestText["paragraphs"][0]["sentences"][0])
sentGramBasisVarsFinding(parsedTestText["paragraphs"][0]["sentences"][0], separators)


def gramBasisFinding():
    return 0