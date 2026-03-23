import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta

conn = sqlite3.connect("salle.db")
cur = conn.cursor()

#Création des tables
cur.execute("""
CREATE TABLE IF NOT EXISTS adherents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prenom TEXT,
    email TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS abonnements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_adherent INTEGER,
    type TEXT,
    date_debut TEXT,
    date_fin TEXT,
    montant REAL
)
""")
conn.commit()

def charger_adherents(filtre=""):
    """Actualise la liste des adhérents avec recherche possible."""
    liste.delete(0, END)
    if filtre.strip() == "":
        cur.execute("SELECT id, nom, prenom, email FROM adherents ORDER BY nom")
    else:
        mot = f"%{filtre.strip()}%"
        cur.execute("""
            SELECT id, nom, prenom, email FROM adherents
            WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ?
            ORDER BY nom
        """, (mot, mot, mot))
    for id_, nom, prenom, email in cur.fetchall():
        liste.insert(END, f"{id_} - {nom} {prenom} ({email})")

def recherche_adherent(event=None):
    """Recherche en direct dans la liste."""
    filtre = entry_recherche.get()
    charger_adherents(filtre)

def ajouter_adherent():
    """Ajoute un nouvel adhérent dans la base."""
    nom = entry_nom.get().strip()
    prenom = entry_prenom.get().strip()
    email = entry_email.get().strip()
    if nom == "" or prenom == "":
        messagebox.showerror("Erreur", "Nom et prénom obligatoires !")
        return
    cur.execute("INSERT INTO adherents (nom, prenom, email) VALUES (?, ?, ?)", (nom, prenom, email))
    conn.commit()
    entry_nom.delete(0, END)
    entry_prenom.delete(0, END)
    entry_email.delete(0, END)
    charger_adherents()
    messagebox.showinfo("OK", "Adhérent ajouté avec succès !")

def supprimer_adherent():
    """Supprime un adhérent et ses abonnements."""
    selection = liste.get(ACTIVE)
    if not selection:
        messagebox.showwarning("Attention", "Sélectionnez un adhérent.")
        return
    id_ = selection.split(" - ")[0]
    if not messagebox.askyesno("Confirmation", "Supprimer cet adhérent et ses abonnements ?"):
        return
    cur.execute("DELETE FROM adherents WHERE id=?", (id_,))
    cur.execute("DELETE FROM abonnements WHERE id_adherent=?", (id_,))
    conn.commit()
    charger_adherents()
    messagebox.showinfo("OK", "Adhérent supprimé.")

def modifier_adherent():
    """Permet de modifier les informations d’un adhérent."""
    selection = liste.get(ACTIVE)
    if not selection:
        messagebox.showwarning("Attention", "Sélectionnez un adhérent.")
        return

    id_ = selection.split(" - ")[0]
    cur.execute("SELECT nom, prenom, email FROM adherents WHERE id=?", (id_,))
    data = cur.fetchone()
    if not data:
        messagebox.showerror("Erreur", "Adhérent introuvable.")
        return

    fen = Toplevel(root)
    fen.title("Modifier adhérent")

    Label(fen, text="Nom :").grid(row=0, column=0)
    entry_nom_mod = Entry(fen); entry_nom_mod.grid(row=0, column=1)
    entry_nom_mod.insert(0, data[0])

    Label(fen, text="Prénom :").grid(row=1, column=0)
    entry_prenom_mod = Entry(fen); entry_prenom_mod.grid(row=1, column=1)
    entry_prenom_mod.insert(0, data[1])

    Label(fen, text="Email :").grid(row=2, column=0)
    entry_email_mod = Entry(fen); entry_email_mod.grid(row=2, column=1)
    entry_email_mod.insert(0, data[2])

    def valider_modif():
        nom = entry_nom_mod.get().strip()
        prenom = entry_prenom_mod.get().strip()
        email = entry_email_mod.get().strip()
        cur.execute("UPDATE adherents SET nom=?, prenom=?, email=? WHERE id=?", (nom, prenom, email, id_))
        conn.commit()
        fen.destroy()
        charger_adherents()
        messagebox.showinfo("OK", "Informations mises à jour.")

    Button(fen, text="Enregistrer", command=valider_modif, bg="lightgreen").grid(row=3, column=0, columnspan=2, pady=6)

def ajouter_abonnement():
    """Ajoute un abonnement pour un adhérent."""
    selection = liste.get(ACTIVE)
    if not selection:
        messagebox.showwarning("Attention", "Sélectionnez un adhérent.")
        return

    id_ = selection.split(" - ")[0]
    fen = Toplevel(root)
    fen.title("Nouvel abonnement")

    Label(fen, text="Type (mensuel / trimestriel / annuel) :").pack()
    entry_type = Entry(fen); entry_type.pack()

    Label(fen, text="Date début (JJ/MM/AAAA) :").pack()
    entry_debut = Entry(fen)
    entry_debut.insert(0, datetime.now().strftime("%d/%m/%Y"))
    entry_debut.pack()

    Label(fen, text="Montant (€) :").pack()
    entry_montant = Entry(fen); entry_montant.pack()

    def valider_abonnement():
        type_ab = entry_type.get().strip().lower()
        date_debut = entry_debut.get().strip()
        montant_str = (entry_montant.get().strip() or "0").replace(",", ".")

        try:
            debut = datetime.strptime(date_debut, "%d/%m/%Y")
        except:
            messagebox.showerror("Erreur", "Format de date incorrect (JJ/MM/AAAA).")
            return

        if type_ab == "mensuel":
            fin = debut + timedelta(days=30)
        elif type_ab == "trimestriel":
            fin = debut + timedelta(days=90)
        elif type_ab == "annuel":
            fin = debut + timedelta(days=365)
        else:
            messagebox.showerror("Erreur", "Type inconnu (mensuel / trimestriel / annuel).")
            return

        try:
            montant = float(montant_str)
        except:
            messagebox.showerror("Erreur", "Montant invalide.")
            return

        date_fin = fin.strftime("%d/%m/%Y")
        cur.execute(
            "INSERT INTO abonnements (id_adherent, type, date_debut, date_fin, montant) VALUES (?, ?, ?, ?, ?)",
            (id_, type_ab, date_debut, date_fin, montant)
        )
        conn.commit()
        fen.destroy()
        messagebox.showinfo("OK", f"Abonnement ajouté jusqu’au {date_fin} pour {montant:.2f} €.")

    Button(fen, text="Valider", command=valider_abonnement, bg="lightblue").pack(pady=5)

def voir_abonnements():
    """Affiche tous les abonnements enregistrés."""
    fen = Toplevel(root)
    fen.title("Liste des abonnements")
    txt = Text(fen, width=70, height=16)
    txt.pack()

    cur.execute("""
        SELECT ad.nom, ad.prenom, a.type, a.date_debut, a.date_fin, a.montant
        FROM abonnements a
        JOIN adherents ad ON ad.id = a.id_adherent
        ORDER BY a.date_fin DESC
    """)
    data = cur.fetchall()
    if not data:
        txt.insert(END, "Aucun abonnement enregistré.")
        return

    for nom, prenom, type_, debut, fin, montant in data:
        txt.insert(END, f"{nom} {prenom} | {type_.capitalize()} | du {debut} au {fin} | {montant:.2f} €\n")

def verifier_alertes():
    """Alerte les abonnements arrivés à expiration."""
    cur.execute("""
        SELECT ad.nom, ad.prenom, a.date_fin
        FROM abonnements a
        JOIN adherents ad ON ad.id = a.id_adherent
    """)
    today = datetime.now().date()
    seuil = today + timedelta(days=7)

    expirés = []


    for nom, prenom, date_fin in cur.fetchall():
        try:
            fin = datetime.strptime(date_fin.strip(), "%d/%m/%Y").date()
        except:
            continue

        #détecte les abonnements expirés ou à 7 jours ou moins
        if fin <= seuil:
            if fin < today:
                etat = f"EXPIRÉ le {date_fin}"
            elif fin == today:
                etat = "expire AUJOURD'HUI"
            else:
                reste = (fin - today).days
                etat = f"expire dans {reste} jour{'s' if reste > 1 else ''} (le {date_fin})"
            expirés.append(f"- {nom} {prenom} : {etat}")
    if expirés:
        messagebox.showwarning("Alertes", "Abonnements presque expirés, proposez aux clients de prolonger. :\n" + "\n".join(expirés))
    else:
        messagebox.showinfo("OK", "Aucun abonnement expiré.")


root = Tk()
root.title("Gestion Salle de Sport")

#Zone d'ajout
Label(root, text="Nom :").grid(row=0, column=0)
entry_nom = Entry(root); entry_nom.grid(row=0, column=1)
Label(root, text="Prénom :").grid(row=1, column=0)
entry_prenom = Entry(root); entry_prenom.grid(row=1, column=1)
Label(root, text="Email :").grid(row=2, column=0)
entry_email = Entry(root); entry_email.grid(row=2, column=1)
Button(root, text="Ajouter adhérent", command=ajouter_adherent, bg="lightgreen").grid(row=3, column=0, columnspan=2, pady=6, sticky="ew")

#Recherche
Label(root, text="Rechercher (nom ou email) :").grid(row=4, column=0)
entry_recherche = Entry(root, width=30)
entry_recherche.grid(row=4, column=1, pady=4)
entry_recherche.bind("<KeyRelease>", recherche_adherent)

#Liste adhérents
liste = Listbox(root, width=50, height=10)
liste.grid(row=5, column=0, columnspan=2, pady=5)

#Boutons d’action
Button(root, text="Modifier", command=modifier_adherent, bg="lightyellow")\
    .grid(row=6, column=0, pady=3, sticky="ew")
Button(root, text="Supprimer", command=supprimer_adherent, bg="lightcoral")\
    .grid(row=6, column=1, pady=3, sticky="ew")
Button(root, text="Abonnement", command=ajouter_abonnement, bg="lightblue")\
    .grid(row=7, column=0, pady=3, sticky="ew")
Button(root, text="Voir abonnements", command=voir_abonnements, bg="khaki")\
    .grid(row=7, column=1, pady=3, sticky="ew")
Button(root, text="Vérifier alertes", command=verifier_alertes, bg="orange")\
    .grid(row=8, column=0, columnspan=2, pady=5, sticky="ew")

charger_adherents()
root.mainloop()


