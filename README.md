# Euro million prediction

![This is an image](https://lonalo-v.azureedge.net/-/media/domain/brands/eum_logo_dark_1line.png=100x20)

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

La conception du modèle de machine learning a d'abord commencé par une analyse exploratoire des données. Cette première partie nous a permis d'observer les ditributions de tirages, notamment la répartition générale des chiffres joués.

### FastAPI


## Installation

L'utilisation de cette API requiert l'installation de librairies spécifiques*, puis le lancement même de l'application à partir de commandes adaptées. 

> *(\*) Les librairies nécessaires sont regroupées dans le fichier requirements.txt, dont l'execution permet l'installation de l'ensemble des éléments.*

### Installer les librairies

En vous connectant à votre Terminal, allez dans le dossier contenant le fichier *requirements.txt* et executez la ligne suivante :

> pip3 install -r requirements.txt

### Mettre en marche l'API
