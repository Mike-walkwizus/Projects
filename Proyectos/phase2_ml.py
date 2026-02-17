import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1️⃣ Création des données
# Nombres entre 0 et 1000
X = np.random.randint(0, 1000, 500).reshape(-1, 1)

# Règle cachée (que le modèle ne connaît pas)
# 0 = petit (<500)
# 1 = grand (>=500)
y = np.array([1 if x >= 500 else 0 for x in X.flatten()])

# 2️⃣ Séparer en train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3️⃣ Créer le modèle
model = LogisticRegression()

# 4️⃣ Entraîner
model.fit(X_train, y_train)

# 5️⃣ Tester
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Précision du modèle :", accuracy)
print("-" * 40)

# 6️⃣ Interaction utilisateur
while True:
    user_input = input("Entre un nombre entre 0 et 1000 (ou quit) : ")

    if user_input == "quit":
        break

    number = int(user_input)
    prediction = model.predict([[number]])

    if prediction[0] == 1:
        print("Le modèle pense que c'est GRAND")
    else:
        print("Le modèle pense que c'est PETIT")

    print("-" * 30)
