from pymorphy2 import MorphAnalyzer

slovo = input().strip()
morph = MorphAnalyzer().parse(slovo)
wordCount = 0

for i in range(len(morph)):
    if morph[i].normal_form == slovo.lower() or len(morph[i].normal_form)//len(slovo.lower()) < 3 and {'UNKN'} not in morph[i].tag:
        # print(morph[i].normal_form, slovo.lower())
        wordCount += 1
print(wordCount)
print(morph)