from tkinter import *
from tkinter.ttk import Treeview
import sqlite3

class listeOgrenciEkran(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = Treeview(self, columns=("ID", "İsim", "Soyisim", "Doğum Tarihi",), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("İsim", text="İsim")
        self.tree.heading("Soyisim", text="Soyisim")
        self.tree.heading("Doğum Tarihi", text="Doğum Tarihi")
        self.tree.pack(fill="both", expand=True)
        self.refresh_data()
        

    def refresh_data(self):
        connection = sqlite3.connect('ogrenci_yonetim.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ogrenciler")
        rows = cursor.fetchall()
        for row in rows:

            self.tree.insert("","end", values=row)
        connection.close()