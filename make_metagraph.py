from reader import gettingData
from normal_parser import parsing, printingParseSentence
from copy import deepcopy
from sent_tokenizer import sentSeparatorsFinding, sentGramBasisVarsFinding, gramBasisFinding, gramBasisFiltering
from analyser import analyzeVarsForming
from metagrapher import metagraphMaker


if __name__ == "__main__":
    # testing
    parsedTestText = parsing(gettingData())
    # printingParseResult(parsedTestText)
    prgf_count = len(parsedTestText["paragraphs"])
    full_text_metagraphs = [None for i in range(prgf_count)]
    for prgf in range(prgf_count):
        sent_count = len(parsedTestText["paragraphs"][prgf]["sentences"])
        prgf_metagraphs = [None for i in range(sent_count)]
        full_text_metagraphs[prgf] = prgf_metagraphs
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
            sent_atba, sent_res, to_MM = analyzeVarsForming(testInputSentence, conjs, separators, sent, prgf, gbVars)
            for i in range(len(sent_atba)):
                lexems = []
                pncts = []
                start = 0
                finish = len(testInputSentence["lexems"])
                for lex in range(finish):
                    lexems.append(testInputSentence["lexems"][lex]["lexem"])
                    if {"PNCT"} in testInputSentence["lexems"][lex]["variants"][0]:
                        pncts.append([lex, testInputSentence["lexems"][lex]["lexem"]])
                pncts.reverse()
                start = separators[i]
                finish = separators[i+1]
                sent_res_i_flag = False
                for j in range(len(sent_res[i])):
                    if True in sent_res[i][j]:
                        sent_res_i_flag = True
                        break
                if not sent_atba[i] or not sent_res_i_flag:
                    print("{}-ю часть {}-го предложения {}-го абзаца невозможно проанализировать.".format(i, sent, prgf))
                    if not sent_atba[i]:
                        print("Причина: Отсутствие грамматической основы части.")
                    if not sent_res_i_flag:
                        print("Причина: Отсутствие вариантов разбора части.")
                    print("\tДанное предложение: ", lexems)
                    print("\tДанная часть: ", lexems[start:finish])
            parts_count = len(separators)-1
            sent_parts_vars_count = [0 for i in range(len(separators)-1)]
            for i in range(len(to_MM)):
                sent_parts_vars_count[to_MM[i][1][0][4]] += 1
            # print(sent_parts_vars_count)
            sent_vars_count = 1
            for i in sent_parts_vars_count:
                sent_vars_count *= i
            if sent_vars_count != 0:
                print("\nУ данного предложения существует следующее количество вариантов разбора: {}\n\n".format(sent_vars_count))
                sent_metagraph = []
                sent_metagraph = metagraphMaker(sent_metagraph, to_MM, pncts, prgf, sent, parts_count, sent_parts_vars_count)
                prgf_metagraphs[sent] = sent_metagraph
            else:
                print("{}-е предложение {}-го абзаца невозможно проанализировать.".format(sent, prgf))
                print("Причина: Отсутствие возможности разбора по крайней мере одной из частей предложения.")

