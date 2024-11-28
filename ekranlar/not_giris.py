from tkinter import *
from tkinter.ttk import Treeview, Combobox
import sqlite3
from tkinter import messagebox


class NotGirisEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Ders seçimi
        Label(self, text="Ders").pack(pady=5)
        self.ders_combobox = Combobox(self, state="readonly", values=["mat1 Matematik", "fizik1 Fizik", "turkce1 Türkçe"])
        self.ders_combobox.pack(pady=5)
        self.ders_combobox.current(0)
        self.ders_combobox.bind("<<ComboboxSelected>>", self.filter_ders)

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
        self.tree.pack(fill="both", expand=True)

        # Alt butonlar (Bir kez tanımlanıyor)
        button_frame = Frame(self)
        button_frame.pack(fill="x")
        Button(button_frame, text="Hesapla", command=self.hesapla).pack(side=LEFT, padx=10, pady=10)
        Button(button_frame, text="Kaydet", command=self.kaydet).pack(side=LEFT, padx=10, pady=10)

        # Dinamik sütun boyutlandırma
        self.bind("<Configure>", self.resize_columns)

        # Öğrenci verilerini yükle
        self.refresh_student_data()

    def resize_columns(self, event):
        """Tablonun sütun genişliklerini dinamik olarak ayarla."""
        total_width = self.tree.winfo_width()
        num_columns = len(self.tree["columns"])
        if num_columns > 0:
            column_width = total_width // num_columns
            for column in self.tree["columns"]:
                self.tree.column(column, width=column_width)
                self.tree.bind("<Double-1>", self.edit_cell)  # Hücreye çift tıklama ile düzenleme

    def refresh_student_data(self):
        """Tüm öğrencileri güncel verilerle yeniler."""
        selected_ders = self.ders_combobox.get().split(" ")[0]  # Ders ID'si
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            # Seçilen dersin öğrencilerini getir
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

            self.tree.delete(*self.tree.get_children())  # Mevcut verileri temizle
            for row in rows:
                self.tree.insert("", "end", values=row)

        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()


    def filter_ders(self, event):
        """Seçilen derse göre filtreleme yap."""
        selected_ders = self.ders_combobox.get().split(" ")[0]  # Ders ID'si
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            # Öğrencileri ve notlarını seçilen derse göre filtrele
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

            self.tree.delete(*self.tree.get_children())  # Mevcut verileri temizle
            for row in rows:
                self.tree.insert("", "end", values=row)

        except sqlite3.Error as e:
            print(f"Veritabanı hatası: {e}")
        finally:
            connection.close()


    def edit_cell(self, event):
        """Bir hücreye çift tıklama ile not girişi yap."""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if column not in ["#4", "#5", "#6"]:  # Vize, Final, Proje sütunları
            return

        # Mevcut değerleri al
        current_value = self.tree.item(item, "values")[int(column[1]) - 1]

        # Input penceresi aç
        input_popup = Toplevel(self)
        input_popup.title("Not Girişi")
        input_popup.geometry("200x100")
        input_popup.transient(self)
        input_popup.grab_set()

        Label(input_popup, text="Yeni Not Değeri:").pack(pady=5)
        entry = Entry(input_popup)
        entry.insert(0, current_value)
        entry.pack(pady=5)

        def save_input():
            new_value = entry.get()
            if not new_value.isdigit():
                messagebox.showerror("Hata", "Not sadece sayısal olabilir!")
                return
            # Yeni değeri tabloya ekle
            values = list(self.tree.item(item, "values"))
            values[int(column[1]) - 1] = new_value
            self.tree.item(item, values=values)
            input_popup.destroy()

        Button(input_popup, text="Kaydet", command=save_input).pack(pady=5)

    def hesapla(self):
        """Başarı notunu hesapla ve durumu belirle."""
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            try:
                vize = float(values[3]) if values[3] else 0
                final = float(values[4]) if values[4] else 0
                proje = float(values[5]) if values[5] else 0

                # Vize ve final ortalaması
                vize_final_ort = (vize * 0.2) + (final * 0.8)
                genel_ort = (vize_final_ort + proje) / 2

                # Durum belirleme
                if genel_ort < 50:
                    durum = "Kaldı"
                else:
                    durum = "Geçti"

                # Tabloyu güncelle
                self.tree.item(item, values=(values[0], values[1], values[2], vize, final, proje, round(genel_ort, 2), durum))
            except ValueError:
                messagebox.showerror("Hata", "Notlar sayısal değer olmalıdır!")

    def kaydet(self):
        """Girilen notları veritabanına kaydet."""
        try:
            connection = sqlite3.connect('ogrenci_yonetim.db')
            cursor = connection.cursor()

            selected_ders = self.ders_combobox.get().split(" ")[0]  # Ders ID'si

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
