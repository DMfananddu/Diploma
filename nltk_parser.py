import nltk
from reader import gettingData
from pymorphy2 import MorphAnalyzer

# testText = gettingData()

def parsing(inputText):
    text = {"text": inputText, "paragraphs": []}
    paragraphs = text["text"]
    for p in paragraphs:
        paragraph = {"paragraph": p, "sentences": []}
        text["paragraphs"].append(paragraph)
        sentences = nltk.sent_tokenize(p)
        for s in sentences:
            sentence = {"sentence": s, "lexems": [], "info": []}
            text["paragraphs"][-1]["sentences"].append(sentence)
            lexems = nltk.word_tokenize(s)
            for l in lexems:
                lexem = {"lexem": l, "variants": []}
                text["paragraphs"][-1]["sentences"][-1]["lexems"].append(lexem)
                morph = MorphAnalyzer().parse(l)
                morphCount = len(morph)
                wordCount = 0
                for i in range(morphCount):
                    if morph[i].score >= 0.1 and (morph[i].normal_form == l.lower() or len(morph[i].normal_form)//len(l) < 3 and {'UNKN'} not in morph[i].tag):
                        # print(morph[i].normal_form, slovo.lower())
                        wordCount += 1
                        lexem["variants"].append(morph[i])
    return text
    # printingParseResult(text)

def printingParseResult(textInfoDict):
    print(textInfoDict["text"])
    paragraphsCount = len(textInfoDict["paragraphs"])
    for p in range(paragraphsCount):
        print("\t", textInfoDict["paragraphs"][p]["paragraph"])
        sentencesCount = len(textInfoDict["paragraphs"][p]["sentences"])
        for s in range(sentencesCount):
            print("\t\t", textInfoDict["paragraphs"][p]["sentences"][s]["sentence"])
            lexemsCount = len(textInfoDict["paragraphs"][p]["sentences"][s]["lexems"])
            for l in range(lexemsCount):
                print("\t\t\t", textInfoDict["paragraphs"][p]["sentences"][s]["lexems"][l]["lexem"])
                variantsCount = len(textInfoDict["paragraphs"][p]["sentences"][s]["lexems"][l]["variants"])
                for v in range(variantsCount):
                    print("\t\t\t\t", textInfoDict["paragraphs"][p]["sentences"][s]["lexems"][l]["variants"][v])

# testing
# parsing(testText)
