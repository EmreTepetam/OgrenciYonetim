from tkinter import *
from tkinter import messagebox
import sqlite3

class KullaniciGirisEkran(Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, width=800, height=600)
        
        self.grid_propagate(False) 
        self.on_login_success = on_login_success  # Giriş başarılı olduğunda çağrılacak fonksiyon

        # Ana çerçeve Dinamik olarak ekranın ortasında
        self.grid(row=0, column=0, sticky="nsew")  # Dinamik konumlandırma

        # Büyük başlık
        Label(
            self, text="Öğrenci Yönetim Sistemi", font=("Arial", 24, "bold"), fg="#2C3E50"
        ).pack(pady=20)

        # Giriş alanlarını içeren alt çerçeve
        input_frame = Frame(self)
        input_frame.pack(pady=10)

        # Kullanıcı Adı Label ve Input
        Label(input_frame, text="Kullanıcı Adı:", font=("Arial", 12), fg="#333333").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        self.kullanici_adi_entry = Entry(input_frame, font=("Arial", 12), bg="white", fg="#555555", relief="solid")
        self.kullanici_adi_entry.grid(row=0, column=1, padx=10, pady=10)

        # Şifre Label ve Input
        Label(input_frame, text="Şifre:", font=("Arial", 12), fg="#333333").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.sifre_entry = Entry(input_frame, show="*", font=("Arial", 12), bg="white", fg="#555555", relief="solid")
        self.sifre_entry.grid(row=1, column=1, padx=10, pady=10)

        # Butonlar
        button_frame = Frame(self)
        button_frame.pack(pady=10)

        Button(
            button_frame,
            text="Giriş Yap",
            command=self.giris_yap,
            font=("Arial", 12, "bold"),
            bg="#1ABC9C",
            fg="white",
            activebackground="#16A085",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5
        ).grid(row=0, column=0, padx=10)

        Button(
            button_frame,
            text="Kayıt Ol",
            command=self.kayit_ol,
            font=("Arial", 12, "bold"),
            bg="#3498DB",
            fg="white",
            activebackground="#2980B9",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5
        ).grid(row=0, column=1, padx=10)

        # Dinamik ortalama Çerçeve büyüklüğünü ve konumunu ayarlama
        self.bind("<Configure>", self.center_frame)

    def center_frame(self, event):
        """Çerçeveyi her boyut değişiminde ekranın ortasına al"""
        self.update_idletasks()
        x = (self.winfo_width() - self.winfo_reqwidth()) // 2
        y = (self.winfo_height() - self.winfo_reqheight()) // 2
        self.place(relx=0.5, rely=0.5, anchor="center")

    def giris_yap(self):
        """Giriş yapma işlemi"""
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        if not kullanici_adi or not sifre:  # Boş alan kontrolü
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre))
            user = cursor.fetchone()
            connection.close()

            if user:
                messagebox.showinfo("Başarılı", "Giriş başarılı!")
                self.destroy()  # Giriş ekranını tamamen kaldır
                self.on_login_success(kullanici_adi)  # Ana menüye geçiş
            else:
                messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")



    def kayit_ol(self):
        """Yeni kullanıcı kaydı oluşturma"""
        kullanici_adi = self.kullanici_adi_entry.get()
        sifre = self.sifre_entry.get()

        if not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)
            """, (kullanici_adi, sifre))
            connection.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut!")
        finally:
            connection.close()
