def gettingData():
    inputData = []
    # цикл на ввод, пока не введем то что нужно для анализа
    print("Если хотите выйти из программы нажмите комбинацию клавиш 'ctrl+C'...\n")
    while True:
        try:
            choiceInputStr = input("Если хотите ввести строку текста в командной строке, введите слово 'вручную',\nесли хотите прочитать текст из файла, введите слово 'файл': ").strip("\n")
        except KeyboardInterrupt:
            print("\nПрощайте!")
            exit()
        if choiceInputStr != "файл" and choiceInputStr != "вручную":
            print("Пожалуйста, введите корректную инструкцию для продолжения работы.\n")
            continue
        elif choiceInputStr != "файл" and choiceInputStr == "вручную":
            # ввод текста вручную в командной строке
            try:
                inputData = [input("Введите текст, оканчивающийся символом переноса строки (или нажмите Enter): ").strip("\n")]
            except KeyboardInterrupt:
                print("\nПрощайте!")
                exit()
            break
        else:
            # ввод текста чтением из файла
            while True:
                try:
                    inputFileName = input("Введите имя файла (полный путь/имя внутри данной директории): ").strip("\n")
                    f = open(inputFileName, encoding="UTF-8").readlines()
                except FileNotFoundError:
                    print("Файл не найден. Повторите попытку...")
                except KeyboardInterrupt:
                    print("\nПрощайте!")
                    exit()
                else:
                    break
            for line in f:
                inputData.append(line.strip("\n"))
            break
    return inputData

# testing
# print(gettingData())