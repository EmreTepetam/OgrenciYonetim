from tkinter import *
from tkinter import messagebox
import sqlite3

class KullaniciGirisEkran(Frame):
    def __init__(self, parent, show_main_screen):
        super().__init__(parent)

        self.show_main_screen = show_main_screen

        Label(self, text="Kullanıcı Adı").grid(row=0, column=0, padx=10, pady=10)
        Label(self, text="Şifre").grid(row=1, column=0, padx=10, pady=10)

        self.kullanici_adi_entry = Entry(self)
        self.sifre_entry = Entry(self, show="*")

        self.kullanici_adi_entry.grid(row=0, column=1)
        self.sifre_entry.grid(row=1, column=1)

        Button(self, text="Giriş Yap", command=self.giris_yap).grid(row=2, column=0, pady=10)
        Button(self, text="Kayıt Ol", command=self.kayit_ol).grid(row=2, column=1, pady=10)

    def giris_yap(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM kullanicilar WHERE kullanici_adi = ? AND sifre = ?
        """, (kullanici_adi, sifre))
        user = cursor.fetchone()
        connection.close()

        if user:
            messagebox.showinfo("Başarılı", "Giriş başarılı!")
            self.show_main_screen()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

    def kayit_ol(self):
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        if not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        try:
            cursor.execute("""
            INSERT INTO kullanicilar (kullanici_adi, sifre)
            VALUES (?, ?)
            """, (kullanici_adi, sifre))
            connection.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut!")
        finally:
            connection.close()
