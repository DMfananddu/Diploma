# функция, которая разделяет предложения по знакам препинания
# нужно учесть инициалы и приведённые нижу общепринятые сокращения
"""
т. д. — так далее
т. п. — тому подобное
д. б. — должно быть
м. б. — может быть
т. е. — то есть
т. к. — так как
"""

DOT_ORD = 46 # код точки
OTHER_SEPARATORS_ORDS = [33, 63] # коды восклицательного и вопросительного знаков
T._TE_TD_TP_TK = "т."



def sentencesTokenize(inputText):
    buf_last_word = "" # место для последнего слова перед возможным знаком препинания
    input_words = inputText.split()
    buf_sentence = ""
    output_sentences = [] # list выходных предложений
    for word in input_words:
        buf_last_word += word
        if buf_last_word == "т." or buf_last_word == "т." or buf_last_word == "т.":
            buf_last_word = "то есть"

        if ord(word[-1]) in OTHER_SEPARATORS_ORDS:
            buf_sentence += word
            output_sentences.append(buf_sentence)
            buf_sentence = ""


# testing
testText = "Н. Р. Брысина и М.А. Кучеренко задолбали, заколебали и т.д., и т. п."
sentencesTokenize(testText)