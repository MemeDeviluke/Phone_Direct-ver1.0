#Были проведены следующие незначительные изменения
#1. Был сделан выход из программы (Просто break в 8 пункте main_function :D)
#2. Была создана опция не сохранять пустой файл, если нет этого желание -> Смотреть функцию save_direct(Изменение незначительное)
#3. Была создана история операций(Просто список из того, какие цифры вводит пользователь D:), которая требуется при проверки открывался ли справочник
# Если нет, то операции будут недоступны, это было сделано, для того, чтобы не было соблазна сохранять файл, не открывая его (Изменения незначительные)


main_direct = ['Телефонный справочник',
               'Открыть телефонный справочник',
               'Сохранить телефонный справочник',
               'Показать контакты',
               'Создать контакт',
               'Найти контакт',
               'Изменить контакт',
               'Удалить контакт',
               'Выход']

temporary_direct = {}
path = 'file.txt'
SEPARATOR = '|'
history_of_operations = []

def show_maindirect_menu():
    for i, item in enumerate(main_direct):
        if i:
            print(f'\t{i}. {item}')
        else:
            print(item)
    while True:
        choice = input(f'Выберите пункт меню ({1}-{len(main_direct) - 1}) ')
        if choice.isdigit() and 0 < int(choice) < len(main_direct):
            return int(choice)
        else:
            print(f'Нужно ввести число от 1 до {len(main_direct) - 1}!')


def open_direct():
    global temporary_direct
    with open(path, 'r', encoding='UTF-8') as file:
        database = file.readlines()
    for c_id, contact in enumerate(database, 1):
        temporary_direct[c_id] = contact.strip().split(SEPARATOR)


def save_direct(temporary_direct, message):
    if temporary_direct:
        data = []
        for contact in temporary_direct.values():
            data.append(SEPARATOR.join(contact))
        data = '\n'.join(data)
        with open(path, 'w', encoding='UTF-8') as file:
            file.write(data)
        show_message('Телефонный справочник сохранён')
    else:
        show_message(message)
        continuing = int(input("Вы собираетесь сохранить пустой справочник? \nЕсли да, то нажмите 1, если нет, то любое другое значение"))
        if continuing == 1:
            data = []
            for contact in temporary_direct.values():
                data.append(SEPARATOR.join(contact))
            data = '\n'.join(data)
            with open(path, 'w', encoding='UTF-8') as file:
                file.write(data)
            show_message('Телефонный справочник сохранён')
        else:
            show_message('Телефонный справочник не был сохранён')


def next_id():
    global temporary_direct
    if temporary_direct:
        return max(temporary_direct) + 1
    else:
        return 1


def show_message(message):
    print('\n' + '=' * len(message))
    print(message)
    print('=' * len(message) + '\n')


def show_contacts(temporary_direct, error_message):
    if temporary_direct:
        print('\n' + '=' * 71)
        for c_id, contact in temporary_direct.items():
            print(f'{c_id:>3}. {contact[0]:<20} | {contact[1]:<20} | {contact[2]:<20}')
        print('=' * 71 + '\n')
    else:
        show_message(error_message)


def take_data(message):
    if isinstance(message, str):
        return input('\n' + message)
    return [input(mes) for mes in message]


def append_contact(new_contact):
    global temporary_direct
    temporary_direct[next_id()] = new_contact


def contact_added(name):
    return f'Контакт "{name}" добавлен'


def find_contact_failed(wordly):
    return f'Контакты содержащие "{wordly}" не найдены'


def change_contact_success(name):
    return f'Контакт "{name}" изменён'


def delete_contact_success(name):
    return f'Контакт "{name}" удалён'


def find_contact(search_word):
    global temporary_direct
    result_direct = {}
    for c_id, contact in temporary_direct.items():
        if search_word.lower() in ' '.join(contact).lower():
            result_direct[c_id] = contact
    return result_direct


def main_find_contact(message):
    search_word = take_data(message)
    resulting = find_contact(search_word)
    show_contacts(resulting, find_contact_failed(search_word))
    return True if resulting else False


def change_contact(c_id, changed_contact):
    global temporary_direct
    current_contact = temporary_direct[c_id]
    for i in range(len(current_contact)):
        current_contact[i] = changed_contact[i] if changed_contact[i] else current_contact[i]
    temporary_direct[c_id] = current_contact
    return current_contact[0]


def delete_contact(c_id):
    global temporary_direct
    return temporary_direct.pop(c_id)[0]


def main_function():
    while True:
        choice = show_maindirect_menu()
        match choice:
            case 1:
                history_of_operations.append(1)
                open_direct()
                show_message('Телефонный справочник открыт')
            case 2:
                history_of_operations.append(2)
                save_direct(temporary_direct, 'Справочник пуст!')
            case 3:
                history_of_operations.append(3)
                show_contacts(temporary_direct, 'Телефонный справочник пуст или не открыт')
            case 4:
                if history_of_operations.count(1) > 0:
                    history_of_operations.append(4)
                    new_contact = take_data(
                        ['Введите имя контакта: ', 'Введите номер контакта: ', 'Введите комментарий контакта: '])
                    append_contact(new_contact)
                    show_message(contact_added(new_contact[0]))
                else:
                    show_message("Справочник ещё не был открыт!")
            case 5:
                if history_of_operations.count(1) > 0:
                    history_of_operations.append(5)
                    main_find_contact("Введите слово для поиска: ")
                else:
                    show_message("Справочник ещё не был открыт!")
            case 6:
                if history_of_operations.count(1) > 0:
                    history_of_operations.append(6)
                    if main_find_contact('Введите слово для поиска контакта, который хотите изменить: '):
                        c_id = int(take_data('Введите ID контакта, который хотите изменить: '))
                        changed_contact = take_data(['Введите новое имя контакта или ENTER, чтобы не изменять: ',
                                                    'Введите новый номер контакта или ENTER, чтобы не изменять: ',
                                                    'Введите новый комментарий контакта или ENTER, чтобы не изменять: '])
                        name = change_contact(c_id, changed_contact)
                        show_message(change_contact_success(name))
                else:
                    show_message("Справочник ещё не был открыт!")
            case 7:
                if history_of_operations.count(1) > 0:
                    history_of_operations.append(7)
                    if main_find_contact('Введите слово для поиска контакта, который хотите удалить: '):
                        c_id = int(take_data('Введите ID контакта, который хотите удалить: '))
                        name = delete_contact(c_id)
                        show_message(delete_contact_success(name))
                else:
                    show_message("Справочник ещё не был открыт!")
            case 8:
                print('Произошел выход!')
                break


main_function()
