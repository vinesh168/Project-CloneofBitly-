from django.shortcuts import render
from django.db import connection
# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request):
    email = request.GET['email']
    psw = request.GET['pswname']
    cursor = connection.cursor()
    query = "insert into users (email, password) values (%s, %s)"
    values = (email,psw)
    cursor.execute(query,values)
    print(cursor.rowcount)
    # query = "Select * from city where name='"+email+"'"
    # cursor.execute(query)
    # row = cursor.fetchone()
    # print(row)
    data = {"email":email, "password": psw}
    return render(request, "first.html",data)