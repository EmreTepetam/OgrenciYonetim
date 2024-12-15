from tkinter import *
from tkcalendar import Calendar
import sqlite3
from tkinter import messagebox

class TakvimEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent, width=800, height=600)
        self.grid_propagate(False) # burda ekran boyutu sabit kalıyor

        # Takvim Widget
        self.calendar = Calendar(self, selectmode="day", date_pattern="dd-mm-yyyy")
        self.calendar.pack(pady=10) # takvim yerleşimi

        # Etkinlik Açıklama Alanı
        Label(self, text="Etkinlik Açıklaması", font=("Arial",12), fg="#555555").pack(pady=5)
        self.etkinlik_aciklama = Entry(self, width=40, font=("Arial",12), fg="#555555", bd=2, relief="groove")
        self.etkinlik_aciklama.pack(pady=5) # burda etkinlik girilecek

        # Butonlar
        Button(
            self, text="Etkinlik Ekle", font=("Arial",12,"bold"),
            fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
            command=self.etkinlik_ekle
        ).pack(pady=5, ipadx=20, ipady=10) # burda etkinlik ekleme butonu var

        Button(
            self, text="Tüm Etkinlikleri Listele", font=("Arial",12,"bold"),
            fg="white", bg="#3498DB", bd=0, relief="flat", activebackground="#2980B9",
            command=self.etkinlikleri_listele
        ).pack(pady=5, ipadx=20, ipady=10) # tum etkinlikleri alttaki listeye getir

        Button(
            self, text="Seçilen Günün Etkinliklerini Göster", font=("Arial",12,"bold"),
            fg="white", bg="#3498DB", bd=0, relief="flat", activebackground="#2980B9",
            command=self.secilen_gunu_goster
        ).pack(pady=5, ipadx=20, ipady=10) # secili takvim gununu al listele

        # Etkinlik Listesi
        self.etkinlik_listesi = Listbox(self, width=50, height=10, font=("Arial",12), fg="#555555")
        self.etkinlik_listesi.pack(pady=10) # liste burada gösterilecek

    def etkinlik_ekle(self):
        """Etkinlik ekler"""
        tarih = self.calendar.get_date()
        aciklama = self.etkinlik_aciklama.get()

        if not aciklama:
            messagebox.showerror("Hata", "Lütfen etkinlik açıklamasını girin!")
            return

        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO etkinlikler (tarih, aciklama) VALUES (?, ?)", (tarih, aciklama))
        connection.commit()
        connection.close()

        self.etkinlik_aciklama.delete(0, END)
        messagebox.showinfo("Başarılı", "Etkinlik başarıyla eklendi!")
        print("etkinlik eklendi") # debug için
        self.etkinlikleri_listele()  # Listeyi güncelle

    def etkinlikleri_listele(self):
        """Veritabanındaki tüm etkinlikleri listeler"""
        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        cursor.execute("SELECT tarih, aciklama FROM etkinlikler ORDER BY tarih ASC")
        etkinlikler = cursor.fetchall()
        connection.close()

        self.etkinlik_listesi.delete(0, END)
        for etkinlik in etkinlikler:
            self.etkinlik_listesi.insert(END, f"{etkinlik[0]} - {etkinlik[1]}")
        print("etkinlik listesi guncellendi") # debug için

    def secilen_gunu_goster(self):
        """Seçilen güne ait etkinlikleri listeler"""
        tarih = self.calendar.get_date()
        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        cursor.execute("SELECT aciklama FROM etkinlikler WHERE tarih = ?", (tarih,))
        etkinlikler = cursor.fetchall()
        connection.close()

        self.etkinlik_listesi.delete(0, END)
        if etkinlikler:
            for etkinlik in etkinlikler:
                self.etkinlik_listesi.insert(END, etkinlik[0])
        else:
            self.etkinlik_listesi.insert(END, "Bu tarihte etkinlik yok.")
        print("secilen gun icin etkinlikler gosterildi") # debug için
