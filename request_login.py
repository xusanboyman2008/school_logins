import requests
from models import create_login, get_login

url = "https://login.emaktab.uz"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

async def login():
    wrong_logins = []
    correct_logins = []
    l = 1
    for login in await get_login():
        if login:
            r = requests.post(url, headers=headers, data={"login": login.login, "password": login.password})
            if len(r.cookies) == 1:
                wrong_logins.append(f"Login: {login.login} 🔑 Password: {login.password}\n")
            else:
                await create_login(login=login.login, password=login.password)
                correct_logins.append(f"Login: {login.login} 🔑 Password: {login.password}\n")
                l += 1
    return wrong_logins, l

async def login_main(data, tg_id):
    data = data
    wrong_logins = []
    correct_logins = []
    l = 1
    for login in data:
        r = requests.post(url, headers=headers, data={"login": login.split(":")[0], "password": login.split(":")[1]})
        if len(r.cookies) == 1:
            wrong_logins.append(f"Login: {login.split(':')[0]} 🔑 Password: {login.split(':')[1]}")
        else:
            await create_login(login=login.split(":")[0], password=login.split(":")[1])
            correct_logins.append(f"Login: {login.split(':')[0]} 🔑 Password: {login.split(':')[1]}")
            l += 1
    return wrong_logins, l - 1
