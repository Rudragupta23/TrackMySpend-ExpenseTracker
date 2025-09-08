import os
import random
import pymysql
import tkinter as tk
from smtplib import SMTP
from datetime import datetime, timedelta
from dotenv import load_dotenv
from twilio.rest import Client
from tkinter import ttk, messagebox
from email.mime.text import MIMEText
from PIL import Image, ImageTk, ImageDraw
from email.mime.multipart import MIMEMultipart

load_dotenv()
timeout = 10
db = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db="money",
    host=os.environ.get('DB_HOST'),
    password=os.environ.get('DB_PASSWORD_DEFAULT'),
    read_timeout=timeout,
    port=12727,
    user=os.environ.get('DB_USER_DEFAULT'),
    write_timeout=timeout,
)
def switch_user(username, password):
    global db
    try:
        db = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="money",
            host=os.environ.get('DB_HOST'),
            password=password,
            read_timeout=timeout,
            port=12727,
            user=username,
            write_timeout=timeout,
        )
        print("Connection successfully...for user", db.user.decode("utf-8"))
        return 0

    except pymysql.Error as e:
        print("invalid credentials.")
        return 1
def database():
    return db
