import random

print("=== IA PIERRE FEUILLE CISEAUX ===")
print("Tape : pierre, feuille ou ciseaux")
print("Tape 'quit' pour quitter\n")

historique_joueur = {
    "pierre": 0,
    "feuille": 0,
    "ciseaux": 0
}

def coup_aleatoire():
    return random.choice(["pierre", "feuille", "ciseaux"])

def coup_intelligent():
   
    if sum(historique_joueur.values()) == 0:
        return coup_aleatoire()

    coup_frequent = max(historique_joueur, key=historique_joueur.get)

    if coup_frequent == "pierre":
        return "feuille"
    elif coup_frequent == "feuille":
        return "ciseaux"
    else:
        return "pierre"

def determiner_gagnant(joueur, ia):
    if joueur == ia:
        return "egalite"
    elif (
        (joueur == "pierre" and ia == "ciseaux") or
        (joueur == "feuille" and ia == "pierre") or
        (joueur == "ciseaux" and ia == "feuille")
    ):
        return "joueur"
    else:
        return "ia"

score_joueur = 0
score_ia = 0

while True:
    joueur = input("Ton choix : ").lower()

    if joueur == "quit":
        break

    if joueur not in ["pierre", "feuille", "ciseaux"]:
        print("Choix invalide !\n")
        continue

    historique_joueur[joueur] += 1

    ia = coup_intelligent()
    print("IA joue :", ia)

    resultat = determiner_gagnant(joueur, ia)

    if resultat == "joueur":
        print("Tu gagnes !\n")
        score_joueur += 1
    elif resultat == "ia":
        print("L'IA gagne !\n")
        score_ia += 1
    else:
        print("Égalité !\n")

    print("Score → Toi:", score_joueur, "| IA:", score_ia)
    print("Statistiques joueur :", historique_joueur)
    print("-" * 40)

print("\n=== FIN DE PARTIE ===")
print("Score final → Toi:", score_joueur, "| IA:", score_ia)
