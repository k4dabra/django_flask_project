from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.

def main(req):
    return render(req, "index.html")

def read_page(req):
    return render(req, "readPage.html")

def add_page(req):
    return render(req, "addPage.html")

def read(req):
    name = req.GET.get("name")
    login = req.GET.get("login")

    if name:
        url = f"http://127.0.0.1:5000/read?name={name}"
        search_key = name
    elif login:
        url = f"http://127.0.0.1:5000/read?login={login}"
        search_key = login

    res = requests.get(url).json()

    return render(req,"readResult.html",{"res":res,"search_key":search_key})

def add(req):
    url = f"http://127.0.0.1:5000/add/"

    package = {
        "name": req.POST.get("name"),
        "login": req.POST.get("login"),
        "password": req.POST.get("password")
    }

    res = requests.post(url,json=package)

    if res.status_code == 200:
        return render(req,"addResult.html",{"name":req.POST.get("name")})

    return HttpResponse("add")
