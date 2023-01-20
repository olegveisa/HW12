from collections import UserDict
from datetime import datetime
import pickle

class Field():
    pass

class Name(Field):
    def __init__(self, name: str):
        self.__private_name = None
        self.name = name

    def __repr__(self):
        return f'{self.name}'

    @property
    def name(self):
        return self.__private_name
    
    @name.setter
    def name(self, value: str):
        if value.isalpha:
            self.__private_name = value
        else:
            raise ValueError('Wrong name')

class Phone(Field):
    
    def __init__(self, phone = None):
        self.__private_value = None
        self.value = phone

    def __repr__(self):
        return f'{self.value}'

    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, value: str):
        if value:
            if value.isdigit() == True:
                self.__private_value = value
            else:
                raise ValueError('Wrong number')

class Birthday(Field):

    def __init__(self, birthday = None):
        self.__private_birthday = None
        self.birthday = birthday
    
    def __repr__(self):
        return f'{self.birthday}'

    @property
    def birthday(self):
        return self.__private_birthday
  
    @birthday.setter
    def birthday(self, birthday: str):
        try:
            if birthday is not None:
                self.__private_birthday = datetime.strptime(birthday, '%d/%m/%Y').date()
        except ValueError:
            print (f'Enter the date in format dd/mm/yyyy')

class Record():
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
    
    def __repr__(self):
        return f'Name: {self.name}, phone: {self.phones}, birthday: {self.birthday}'

    def add_phone(self, value: Phone):
        self.phones.append(value)
    
    def change_phone(self, old_phone: Phone, new_phone: Phone):
        self.phones.remove(old_phone)
        self.phones.append(new_phone)

    def delete_phone(self, phone: Phone):
        self.phones.remove(phone)

    def days_to_birthday(self, birthday: Birthday):
        self.birthday = birthday

        if self.birthday.birthday is not None:
            current_date = datetime.now().date()
            current_year = current_date.year
            user_date = self.birthday.birthday.replace(year = current_year)
            delta_days = user_date - current_date
            try:
                if 0 < delta_days.days:
                    return f'{delta_days.days} days left until birthday'
                else:
                    user_date = self.birthday.birthday.replace(year = user_date.year + 1)
                    delta_days = user_date - current_date
                    if 0 < delta_days.days:
                        return f'{delta_days.days} days left until birthday'
            except ValueError:
                print('Enter valid date')

class AddressBook(UserDict):

    def iterator(self):
        for record in self.data.values():
            yield record.__repr__()

    def print_page(self, len):
        for _ in range(len):
            try:
                print(next(ab_iterator))
            except StopIteration:
                print('='*60)

    def add_record(self, record: Record):
        self.data[record.name.name] = record
    
    def serialization(self):
        with open('addressbook.bin', 'wb') as file:
            pickle.dump(ab, file)
            print('Serialization - OK')

    def deserialization(self):
        with open('addressbook.bin', 'rb') as file:
            ab = pickle.load(file)
            print(ab, '\nDeserealization - OK')
    
    def search(self, user_search):
        for record in ab.data.values():
            res = str(record).lower().find(user_search)
            if res is not -1:
                print(record)


if __name__ == '__main__':

    ab = AddressBook()
    name = Name('Bill')
    phone = Phone('1234567890')
    birthday = Birthday('04/07/1996')
    rec = Record(name, phone, birthday)
    ab.add_record(rec)

    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
    print(ab['Bill'].days_to_birthday(birthday))
    print('All Ok)')

    name = Name('Oleg')
    phone = Phone('0931685506')
    birthday = Birthday('14/03/1998')
    rec = Record(name, phone, birthday)
    ab.add_record(rec)

    name = Name('Helg')
    phone = Phone('066998899')
    birthday = Birthday()
    rec = Record(name, phone, birthday)
    ab.add_record(rec)

    name = Name('Helga')
    phone = Phone('0934123225')
    birthday = Birthday('06/06/1977')
    rec = Record(name, phone, birthday)
    ab.add_record(rec)

    name = Name('Polina')
    phone = Phone()
    birthday = Birthday('29/07/1998')
    rec = Record(name, phone, birthday)
    ab.add_record(rec)

    ab_iterator = ab.iterator()
    AddressBook.print_page(AddressBook, 6)
    AddressBook.serialization(AddressBook)
    AddressBook.deserialization(AddressBook)

    name = Name('Jim')
    phone = Phone('31233123')
    birthday = Birthday('20/11/1998')
    rec = Record(name, phone, birthday)
    ab.add_record(rec)

    ab_iterator = ab.iterator()
    AddressBook.print_page(AddressBook, 6)
    AddressBook.serialization(AddressBook)
    AddressBook.deserialization(AddressBook)

    user_search = 'Oleg'
    AddressBook.search(AddressBook, user_search.lower())

    user_search = 'polina'
    AddressBook.search(AddressBook, user_search.lower())
    