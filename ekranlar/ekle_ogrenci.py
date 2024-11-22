from tkinter import *
import sqlite3

class ekleOgrenciEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, text="İsim").grid(row=0, column=0, padx=10, pady=10)
        Label(self, text="Soyisim").grid(row=1, column=0, padx=10, pady=10)
        Label(self, text="Doğum Tarihi").grid(row=2, column=0, padx=10, pady=10)
        Label(self, text="Öğrenci Ekleme Ekranı").pack

        self.isim = Entry(self)
        self.soyisim = Entry(self)
        self.dogum_tarihi = Entry(self)

        self.isim.grid(row=0, column=1)
        self.soyisim.grid(row=1, column=1)
        self.dogum_tarihi.grid(row=2, column=1)

        Button(self, text="Kaydet", command=self.kaydet_ogrenci).grid(row=3, column=0, columnspan=2, pady=10)

    def kaydet_ogrenci(self):
        Connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = Connection.cursor()
        cursor.execute("""
        INSERT INTO ogrenciler (isim, soyisim, dogum_tarihi)
        VALUES (?, ?, ?)
        """, (self.isim.get(), self.soyisim.get(), self.dogum_tarihi.get()))

        Connection.commit()
        Connection.close()
        print("Öğrenci Eklendi!")
        