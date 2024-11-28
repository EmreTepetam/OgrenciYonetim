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

    # Notlar tablosunu oluştur
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ogrenci_id INTEGER NOT NULL,
        ders_id TEXT NOT NULL,
        not_turu TEXT NOT NULL,
        not_degeri REAL NOT NULL,
        FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler (id),
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
        ogrenci_no TEXT UNIQUE  -- Öğrenci numarası sütunu eklendi
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
    cursor.execute("INSERT OR IGNORE INTO dersler (id, ders_adi) VALUES ('fiz1', 'Fizik')")
    cursor.execute("INSERT OR IGNORE INTO dersler (id, ders_adi) VALUES ('kim1', 'Kimya')")

    connection.commit()
    connection.close()
    print("Tablolar oluşturuldu ve örnek veriler eklendi.")


def add_ogrenci_no_column():
    """Öğrenciler tablosuna ogrenci_no sütunu ekler."""
    connection = sqlite3.connect('ogrenci_yonetim.db')
    cursor = connection.cursor()

    try:
        # Eğer ogrenci_no sütunu yoksa ekle
        cursor.execute("""
        ALTER TABLE ogrenciler
        ADD COLUMN ogrenci_no TEXT UNIQUE
        """)
        connection.commit()
        print("ogrenci_no sütunu başarıyla eklendi.")
    except sqlite3.OperationalError as e:
        print(f"ogrenci_no sütunu zaten mevcut veya hata oluştu: {e}")
    finally:
        connection.close()


def reset_ogrenciler_table():
    """Öğrenciler tablosunu sıfırlar ve yeniden oluşturur."""
    connection = sqlite3.connect('ogrenci_yonetim.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS ogrenciler")
    cursor.execute("""
    CREATE TABLE ogrenciler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT NOT NULL,
        soyisim TEXT NOT NULL,
        dogum_tarihi TEXT NOT NULL,
        ogrenci_no TEXT UNIQUE
    )
    """)
    connection.commit()
    connection.close()
    print("ogrenciler tablosu sıfırlandı ve yeniden oluşturuldu.")


if __name__ == "__main__":
    create_tables()
    add_ogrenci_no_column()  # ogrenci_no sütununu eklemeyi dener
