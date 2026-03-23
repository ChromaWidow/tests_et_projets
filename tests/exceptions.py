import sqlite3
conn = sqlite3.connect("ecole.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS professeur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    anciennete INTEGER,
    matiere TEXT NOT NULL
)
""")

professeur = [
    ("Bob", 111, "Mathematique"),
    ("Patrick", 113, "Anglais"),
    ("Carlos", 112, "Mathematique")
]

cursor.executemany("""
INSERT INTO professeur (nom, anciennete, matiere)
VALUES (?,?,?)
""", professeur)

cursor.execute("SELECT * FROM professeur")
resultats = cursor.fetchall()

for professeur in resultats:
    print(professeur)

print(cursor.fetchall)
conn.close()