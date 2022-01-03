from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from . models import Article, Category
from . forms import ArticleForm
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializers import ArticleSerializer

def is_operator(user):
    return user.groups.filter(name = 'Operator').exists()

@login_required
def dashboard(request):
    request.session['is_operator'] = is_operator(request.user)
    context = {
        'title': 'Dashboard'
    }
    return render(request, 'back/dashboard.html', context)

@login_required
def blogs(request):
    request.session['is_operator'] = is_operator(request.user)
    articles = Article.objects.filter(user = request.user)
    context = {
        'title': 'Blogs',
        'articles': articles
    }
    return render(request, 'back/blogs.html', context)

@login_required
def add_article(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        forms_article = ArticleForm(request.POST)
        if forms_article.is_valid():
            forms_article_save = forms_article.save(commit = False)
            forms_article_save.user = request.user

            forms_article_save.save()
            return redirect('blogs')
    else:
        forms_article = ArticleForm()
    context = {
        'title': 'Add Blog',
        'categories': categories,
        'forms_article': forms_article
    }
    if request.method == "POST":
        title = request.POST.get('title')
        body = request.POST.get('body')
        category_name = request.POST.get('category')
        selectCategory = Category.objects.get(name = category_name)
        print(selectCategory)
        Article.objects.create(
            user = request.user,
            title = title,
            body = body,
            category = selectCategory
        )
        return redirect(blogs)

    return render(request, 'back/add_article.html', context)

def detail_article(request, id):
    article = Article.objects.get(id=id)
    context = {
        'title': 'Detail {}'.format(article.title),
        'article': article
    }
    return render(request, 'back/detail_article.html', context)

def edit_article(request, id):
    article = Article.objects.get(id=id)

    if request.method == 'POST':
        forms_article = ArticleForm(request.POST, instance = article)
        if forms_article.is_valid():
            forms_article_save = forms_article.save(commit = False)
            forms_article_save.user = request.user

            forms_article_save.save()
            return redirect('blogs')
    else:
        forms_article = ArticleForm(instance = article)

    context = {
        'title': 'Edit {}'.format(article.title),
        'title_form': article.title,
        'article': article,
        'forms_article': forms_article
    }
    return render(request, 'back/add_article.html', context)

def delete_article(request, id):
    Article.objects.get(id=id).delete()
    return redirect(blogs)

@user_passes_test(is_operator)
def users(request):
    users = User.objects.all()
    print('users: %s', users)
    context = {
        'title': 'Users',
        'users': users
    }
    return render(request, 'back/users.html', context)

def _check_authentication(request, x_api_key):
    try:
        key = request.user.api.api_key
    except:
        return {
            'status': False,
            'message': 'maaf api key anda belum login'
        }
    if key != x_api_key:
        return {
            'status': False,
            'message': 'maaf api key anda salah'
        }
    
    return True

@api_view(['GET'])
def get_articles(request, x_api_key):
    authentication = _check_authentication(request, x_api_key)
    if (authentication != True):
        return Response(authentication)

    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many = True)
    content = {
        'status': True,
        'count': articles.count(),
        'data': serializer.data
    }
    return Response(content)

@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_api(request, pk, x_api_key):
    authentication = _check_authentication(request, x_api_key)
    if (authentication != True):
        return Response(authentication)
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response({
                'status': False,
                'message': 'Maaf data tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Berhasil memperbarui article',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response({
            'status': True,
            'message': ('Berhasil menghapus %s' %(article.title)),
        })

@api_view(['POST'])
def add_article_api(request, x_api_key):
    authentication = _check_authentication(request, x_api_key)
    if (authentication != True):
        return Response(authentication)

    if request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': 'Berhasil membuat article',
                'data': serializer.data
            })
            
        return Response({
            'status': False,
            'message': 'maaf request anda salah'
        })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'status': False,
            'message': 'maaf harus menggunakan method post saja'
        })
