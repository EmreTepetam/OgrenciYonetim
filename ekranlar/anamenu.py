from tkinter import *
import sqlite3

class AnamenuEkran(Frame):
    def __init__(self, parent, kullanici_adi):
        super().__init__(parent, width=800, height=600)
        self.grid_propagate(False) # ekran boyutunun otomatik değişmemesi için

        # Başlık
        Label(
            self, 
            text=f"Hoşgeldin {kullanici_adi}!", 
            font=("Arial", 24, "bold"), 
            fg="#333333", 
        ).pack(pady=20) # kullaniciya hoşgeldin diyoruz

        # Öğrenci sayısını gösteren etiket
        self.ogrenci_sayisi_label = Label(
            self, 
            text="", 
            font=("Arial", 14), 
            fg="#3498DB", 
        )
        self.ogrenci_sayisi_label.pack(pady=10) # öğrenci sayısını yazacak

        # Hakkında yazısı
        about_text = (
            "Sistem Analizi ve Tasarımı dersi için oluşturulan bu uygulama, "
            "öğrenci yönetimini kolaylaştırmak için tasarlanmıştır. "
            "\n\nUygulama, öğrencileri, dersleri ve notları kolayca yönetmenizi sağlar."
            "\n\nGeliştirici: Emre TEPETAM/23660210090, Mersin Üniversitesi/Bilgisayar Programcılığı Öğrencisi"
        )
        Label(
            self, 
            text=about_text, 
            font=("Arial", 12), 
            fg="#555555", 
            wraplength=600, 
            justify="center"
        ).pack(pady=20) # hakkında metni ortalandı

        # Öğrenci sayısını veritabanından yükleme
        self.load_student_count() # ogrenci sayisi yukle fonks cagir

        # Dinamik yerleşim için ayarlama
        self.bind("<Configure>", self.center_frame) # boyut degisince ortala

    def load_student_count(self):
        """Veritabanından öğrenci sayısını yükler ve ekrana yazar"""
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            # Toplam öğrenci sayısını hesapla
            cursor.execute("SELECT COUNT(*) FROM ogrenciler")
            count = cursor.fetchone()[0]
            print("ogrenci sayisi cekildi") # debug için

            # Etikete yaz
            self.ogrenci_sayisi_label.config(text=f"Sistemde toplam {count} öğrenci kayıtlı")
        except sqlite3.Error as e:
            self.ogrenci_sayisi_label.config(text="Öğrenci bilgileri yüklenemedi")
            print(f"Veritabanı hatası: {e}") # debug için
        finally:
            connection.close()
            print("baglanti kapandi") # debug için

    def center_frame(self, event):
        """Tüm bileşenleri dinamik olarak ortala"""
        self.update_idletasks()
        x = (self.winfo_width() - self.winfo_reqwidth()) // 2
        y = (self.winfo_height() - self.winfo_reqheight()) // 2
        self.place(relx=0.5, rely=0.5, anchor="center") # her boyut degisiminde ortala
