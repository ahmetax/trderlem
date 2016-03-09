# -*- coding: utf-8 -*-
#gamet.py
#2016-03-07
#author = Ahmet Aksoy
#Son güncelleme = 2016-03-08
#Python 3.5.1 ile test edildi
from selenium import webdriver
from urllib.parse import urlparse
import turlib
import turkcemi
import re
import time, datetime

adresler = [
    "http://webmaster.gamet.com.tr/arsiv/"
]


sayfasay =0
baslama = int(time.time())

outfilename = "temp/"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+"-metin.txt"
outfile = open(outfilename,"a",encoding="utf-8")

def get_base_url(url):
    o =urlparse(url)
    base_url=''
    if o.scheme > '':
        base_url += o.scheme+"://"
    base_url += o.netloc
    return base_url

#Varsayılan driver olarak Firefox kullanılacak
def get_driver():
    try:
        driver = webdriver.Firefox()
    except:
        driver = None
    return driver

def load_arsiv_page(driver,adres):
    global sayfasay
    if adres[-1]=='/': adres = adres[:-1]
    base_url = get_base_url(adres)
    driver.get(adres)
    elements = driver.find_elements_by_xpath("//li/a[@href]")
    for a in elements:
        b = a.get_attribute('href')
        if b[-1]=='/': b = b[:-1]
        if b == base_url: continue
        if not b.startswith(base_url): continue
        if b == adres: continue
        sayfasay += 1
        print("{} {} {:05d} {}".format(turlib.damga(), turlib.gecen_sure(baslama), sayfasay, b))
        #link başka bir siteye ait olmasın
        if base_url in b:
            sayfa = turlib.sayfaOku(b)
            if sayfa == None: continue
            #sayfadan tüm linkleri kaldır
            for tag in sayfa.findAll('a', href=True):
                tag.extract()

            paragraflar = sayfa.find_all('div',attrs={'class' : 'entry-content'})
            for p in paragraflar:
                #script bölümlerini temizle
                [s.extract() for s in p('script')]
                #div - class=sharedaddy bölümünü temizle
                for div in p.findAll('div', attrs={'class':'sharedaddy'}):
                    div.extract()
                #http:// ile başlayan ardışık karakterleri sil
                re.sub('(http.*)\s','',p.text)
                print(p.text)
                print(p.text,file=outfile,flush=True)
                if turkcemi.turkcemi(p.text,fout=outfile) == True:
                    print("Bu metin Türkçedir")
                else:
                    print("Bu metin Türkçe değildir veya yeterli sayıda geçerli Türkçe sözcük barındırmamaktadır.")

def main():
    driver = get_driver()
    if driver != None:
        for adres in adresler:
            load_arsiv_page(driver,adres)
            break
    outfile.close()

if __name__ == "__main__":
    main()
