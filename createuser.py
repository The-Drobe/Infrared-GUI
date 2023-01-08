from werkzeug.security import generate_password_hash
import json
Username = input("Please input user name: ")
Password =  input("Please input Password: ")

try:
    with open("users.json") as file:
        data = json.load(file)
except FileNotFoundError:
    print("no users.json file creating a new one")
    data = {}
data[Username] = generate_password_hash(Password)

print(data)

with open("users.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

print("user successfully created!")