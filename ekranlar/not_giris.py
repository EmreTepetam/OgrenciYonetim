from tkinter import *
from tkinter.ttk import Treeview, Combobox
import sqlite3
from tkinter import messagebox

class NotGirisEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Öğrenci listesi
        self.tree = Treeview(self, columns=("ID", "İsim", "Soyisim"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("İsim", text="İsim")
        self.tree.heading("Soyisim", text="Soyisim")
        self.tree.pack(fill="both", expand=True)

        # Seçim olayını bağla
        self.tree.bind("<<TreeviewSelect>>", self.refresh_notlar)

        # Ders seçimi
        Label(self, text="Ders").pack(pady=5)
        self.ders_combobox = Combobox(self, state="readonly")
        self.ders_combobox.pack(pady=5)

        # Not türü seçimi
        Label(self, text="Not Türü").pack(pady=5)
        self.not_turu_combobox = Combobox(self, state="readonly", values=["Vize", "Final"])
        self.not_turu_combobox.pack(pady=5)

        # Not girişi
        Label(self, text="Not Değeri").pack(pady=5)
        self.not_degeri_entry = Entry(self)
        self.not_degeri_entry.pack(pady=5)

        Button(self, text="Not Ekle", command=self.not_ekle).pack(pady=10)

        # Not listeleme ekranı
        self.not_tree = Treeview(self, columns=("Ders", "Not Türü", "Not Değeri"), show="headings")
        self.not_tree.heading("Ders", text="Ders")
        self.not_tree.heading("Not Türü", text="Not Türü")
        self.not_tree.heading("Not Değeri", text="Not Değeri")
        self.not_tree.pack(fill="both", expand=True)

        self.refresh_student_data()
        self.refresh_ders_data()

    def refresh_student_data(self):
        """Veritabanından öğrenci bilgilerini getir."""
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("SELECT id, isim, soyisim FROM ogrenciler")
            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())  # Mevcut verileri temizle
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def refresh_ders_data(self):
        """Veritabanından ders bilgilerini getir."""
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("SELECT id, ders_adi FROM dersler")
            rows = cursor.fetchall()

            ders_listesi = [f"{row[0]} - {row[1]}" for row in rows]
            self.ders_combobox['values'] = ders_listesi
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def not_ekle(self):
        """Seçili öğrenciye not ekle."""
        try:
            selected_item = self.tree.selection()[0]
            ogrenci_id = self.tree.item(selected_item)['values'][0]

            ders_id = self.ders_combobox.get().split(" - ")[0]
            not_turu = self.not_turu_combobox.get()
            not_degeri = self.not_degeri_entry.get()

            if not ders_id or not not_turu or not not_degeri:
                messagebox.showerror("Hata", "Tüm alanları doldurun!")
                return

            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO notlar (ogrenci_id, ders_id, not_turu, not_degeri)
            VALUES (?, ?, ?, ?)
            """, (ogrenci_id, ders_id, not_turu, float(not_degeri)))
            connection.commit()

            messagebox.showinfo("Başarılı", "Not başarıyla eklendi!")
            self.refresh_notlar()  # Notları yenile
        except IndexError:
            messagebox.showerror("Hata", "Lütfen bir öğrenci seçin!")
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def refresh_notlar(self, event=None):
        """Seçili öğrencinin notlarını yenile."""
        try:
            selected_item = self.tree.selection()[0]
            ogrenci_id = self.tree.item(selected_item)['values'][0]

            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("""
            SELECT ders_id, not_turu, not_degeri
            FROM notlar
            WHERE ogrenci_id = ?
            """, (ogrenci_id,))
            rows = cursor.fetchall()

            self.not_tree.delete(*self.not_tree.get_children())  # Mevcut verileri temizle
            for row in rows:
                self.not_tree.insert("", "end", values=row)
        except IndexError:
            self.not_tree.delete(*self.not_tree.get_children())  # Seçim yoksa tabloyu temizle
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()
