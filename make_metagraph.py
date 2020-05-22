from reader import gettingData
from normal_parser import parsing, printingParseSentence
from copy import deepcopy
from sent_tokenizer import sentSeparatorsFinding, sentGramBasisVarsFinding, gramBasisFinding, gramBasisFiltering
from preanalyser import analyzeVarsForming


if __name__ == "__main__":
    # testing
    parsedTestText = parsing(gettingData())
    # printingParseResult(parsedTestText)
    prgf_count = len(parsedTestText["paragraphs"])
    for prgf in range(prgf_count):
        sent_count = len(parsedTestText["paragraphs"][prgf]["sentences"])
        for sent in range(sent_count):
            testInputSentence = parsedTestText["paragraphs"][prgf]["sentences"][sent]
            separators, conjs = sentSeparatorsFinding(testInputSentence)
            # printingParseResult(parsedTestText)
            subj_vars, pred_vars = sentGramBasisVarsFinding(testInputSentence, separators)
            gbVars = gramBasisFiltering(testInputSentence, gramBasisFinding(testInputSentence, subj_vars, pred_vars), len(separators))
            if separators[0] != 0:
                new_separators = [0]
                new_separators.extend(separators)
                separators = new_separators
            # testing
            sent_atba, sent_res = analyzeVarsForming(testInputSentence, separators, sent, prgf, gbVars)
            for i in range(len(sent_atba)):
                lexems = []
                start = 0
                finish = len(testInputSentence["lexems"])
                for lex in range(finish):
                    lexems.append(testInputSentence["lexems"][lex]["lexem"])
                if separators:
                    if i == 0:
                        finish = separators[i]
                    elif i == len(sent_atba) - 1:
                        start = separators[i]
                    else:
                        start = separators[i]
                        finish = separators[i+1]
                if not sent_atba[i] or True not in sent_res[i][0]:
                    print("{}-ю часть {}-го предложения {}-го абзаца невозможно проанализировать.".format(i+1, sent, par))
                    if not sent_atba[i]:
                        print("Причина: Отсутствие грамматической основы предложения.")
                        continue
                    if True not in sent_res[i]:
                        print("Причина: Отсутствие вариантов разбора предложения.")
                    print("\tДанное предложение: ", lexems)
                    print("\tДанная часть: ", lexems[start:finish+1])
