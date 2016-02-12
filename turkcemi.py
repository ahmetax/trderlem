# -*- coding: utf-8 -*-
#turkcemi.py
#2016-02-08
#author = Ahmet Aksoy
#Son güncelleme = 2016-02-08
#Python 3.5.1 ile test edildi
import time, sys
import derlem

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
ozel_adlar = []
with open("./veri/ozel_adlar.txt",encoding="utf-8") as fin:
    for soz in fin:
        ozel_adlar.append(soz.strip())
print("ozel_adlar boyu = "+str(len(ozel_adlar)))


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
            sat0 =sat0[:-1]+' '     # - yerine boşluk 10.02.2016
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
    yok_liste = []
    say = len(liste)
    print("Sozcuk sayısı = ",say)
    var = 0
    yok = 0
    for soz in liste:
        if len(soz)<2: continue
        soz2 = inceltme_yok(kucukHarfYap(soz))
        if soz2  in dertop or soz2 in ozel_adlar:
            var += 1
            if var % 1000 ==0:
                print(var)
        else:
            yok += 1
            if soz2 not in yok_liste:
                yok_liste.append(soz2)
    var = say - len(yok_liste)
    fout = open("eksik.txt", "w")
    for soz in yok_liste:
        print(soz,)
        fout.write(soz+"\n")
    fout.close()
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
    basla = time.perf_counter()

    #fin = open("D:/aaa-kaynaklar/alice.txt",encoding="utf-8")
    #fin = open("D:/aaa-kaynaklar/Başkasının Karısı.txt",encoding="utf-8")
    #fin = open("D:/aaa-kaynaklar/calikusu.txt",encoding="cp1254")
    fad = "D:/aaa-kaynaklar/calikusu.txt"

    metin = ""
    try:
        fin = open(fad, encoding="utf-8")
        metin = fin.read()
    except UnicodeDecodeError:
        fin = open(fad, encoding="cp1254")
        metin = fin.read()
    except Exception as e:
        print(e)
        sys.exit()
    finally:
        fin.close()

    turkcemi(metin)
    print("Toplam çalışma süresi = {} saniye".format(time.perf_counter()-basla))
