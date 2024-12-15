from tkinter import *
from fpdf import FPDF
import pandas as pd
import sqlite3
from tkinter import messagebox
from tkinter import filedialog

class RaporlamaEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent, width=800, height=600)
        self.grid_propagate(False) 

        # Başlık
        Label(self, text="Raporlama Ekranı", font=("Arial", 16), fg="#333333").pack(pady=10)
        
        # PDF Raporlama Butonu
        Button(
            self, text="PDF Raporu Oluştur", font=("Arial",12,"bold"),
            fg="white", bg="#1ABC9C", bd=0, relief="flat", activebackground="#16A085",
            command=self.pdf_raporu_olustur
        ).pack(pady=5, ipadx=20, ipady=10)
        
        # Excel Raporlama Butonu
        Button(
            self, text="Excel Raporu Dışa Aktar", font=("Arial",12,"bold"),
            fg="white", bg="#3498DB", bd=0, relief="flat", activebackground="#2980B9",
            command=self.excel_dosya_aktar
        ).pack(pady=5, ipadx=20, ipady=10)

    def pdf_raporu_olustur(self):
        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        cursor.execute("SELECT ogrenci_no, isim, soyisim, dogum_tarihi FROM ogrenciler")
        rows = cursor.fetchall()
        connection.close()

        if not rows:
            messagebox.showerror("Hata", "Veritabanında öğrenci verisi bulunamadı!")
            return
        pdf = FPDF()
        pdf.add_page()

        # Yazı tipi ekle
        try:
            pdf.add_font("DejaVu", '', "fonts/DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", size=12)
        except RuntimeError:
            pdf.add_font("Arial", '', "C:/Windows/Fonts/Arial.ttf", uni=True)
            pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Öğrenci Listesi Raporu", ln=True, align='C')
        pdf.cell(40, 10, txt="Ogrenci No", border=1, align='C')
        pdf.cell(60, 10, txt="İsim", border=1, align='C')
        pdf.cell(60, 10, txt="Soyisim", border=1, align='C')
        pdf.cell(40, 10, txt="Doğum Tarihi", border=1, align='C')
        pdf.ln()

        for row in rows:
            pdf.cell(40, 10, txt=row[0], border=1, align='C')
            pdf.cell(60, 10, txt=row[1], border=1, align='C')
            pdf.cell(60, 10, txt=row[2], border=1, align='C')
            pdf.cell(40, 10, txt=row[3], border=1, align='C')
            pdf.ln()

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF files", "*.pdf")],
                                                title="PDF Raporunu Kaydet")
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Başarılı", "PDF raporu başarıyla oluşturuldu!")

    def excel_dosya_aktar(self):
        connection = sqlite3.connect('ogrenci_yonetim.db')
        df = pd.read_sql_query("SELECT ogrenci_no, isim, soyisim, dogum_tarihi FROM ogrenciler", connection)
        connection.close()

        if df.empty:
            messagebox.showerror("Hata", "Veritabanında öğrenci verisi bulunamadı!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx")],
                                                 title="Excel Dosyasını Kaydet")
        if file_path:
            df.to_excel(file_path, index=False, engine='openpyxl')
            messagebox.showinfo("Başarılı", "Excel dosyası başarıyla oluşturuldu!")
