from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from blog.models import Article
from users.models import Biodata

def index(request):
    articles = Article.objects.all()
    context = {
        'title': 'Home',
        'articles': articles
    }
    return render(request, 'front/index.html', context)

def detail_article(request, id):
    article = Article.objects.get(id = id)
    context = {
        'title': 'Detail Article',
        'article': article
    }
    return render(request, 'front/detail_article.html', context)

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'front/about.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print("is login success")
            return redirect('index')
        else:
            print("is not login success")
            pass
    context = {
        'title': 'Login'
    }
    return render(request, 'account/login.html', context)

def logout_view(request):
    print('request logout')
    logout(request)
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        print(username, password, first_name, last_name, email, address, phone)
        user = User.objects.create_user(
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        Biodata.objects.create(
            user = user,
            address = address,
            phone = phone
        )
        return redirect('login')

    context = {
        'title': 'Register'
    }
    return render(request, 'account/register.html', context)