from tkinter import *
from tkinter import messagebox
import sqlite3

class DersYonetimEkran(Frame):
    def __init__(self, parent, refresh_callbacks=None):
        super().__init__(parent, width=800, height=600)
        self.grid_propagate(False) # ekran boyutu sabit kalsın değişmesin

        self.refresh_callbacks = refresh_callbacks or [] # liste boş olabilir

        # Başlık
        Label(self, text="Ders Yönetim Sistemi", font=("Arial", 16), fg="#333333").pack(pady=10) # ders yönetim başlığı

        # Ders ID Alanı
        Label(self, text="Ders ID (örn. mat1):", font=("Arial",12), fg="#555555").pack(pady=5) # ders id girilsin
        self.ders_id_entry = Entry(self, width=30, font=("Arial",12), bd=2, relief="groove", fg="#555555")
        self.ders_id_entry.pack(pady=5)

        # Ders Adı Alanı
        Label(self, text="Ders Adı:", font=("Arial",12), fg="#555555").pack(pady=5)
        self.ders_adi_entry = Entry(self, width=30, font=("Arial",12), bd=2, relief="groove", fg="#555555")
        self.ders_adi_entry.pack(pady=5)

        # Ders Ekle Butonu
        Button(
            self, text="Ders Ekle", font=("Arial",12,"bold"),
            fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
            command=self.ders_ekle
        ).pack(pady=10, ipadx=20, ipady=10) # ders ekleme butonu

        # Ders Listesi Başlık
        Label(self, text="Ders Listesi:", font=("Arial",12), fg="#555555").pack(pady=5)

        self.ders_listesi = Listbox(self, width=50, height=10, font=("Arial",12), fg="#555555")
        self.ders_listesi.pack(pady=5) # dersler buraya gelecek

        # Alt Butonlar Yana Yana
        button_frame = Frame(self)
        button_frame.pack(pady=10)

        # Ders Sil, Güncelle ve Öğrenci Ata Butonları
        Button(
            button_frame, text="Ders Sil", font=("Arial",12,"bold"),
            fg="white", bg="#E74C3C", bd=0, relief="flat", activebackground="#C0392B",
            command=self.ders_sil
        ).pack(side=LEFT, padx=5, ipadx=20, ipady=10)

        Button(
            button_frame, text="Ders Güncelle", font=("Arial",12,"bold"),
            fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
            command=self.ders_guncelle
        ).pack(side=LEFT, padx=5, ipadx=20, ipady=10)

        Button(
            button_frame, text="Öğrenci Ata", font=("Arial",12,"bold"),
            fg="white", bg="#3498DB", bd=0, relief="flat", activebackground="#2980B9",
            command=self.ogrenci_ata
        ).pack(side=LEFT, padx=5, ipadx=20, ipady=10)

        self.refresh_ders_listesi()

    def ders_ekle(self):
        ders_id = self.ders_id_entry.get().strip()
        ders_adi = self.ders_adi_entry.get().strip()

        if not ders_id or not ders_adi:
            messagebox.showerror("Hata", "Ders ID ve Ders Adı boş bırakılamaz!")
            return

        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO dersler (id, ders_adi) VALUES (?, ?)", (ders_id, ders_adi))
            connection.commit()
            messagebox.showinfo("Başarılı", "Ders başarıyla eklendi!")
            print("ders eklendi veritabanina") # debug için
            self.refresh_ders_listesi()

            for callback in self.refresh_callbacks:
                callback()
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu ID zaten mevcut veya ders adı tekrar ediyor!")
            print("ders eklerken hata") # debug için
        finally:
            connection.close()
            print("ders ekle baglanti kapandi") # debug için

    def ders_sil(self):
        selected_ders = self.ders_listesi.curselection()
        if not selected_ders:
            messagebox.showerror("Hata", "Lütfen bir ders seçin!")
            return
        ders_id = self.ders_listesi.get(selected_ders).split(" - ")[0]
        confirmation = messagebox.askyesno("Ders Sil", f"{ders_id} dersini silmek istediğinizden emin misiniz?")

        if not confirmation:
            return

        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM dersler WHERE id = ?", (ders_id,))
            connection.commit()
            messagebox.showinfo("Başarılı", "Ders başarıyla silindi!")
            print("ders silindi") # debug için
            self.refresh_ders_listesi()

            for callback in self.refresh_callbacks:
                callback()
        finally:
            connection.close()
            print("ders sil baglanti kapandi") # debug için

    def ogrenci_ata(self):
        selected_ders = self.ders_listesi.curselection()
        if not selected_ders:
            messagebox.showerror("Hata", "Lütfen bir ders seçin!")
            return

        ders_id = self.ders_listesi.get(selected_ders).split(" - ")[0]
        DersAtamaEkrani(self, ders_id)
        print("ogrenci ata ekrani acildi") # debug için

    def ders_guncelle(self):
        selected_ders = self.ders_listesi.curselection()
        if not selected_ders:
            messagebox.showerror("Hata", "Lütfen bir ders seçin!")
            return

        ders_id = self.ders_listesi.get(selected_ders).split(" - ")[0]

        new_name = self.prompt_update_ders(ders_id)
        if not new_name:
            return

        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        try:
            cursor.execute("UPDATE dersler SET ders_adi = ? WHERE id = ?", (new_name, ders_id))
            connection.commit()
            messagebox.showinfo("Başarılı", "Ders başarıyla güncellendi!")
            print("ders guncellendi") # debug için
            self.refresh_ders_listesi()
        finally:
            connection.close()
            print("ders guncelle baglanti kapandi") # debug için

    def refresh_ders_listesi(self):
        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        cursor.execute("SELECT id, ders_adi FROM dersler")
        dersler = cursor.fetchall()
        connection.close()

        self.ders_listesi.delete(0, END)
        for ders in dersler:
            self.ders_listesi.insert(END, f"{ders[0]} - {ders[1]}")
        print("ders listesi yenilendi") # debug için

    def prompt_update_ders(self, ders_id):
        new_window = Toplevel(self)
        new_window.title("Ders Güncelle")

        Label(new_window, text=f"{ders_id} dersini güncelle:", font=("Arial",12), fg="#555555").pack(pady=10)
        entry = Entry(new_window, font=("Arial",12), bd=2, relief="groove", fg="#555555")
        entry.pack(pady=10)

        result = []

        def on_submit():
            result.append(entry.get().strip())
            new_window.destroy()
            print("ders guncelleme onaylandi") # debug için

        Button(
            new_window, text="Güncelle", font=("Arial",12,"bold"),
            fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
            command=on_submit
        ).pack(pady=10, ipadx=20, ipady=10)

        new_window.transient(self)
        new_window.grab_set()
        self.wait_window(new_window)

        return result[0] if result else None


class DersAtamaEkrani(Toplevel):
    def __init__(self, parent, ders_id):
        super().__init__(parent)
        self.title(f"{ders_id} için Öğrenci Atama")
        self.geometry("400x300")
        self.ders_id = ders_id

        # Öğrenci listesi
        self.ogrenci_listesi = Listbox(self, selectmode=MULTIPLE, font=("Arial",12), fg="#555555")
        self.ogrenci_listesi.pack(fill="both", expand=True, padx=10, pady=10)

        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        cursor.execute("SELECT ogrenci_no, isim, soyisim FROM ogrenciler")
        ogrenciler = cursor.fetchall()
        connection.close()

        for ogrenci in ogrenciler:
            self.ogrenci_listesi.insert(END, f"{ogrenci[0]} - {ogrenci[1]} {ogrenci[2]}")

        Button(
            self, text="Kaydet", font=("Arial",12,"bold"),
            fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
            command=self.kaydet
        ).pack(pady=10, ipadx=20, ipady=10)

    def kaydet(self):
        selected_indices = self.ogrenci_listesi.curselection()
        if not selected_indices:
            messagebox.showerror("Hata", "Lütfen en az bir öğrenci seçin!")
            return

        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        
        try:
            for index in selected_indices:
                ogrenci = self.ogrenci_listesi.get(index).split(" ")[0]
                cursor.execute("INSERT OR IGNORE INTO ogrenci_ders (ogrenci_id, ders_id) VALUES (?, ?)", (ogrenci, self.ders_id))
            connection.commit()
            messagebox.showinfo("Başarılı", "Öğrenciler başarıyla derse atandı!")
            print("ogrenciler derse atandi") # debug için
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
            print("ogrenci atarken hata") # debug için
        finally:
            connection.close()
            print("ogrenci ata baglanti kapandi") # debug için

        self.destroy()
