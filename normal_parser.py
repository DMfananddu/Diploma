import nltk
from reader import gettingData
from rusenttokenize import ru_sent_tokenize
from pymorphy2 import MorphAnalyzer

# функция получает строку и делает из него специальную иерархическую структуру
def parsing(inputText):
    # текст - текст (list) + его абзацы
    text = {"text": inputText, "paragraphs": []}
    # параграфы - list параграфов
    paragraphs = text["text"]
    for p in paragraphs:
        # параграф - текст парграфа + предложения
        paragraph = {"paragraph": p, "sentences": []}
        text["paragraphs"].append(paragraph)
        # производим токенизацию предложений с использованием nltk
        sentences = ru_sent_tokenize(p)
        for s in sentences:
            # предложение - текст предложения + предложения + информация (для будущих шагов)
            sentence = {"sentence": s, "lexems": [], "info": []}
            text["paragraphs"][-1]["sentences"].append(sentence)
            # производим токенизацию предложений с использованием nltk
            lexems = nltk.word_tokenize(s, language="russian")
            for l in lexems:
                # лексема - лексема + варианты её морф.значений (из словаря pymorphy2)
                lexem = {"lexem": l, "variants": []}
                text["paragraphs"][-1]["sentences"][-1]["lexems"].append(lexem)
                morph = MorphAnalyzer().parse(l.lower())
                morphCount = len(morph)
                wordCount = 0
                for i in range(morphCount):
                    # если вероятность слова > вероятности междометия (отн. других)
                    # И (
                    # норм.форма == самой лексеме
                    # ИЛИ (
                    #   длина норм.формы менее, чем в 3 раза превышает длина лексемы
                    #   И данный вариант не "UNKN"
                    #   (иначе дальнейший такого варианта не имеет смысла)
                    #   )
                    # )
                    if morph[i].score >= 0.01 and (morph[i].normal_form == l.lower() or len(morph[i].normal_form)//len(l) < 3 and {'UNKN'} not in morph[i].tag):
                        # print(morph[i].normal_form, slovo.lower())
                        wordCount += 1
                        lexem["variants"].append(morph[i].tag)
    return text


# просто функция печати всей этой структуры
def printingParseText(textInfoDict):
    print(textInfoDict["text"])
    paragraphsCount = len(textInfoDict["paragraphs"])
    for p in range(paragraphsCount):
        print("\t", textInfoDict["paragraphs"][p]["paragraph"])
        sentencesCount = len(textInfoDict["paragraphs"][p]["sentences"])
        for s in range(sentencesCount):
            print("\t\t", textInfoDict["paragraphs"][p]["sentences"][s]["sentence"])
            print("\t\t", textInfoDict["paragraphs"][p]["sentences"][s]["info"])
            lexemsCount = len(textInfoDict["paragraphs"][p]["sentences"][s]["lexems"])
            for l in range(lexemsCount):
                print("\t\t\t", textInfoDict["paragraphs"][p]["sentences"][s]["lexems"][l]["lexem"])
                variantsCount = len(textInfoDict["paragraphs"][p]["sentences"][s]["lexems"][l]["variants"])
                for v in range(variantsCount):
                    print("\t\t\t\t", textInfoDict["paragraphs"][p]["sentences"][s]["lexems"][l]["variants"][v])


# просто функция печати всей этой структуры
def printingParseSentence(sentenceInfoDict):
    print("\t\t", sentenceInfoDict["sentence"])
    print("\t\t", sentenceInfoDict["info"])
    lexemsCount = len(sentenceInfoDict["lexems"])
    for l in range(lexemsCount):
        print("\t\t\t", sentenceInfoDict["lexems"][l]["lexem"])
        variantsCount = len(sentenceInfoDict["lexems"][l]["variants"])
        for v in range(variantsCount):
            print("\t\t\t\t", sentenceInfoDict["lexems"][l]["variants"][v])

# testing
# printingParseText(parsing(gettingData()))

