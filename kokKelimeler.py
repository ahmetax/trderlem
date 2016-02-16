# -*- coding: utf-8 -*-
#kokKelimeler.py
#2016-02-14
#author = Ahmet Aksoy
#Son güncelleme = 2016-02-15
#Python 3.5.1 ve 3.4 ile test edildi
"""
Bu modülde Kelime sınıfını oluşturacağız
Parametre olarak verilen kelimeden
kökü
ekler (tek parça)
ekler2 (parçalar - ile ayrılmış)
tip (özel isim, isim, sıfat, zarf, vb)
...
döndürülecek

Tarama işlemleri kelimenin başından başlayacak
"""
import time
from trkmodul import kucukharf, buyukharf

dertop = []
with open("./veri/dertop.txt",encoding="utf-8") as fin:
    say=0
    for soz in fin:
        say+=1
        if say>1500000: break
        if soz>='a' and soz < 'zzzzzzzzzzzzzzzzzzzzzz':
            dertop.append(soz.strip())
print("dertop boyu = "+str(len(dertop)))

lstKokler = []
with open("./veri/kok-kokler.txt",encoding="utf-8") as fin:
    for soz in fin:
        lstKokler.append(soz.strip())
print("kokler boyu = "+str(len(lstKokler)))

lstEkler = []
with open("./veri/kok-ekler.txt",encoding="utf-8") as fin:
    for soz in fin:
        lstEkler.append(soz.strip())


class KoklerTR:
    pass

class EklerTR:
    pass

class Kelime:
    def __init__(self, kelimeler):
        self.kokler = KoklerTR()
        self.ekler = EklerTR()
        self.kelimeler = kelimeler

    def kok(self):
        pass

    def ekler(self):
        pass

    def ekler2(self):
        pass

    def tip(self):
        pass

    def oneri(self):
        pass

"""
Türkçe karakterler olmaksızın girilen bir stringi düzgün hale getirmek
c : ç
g : ğ
i : ı
s : ş
o : ö
u : ü
"""

def deasciify(soz):
    liste = []
    ysoz=''
    for i in range(len(soz)):
        if soz[i]=='c':
            ysoz += 'C'
        elif soz[i]=='g':
            ysoz += 'G'
        elif soz[i]=='i':
            ysoz += 'I'
        elif soz[i]=='o':
            ysoz += 'O'
        elif soz[i]=='s':
            ysoz += 'S'
        elif soz[i]=='u':
            ysoz += 'U'
        else:
            ysoz += soz[i]
    liste =[]
    liste.append(ysoz)
    i = 0
    while i < len(ysoz):
        for j in range(len(liste)):
            ysoz= liste[j]
            if ysoz[i] in "CGIOSU":
                if ysoz[i]=='C':
                    ys1=ysoz[:i]+'c'+ysoz[i+1:]
                    ys2=ysoz[:i]+'ç'+ysoz[i+1:]
                    del liste[j]
                    liste.append(ys1)
                    liste.append(ys2)
                    i-=1
                    break
                elif ysoz[i]=='G':
                    ys1=ysoz[:i]+'g'+ysoz[i+1:]
                    ys2=ysoz[:i]+'ğ'+ysoz[i+1:]
                    del liste[j]
                    liste.append(ys1)
                    liste.append(ys2)
                    i-=1
                    break
                elif ysoz[i]=='I':
                    ys1=ysoz[:i]+'i'+ysoz[i+1:]
                    ys2=ysoz[:i]+'ı'+ysoz[i+1:]
                    del liste[j]
                    liste.append(ys1)
                    liste.append(ys2)
                    i-=1
                    break
                elif ysoz[i]=='O':
                    ys1=ysoz[:i]+'o'+ysoz[i+1:]
                    ys2=ysoz[:i]+'ö'+ysoz[i+1:]
                    del liste[j]
                    liste.append(ys1)
                    liste.append(ys2)
                    i-=1
                    break
                elif ysoz[i]=='S':
                    ys1=ysoz[:i]+'s'+ysoz[i+1:]
                    ys2=ysoz[:i]+'ş'+ysoz[i+1:]
                    del liste[j]
                    liste.append(ys1)
                    liste.append(ys2)
                    i-=1
                    break
                elif ysoz[i]=='U':
                    ys1=ysoz[:i]+'u'+ysoz[i+1:]
                    ys2=ysoz[:i]+'ü'+ysoz[i+1:]
                    del liste[j]
                    liste.append(ys1)
                    liste.append(ys2)
                    i-=1
                    break
                else:
                    pass
        i += 1

    #kelime listesinde (dertop) olanları ayır
    liste2 = []
    for l in liste:
        if l in dertop:
            liste2.append(l)
    return liste2, liste

def duzelt(cumleler):
    ycumleler=''
    sozler = str(cumleler).split()
    for soz in sozler:
        if soz in dertop:
            ycumleler += ' '+soz
            continue
        #aday sözcükleri üret
        s,sx = deasciify(soz)
        if len(s)<1:
            ycumleler += ' '+soz
        elif len(s)>1:
            ss=" ("
            for i in range(len(s)):
                ss+=s[i]
                if i <len(s)-1:
                    ss += "/"
            ycumleler += ' '+ss+')'
        else:
            ycumleler += ' '+s[0]
    return ycumleler

#dertop listesindeki tüm elemanların "in" kontrolü
def dertop_kontrol():
    say=0
    with open("dertop-kontrol.txt","w") as fout:
        for i in range(len(dertop)):
            if dertop[i] not in dertop:
                print(dertop[i])
                print(dertop[i], file=fout)
            say += 1
            if say % 1000 == 0:
                print(say,end=" ")
            if say % 10000 == 0:
                print("")
                fout.flush()

#Türkçe karakterler için upper() ve lower() metodlarının kontrolü
def up_lo_kontrol():
    up = "ÇĞIİÖŞÜ"
    lo = "çğıiöşü"
    if up.lower() != lo:
        print("up.lower() != lo")
        print("{}.lower() != {}".format(up,up.lower()))

    if lo.upper() != up:
        print("lo.upper() != up")
        print("{}.upper() != {}".format(lo,lo.upper()))

def up_lo_kontrol2():
    up = "ÇĞIİÖŞÜ"
    lo = "çğıiöşü"

    if kucukharf(up) != lo:
        print("kucukharf(up) != lo")
        print("kucukharf({}) != {}".format(up,kucukharf(up)))
    else:
        print("kucukharf({}) = {}".format(up,kucukharf(up)))


    if buyukharf(lo) != up:
        s=buyukharf(lo)
        print("buyukharf(lo) != up")
        print("buyukharf({}) != {}".format(lo,s))
        for i in range(len(s)):
            print("({} - {}) ".format(s[i],hex(ord(s[i]))) )


    else:
        print("buyukharf({}) = {}".format(lo,buyukharf(lo)))


if __name__ == "__main__":
    up_lo_kontrol()
    print()
    up_lo_kontrol2()
    #exit()
    s = kucukharf("yokmus")
    l1, l2 = deasciify(s)
    print(l1)
    print(l2)
    s = kucukharf("cepecevre")
    l1, l2 = deasciify(s)
    print(l1)
    print(l2)
    s = kucukharf("kose")
    l1, l2 = deasciify(s)
    print(l1)
    print(l2)
    s = kucukharf("sisesi")
    l1, l2 = deasciify(s)
    print(l1)
    print(l2)

    s = kucukharf('Bir varmis bir yokmus bu köse yaz kösesi bu köse kis kösesi ortasinda su sisesi')
    print()
    print(duzelt(s))


    """
    say = 0
    fout =open("veri/ekler.txt","w",encoding="utf-8")
    fcok =open("veri/coklar.txt","w",encoding="utf-8")
    fyok =open("veri/yoklar.txt","w",encoding="utf-8")
    ftek =open("veri/tekler.txt","w",encoding="utf-8")
    t0 = time.perf_counter()
    for soz in dertop:
        adaylar = []        #kök adayları buraya depolanacak
        s=soz
        if s in lstKokler:
            adaylar.append(s)
            print(soz,file=ftek)
            continue
        else:
            nx = len(soz)
            n = 1
            while n < nx:
                s = soz[:n]
                if s in lstKokler:
                    sek = soz[len(s):]
                    if sek in lstEkler:
                        adaylar.append(s)       # parçalar her iki listede bulundu
                n += 1
                if n>=nx:
                    break

        if len(adaylar)==0:
            print(soz,file=fyok)    # hiç aday yok. Ya hatalı, ya da kök listesine eklenmeli
        else:
            for aday in adaylar:
                sonuc = aday+"-"+soz[len(aday):]
                if len(adaylar)==1:
                    print(sonuc,file=fout)  # tek aday var
                else:
                    print(sonuc,end=" ",file=fcok)  # çok aday var
            if len(adaylar)>1:
                print("",file=fcok)

        say +=1
        if say%100==0:
            fout.flush()
            ftek.flush()
            fyok.flush()
            fcok.flush()
            print(say, end=" ")
            print()

    fout.close()
    ftek.close()
    fyok.close()
    print('Toplam süre = {} saniye'.format(time.perf_counter()-t0))
    """