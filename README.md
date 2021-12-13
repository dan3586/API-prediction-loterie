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

#### Classifieur

La classification d'un tirage et le calcul des probabilités de gain et de perte est la partie sensible du travail. Il s'agit en effet de trouver l'algorithme le mieux adapté en terme de complexité et dont les paramètres permettent d'échapper aux situations de sur/sous ajustements. Nous avons décidé de travailler avec une régression logistique et une forêt aléatoire. A la suite des obtenus résultats, nous avons décidé de travailler avec les forêts aléatoires. Puis pour donner plus de rigueur à notre modèle, nous avons effectué une recherche par quadrillage afin de déterminer les hyper-paramètres maximisant la précision.
### FastAPI


## Installation

L'utilisation de cette API requiert l'installation de librairies spécifiques*, puis le lancement même de l'application à partir de commandes adaptées. 

> *(\*) Les librairies nécessaires sont regroupées dans le fichier requirements.txt, dont l'execution permet l'installation de l'ensemble des éléments.*

### Installer les librairies

En vous connectant à votre Terminal, allez dans le dossier contenant le fichier *requirements.txt* et executez la ligne suivante :

> pip3 install -r requirements.txt

### Mettre en marche l'API
