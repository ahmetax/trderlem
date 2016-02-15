# -*- coding: utf-8 -*-
#kokKelimeler.py
#2016-02-14
#author = Ahmet Aksoy
#Son güncelleme = 2016-02-14
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
dertop = []
with open("./veri/dertop.txt",encoding="utf-8") as fin:
    for soz in fin:
        if soz>='a' and soz < 'b':
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


if __name__ == "__main__":
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
                        adaylar.append(s)
                n += 1
                if n>=nx:
                    break

        if len(adaylar)==0:
            print(soz,file=fyok)
        else:
            for aday in adaylar:
                sonuc = aday+"-"+soz[len(aday):]
                if len(adaylar)==1:
                    print(sonuc,file=fout)
                else:
                    print(sonuc,end=" ",file=fcok)
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
    print("\nToplam süre = {} saniye".format(time.perf_counter()-t0))
