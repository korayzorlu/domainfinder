from django import views
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import Domain, Subdomain

import requests
import json
from requests.auth import HTTPBasicAuth

import os

from .serializers import DomainSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend

class DomainViewSet(viewsets.ReadOnlyModelViewSet, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]
    
    def get_queryset(self):
        queryset = Domain.objects.all()
        serializer_class = DomainSerializer

        content_list = []
        
        for query in queryset:
            content = {}
            content["domainName"] = query.name
            subdomainset = Subdomain.objects.filter(domain = query)
            subdomain_list = []
            if subdomainset:
                for subdomain in subdomainset:
                    subdomain_list.append(subdomain.name)
                content["subdomains"] = subdomain_list
            else:
                content["subdomains"] = []
            content_list.append(content)

        return queryset
    

# Create your views here.
@login_required(login_url = "/admin")
def index(request):
    domains = Domain.objects.filter(user = request.user)
    
    dd = requests.get("http://" + request.get_host() + "/restapi/domains/?name=google.com",auth=HTTPBasicAuth('admin', 'administration')).json()
    print(dd)
    i = 0

    context = {
                "domains" : domains,
                "i" : i
            }

    return render(request, "index.html", context)

@login_required(login_url = "/admin")
def subdomainIndex(request, id):
    domains = Domain.objects.filter(user = request.user)
    domain = get_object_or_404(Domain, id = id)

    subdomains = Subdomain.objects.filter(domain = domain)

    i = 0

    context = {
                "domains" : domains,
                "i" : i
            }

    return render(request, "index.html", context)

def addRow(request, name):
    os.system("ls")
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