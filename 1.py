from nltk import tokenize
from rusenttokenize import ru_sent_tokenize
testText = "Я: она, ты."

# sent = tokenize.sent_tokenize(testText, language="russian")
# print(sent)
# sent = ru_sent_tokenize(testText)
# print(sent)
# words = tokenize.word_tokenize(sent[0], language="russian")
# print(words)
# print(ord("—"), ord("-"), ord(":"))


def recursia(chislo, slist):
    if chislo > 3:
        print("выход")
        return
    chislo += 1
    slist.append(chislo)
    print("до рекурсии", chislo, slist)
    recursia(chislo, slist)
    print("после рекурсии", chislo, slist)

recursia(0, [])