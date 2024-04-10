from dotenv import load_dotenv
import os
from itsdangerous import URLSafeSerializer
from flask import make_response, redirect, url_for, request
from project.object.users import getUser

load_dotenv(dotenv_path=".env")
KEY = os.getenv("KEY")
serializer = URLSafeSerializer(KEY)


def readCookie():
    encrypted_data = request.cookies.get("user_info")

    if encrypted_data:
        try:
            data = serializer.loads(encrypted_data, max_age=3600)
            return data
        except Exception:
            pass

    return None


def createCookie(username):
    data = {"username": username}
    encrypted_data = serializer.dumps(data)
    response = make_response(redirect(url_for('main.get')))
    response.set_cookie("user_info", encrypted_data, httponly=True, samesite="Strict", secure=False)

    return response


def deleteCookie():
    response = make_response(redirect(url_for("main.get")))
    response.set_cookie("user_info", expires=0)

    return response


def get_current_user():
    cookie = readCookie()
    if cookie:
        username = cookie["username"]
        if username and getUser(username):
            return getUser(username)
        else:
            return None
    return None
