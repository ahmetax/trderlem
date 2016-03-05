# -*- coding: utf-8 -*-
"""
Bu dosyada çeşitli fonksiyonlar bulunacak
"""
import requests
from bs4 import BeautifulSoup
import re

def get_base_url(url):
    url1=url
    #if url1[-1]=='/':
    #    url1 = url1[:-1]
    if url1.startswith("http://"):
        url2 = url1[7:]
        url2 = "http://"+url2.split('/')[0]
        return url2
    elif url1.startswith("https://"):
        url2 = url1[8:]
        url2 = "https://"+url2.split('/')[0]
        return url2
    else:
        return url1.split('/')[0]
    #base_url = re.findall("^(http:\/\/.*)\/",url1)[0]
    #return base_url

def linkleriAl(sayfa_url):
    linkler=[]
    base_url = get_base_url(sayfa_url)
    if base_url == "":
        return linkler
    soup = sayfaOku(sayfa_url)
    for link in soup.findAll('a'):
        if 'href' in link.attrs:
            adres = link.attrs['href']
            if (base_url in adres) and (adres not in linkler):
                linkler.append(adres)
    return linkler

def sayfaOku(sayfa_url):
    try:
        r = requests.get(sayfa_url)
    except Exception as e:
        print(e)
        print(sayfa_url)
        return ""
    soup = BeautifulSoup(r.content,"lxml")

    #print(soup.prettify())
    return soup

def turkcemi():
    True
