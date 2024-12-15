from tkinter import *
from tkinter.ttk import Treeview, Style
from tkinter import messagebox, simpledialog
import sqlite3

class listeOgrenciEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")  
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Başlık
        self.header = Label(self, text="Öğrenci Listesi", font=("Arial", 20, "bold"), fg="#333333")
        self.header.grid(row=0, column=0, pady=10, columnspan=2, sticky="n")

        # Arama Alanı
        search_frame = Frame(self)
        search_frame.grid(row=1, column=0, pady=5, columnspan=2, sticky="n")
        
        Label(search_frame, text="Arama:", font=("Arial",12), fg="#555555").grid(row=0, column=0, padx=5)
        self.arama_entry = Entry(search_frame, font=("Arial",12), fg="#555555", bd=2, relief="groove")  
        self.arama_entry.grid(row=0, column=1, padx=5)

        # IDye Göre Ara
        Button(
            search_frame, text="ID'ye Göre Ara", font=("Arial",12,"bold"),
            fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
            command=self.ara_id
        ).grid(row=0, column=2, padx=5)

        # İsim/Soyisim e Göre Ara
        Button(
            search_frame, text="İsim/Soyisim'e Göre Ara", font=("Arial",12,"bold"),
            fg="white", bg="#3498DB", bd=0, relief="flat", activebackground="#2980B9",
            command=self.ara_isim
        ).grid(row=0, column=3, padx=5)

        # Öğrenci Listesi (Treeview)
        style = Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="white", fieldbackground="white", foreground="#333333")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#2C3E50", foreground="white")

        self.tree = Treeview(self, columns=("Öğrenci No", "İsim", "Soyisim", "Doğum Tarihi"), show="headings")
        self.tree.heading("Öğrenci No", text="Öğrenci No")
        self.tree.heading("İsim", text="İsim")
        self.tree.heading("Soyisim", text="Soyisim")
        self.tree.heading("Doğum Tarihi", text="Doğum Tarihi")
        self.tree.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # Dinamik boyutlandırma
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Alt Butonlar
        button_frame = Frame(self)
        button_frame.grid(row=3, column=0, pady=10, columnspan=2, sticky="s")

        # Güncelle
        Button(
            button_frame, text="Güncelle", font=("Arial",12,"bold"),
            fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
            command=self.guncelle
        ).pack(side=LEFT, padx=10)

        # Sil
        Button(
            button_frame, text="Sil", font=("Arial",12,"bold"),
            fg="white", bg="#E74C3C", bd=0, relief="flat", activebackground="#C0392B",
            command=self.sil
        ).pack(side=LEFT, padx=10)

        # Yenile
        Button(
            button_frame, text="Yenile", font=("Arial",12,"bold"),
            fg="white", bg="#3498DB", bd=0, relief="flat", activebackground="#2980B9",
            command=self.refresh_data
        ).pack(side=LEFT, padx=10)

        # Verileri yükle
        self.refresh_data()

    def refresh_data(self):
        """Veritabanından verileri al ve Treeview'e yükle"""
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
        """ID'ye göre arama yap"""
        arama = self.arama_entry.get()
        self.search_query("ogrenci_no", arama)

    def ara_isim(self):
        """İsim/Soyisim'e göre arama yap"""
        arama = self.arama_entry.get()
        self.search_query("isim", arama, "soyisim")

    def search_query(self, column1, arama, column2=None):
        """Arama sorgusunu çalıştır"""
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            if column2:
                cursor.execute(f"""
                SELECT ogrenci_no, isim, soyisim, dogum_tarihi 
                FROM ogrenciler 
                WHERE {column1} LIKE ? OR {column2} LIKE ?""", (f"%{arama}%", f"%{arama}%"))
            else:
                cursor.execute(f"SELECT ogrenci_no, isim, soyisim, dogum_tarihi FROM ogrenciler WHERE {column1} LIKE ?", (f"%{arama}%",))

            rows = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def guncelle(self):
        """Seçilen öğrenciyi güncelle"""
        try:
            selected_item = self.tree.selection()[0]
            ogrenci_no = self.tree.item(selected_item)["values"][0]

            def custom_dialog(title, prompt):
                dialog = Toplevel(self)
                dialog.title(title)
                dialog.geometry("300x100")
                dialog.transient(self)  
                dialog.grab_set()  
                dialog.attributes("-topmost", True)

                Label(dialog, text=prompt, font=("Arial",12), fg="#555555").pack(pady=10)  
                entry = Entry(dialog, font=("Arial",12), fg="#555555", bd=2, relief="groove")  
                entry.pack(pady=5)

                result = []

                def on_submit():
                    result.append(entry.get())
                    dialog.destroy()

                Button(
                    dialog, text="Tamam", font=("Arial",12,"bold"),
                    fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
                    command=on_submit
                ).pack(pady=5, ipadx=20, ipady=10)  
                self.wait_window(dialog)
                return result[0] if result else None

            new_name = custom_dialog("Güncelle", "Yeni isim:")
            if not new_name:
                return

            new_surname = custom_dialog("Güncelle", "Yeni soyisim:")
            if not new_surname:
                return

            new_birthdate = custom_dialog("Güncelle", "Yeni doğum tarihi (GG-AA-YYYY):")
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
        """Seçilen öğrenciyi sil"""
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
