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

 1. **Sans Partitionnemen**

| Nœuds | RDD - Temps sans partitionnement | DataFrame - Temps sans partitionnement |
|-------|----------------------------------|---------------------------------------|
| 1     | 68s                              | 204s                                   |
| 2     | 65s                              | 174s                                   |
| 4     | 68s                              | 184s                                   |

2. **Avec Partitionnement**

| Nœuds | RDD - Temps avec partitionnement | DataFrame - Temps avec partitionnement |
|-------|----------------------------------|----------------------------------------|
| 1     | 56s                              | 103s                                    |
| 2     | 55s                              | 95s                                    |
| 4     | 54s                              | 99s                                    |

### page_links_en.nt.bz

1. **Sans Partitionnement**

| Nœuds | RDD - Temps sans partitionnement | DataFrame - Temps sans partitionnement |
|-------|----------------------------------|---------------------------------------|
| 1     | s                              | s                                   |
| 2     | s                              | s                                   |
| 4     | s                              | s                                   |

2. **Avec Partitionnement**

| Nœuds | RDD - Temps avec partitionnement | DataFrame - Temps avec partitionnement |
|-------|----------------------------------|----------------------------------------|
| 1     | s                              | s                                    |
| 2     | s                              | s                                    |
| 4     | s                              | s                                    |


