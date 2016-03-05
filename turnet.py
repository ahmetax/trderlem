# -*- coding: utf-8 -*-
#author: Ahmet Aksoy
#Başlangıç: 2016.03.04
#Son güncelleme: 2016.03.04
#Python3.5.1 ile test edildi

import turlib

#ziyaret_edilenler listesinde daha önce işlem yapılmış sayfa adresleri tutulacak
ziyaret_edilenler = []
#Bulunan ve henüz ziyaret edilmemiş adresler bu listede tutulacak
yeni_linkler = []

def ziyaret_edilenleri_oku():
    global ziyaret_edilenler
    with open("linkler/ziyaret_edilenler.txt",encoding="utf-8") as zl:
        for l in zl:
            ziyaret_edilenler.append(l)

def yeni_linkleri_oku():
    global yeni_linkler
    with open("linkler/yeni_linkler.txt",encoding="utf-8") as yl:
        for l in yl:
            yeni_linkler.append(l)

def main():
    #Daha önce ziyaret edilen adreslerin listesini belleğe al
    ziyaret_edilenleri_oku()
    #Daha önce tespit edilen ama henüz ziyaret edilmemiş adresleri belleğe al
    yeni_linkleri_oku()

    #yeni linkler tamamlanıncaya kadar işlemlere devam et
    while len(yeni_linkler)>0:
        url = yeni_linkler[0].strip()
        print(url)
        #Bu adresteki linkleri al
        linkler = turlib.linkleriAl(url)
        for link in linkler:
            if link not in yeni_linkler:
                yeni_linkler.append(link)

        #Bu adresteki sayfayı oku, sadece text haline dönüştür
        #Belli bir boyutun üzerindeyse Türkçe kontrolü yap
        #Uygun boyutta ve Türkçeyse ayrıştırma işlemlerini uygula
        #sayfa = turlib.sayfaOku(url)
        #print(sayfa)

        #En baştaki adresi ziyaret edilenler listesine ekle ve yeni_linkler listesinden sil
        ziyaret_edilenler.append(url)
        yeni_linkler.pop(0)

if __name__ == "__main__":
    main()
