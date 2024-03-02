import pickle
from classes import AddressBook
from classes import Record
from classes import Field
from classes import Birthday
from classes import Name
import datetime as dt                                                                        
from datetime import datetime as dtdt
from collections import UserDict


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено.
    
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return str(e)

    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    contacts[name] = record
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, new_phone = args
    if name in contacts:
        contacts[name] = new_phone
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return f"The phone number for {name} is {contacts[name]}."
    else:
        return f"Contact {name} not found."

@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts found."
    else:
        all_contacts = "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
        return f"All contacts:\n{all_contacts}"
    
@input_error
def add_birthday(args, contacts):
    name, birthday = args
    if name in contacts:
        contacts[name].add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, contacts):
    name = args[0]
    if name in contacts and contacts[name].birthday:
        return f"The birthday for {name} is {contacts[name].birthday.value.strftime('%d.%m.%Y')}."
    else:
        return f"Birthday not found for {name}."
    
@input_error
def birthdays(contacts):
    upcoming_birthdays = AddressBook.get_upcoming_birthdays(contacts.values())
    if upcoming_birthdays:
        return "Upcoming birthdays:\n" + "\n".join(f"{contact['name']}: {contact['birthday']}" for contact in upcoming_birthdays)
    else:
        return "No upcoming birthdays."

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)  # Зберегти дані перед виходом з програми
            break
        elif command == "hello":
            print("How can I assist you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()