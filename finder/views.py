from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import Article

# Create your views here.
@login_required(login_url = "/admin")
def index(request):
    articles = Article.objects.filter(user = request.user)

    i = 0

    context = {
                "articles" : articles,
                "i" : i
            }

    return render(request, "index.html", context)

def addRow(request, title):

    newTitle = title
    article = Article()
    article.user = request.user
    article.title = newTitle
    article.save()

    return redirect("index")

def deleteRow(request, list):

    idList = list.split(",")
    for id in idList:
        article = Article.objects.filter(id = id)
        article.delete()

    return redirect("index")