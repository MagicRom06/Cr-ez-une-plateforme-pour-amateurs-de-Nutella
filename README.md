# OC-P8 Créez une plateforme pour amateurs de Nutella

## Contexte
La startup Pur Beurre, avec laquelle vous avez déjà travaillé, souhaite développer une plateforme web à destination de ses clients. Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé" (même si nous savons tous que le gras c’est la vie).

## Parcours utilisateur
L'utilisateur arrive sur le site, recherche un aliment, le choisi et l'interface lui indique un ou plusieurs subsituts.
Il est aussi possible de créer un compte avec une adresse email et un mot de passe afin d'enregistrer des substituts.

## Prérequis
Cette application utilise python 3.8 et Django 3.2

## Fonctionalités
- Recherche de produit<br>
- Affichage du détail d'un produit<br>
- Proposition d'un ou plusieurs substituts en fonction du produit recherché<br>
- Affichage du détail d'un substitut<br>
- Création d'un compte personnel
- Authentification (email, google)
- Enregistrement d'un substitut

## Démarage du site en local
git clone https://github.com/MagicRom06/Cr-ez-une-plateforme-pour-amateurs-de-Nutella.git<br>
Pour activer l'environnement virtuel une fois dans le repertoire, executer la commande pipenv shell<br>
exécuter la commande "pipenv install" pour installer les dépendances<br>
Pour ajouter les données nécessaires, executer "python manage.py load_data".
Exécuter "python manage.py runserver" pour lancer l'application.
Depuis le navigateur, aller sur l'URL http://127.0.0.1:8000/ accèder à l'application.

## Adresse du site en ligne
https://pur-beurre-rh.herokuapp.com/