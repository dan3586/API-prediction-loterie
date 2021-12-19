# Euro million prediction

![This is an image](https://lonalo-v.azureedge.net/-/media/domain/brands/eum_logo_dark_1line.png)

> * Source : *https://www.loterie-nationale.be/nos-jeux/euromillions/*

## Résumé

Ce projet consiste en la mise en place d'une API permettant de :
>   * Prédire le pourcentage de gain au loto d'une combinaison de chiffres 
>   * Générer des combinaisons ayant de fortes probabilités de gain
>   * Enrichir la base de données et le modèle grâce à l'ajout de nouvelles combinaisons gagnantes

Pour ce faire nous avons uilisé la librairie de Machine Learning __Sklearn__  et le framework __FastAPI__.

## Jeu de données

Les données utilisées pour produire ce travail sont extraites des précédents résultats de tirages et de gain. Il s'agit donc de combinaisons (uniquement gagnantes), de la date de tirage, du nombre de gagnants et de la somme mise en jeu. En sachant que le jeu respecte les règles suivantes :
> * Chaque tirage est indépendant des autres
> * Un tirage génère 5 numéros de 1 à 50 et deux numéros étoiles de 1 à 12
> * Un gagnant est défini lorsqu’il obtient 5 bons numéros et 2 bons numéros étoiles

## Choix techniques 

Des choix d'implémentation ont été fait afin d'apporter de l'optimalité à cette API.

### Machine Learning

#### Exploratory Data Analysis (EDA)

La conception du modèle de machine learning a d'abord commencé par une analyse exploratoire des données. Cette première partie nous a permis d'observer les ditributions de tirages, notamment la répartition générale des chiffres joués. Par la suite, nous avons observé la distribution des chiffres dans chaque numéros normal (N1 à N5) puis dans les numéros étoiles (E1,E2). A l'issue de cela, nous avions une idée des possibles stratégies d'implémention que nous pourrions prendre, selon ce qui est demandé. 

#### Pre-processing

Les observations faites précédemment et les stratégies établies nous ont conduis à faire une sélection de variables sur les données. Cela consistait ainsi à la suppression des variables Date, Winners (nombre de gagnants) et Gain (somme en jeu), considérés comme inutiles à la prévision. De plus, malgré le désir d'effectuer du __features engineering__, nous sommes rendu compte de la non viabilité de ces opérations sur les données. On arriverait à une situation où le modèle donnerait une probabilité de gain de 100 % à chaque combinaison saisie, quelle soit bonne ou mauvaise.

##### Ajout de données

La génération de fausse données nous a permis d'avoir un dataset pour servir à l'entrainement du modèle. Nous avons fait le choix d'avoir un jeu de données final ayant un ratio de 20 % de tirages gagnants et 80 % de non gagnants. Après avoir testé différents scénarios, nous avons conclut que les résultats obtenus dans cette configuration étaient proches de la réalité. 

##### Conception du modèle

L'algorithme utilisé est un RandomForestClassifier, méthode privilégiée car permet de tester plusieurs issues possibles via l'entrainement de plusieurs arbres de décision, puis du choix de la classe par vote de la majorité des arbres. A la suite de ce choix, nous avons entrainé le classifieur avec les données, puis effectué une recherche par quadrillages afin d'optimiser les hyper-paramètres de la classification. Cette opération permet de trouver les valeurs des paramètres qui permettent de maximiser la précision de la classe prédite.  

##### Génération de tirages gagnants

Pour qu'une combinaison soit générée comme ayant un fort taux de gain, nous nous sommes basé sur les résultats obtenus par le modèle. En effet, la précision maximale de notre modèle est de 58 %. Ce qui veut dire que le modèle arrive à prédire la classe d'un tirage un peu plus une fois sur deux. De ce fait, afin de générer des tirages proches de ce taux, nous avons fixé à 50 % le taux minimal pour être considéré comme fort. En notant que le tirage en sortie est obtenu dans un échantillon de 2000 combinaisons testées.

### FastAPI

La mise en place de la partie serveur de l'API s'est effectué en requêtant les différentes fonctions de prédiction déjà implémentées, afin de retourner leurs résultat sur le serveur. Les étapes de traitement peuvent être résumé comme suit :
> * Définition de la classe de tirage (N1,N2,N3,N4,N5,E1,E2) et de celle du format des données initiales (Date,N1,N2,N3,N4,N5,E1,E2,Winner,Gain).
> * Conception des différentes méthodes d'interrogation des fonctions de prédiction.
> * Mise en place des critères d'existence de chacune des variables saisies.

## Installation

L'utilisation de cette API requiert l'installation de librairies spécifiques*, puis le lancement même de l'application à partir de commandes adaptées. 

> *(\*) Les librairies nécessaires sont regroupées dans le fichier requirements.txt, dont l'execution permet l'installation de l'ensemble des éléments.*

### Installer les librairies

En vous connectant à votre Terminal, allez dans le dossier contenant le fichier *requirements.txt* et executez la ligne suivante :

> pip3 install -r requirements.txt

### Mettre en marche l'API

Une fois les librairies installées, déplacez-vous dans le dossier contenant le fichier __main.py__ et lancez la commande suivante :
> *uvicorn main:app --reload*

Puis sur votre navigateur, allez sur le lien suivant :
> *http://127.0.0.1:8000/docs#/*
