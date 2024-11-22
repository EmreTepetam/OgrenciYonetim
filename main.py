from tkinter import *
from ekranlar.ekle_ogrenci import ekleOgrenciEkran
from ekranlar.liste_ogrenci import listeOgrenciEkran

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Öğrenci Yönetim Sistemi")
        self.geometry("600x400")
        self.frames = {}

        for F in (ekleOgrenciEkran, listeOgrenciEkran):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ekleOgrenciEkran)

    def show_frame(self, container):
        """Bir ekranı göster."""
        frame = self.frames[container]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()