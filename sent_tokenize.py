from normal_parser import parsing, printingParseResult

def sentTokenize(inputSentence):
    outputSentence = ""
    lenInputSentence = len(inputSentence["lexems"])
    allSubjectForms = []
    allPredicateForms = []
    for lexIndex in range(lenInputSentence):
        allSubjectForms.append(subjectFormFinding(inputSentence["lexems"][lexIndex]["variants"]))
        allPredicateForms.append(predicateFormFinding(inputSentence["lexems"][lexIndex]["variants"]))
    outputSentence = inputSentence
    return allSubjectForms, allPredicateForms

# приоритеты существит., местоим., числит., прил., причастия, наречия, инфинитива
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
ADVB_PREDICATE_PRIORITY = 3
NOUN_PREDICATE_PRIORITY = 4
COMP_PREDICATE_PRIORITY = 5
ADJF_PREDICATE_PRIORITY = 6
ADJS_PREDICATE_PRIORITY = 7
NUMR_PREDICATE_PRIORITY = 8
NPRO_PREDICATE_PRIORITY = 9
PRTF_PREDICATE_PRIORITY = 10
PRTS_PREDICATE_PRIORITY = 11


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
testSentence = ["В знакомой сакле огонёк то трепетал, то снова гас."]
# printingParseResult(parsing(testSentence))
resSub, resPred = sentTokenize(parsing(testSentence)["paragraphs"][-1]["sentences"][-1])
for i in range(len(resSub)):
    print(i)
    for j in range(len(resSub[i])):
        print("\t", resSub[i][j])
for i in range(len(resPred)):
    print(i)
    for j in range(len(resPred[i])):
        print("\t", resPred[i][j])
