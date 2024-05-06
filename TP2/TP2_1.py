# Un administrateur d’un site web veut assurer un maximum de sécurité pour les utilisateurs du site.
# Pour ceci il décide de réaliser une application qui évalue la force des mots de passe des différents
# utilisateurs du site, sachant qu’un mot de passe est une chaine de caractères qui ne comporte pas
# d’espaces.
# 1. Écrire une fonction nb_min(password) qui retourne le nombre de caractères minuscules.
# 2. Écrire une fonction nb_maj(password) qui retourne le nombre de caractères majuscules.
# 3. Écrire une fonction nb_non_alpha(password) qui retourne le nombre de caractères non
# alphabétiques.
# 4. Écrire une fonction long_min(password) qui retourne la longueur de la plus longue
# séquence de lettres minuscules.
# 5. Écrire une fonction long_maj(password) qui retourne la longueur de la plus longue
# séquence de lettres majuscules.
# 6. Écrire une fonction score(password) qui retourne le score du mot de passe. Celui‑ci est
# défini par des bonus :
# • Nombre total de caractères * 4
# • (Nombre total de caractères – nombre de lettres majuscules)*2
# • (Nombre total de caractères – nombre de lettres minuscules)*3
# • Nombre de caractères non alphabétiques*5
# et des pénalités :
# • La longueur de la plus longue séquence de lettres minuscules*2
# • La longueur de la plus longue séquence de lettres majuscules*3
# 7. Écrire le programme qui demande un mot de passe à l’utilisateur et affiche le score de celui‑ci :
# • “Très faible” si le score < 20
# • “Faible” si le score < 40
# • “Fort” si le score < 80
# • “Très fort” sinon
