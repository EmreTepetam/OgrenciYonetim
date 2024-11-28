from tkinter import *
from tkinter import messagebox
import sqlite3
import random

class ekleOgrenciEkran(Frame):
    def __init__(self, parent, refresh_callbacks):
        super().__init__(parent)
        self.refresh_callbacks = refresh_callbacks  # Liste yenileme fonksiyonlarını alıyoruz

        Label(self, text="İsim").grid(row=0, column=0, padx=10, pady=10)
        Label(self, text="Soyisim").grid(row=1, column=0, padx=10, pady=10)
        Label(self, text="Doğum Tarihi").grid(row=2, column=0, padx=10, pady=10)

        self.isim_entry = Entry(self)
        self.soyisim_entry = Entry(self)
        self.dogum_tarihi_entry = Entry(self)

        self.isim_entry.grid(row=0, column=1)
        self.soyisim_entry.grid(row=1, column=1)
        self.dogum_tarihi_entry.grid(row=2, column=1)

        Button(self, text="Kaydet", command=self.kaydet_ogrenci).grid(row=3, column=0, columnspan=2, pady=10)

    def generate_unique_ogrenci_no(self):
        """Rastgele ve benzersiz bir öğrenci numarası üret."""
        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()

        while True:
            ogrenci_no = str(random.randint(100, 9999))  # 3-4 haneli bir numara oluştur
            cursor.execute("SELECT 1 FROM ogrenciler WHERE ogrenci_no = ?", (ogrenci_no,))
            if not cursor.fetchone():  # Eğer numara kullanılmamışsa döngüyü kır
                connection.close()
                return ogrenci_no

    def kaydet_ogrenci(self):
        isim = self.isim_entry.get()
        soyisim = self.soyisim_entry.get()
        dogum_tarihi = self.dogum_tarihi_entry.get()
        ogrenci_no = self.generate_unique_ogrenci_no()  # Otomatik öğrenci no üret

        if not isim or not soyisim or not dogum_tarihi:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO ogrenciler (ogrenci_no, isim, soyisim, dogum_tarihi)
            VALUES (?, ?, ?, ?)
            """, (ogrenci_no, isim, soyisim, dogum_tarihi))
            connection.commit()
            connection.close()

            messagebox.showinfo("Başarılı", f"Öğrenci başarıyla eklendi! Öğrenci No: {ogrenci_no}")

            # Liste yenileme fonksiyonlarını çağır
            for callback in self.refresh_callbacks:
                callback()
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu öğrenci numarası zaten mevcut!")
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
