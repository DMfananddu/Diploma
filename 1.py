from pymorphy2 import MorphAnalyzer

slovo = "Москва"
morph = MorphAnalyzer().parse(slovo)
wordCount = 0

for i in range(len(morph)):
    if morph[i].normal_form == slovo:
        wordCount += 1

print(wordCount)