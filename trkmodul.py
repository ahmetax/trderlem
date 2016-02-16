# -*- coding: utf-8 -*-
#trkmodul.py
#2016-02-16
#author = Ahmet Aksoy
#Son güncelleme = 2016-02-16
#Python 3.5.1 ile test edildi

#Sadece I ve İ harfleri küçük harfe dönüşürken sorun yaratıyor.
#Bu yüzden sadec I ve İ harflerini kontrol etmek yeterli olacak

#BHARFX = [u'Iİ']
#KHARFX = [u'ıi']
BHARFX = ('İ', 'I')
KHARFX = ('i', 'ı')

def kucukharf(sozcuk):
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

def buyukharf(sozcuk):
    ss = ''
    for i in range(len(sozcuk)):
        ok = False
        for j in range(len(KHARFX)):
            if sozcuk[i]== KHARFX[j]:
                ss += BHARFX[j]
                ok = True
                break
        if ok == False:
            ss += sozcuk[i]
    ss = ss.upper()
    return ss

def up_lo_kontrol2():
    up = "ÇĞIİÖŞÜ"
    lo = "çğıiöşü"

    if kucukharf(up) != lo:
        s = kucukharf(up)
        print("kucukharf(up) != lo")
        print("kucukharf({}) != {}".format(up, s))
        for i in range(len(s)):
            print("({} - {}) ".format(s[i], hex(ord(s[i]))), end=" ")
        print()
    else:
        print("kucukharf('{}') = '{}'".format(up,kucukharf(up)))
    print()

    if buyukharf(lo) != up:
        s = buyukharf(lo)
        print("buyukharf(lo) != up")
        print("buyukharf('{}') != '{}'".format(lo,up))
        for i in range(len(s)):
            print("({} - {}) ".format(s[i], hex(ord(s[i]))), end=" ")
        print()
    else:
        print("buyukharf({}) = {}".format(lo, buyukharf(lo)))
    print()



if __name__ == "__main__":
    for i in range(len(KHARFX)):
        print("({} - {}) ".format(KHARFX[i],hex(ord(KHARFX[i])), end=" "))
    print()

    for i in range(len(BHARFX)):
        print("({} - {}) ".format(BHARFX[i],hex(ord(BHARFX[i]))), end=" ")
    print()
    print()

    up_lo_kontrol2()
