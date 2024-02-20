import matplotlib.pyplot as plt
import numpy as np

# Données de test
x = np.linspace(0, 2 * np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(2 * x)
y4 = np.cos(2 * x)

# Création de la figure avec une grille de sous-graphiques
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(15, 8))

# Graphique 1
axs[0, 0].plot(x, y1)
axs[0, 0].set_title("Sin(x)")

# Graphique 2
axs[0, 1].plot(x, y2, "orange")
axs[0, 1].set_title("Cos(x)")

# Graphique 3
axs[1, 0].plot(x, y3, "green")
axs[1, 0].set_title("Sin(2x)")

# Graphique 4
axs[1, 2].plot(x, y4, "red")
axs[1, 2].set_title("Cos(2x)")

# Réglages supplémentaires (optionnels)
plt.suptitle("Figures avec plusieurs graphiques", fontsize=16)
plt.tight_layout()  # Ajuster automatiquement les espacements entre les sous-graphiques
plt.show()
