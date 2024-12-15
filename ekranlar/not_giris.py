from tkinter import *
from tkinter.ttk import Treeview, Combobox, Style
import sqlite3
from tkinter import messagebox

class NotGirisEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Ana çerçeveyi grid'e yerleştiriyoruz
        self.grid(row=0, column=0, sticky="nsew")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Üst çerçeve - Ders Seçimi
        top_frame = Frame(self)
        top_frame.grid(row=0, column=0, pady=5)

        
        Label(top_frame, text="Ders", font=("Arial", 12), fg="#555555").pack(side=LEFT, padx=10, pady=10)  
        
        self.ders_combobox = Combobox(top_frame, state="readonly", font=("Arial", 12))  
        self.ders_combobox.pack(side=LEFT, padx=10, pady=10)  
        self.ders_combobox.bind("<<ComboboxSelected>>", self.filter_ders)

        self.refresh_ders_list()
        style = Style()
        style.configure("Treeview", foreground="black")  # Hücre metinlerini siyah yap
        style.configure("Treeview.Heading", foreground="black")  # Başlık metinlerini siyah yap

        # Öğrenci not girişi tablosu
        self.tree = Treeview(self, columns=("Öğrenci No", "İsim", "Soyisim", "Vize", "Final", "Proje", "Başarı Notu", "Durum"), show="headings")
        self.tree.heading("Öğrenci No", text="Öğrenci No")
        self.tree.heading("İsim", text="İsim")
        self.tree.heading("Soyisim", text="Soyisim")
        self.tree.heading("Vize", text="Vize")
        self.tree.heading("Final", text="Final")
        self.tree.heading("Proje", text="Proje")
        self.tree.heading("Başarı Notu", text="Başarı Notu")
        self.tree.heading("Durum", text="Durum")
        self.tree.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Grid ayarları - tablo satır ve sütunu genişlesin
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        button_frame = Frame(self)
        button_frame.grid(row=2, column=0, pady=10)

        # Hesapla Butonu
        Button(
            button_frame, text="Hesapla", font=("Arial", 12, "bold"),
            bg="#1ABC9C", fg="white", bd=0, relief="flat", activebackground="#16A085",
            command=self.hesapla
        ).pack(side=LEFT, padx=10, pady=10, ipadx=20, ipady=10)

        # Kaydet Butonu
        Button(
            button_frame, text="Kaydet", font=("Arial", 12, "bold"),
            bg="#3498DB", fg="white", bd=0, relief="flat", activebackground="#2980B9",
            command=self.kaydet
        ).pack(side=LEFT, padx=10, pady=10, ipadx=20, ipady=10)

        # Dinamik sütun boyutlandırma
        self.bind("<Configure>", self.resize_columns)

        # Öğrenci verilerini yükle
        self.refresh_student_data()

    def resize_columns(self, event):
        """Tablonun sütun genişliklerini dinamik olarak ayarla"""
        total_width = self.tree.winfo_width()
        num_columns = len(self.tree["columns"])
        if num_columns > 0:
            column_width = total_width // num_columns
            for column in self.tree["columns"]:
                self.tree.column(column, width=column_width)
                self.tree.bind("<Double-1>", self.edit_cell)

    def refresh_student_data(self):
        """Tüm öğrencileri güncel verilerle yenile"""
        selected_ders = self.ders_combobox.get().split(" ")[0] if self.ders_combobox.get() else ''
        if not selected_ders:
            return
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            cursor.execute("""
            SELECT ogrenciler.ogrenci_no, ogrenciler.isim, ogrenciler.soyisim, 
                vize, final, proje, genel_ort, durum
            FROM ogrenciler
            LEFT JOIN notlar ON ogrenciler.ogrenci_no = notlar.ogrenci_id AND notlar.ders_id = ?
            WHERE ogrenciler.ogrenci_no IN (
                SELECT ogrenci_id FROM ogrenci_ders WHERE ders_id = ?
            )
            """, (selected_ders, selected_ders))

            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)

        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def refresh_ders_list(self):
        """Veritabanından ders listesini Combobox'a yükle"""
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            cursor.execute("SELECT id, ders_adi FROM dersler")
            dersler = cursor.fetchall()

            ders_listesi = [f"{ders[0]} {ders[1]}" for ders in dersler]
            self.ders_combobox["values"] = ders_listesi

            if ders_listesi:
                self.ders_combobox.current(0)
        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def filter_ders(self, event):
        """Seçilen derse göre filtreleme yap"""
        selected_ders = self.ders_combobox.get().split(" ")[0] if self.ders_combobox.get() else ''
        if not selected_ders:
            return
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            cursor.execute("""
            SELECT ogrenciler.ogrenci_no, ogrenciler.isim, ogrenciler.soyisim, 
                vize, final, proje, genel_ort, durum
            FROM ogrenciler
            LEFT JOIN notlar ON ogrenciler.ogrenci_no = notlar.ogrenci_id AND notlar.ders_id = ?
            WHERE ogrenciler.ogrenci_no IN (
                SELECT ogrenci_id FROM ogrenci_ders WHERE ders_id = ?
            )
            """, (selected_ders, selected_ders))

            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)

        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()

    def edit_cell(self, event):
        """Bir hücreye çift tıklama ile not girişi yap"""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if column not in ["#4", "#5", "#6"]:  # Vize, Final, Proje sütunları
            return

        current_value = self.tree.item(item, "values")[int(column[1]) - 1]

        input_popup = Toplevel(self)
        input_popup.title("Not Girişi")
        input_popup.geometry("200x100")
        input_popup.transient(self)
        input_popup.grab_set()

        Label(input_popup, text="Yeni Not Değeri:", font=("Arial", 12), fg="#555555").pack(pady=10)  
        
        entry = Entry(input_popup, font=("Arial", 12), bd=2, relief="groove")  
        entry.insert(0, current_value)
        entry.pack(pady=10)
        entry.focus_set()

        def save_input():
            new_value = entry.get()
            if not new_value.isdigit():
                messagebox.showerror("Hata", "Not sadece sayısal olabilir!")
                return
            values = list(self.tree.item(item, "values"))
            values[int(column[1]) - 1] = new_value
            self.tree.item(item, values=values)
            input_popup.destroy()
        entry.bind("<Return>", lambda e: save_input())
        # Kaydet butonu tasarımını uyguluyoruz
        Button(
            input_popup, text="Kaydet", font=("Arial", 12, "bold"),
            bg="#1ABC9C", fg="white", bd=0, relief="flat", activebackground="#16A085",
            command=save_input
        ).pack(pady=10, ipadx=20, ipady=10)

    def hesapla(self):
        """Başarı notunu hesapla ve durumu belirle"""
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            try:
                vize = float(values[3]) if values[3] else 0
                final = float(values[4]) if values[4] else 0
                proje = float(values[5]) if values[5] else 0

                vize_final_ort = (vize * 0.2) + (final * 0.8)
                genel_ort = (vize_final_ort + proje) / 2

                durum = "Kaldı" if genel_ort < 50 else "Geçti"

                self.tree.item(item, values=(values[0], values[1], values[2], vize, final, proje, round(genel_ort, 2), durum))
            except ValueError:
                messagebox.showerror("Hata", "Notlar sayısal değer olmalıdır!")

    def kaydet(self):
        """Girilen notları veritabanına kaydet"""
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            selected_ders = self.ders_combobox.get().split(" ")[0] if self.ders_combobox.get() else ''

            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                cursor.execute("""
                INSERT OR REPLACE INTO notlar (ogrenci_id, ders_id, vize, final, proje, genel_ort, durum)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (values[0], selected_ders, values[3], values[4], values[5], values[6], values[7]))
            connection.commit()
            messagebox.showinfo("Başarılı", "Notlar kaydedildi!")
        except sqlite3.Error as e:
            messagebox.showerror("Hata", f"Veritabanı hatası: {e}")
        finally:
            connection.close()
