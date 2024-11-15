# Pagerank_Project
--------

### Installation Prérequis

--------

Avant d'exécuter les scripts, il est recommandé d'installer le SDK Google Cloud (CLI) sur votre ordinateur pour éviter les problèmes de connexion avec Cloud Shell. Vous pouvez télécharger et l'installer en suivant les instructions ci-dessous :

[Installer le SDK Google Cloud](https://cloud.google.com/sdk/docs/install?hl=fr)

-------

### Exécution des Fichiers

-------

Pour exécuter le projet Pagerank, suivez ces étapes :

1. **Rendez le script exécutable** :

chmod +x run_pagerank.sh

2. **Exécutez le script** :

./run_pagerank.sh

-------

### Fichiers de Données

-------

Il existe deux types de fichiers de données avec lesquels nous travaillons :

- \`page_links_en.nt.bz2\`
- \`small_page_links.nt\`

-------

### Méthodes de Pagerank

-------

Il existe deux méthodes pour calculer le Pagerank :

1. **Approche basée sur RDD**
2. **Approche basée sur DataFrame**

-------

## Résultats d'Exécution 

-------

### small_page_links.nt

Les résultats pour ces données ont été obtenus en choisissant les configurations suivantes : master-machine-type="n1-standard-4", master-boot-disk-size=50, et worker-boot-disk-size=50.


 1. **Sans Partitionnemen**

| Nœuds | RDD - Temps sans partitionnement | DataFrame - Temps sans partitionnement |
|-------|----------------------------------|---------------------------------------|
| 1     | 103s                             | 204s                                   |
| 2     | 95s                              | 174s                                   |
| 4     | 99s                              | 184s                                   |

2. **Avec Partitionnement**

| Nœuds | RDD - Temps avec partitionnement | DataFrame - Temps avec partitionnement |
|-------|----------------------------------|----------------------------------------|
| 1     | 56s                              | 103s                                   |
| 2     | 55s                              | 95s                                    |
| 4     | 54s                              | 99s                                    |

3. **Meilleurs Scores**

### page_links_en.nt.bz

Les résultats pour ces données volumineuses ont été obtenus en choisissant les configurations suivantes : master-machine-type="n1-standard-4", master-boot-disk-size=500, et worker-boot-disk-size=500.

1. **Avec Partitionnement**

| Nœuds | RDD - Temps avec partitionnement | DataFrame - Temps avec partitionnement |
|-------|----------------------------------|----------------------------------------|
| 1     | 8248s                            | 8388s                                  |
| 2     | -s                                | 4338s                                      |
| 4     | -s                                | 3593s                                      |


2. **Meilleurs Scores**

Le plus grand pagerak est : http://dbpedia.org/resource/Living_people

( Imge mountasser)

| URL | Rank |
| --- | ---- |
| <http://dbpedia.org/resource/Living_people> | 38525.86 |
| <http://dbpedia.org/resource/United_States> | 7267.18 |
| <http://dbpedia.org/resource/Year_of_birth_missing_%28living_people%29> | 4666.78 |
| <http://dbpedia.org/resource/United_Kingdom> | 2853.39 |
| <http://dbpedia.org/resource/France> | 2765.00 |
| <http://dbpedia.org/resource/Germany> | 2423.81 |
| <http://dbpedia.org/resource/Race_and_ethnicity_in_the_United_States_Census> | 2260.67 |
| <http://dbpedia.org/resource/Canada> | 2195.43 |
| <http://dbpedia.org/resource/England> | 2190.84 |
| <http://dbpedia.org/resource/World_War_II> | 2007.83 |


### Note 

Les résultats pour les données en mode 'sans partitionnement' ne sont pas disponibles, car tous les crédits ont été consommés
