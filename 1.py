from pymorphy2 import MorphAnalyzer

slovo = "е"
morph = MorphAnalyzer().parse(slovo)
wordCount = 0

for i in range(len(morph)):
    if morph[i].normal_form == slovo.lower() or len(morph[i].normal_form)//len(slovo.lower()) < 3:
        wordCount += 1
print(wordCount)
print(morph)