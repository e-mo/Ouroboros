# session_pass.py
import requests
import logging

def construct_payload(uname, pwd):
    return {
        'submit': 'true',
        'uname': uname,
        'pwd': pwd
    }

def session_pass(uname, pwd):
    url = 'https://login.eternalcitygame.com/login.php'
    payload = construct_payload(uname, pwd)
    session = requests.Session()

    session.get(url)
    session.post(url, data=payload, cookies=session.cookies)

    return session.cookies.get('pass')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('usage: session_pwd.py UNAME PWD')
        exit()

    uname = sys.argv[1]
    pwd = sys.argv[2]
    spass = session_pass(uname, pwd)

    if spass == None:
        print('Unable to fetch session password')
        print('Check login credentials')
        exit()

    print("UNAME: %s\nPWD: %s\nSPASS: %s" % (uname, pwd, spass))
