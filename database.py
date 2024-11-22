import sqlite3

def create_tables():
    connection = sqlite3.connect('ogrenci_yonetim.db')
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ogrenciler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT NOT NULL,
        soyisim TEXT NOT NULL,
        dogum_tarihi TEXT
    )
    """)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()