# -*- coding: utf-8 -*-
#kelimeler.py
#2016-02-13
#author = Ahmet Aksoy
#Son güncelleme = 2016-02-13
#Python 3.5.1 ile test edildi
"""
Bu modülde Kelime sınıfını oluşturacağız
Parametre olarak verilen kelimeden
kökü
ekler (tek parça)
ekler2 (parçalar - ile ayrılmış)
tip (özel isim, isim, sıfat, zarf, vb)
...
döndürülecek
"""
import time
dertop = []
with open("./veri/mertop.txt",encoding="utf-8") as fin:
    for soz in fin:
        if soz>='a' and soz < 'b':
            dertop.append(soz.strip())
print("dertop boyu = "+str(len(dertop)))

lstKokler = []
with open("./veri/kokler.txt",encoding="utf-8") as fin:
    for soz in fin:
        lstKokler.append(soz.strip())
print("kokler boyu = "+str(len(lstKokler)))

lstEkler = []
"""
with open("./veri/ekler.txt",encoding="utf-8") as fin:
    for soz in fin:
        lstEkler.append(soz.strip())
"""

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
    fyok =open("veri/yoklar.txt","w",encoding="utf-8")
    ftek =open("veri/tekler.txt","w",encoding="utf-8")
    t0 = time.perf_counter()
    for soz in dertop:
        s=soz
        if s in lstKokler:
            print(s,file=ftek)
        else:
            n = len(soz)
            while n>0:
                s = soz[:n-1]
                if s in lstKokler:
                    s1 = soz[n-1:]
                    s2 = s+'-'+s1
                    if s1 not in lstEkler:
                        lstEkler.append(s1)
                        print(s2,file=fout)
                        break
                n -= 1
                if n<1:
                    print(soz,file=fyok)
                    break
        say +=1
        if say%10==0:
            fout.flush()
            ftek.flush()
            fyok.flush()
            print(say, end=" ")

    fout.close()
    ftek.close()
    fyok.close()
    print("\nToplam süre = {} saniye".format(time.perf_counter()-t0))
