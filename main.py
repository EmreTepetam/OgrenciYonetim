from tkinter import *
from ekranlar.kullanici_giris import KullaniciGirisEkran
from ekranlar.anamenu import AnamenuEkran

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Öğrenci Yönetim Sistemi")
        self.geometry("800x600")
        self.minsize(600, 400)

        self.container = Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}  # burada çerçeveler saklanıyor belki lazım olur

        # giris ekranını hemen göster
        self.show_login_screen()

    def show_login_screen(self):
        # varsa eski login i sil
        if "login" in self.frames:
            self.frames["login"].destroy()
            del self.frames["login"]

        # yeni login ekranı olustur
        login_frame = KullaniciGirisEkran(self.container, on_login_success=self.show_main_screen)
        self.frames["login"] = login_frame
        login_frame.grid(row=0, column=0, sticky="nsew")
        login_frame.tkraise()

    def show_main_screen(self, kullanici_adi):
        print("Giriş başarılı, ana menüye geçiş yapılıyor...") # debug için 
        self.kullanici_adi = kullanici_adi # kullanici adi saklamak icin

        # eski login sil
        if "login" in self.frames:
            self.frames["login"].destroy()
            del self.frames["login"]

        # menü oluştur
        self.create_menu()

        # ekranları yükle
        self.load_frames(kullanici_adi)

        # ana menü ekrana gelmiyorsa hata yazalım
        if "AnamenuEkran" in self.frames:
            self.show_frame("AnamenuEkran")
        else:
            print("Hata: AnamenuEkran yüklenemedi") # debug için

    def create_menu(self):
        # menubar yapıyoruz
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        # menü seçenekleri tek tek ekleniyor
        menu_bar.add_command(label="Ana Menü", command=lambda: self.show_frame("AnamenuEkran"))
        menu_bar.add_command(label="Öğrenci Ekle", command=lambda: self.show_frame("ekleOgrenciEkran"))
        menu_bar.add_command(label="Öğrenci Listesi", command=lambda: self.show_frame("listeOgrenciEkran"))
        menu_bar.add_command(label="Not Girişi", command=lambda: self.show_frame("NotGirisEkran"))
        menu_bar.add_command(label="Ders Yönetimi", command=lambda: self.show_frame("DersYonetimEkran"))
        menu_bar.add_command(label="Takvim", command=lambda: self.show_frame("TakvimEkran"))
        menu_bar.add_command(label="Raporlama", command=lambda: self.show_frame("RaporlamaEkran"))

    def load_frames(self, kullanici_adi):
        # burda diğer ekranlar yükleniyor belki callback falan lazım
        from ekranlar.ekle_ogrenci import ekleOgrenciEkran
        from ekranlar.liste_ogrenci import listeOgrenciEkran
        from ekranlar.not_giris import NotGirisEkran
        from ekranlar.takvim import TakvimEkran
        from ekranlar.raporlama import RaporlamaEkran
        from ekranlar.ders_yonetimi import DersYonetimEkran
        from ekranlar.anamenu import AnamenuEkran

        refresh_callbacks = [] # bu belki lazım olur belki değil

        # her ekranı oluşturuyoruz
        self.frames["AnamenuEkran"] = AnamenuEkran(self.container, kullanici_adi)
        self.frames["ekleOgrenciEkran"] = ekleOgrenciEkran(self.container, refresh_callbacks)
        self.frames["listeOgrenciEkran"] = listeOgrenciEkran(self.container)
        self.frames["NotGirisEkran"] = NotGirisEkran(self.container)
        self.frames["DersYonetimEkran"] = DersYonetimEkran(self.container)
        self.frames["TakvimEkran"] = TakvimEkran(self.container)
        self.frames["RaporlamaEkran"] = RaporlamaEkran(self.container)

    def show_frame(self, frame_name):
        # ekranları yeniden oluşturmak için önce hepsini siliyoruz
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}  # burda da frame sözlüğünü sıfırlıyoruz

        # tekrar oluştur
        if frame_name == "AnamenuEkran":
            from ekranlar.anamenu import AnamenuEkran
            self.frames["AnamenuEkran"] = AnamenuEkran(self.container, self.kullanici_adi)
        elif frame_name == "ekleOgrenciEkran":
            from ekranlar.ekle_ogrenci import ekleOgrenciEkran
            self.frames["ekleOgrenciEkran"] = ekleOgrenciEkran(self.container, [])
        elif frame_name == "listeOgrenciEkran":
            from ekranlar.liste_ogrenci import listeOgrenciEkran
            self.frames["listeOgrenciEkran"] = listeOgrenciEkran(self.container)
        elif frame_name == "NotGirisEkran":
            from ekranlar.not_giris import NotGirisEkran
            self.frames["NotGirisEkran"] = NotGirisEkran(self.container)
        elif frame_name == "DersYonetimEkran":
            from ekranlar.ders_yonetimi import DersYonetimEkran
            self.frames["DersYonetimEkran"] = DersYonetimEkran(self.container)
        elif frame_name == "TakvimEkran":
            from ekranlar.takvim import TakvimEkran
            self.frames["TakvimEkran"] = TakvimEkran(self.container)
        elif frame_name == "RaporlamaEkran":
            from ekranlar.raporlama import RaporlamaEkran
            self.frames["RaporlamaEkran"] = RaporlamaEkran(self.container)

        # yeni frame i grid ediyoruz
        frame = self.frames[frame_name]
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise() # öne getir
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
