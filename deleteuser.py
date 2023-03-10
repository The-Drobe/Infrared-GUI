from werkzeug.security import generate_password_hash
import json

try:
    with open("users.json") as file:
        data = json.load(file)
except FileNotFoundError:
    print("no users.json file exists consider creating a new user via running 'docker exec -i containername python3 createuser.py'")
    exit()
except json.JSONDecodeError:
    print("Invalid users.json file detected consider creating a new user via running 'docker exec -i containername python3 createuser.py")
    exit()

for i in data.keys():
    print(i)

selection = input('please input the user above you wish to remove: ')
try:
    data.pop(selection)
except KeyError:
    print("that user does not exist. Exiting")
    exit()

print(data)

with open("users.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

print("user successfully deleted!")