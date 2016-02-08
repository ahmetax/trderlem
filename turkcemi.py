# -*- coding: utf-8 -*-
#turkcemi.py
#2016-02-08
#author = Ahmet Aksoy
#Son güncelleme = 2016-02-08
#Python 3.5.1 ile test edildi

"""
Amaç: Bir metni okuyup sözcüklerine ayırmak
sonra da bu sözcüklerin ne kadarının dertop.txt
dosyasında yer aldığını belirlemek
"""
BHARF = "ÇĞİIÖŞÜ"
KHARF = "çğiıöşü"
BHARFX = "Iİ"
KHARFX = "ıi"
AYRACLAR = ",\.;«»!?-:/\*+_=\"<>()'[]|º#&%"

#Dikkat! dertop listesinde uzatma/inceltme işaretli sözcükler yok
#Bütün sözcükler küçük harf
dertop = []
with open("./veri/dertop.txt",encoding="utf-8") as fin:
    for soz in fin:
        dertop.append(soz.strip())
print("dertop boyu = "+str(len(dertop)))

def kucukHarfYap(sozcuk):
    ss = ''
    for i in range(len(sozcuk)):
        ok = False
        for j in range(len(BHARFX)):
            if sozcuk[i]== BHARFX[j]:
                ss += KHARFX[j]
                ok = True
                break
        if ok == False:
            ss += sozcuk[i]
    ss = ss.lower()
    return ss

def inceltme_yok(sozcuk):
    s=""
    for harf in sozcuk:
        if harf=='â' or harf=='Â':
            s += 'a'
        elif harf == 'ê' or harf=='Ê':
            s += 'e'
        elif harf == 'û' or harf=='Û':
            s += 'u'
        else:
            s+=harf
    return s


def parcala(metin):
    sozcukler = []
    sat0 = ''
    for sat in metin.split():
        sat0 += sat.strip()
        if sat[-1]=='-':    #Satır sonunda tire varsa
            sat0 =sat0[:-1]
            continue
        else:
            #AYRACLAR içindeki karakterler de aslında sözcükleri ayırıyor
            for a in AYRACLAR:
                sat0 = sat0.replace(a,' ')

            kelimeler = sat0.split()    #boşluklara göre parçala
            for kelime in kelimeler:
                if kelime.isalpha():
                    sozcukler.append(kelime)
                elif kelime.isalnum():
                    pass
                elif kelime.isdigit():
                    pass
                else:
                    k = kelime.strip(AYRACLAR)
                    sozcukler.append(k)
            sat0=''

    return sozcukler

def turkcemi(metin):
    #metni sözcüklerine ayır
    liste = parcala(metin)
    say = 0
    var = 0
    for soz in liste:
        say += 1
        soz2 = inceltme_yok(kucukHarfYap(soz))
        if soz2 in dertop:
            var += 1
            print(soz+" dertop listesinde bulundu!")
        else:
            print(soz+" dertop listesinde bulunamadı!")
    print("Toplam= {} Bulunan= {} Bulunma Oranı= % {}".format(say,var,100*var/say))


if __name__ == "__main__":
    #kucukHaryYap fonksiyonunun Türkçe karakterler için doğru çalıştığından emin olalım
    assert kucukHarfYap("ÇĞIİÖŞÜ")=="çğıiöşü"

    metin = """
    Bu bir Türkçe şarkı metnidir.
    Semavi dinler ne durumda?
    Cengaverler ne yapmışlar?
    Yoksa cengâver mi demeliydi?
    Peki paşalar ne demiş bu işe?
    Bu köşe yaz köşesi, o köşe kış köşesi, ortasında su şişesi.
    Çekoslavakyalılaştıramadıklarımızdan mısınız?
    Avustralyalılaştıramadıklarımızdan mısınız?
    İstanbul, Eskişehir, Ankara tren güzergahında...
    ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ
    """
    turkcemi(metin)
