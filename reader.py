def gettingData():
    # выбор сповоба ввода текста:
    inputStr = ""
    inputFile = []
    while True:
        choiceInputStr = input("Если хотите ввести строку текста в командной строке, введите слово 'вручную',\nесли хотите прочитать текст из файла, введите слово 'файл': ").strip("\n")
        if choiceInputStr != "файл" and choiceInputStr != "вручную":
            print("Пожалуйста, введите корректную инструкцию для продолжения работы.\n")
            continue
        elif choiceInputStr != "файл" and choiceInputStr == "вручную":
            # ввод текста вручную в командной строке
            inputStr = [input("Введите текст, оканчивающийся символом переноса строки (или нажмите Enter): ").strip("\n")]
            break
        else:
            # ввод текста чтением из файла
            inputFileName = input("Введите имя файла (полный путь/имя внутри данной директории): ").strip("\n")
            f = open(inputFileName, encoding="UTF-8").readlines()
            for line in f:
                inputFile.append(line.strip("\n"))
            break
    inputData = inputStr or inputFile
    return inputData