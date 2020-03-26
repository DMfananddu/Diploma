import nltk
from reader import gettingData
from pymorphy2 import MorphAnalyzer

text = input().strip()

sentences = nltk.sent_tokenize(text)
for sentence in sentences:
    words = nltk.word_tokenize(sentence)
    for word in words:
        morph = MorphAnalyzer().parse(word)
        wordCount = 0

        for i in range(len(morph)):
            if morph[i].normal_form == word.lower() or len(morph[i].normal_form)//len(word.lower()) < 3 and {'UNKN'} not in morph[i].tag:
                # print(morph[i].normal_form, slovo.lower())
                wordCount += 1
        print("\n", word, wordCount)
        print(morph)
    print(words)
