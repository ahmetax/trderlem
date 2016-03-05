# -*- coding: utf-8 -*-
"""
Bu dosyada çeşitli fonksiyonlar bulunacak
"""
import requests
from bs4 import BeautifulSoup

def linkleriAl(sayfa_url):
    linkler=[]
    soup = sayfaOku(sayfa_url)
    for link in soup.findAll('a'):
        if 'href' in link.attrs:
            if link.attrs['href'] not in linkler:
                linkler.append(link.attrs['href'])
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
