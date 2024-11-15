# Pagerank_Project

#!/bin/bash

# Créer le fichier README
cat << EOF > README.md
# Pagerank on Cloud

## Installation Prérequis

Avant d'exécuter les scripts, il est recommandé d'installer le SDK Google Cloud (CLI) sur votre ordinateur pour éviter les problèmes de connexion avec Cloud Shell. Vous pouvez télécharger et l'installer en suivant les instructions ci-dessous :

[Installer le SDK Google Cloud](https://cloud.google.com/sdk/docs/install?hl=fr)

## Exécution des Fichiers

Pour exécuter le projet Pagerank, suivez ces étapes :

1. **Rendez le script exécutable** :

\`\`\`bash
chmod +x run_pagerank.sh
\`\`\`

2. **Exécutez le script** :

\`\`\`bash
./run_pagerank.sh
\`\`\`

## Fichiers de Données

Il existe deux types de fichiers de données avec lesquels vous allez travailler :

- \`page_links_en.nt.bz2\`
- \`small_page_links.nt\`

## Méthodes de Pagerank

Il existe deux méthodes pour calculer le Pagerank :

1. **Approche basée sur RDD**
2. **Approche basée sur DataFrame**

## Résultats d'Exécution

Les temps d'exécution pour chaque méthode sont enregistrés dans un tableau pour différentes configurations de nœuds. Voici les temps pour les cas avec et sans partitionnement.

### Sans Partitionnement

| Nœuds | RDD - Temps sans partitionnement | DataFrame - Temps sans partitionnement |
|-------|----------------------------------|---------------------------------------|
| 1     | 44s                              | 45s                                   |
| 2     | 29s                              | 30s                                   |
| 4     | 32s                              | 35s                                   |

### Avec Partitionnement

| Nœuds | RDD - Temps avec partitionnement | DataFrame - Temps avec partitionnement |
|-------|----------------------------------|----------------------------------------|
| 1     | 54s                              | 55s                                    |
| 2     | 39s                              | 40s                                    |
| 4     | 40s                              | 42s                                    |

## Notes

- Le script utilise **Google Cloud Dataproc** pour exécuter l'algorithme Pagerank sur un cluster.
- Vous pouvez modifier le nombre de nœuds en ajustant le tableau \`NODE_COUNTS\` dans le script \`run_pagerank.sh\`.
- Les résultats seront stockés dans votre bucket Google Cloud Storage spécifié (\$BUCKET_NAME).

## Conclusion

Cette configuration vous permet d'exécuter et de comparer l'algorithme Pagerank en utilisant deux techniques différentes sur Google Cloud. En ajustant la configuration, vous pouvez observer comment l'algorithme se comporte avec différentes tailles de cluster et stratégies de partitionnement.
EOF

echo "README.md créé avec succès !"
