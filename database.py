import sqlite3

def create_tables():
    """Veritabanında gerekli tabloları oluşturur."""
    connection = sqlite3.connect('ogrenci_yonetim.db')
    cursor = connection.cursor()

    # Dersler tablosunu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dersler (
        id TEXT PRIMARY KEY,
        ders_adi TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ogrenci_ders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ogrenci_id TEXT NOT NULL,  -- Öğrenci numarası
        ders_id TEXT NOT NULL,     -- Ders kimliği
        FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler (ogrenci_no),
        FOREIGN KEY (ders_id) REFERENCES dersler (id)
    )
    """)

    # Notlar tablosunu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ogrenci_id TEXT NOT NULL,  -- Öğrenci numarası (ogrenci_no) kullanılacak
        ders_id TEXT NOT NULL,
        vize REAL DEFAULT 0,      -- Vize notu
        final REAL DEFAULT 0,     -- Final notu
        proje REAL DEFAULT 0,     -- Proje notu
        genel_ort REAL DEFAULT 0, -- Genel başarı notu
        durum TEXT DEFAULT 'Kaldı', -- Durum (Geçti/Kaldı)
        FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler (ogrenci_no),
        FOREIGN KEY (ders_id) REFERENCES dersler (id)
    )
    """)

    # Öğrenciler tablosunu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ogrenciler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT NOT NULL,
        soyisim TEXT NOT NULL,
        dogum_tarihi TEXT NOT NULL,
        ogrenci_no TEXT UNIQUE NOT NULL -- Öğrenci numarası zorunlu
    )
    """)

    # Kullanıcılar tablosunu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kullanicilar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_adi TEXT NOT NULL UNIQUE,
        sifre TEXT NOT NULL
    )
    """)

    # Örnek dersler ekle
    cursor.execute("INSERT OR IGNORE INTO dersler (id, ders_adi) VALUES ('mat1', 'Matematik')")
    cursor.execute("INSERT OR IGNORE INTO dersler (id, ders_adi) VALUES ('fizik1', 'Fizik')")
    cursor.execute("INSERT OR IGNORE INTO dersler (id, ders_adi) VALUES ('turkce1', 'Türkçe')")

    connection.commit()
    connection.close()
    print("Tablolar oluşturuldu ve örnek veriler eklendi.")


def reset_notlar_table():
    """Notlar tablosunu sıfırlar ve yeniden oluşturur."""
    connection = sqlite3.connect('ogrenci_yonetim.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS notlar")
    cursor.execute("""
    CREATE TABLE notlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ogrenci_id TEXT NOT NULL,
        ders_id TEXT NOT NULL,
        vize REAL DEFAULT 0,
        final REAL DEFAULT 0,
        proje REAL DEFAULT 0,
        genel_ort REAL DEFAULT 0,
        durum TEXT DEFAULT 'Kaldı',
        FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler (ogrenci_no),
        FOREIGN KEY (ders_id) REFERENCES dersler (id)
    )
    """)
    connection.commit()
    connection.close()
    print("notlar tablosu sıfırlandı ve yeniden oluşturuldu.")



if __name__ == "__main__":
    create_tables()
