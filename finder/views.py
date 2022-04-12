from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import Domain, Subdomain

import requests

# Create your views here.
@login_required(login_url = "/admin")
def index(request):
    domains = Domain.objects.filter(user = request.user)

    i = 0

    context = {
                "domains" : domains,
                "i" : i
            }

    return render(request, "index.html", context)

def addRow(request, name):
    newDomain = name
    domain = Domain()
    domain.user = request.user
    domain.name = newDomain
    domain.save()
    
    def domain_scanner(domain_name,sub_domnames):
        #print('----URL after scanning subdomains----')
        i = 0

        for subdomain in sub_domnames:
            i = i + 1
            url = f"https://{subdomain}.{domain_name}"

            try:
                requests.get(url)
                newSubdomain = url
                subdomain2 = Subdomain()
                subdomain2.name = newSubdomain
                subdomain2.domain = domain
                subdomain2.save()
                #print(str(i) + str(url))
            except requests.ConnectionError:
                pass

    dom_name = name
    with open('subdomains.txt','r') as file:
        subdoms = file.read()
        sub_dom = subdoms.splitlines()

    domain_scanner(dom_name,sub_dom)

    

    return redirect("index")

def deleteRow(request, list):

    idList = list.split(",")
    for id in idList:
        domain = Domain.objects.filter(id = id)
        domain.delete()

    return redirect("index")