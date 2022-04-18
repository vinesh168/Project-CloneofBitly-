import string

from django.shortcuts import render, redirect
from django.db import connection
from django.core.mail import send_mail
from django.conf import settings

import random


# Create your views here.
def index(request):
    return render(request, "home.html")


def signup(request):
    email = request.POST['email']
    psw = request.POST['pswname']

    cursor = connection.cursor()
    query1 = "select * from user where email= '" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchall()

    if len(data) > 0:

        return render(request, "first.html")

    else:
        otp = random.randint(1000, 9999)
        strotp = str(otp)
        query2 = "insert into user (email, password, otp) values (%s, %s, %s)"
        values2 = (email, psw, strotp)
        cursor.execute(query2, values2)
        # print(cursor.rowcount)

        subject = 'otp for verification'
        message = f'Hi {email}, thank you for registering your otp is {otp}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

        data = {"email": email}
        return render(request, "verificationpage.html", data)


def signin(request):
    return render(request, "login.html")


def login(request):
    email = request.POST['email']
    psw = request.POST['psw']
    cursor = connection.cursor()
    query1 = "select * from user where email= '" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data == None:
        return render(request, "index.html")

    else:
        if data[1] == psw:
            data = {"email": "Login successfully"}
            return render(request, "message.html", data)
        else:
            data = {"email": "password is not correct"}
            return render(request, "message.html", data)


def otp_verification(request):
    email = request.POST['email']
    otp = request.POST['otp']

    cursor = connection.cursor()
    query1 = "select * from user where email= '" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()

    if data[3] == otp:
        query2 = "update user set is_verify=1 where email= '" + email + "'"
        cursor.execute(query2)
        if cursor.rowcount == 1:
            data = {"email": email, "password": "your otp verified successfully"}
            return render(request, "message.html", data)


def generateSHORTURL():
    letter = string.ascii_letters + string.digits
    shortUrl = ''
    for i in range(6):
        shortUrl = shortUrl + ''.join(random.choice(letter))
    return shortUrl



def urlshortner(request):
    longlink = request.GET['link']
    customUrl = request.GET['customurl']

    if customUrl is None or customUrl=='':
        shortUrl = generateSHORTURL()
        customUrl = shortUrl
        cursor = connection.cursor()
        query1 = "select * from links where short_link = '" + customUrl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        while data is not None:
            shortUrl = generateSHORTURL()
            data = cursor.fetchone()

        customUrl = shortUrl

        query2 = "insert into links (long_link, short_link) values (%s, %s)"
        value = (longlink, customUrl)
        cursor.execute(query2, value)
        data = {"email": "your url is shorten with nano.co/" + customUrl}
        return render(request, "message.html", data)

    else:
        cursor = connection.cursor()
        query1 = "select * from links where short_link = '" + customUrl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        if data is not None:
            data = {"email" : "already custom urls exist please try some other url"}
            return render(request, "message.html", data)
        else:
            query2 = "insert into links (long_link, short_link) values (%s, %s)"
            value = (longlink, customUrl)
            cursor.execute(query2, value)
            data = {"email": "your url is shorten with nano.co/"+customUrl}
            return render(request, "message.html", data)

def handlingShortUrl(request, **kwargs):
    shortUrl = kwargs['url']

    cursor = connection.cursor()
    query1 = "select long_link from links where short_link = '" + shortUrl + "'"
    cursor.execute(query1)
    data = cursor.fetchone()

    if data is None:
        data={'email': 'error is coming '}
        return render(request, "message.html", data)
    else:
        return redirect(data[0])

