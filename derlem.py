# -*- coding: utf-8 -*-

import sqlite3 as sql
import os, time

#BHARF = "ÇĞİIÖŞÜ"
#KHARF = "çğiıöşü"
#string.lower() metodu I ve İ dönüşümlerinde sorunlu
BHARFX = "Iİ"
KHARFX = "ıi"

AYRACLAR = ",\.;«»!?-:/\*+_=\"<>()'[]|º#&%"

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

class Veritabani:
    def __init__(self, dosya=None):
        if dosya is None:
            self.vt = sql.connect(":memory:")
        else:
            self.vt = sql.connect(dosya)

    def sema(self, sema):
        cr = self.vt.cursor()
        cr.execute(sema)
        self.vt.commit()

    def sorgu(self, sorgu):
        cr = self.vt.cursor()
        cr.execute(sorgu)
        self.vt.commit()

    def cevap(self, sorgu):
        cr = self.vt.cursor()
        cr.execute(sorgu)
        return cr.fetchall()


class AnaSozluk(Veritabani):
    def __init__(self, dosya="anasozluk.db", yeni=False):
    #def __init__(self, dosya=None, yeni=False):
        Veritabani.__init__(self, dosya)
        try:
            cevap = self.cevap("select * from sozcukler limit 1")
        except:
            yeni = True

        if (yeni is True) or (os.path.isfile(dosya) is False):
            self.sema("CREATE TABLE sozcukler (sozcuk TEXT, frekans INT)")

    def liste_ekle(self, liste):
        for kelime, sayi_ in liste.items():
            #print (kelime, sayi_)
            self.ekle(kelime, sayi = sayi_)

    def ekle(self, sozcuk, sayi =1):
        kelime, frekans = self.kontrol(sozcuk)
        if kelime is not None:
            if frekans == 0:
                sorgu_cumlesi = 'insert into sozcukler values("%s", 1) ' % kelime
                self.sorgu(sorgu_cumlesi)
            else:
                sorgu_cumlesi = "update sozcukler set frekans = %d where sozcuk = '%s'  " % (frekans + sayi, kelime)
                self.sorgu(sorgu_cumlesi)

    def kontrol(self, sozcuk):
        cr = self.vt.cursor()
        cr.execute('select * from sozcukler where sozcuk = "%s" ' % sozcuk)
        cevaplar = cr.fetchall()
        if len(cevaplar) > 1:
            return None, "Birden fazla sozcuk dondu, problem var"
        elif len(cevaplar) == 1:
            return cevaplar[0]
        else:
            return sozcuk, 0

    def hepsi_varmi(self,liste):
        cr = self.vt.cursor()
        for kelime, sayi_ in liste.items():
            cr.execute('select * from sozcukler where sozcuk = "%s" ' % kelime)
            cevaplar = cr.fetchall()
            if len(cevaplar) <= 0:
                print (kelime, sayi_)
                return False
        return True

    def kapat(self):
        self.vt.commit()
        self.vt.close()


class Derlem:
    def __init__(self, icerik):
        self.anasozluk = AnaSozluk()
        self.icerik = icerik
        self.incele()

    def incele(self):
        def is_tek_tire_var(sozcuk_):
            if sozcuk_.count("-") == 1:
                return True
            return False

        def is_tirnak_icinde(sozcuk_):
            if sozcuk_[0] == "'" or sozcuk_[-1] == "'":
                return True
            elif sozcuk_[0] == '"' or sozcuk_[-1] == '"':
                return True
            else:
                return False

        def is_tek_tirnak_alpha(sozcuk_):
            if is_tirnak_icinde(sozcuk_):
                return False
            var = sozcuk_.count("'")
            if (sozcuk_[0] == "'") or (sozcuk_[-1] == "'"):
                return False
            say0 = sozcuk_.find("'")

            if var == 1:
                s1 = sozcuk_[:say0]
                s2 = sozcuk_[say0 + 1:]
                if s1.isalpha() and s2.isalpha():
                    return True
                else:
                    return False
            else:
                return False

        sozcukler = []
        hatalar = []
        satir0 = ""
        for satir in self.icerik:
            satir0 += str(satir).strip()
            if len(satir0) > 0:
                if satir0[-1] == "-":
                    satir0 = satir0[:-1]+' '   # Satır sonundaki tireyi boşluk yap
                    continue
                else:
                    for ayirac in AYRACLAR:
                        satir0 = satir0.replace(ayirac, " ")
                    for kelime in satir0.split():
                        if kelime.isalpha():
                            sozcukler.append(kelime)
                        elif kelime.isalnum() or kelime.isdigit():
                            pass
                        else:
                            k = kelime.strip(AYRACLAR)
                            sozcukler.append(k)
                    satir0 = ""
        temp = {}
        for sozcuk in sozcukler:
            if (sozcuk == "") or (sozcuk.isdigit()):
                continue
            if is_tek_tirnak_alpha(sozcuk):
                pass
            elif is_tek_tire_var(sozcuk):
                pass
            elif sozcuk.isalpha():
                pass
            else:
                hatalar.append(sozcuk)
                continue
            #sozcuk = sozcuk.lower()
            sozcuk = kucukHarfYap(sozcuk)
            if sozcuk in temp:
                temp[sozcuk] += 1
            else:
                temp[sozcuk] = 1
        #Bulunan sözcüklerin tümü veritabanında mevcutsa,
        # o doküman daha önce çok büyük olasılıkla taranmıştır
        if self.anasozluk.hepsi_varmi(temp)==True:
            print("Tüm kelimeler var! Bu belge daha önce taranmış!")
        else:
            self.anasozluk.liste_ekle(temp)


class PDFDerlem(Derlem):
    def __init__(self, hedef):
        #TODO duzgun turkce metin cikarabilen bir pdf modulu bulmak gerek.
        #import pyPdf
        icerik = ""
        pdf = pyPdf.PdfFileReader(open(hedef,"rb"))
        for sayfa in pdf.pages:
            icerik += sayfa.extractText()
        Derlem.__init__(self, icerik.encode("utf8").splitlines(True))

'''
pdfminer3k örneği için aşağıdaki kitaptan yararlandım:
Web Scraping with Python:
Collecting Data from the~Modern Web
Yazar: Ryan Mitchell
'''
class PDFDerlemMiner(Derlem):
    def __init__(self, hedef):
        #TODO duzgun turkce metin cikarabilen bir pdf modulu bulmak gerek.
        from pdfminer.pdfinterp import PDFResourceManager, process_pdf
        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from io import StringIO
        from io import open

        def readPdf(pdfFile):
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            laparams = LAParams()
            device = TextConverter(rsrcmgr,retstr,laparams=laparams)

            process_pdf(rsrcmgr,device,pdfFile)
            device.close()

            content = retstr.getvalue()
            retstr.close()
            return content

        icerik = ""
        pdfFile = open(hedef,"rb")
        pdf = readPdf(pdfFile)
        print(pdf)
        pdfFile.close()
        #Derlem.__init__(self, icerik.encode("utf8").splitlines(True))


class HTMLDerlem(Derlem):
    def __init__(self, hedef):
        from bs4 import BeautifulSoup
        import urllib.request
        text = ""
        url = hedef
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html,"lxml")
        if soup is not None:
            for script in soup(["script", "style"]):
                script.extract()  # rip it out
            text = soup.getText()
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)

        #Derlem.__init__(self, text.encode("utf-8").splitlines(True))
        Derlem.__init__(self, text.splitlines(True))

class TXTDerlem(Derlem):
    def __init__(self, hedef):
        icerik = ""
        with open(hedef,encoding="utf-8") as fdosya:
            for sat in fdosya:
                icerik += sat
        Derlem.__init__(self, icerik.splitlines(True))

class TXTDerlemTR(Derlem):
    def __init__(self, hedef):
        icerik = ""
        try:
            with open(hedef,encoding="utf-8") as fdosya:
                for sat in fdosya:
                    icerik += sat
        except UnicodeDecodeError:
            with open(hedef,encoding="cp1254") as fdosya:
                for sat in fdosya:
                    icerik += sat

        Derlem.__init__(self, icerik.splitlines(True))


#Veritabanındaki bilgileri kolay algılanır şekilde metin dosyasına
#en yüksek frekans en başta olacak şekilde yazıyoruz
#Hatalı girişler zamanla listenin sonunda kalacakları için elenecekler
def dosyaya():
    vt = sql.connect('anasozluk.db')
    tf = open("veri/sqlite_dokum.txt","w")
    cr = vt.cursor()
    sorgu = "select * from sozcukler ORDER BY frekans DESC"

    cr.execute(sorgu)
    vt.commit()
    cevaplar = cr.fetchall()
    if cevaplar:
        for cevap in cevaplar:
            satir = "{:08d} {}\n".format(cevap[1],cevap[0])
            tf.write(satir)

    tf.close()
    vt.close()

def txt_dosyabul(klasor):
    liste = []
    #klasördeki .txt uzantılı ve ismi zzz_ ile başlamayan dosyaları bul
    for dir, dirs, files in os.walk(klasor):
        for dosya in files:
            if dosya.endswith(".txt"):
                if not dosya.startswith("zzz_"):
                    #liste.append(os.path.join(root,dosya))
                    liste.append(dosya)

    return klasor, liste

if __name__ == '__main__':
    #assert kucukHarfYap("ÇĞIİÖŞÜ")=="çğıiöşü"
    basla = time.perf_counter()
    #htmltest = HTMLDerlem("http://manap.se/test.txt")
    #pdftest = PDFDerlemMiner("veri/test.pdf")
    #txttest = TXTDerlem("veri/txttest.txt")
    #dosyaya()
    DATA_KLASOR = "D:/aaa-kaynaklar"
    klasor, dosyalar = txt_dosyabul(DATA_KLASOR)
    for d in dosyalar:
        print(d)
        txttest = TXTDerlemTR(klasor+"/"+d)
        print("Toplam çalışma süresi = {} saniye".format(time.perf_counter()-basla))


