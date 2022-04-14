from django import views
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import Domain, Subdomain

import whois
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
    permission_classes = [AllowAny]

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
            content["domainCreationDate"] = query.creation_date
            content["domainExpirationDate"] = query.expiration_date
            content["domainNameServers"] = query.name_servers
            content["domainRegistrantName"] = query.registrant_name
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
    try:
        w = whois.whois(name)
        domain.creation_date = str(w["creation_date"])
        domain.expiration_date = str(w["expiration_date"])
        domain.name_servers = str(w["name_servers"])
        if w.registrant_name:
            domain.registrant_name = w["registrant_name"]
        else:
            domain.registrant_name = ""
    except:
        pass
    domain.save()
    
    def domain_scanner(domain_name,sub_domnames):
        for subdomain in sub_domnames:
            url = f"https://{subdomain}.{domain_name}"

            try:
                requests.get(url)
                newSubdomain = url
                subdomain2 = Subdomain()
                subdomain2.name = newSubdomain
                subdomain2.domain = domain
                subdomain2.save()
                print(url)
            except:
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