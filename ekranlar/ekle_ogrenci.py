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

        if not isim or not soyisim or not dogum_tarihi:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")
            return

        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            # Rastgele öğrenci numarası oluştur
            ogrenci_no = self.generate_unique_ogrenci_no()

            # Öğrenci ekle
            cursor.execute("""
            INSERT INTO ogrenciler (isim, soyisim, dogum_tarihi, ogrenci_no)
            VALUES (?, ?, ?, ?)
            """, (isim, soyisim, dogum_tarihi, ogrenci_no))

            # Yeni öğrenciye varsayılan dersler ata
            cursor.execute("INSERT INTO ogrenci_ders (ogrenci_id, ders_id) VALUES (?, 'mat1')", (ogrenci_no,))
            cursor.execute("INSERT INTO ogrenci_ders (ogrenci_id, ders_id) VALUES (?, 'fizik1')", (ogrenci_no,))
            cursor.execute("INSERT INTO ogrenci_ders (ogrenci_id, ders_id) VALUES (?, 'turkce1')", (ogrenci_no,))

            connection.commit()
            messagebox.showinfo("Başarılı", "Öğrenci başarıyla eklendi!")

            # Giriş kutularını temizle
            self.isim_entry.delete(0, END)
            self.soyisim_entry.delete(0, END)
            self.dogum_tarihi_entry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
        finally:
            connection.close()

            # Not giriş ekranını güncelle
            if self.refresh_callbacks:
                for callback in self.refresh_callbacks:
                    callback()
