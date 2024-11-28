from tkinter import *
from tkinter.ttk import Treeview
from tkinter import messagebox, simpledialog  # Eksik olan import
import sqlite3


class listeOgrenciEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Arama alanı
        Label(self, text="Arama:").pack(pady=5)
        self.arama_entry = Entry(self)
        self.arama_entry.pack(pady=5)

        # Arama butonları
        Button(self, text="ID'ye Göre Ara", command=self.ara_id).pack(pady=5)
        Button(self, text="İsim/Soyisim'e Göre Ara", command=self.ara_isim).pack(pady=5)

        # Öğrenci listesi
        self.tree = Treeview(self, columns=("Öğrenci No", "İsim", "Soyisim", "Doğum Tarihi"), show="headings")
        self.tree.heading("Öğrenci No", text="Öğrenci No")
        self.tree.heading("İsim", text="İsim")
        self.tree.heading("Soyisim", text="Soyisim")
        self.tree.heading("Doğum Tarihi", text="Doğum Tarihi")
        self.tree.pack(fill="both", expand=True)

        self.refresh_data()

        # Alt butonlar
        Button(self, text="Güncelle", command=self.guncelle).pack(side=LEFT, padx=10, pady=10)
        Button(self, text="Sil", command=self.sil).pack(side=LEFT, padx=10, pady=10)
        Button(self, text="Yenile", command=self.refresh_data).pack(side=LEFT, padx=10, pady=10)

    def refresh_data(self):
        """Veritabanından verileri al ve Treeview'e yükle."""
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("SELECT ogrenci_no, isim, soyisim, dogum_tarihi FROM ogrenciler")
            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())  # Mevcut verileri temizle
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()


    def ara_id(self):
        """ID'ye göre arama yap."""
        arama = self.arama_entry.get()
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("SELECT ogrenci_no, isim, soyisim, dogum_tarihi FROM ogrenciler WHERE ogrenci_no LIKE ?", (f"%{arama}%",))
            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def ara_isim(self):
        """İsim/Soyisim'e göre arama yap."""
        arama = self.arama_entry.get()
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("""
            SELECT ogrenci_no, isim, soyisim, dogum_tarihi
            FROM ogrenciler
            WHERE isim LIKE ? OR soyisim LIKE ?
            """, (f"%{arama}%", f"%{arama}%"))
            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def guncelle(self):
        """Seçilen öğrenciyi güncelle."""
        try:
            selected_item = self.tree.selection()[0]
            ogrenci_no = self.tree.item(selected_item)["values"][0]

            # Yeni veriler için özel dialog pencereleri
            def custom_dialog(title, prompt):
                dialog = Toplevel(self)
                dialog.title(title)
                dialog.geometry("300x100")
                dialog.transient(self)  # Ana pencerenin üzerine çıkar
                dialog.grab_set()  # Etkileşim kilidi
                dialog.attributes("-topmost", True)  # Pencereyi her zaman en üstte yapar

                Label(dialog, text=prompt).pack(pady=10)
                entry = Entry(dialog)
                entry.pack(pady=5)

                result = []

                def on_submit():
                    result.append(entry.get())
                    dialog.destroy()

                Button(dialog, text="Tamam", command=on_submit).pack(pady=5)
                self.wait_window(dialog)  # Pencere kapatılana kadar bekler
                return result[0] if result else None

            new_name = custom_dialog("Güncelle", "Yeni isim:")
            if not new_name:
                return

            new_surname = custom_dialog("Güncelle", "Yeni soyisim:")
            if not new_surname:
                return

            new_birthdate = custom_dialog("Güncelle", "Yeni doğum tarihi (YYYY-MM-DD):")
            if not new_birthdate:
                return

            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("""
            UPDATE ogrenciler
            SET isim = ?, soyisim = ?, dogum_tarihi = ?
            WHERE ogrenci_no = ?
            """, (new_name, new_surname, new_birthdate, ogrenci_no))
            connection.commit()

            messagebox.showinfo("Başarılı", "Öğrenci güncellendi!")
            self.refresh_data()
        except IndexError:
            messagebox.showerror("Hata", "Lütfen bir öğrenci seçin!")
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
        finally:
            if 'connection' in locals():
                connection.close()

    def sil(self):
        """Seçilen öğrenciyi sil."""
        try:
            selected_item = self.tree.selection()[0]
            ogrenci_no = self.tree.item(selected_item)["values"][0]

            confirmation = messagebox.askyesno("Sil", "Bu öğrenciyi silmek istediğinizden emin misiniz?")
            if not confirmation:
                return

            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM ogrenciler WHERE ogrenci_no = ?", (ogrenci_no,))
            connection.commit()

            messagebox.showinfo("Başarılı", "Öğrenci başarıyla silindi!")
            self.refresh_data()
        except IndexError:
            messagebox.showerror("Hata", "Lütfen bir öğrenci seçin!")
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
        finally:
            if 'connection' in locals():
                connection.close()
