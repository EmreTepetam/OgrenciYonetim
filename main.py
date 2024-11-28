from tkinter import *
from ekranlar.kullanici_giris import KullaniciGirisEkran
from ekranlar.ekle_ogrenci import ekleOgrenciEkran
from ekranlar.liste_ogrenci import listeOgrenciEkran
from ekranlar.not_giris import NotGirisEkran

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Öğrenci Yönetim Sistemi")
        self.geometry("800x600")  # Varsayılan boyut
        self.minsize(600, 400)  # Minimum boyut

        # Ana ekran çerçevesi
        self.container = Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Dinamik boyutlandırma
        self.bind("<Configure>", self.resize_frames)

        # Giriş ekranını göster
        self.show_login_screen()

    def resize_frames(self, event):
        """Pencere boyutu değiştiğinde ekranları yeniden boyutlandır."""
        for frame in self.frames.values():
            frame.configure(width=self.winfo_width(), height=self.winfo_height())

    def show_login_screen(self):
        login_frame = KullaniciGirisEkran(self.container, self.show_main_screen)
        login_frame.pack(fill="both", expand=True)
        self.frames['login'] = login_frame

    def show_main_screen(self):
        self.frames['login'].pack_forget()

        liste_frame = listeOgrenciEkran(self.container)
        not_frame = NotGirisEkran(self.container)

        ekle_frame = ekleOgrenciEkran(self.container, refresh_callbacks=[liste_frame.refresh_data, not_frame.refresh_student_data])

        for F, frame in [(ekleOgrenciEkran, ekle_frame), (listeOgrenciEkran, liste_frame), (NotGirisEkran, not_frame)]:
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_menu()
        self.show_frame(ekleOgrenciEkran)

    def create_menu(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        menu_bar.add_command(label="Öğrenci Ekle", command=lambda: self.show_frame(ekleOgrenciEkran))
        menu_bar.add_command(label="Öğrenci Listesi", command=lambda: self.show_frame(listeOgrenciEkran))
        menu_bar.add_command(label="Not Girişi", command=lambda: self.show_frame(NotGirisEkran))
        menu_bar.add_command(label="Çıkış", command=self.show_login_screen)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
