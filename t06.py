from collections import UserDict
import re

# базовый класс полей
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# зберігання імені контакту
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")  # !!!!!!!!!! перевірка на порожнє значення
        super().__init__(value)

# зберігання телефону 
class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number format. Must be 10 digits.")  # перевірка формату
        super().__init__(value)

    @staticmethod
    def validate(value):
        return bool(re.fullmatch(r"\d{10}", value))  # перевірка що номер має рівно 10 цифр

# сохр імя + тел
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []  
    def add_phone(self, phone):
        self.phones.append(Phone(phone)) 

    def remove_phone(self, phone):
        # видалення телефону із списку
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        # редагування
        for index, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
        raise ValueError(f"Phone '{old_phone}' not found in contact.")  # якщо телефон не знайдено

    def find_phone(self, phone):
        # пошук телефону у списку
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def __str__(self):
        # повертаємо форматований рядок для контакту
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# клас адресної книги, успадкований від UserDict
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record  # додаємо запис до книги

    def find(self, name):
        return self.data.get(name)  # знаходимо запис за іменем

    def delete(self, name):
        if name in self.data:
            del self.data[name]  # видаляємо запис
        else:
            raise KeyError(f"Contact '{name}' not found.")  # запис не знайдено

if __name__ == "__main__":
    # створення нової адресної книги
    book = AddressBook()

    # створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # додавання запису John до адресної книги
    book.add_record(john_record)

    # створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Contact name: John, phones: 1112223333; 5555555555

    # пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # 5555555555

    # видалення запису Jane
    book.delete("Jane")
