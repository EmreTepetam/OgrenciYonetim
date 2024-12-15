from tkinter import *
from tkinter import messagebox
import sqlite3
import random

class ekleOgrenciEkran(Frame):
    def __init__(self, parent, refresh_callbacks):
        super().__init__(parent, width=800, height=600)
        self.refresh_callbacks = refresh_callbacks
        self.grid_propagate(False) # ekran boyutu sabit kalsun

        # Başlık
        Label(
            self, text="Öğrenci Ekleme Ekranı", font=("Arial", 20, "bold"), fg="#333333"
        ).pack(pady=20) # ogrenci ekleme baslik

        # Giriş kutuları ve etiketler için çerçeve
        form_frame = Frame(self, )
        form_frame.pack(pady=10) # form cercevesi

        # İsim
        Label(form_frame, text="İsim:", font=("Arial", 12), fg="#555555").grid(row=0, column=0, padx=10, pady=10, sticky=E) # isim label
        self.isim_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="groove")
        self.isim_entry.grid(row=0, column=1, padx=10, pady=10)

        # Soyisim
        Label(form_frame, text="Soyisim:", font=("Arial", 12), fg="#555555").grid(row=1, column=0, padx=10, pady=10, sticky=E) # soyisim label
        self.soyisim_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="groove")
        self.soyisim_entry.grid(row=1, column=1, padx=10, pady=10)

        # Doğum Tarihi
        Label(form_frame, text="Doğum Tarihi:", font=("Arial", 12), fg="#555555").grid(row=2, column=0, padx=10, pady=10, sticky=E) # dogum tarihi label
        self.dogum_tarihi_entry = Entry(form_frame, font=("Arial", 12), bd=2, relief="groove")
        self.dogum_tarihi_entry.grid(row=2, column=1, padx=10, pady=10)

        # Kaydet Butonu
        Button(
            self, text="Kaydet", font=("Arial", 12, "bold"), bg="#1ABC9C", fg="white",
            command=self.kaydet_ogrenci, bd=0, relief="flat", activebackground="#16A085"
        ).pack(pady=20, ipadx=20, ipady=10) 

        # Dinamik ortalama
        self.bind("<Configure>", self.center_frame)

    def center_frame(self, event):
        # ekran boyutu degisince ortala
        self.update_idletasks()
        x = (self.winfo_width() - self.winfo_reqwidth()) // 2
        y = (self.winfo_height() - self.winfo_reqheight()) // 2
        self.place(relx=0.5, rely=0.5, anchor="center")

    def generate_unique_ogrenci_no(self):
        # benzersiz ogrenci no uret
        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()

        while True:
            ogrenci_no = str(random.randint(100, 9999))
            cursor.execute("SELECT 1 FROM ogrenciler WHERE ogrenci_no = ?", (ogrenci_no,))
            if not cursor.fetchone():
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

            ogrenci_no = self.generate_unique_ogrenci_no()

            cursor.execute("""
            INSERT INTO ogrenciler (isim, soyisim, dogum_tarihi, ogrenci_no)
            VALUES (?, ?, ?, ?)
            """, (isim, soyisim, dogum_tarihi, ogrenci_no))

            cursor.execute("INSERT INTO ogrenci_ders (ogrenci_id, ders_id) VALUES (?, 'mat1')", (ogrenci_no,))
            cursor.execute("INSERT INTO ogrenci_ders (ogrenci_id, ders_id) VALUES (?, 'fizik1')", (ogrenci_no,))
            cursor.execute("INSERT INTO ogrenci_ders (ogrenci_id, ders_id) VALUES (?, 'turkce1')", (ogrenci_no,))

            connection.commit()
            messagebox.showinfo("Başarılı", "Öğrenci başarıyla eklendi!")
            print("ogrenci eklendi") # debug için

            self.isim_entry.delete(0, END)
            self.soyisim_entry.delete(0, END)
            self.dogum_tarihi_entry.delete(0, END)

        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
            print("veritabani hatasi") # debug için
        finally:
            connection.close()
            print("baglanti kapandi") # debug için

            if self.refresh_callbacks:
                for callback in self.refresh_callbacks:
                    callback()
                    print("callback cagirildi") # debug için
