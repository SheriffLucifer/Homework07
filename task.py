from os import path

phonebook = "phonebook.txt"
all_data = []
last_id = 0

if not path.exists(phonebook):
    with open(phonebook, "w", encoding="utf-8") as _:
        pass


def read_records():

    global all_data, last_id

    with open(phonebook, "r", encoding="utf-8") as f:
        all_data = [i.strip() for i in f]
        if all_data:
            last_id = int(all_data[-1][0])

        return all_data


def show_all():

    if not all_data:
        print("Нет данных")
    else:
        print(*all_data, sep="\n")


def add_new_contact():

    global last_id

    array = ['фамилию', 'имя', 'отчество', 'номер телефона']
    answers = []
    for i in array:
        answers.append(data_collection(i))

    if not exist_contact(0, " ".join(answers)):
        last_id += 1
        answers.insert(0, str(last_id))

        with open(phonebook, 'a', encoding="utf-8") as f:
            f.write(f'{" ".join(answers)}\n')
        print("Запись успешно добавлена в телефонную книгу!\n")
    else:
        print("Данные уже существуют!")


def del_contact():

    global all_data

    symbol = "\n"
    show_all()
    del_record = input("Введите номер записи: ")

    if exist_contact(del_record, ""):
        all_data = [k for k in all_data if k[0] != del_record]

        with open(phonebook, 'w', encoding="utf-8") as f:
            f.write(f'{symbol.join(all_data)}\n')
        print("Запись удалена!\n")
    else:
        print("Данные неверны!")


def change_contact(data_tuple):

    global all_data
    symbol = "\n"

    record_id, num_data, data = data_tuple

    for i, v in enumerate(all_data):
        if v[0] == record_id:
            v = v.split()
            v[int(num_data)] = data
            if exist_contact(0, " ".join(v[1:])):
                print("Данные уже существуют!")
                return
            all_data[i] = " ".join(v)
            break

    with open(phonebook, 'w', encoding="utf-8") as f:
        f.write(f'{symbol.join(all_data)}\n')
    print("Запись изменена!\n")


def search_contact():
    search_data = exist_contact(0, input("Введите данные для поиска: "))
    if search_data:
        print(*search_data, sep="\n")
    else:
        print("Данные неверны!")


def exist_contact(rec_id, data):

    if rec_id:
        applicants = [i for i in all_data if rec_id in i[0]]
    else:
        applicants = [i for i in all_data if data in i]
    return applicants


def data_collection(num):

    answer = input(f"Введите {num}: ")
    while True:
        if num in "фамилию имя отчество":
            if answer.isalpha():
                break
        if num == "номер телефона":
            if answer.isdigit() and len(answer) == 11:
                break
        answer = input(f"Данные неверны!\n"
                       f"Используйте только буквы алфавита,"
                       f" длина номера должна быть 11 цифр\n"
                       f"Введите {num}: ")
    return answer


def main_menu():

    play = True
    while play:
        read_records()
        answer = input("Телефонный справочник:\n"
                       "1. Показать все записи\n"
                       "2. Добавить запись\n"
                       "3. Поиск\n"
                       "4. Изменение данных\n"
                       "5. Удаление\n"
                       "6. Экспорт/Импорт\n"
                       "7. Выход\n")
        match answer:
            case "1":
                show_all()
            case "2":
                add_new_contact()
            case "3":
                search_contact()
            case "4":
                work = edit_menu()
                if work:
                    change_contact(work)
            case "5":
                del_contact()
            case "6":
                exp_imp_menu()
            case "7":
                play = False
            case _:
                print("Попробуйте еще раз!\n")


def edit_menu():

    add_dict = {"1": "Фамилия", "2": "Имя", "3": "Отчество", "4": "номер телефона"}

    show_all()
    record_id = input("Введите id записи: ")

    if exist_contact(record_id, ""):
        while True:
            print("\Изменить:")
            change = input("1. Фаимилию\n"
                           "2. Имя\n"
                           "3. Отчество\n"
                           "4. Номер телефона\n"
                           "5. Выход\n")

            match change:
                case "1" | "2" | "3" | "4":
                    return record_id, change, data_collection(add_dict[change])
                case "5":
                    return 0
                case _:
                    print("Данные не распознаны, повторите ввод.")
    else:
        print("Данные неверны!")


def exp_bd(name):

    symbol = "\n"

    if not path.exists(name):
        with open(f"{name}.txt", "w", encoding="utf-8") as f:
            f.write(f'{symbol.join(all_data)}\n')


def ipm_bd(name):
    global phonebook
    if path.exists(name):
        phonebook = name
        read_records()


def exp_imp_menu():

    while True:
        print("\nМеню экспорта/импорта:")
        move = input("1. Импорт\n"
                     "2. Экспорт\n"
                     "3. Выход\n")

        match move:
            case "1":
                ipm_bd(input("Введите имя файла: "))
            case "2":
                exp_bd(input("Введите имя файла: "))
            case "3":
                return 0
            case _:
                print("Данные не распознаны, повторите ввод.")


main_menu()