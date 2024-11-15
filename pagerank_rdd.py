from pyspark import SparkContext, SparkConf
import re
import sys

def parse_neighbors(urls):
    """Fonction pour analyser les voisins d'une page (URL)"""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[2]

def main(input_path, output_path, iterations, partitioning):
    """Fonction principale pour exécuter l'algorithme PageRank"""
    
    # Initialiser le SparkContext
    conf = SparkConf().setAppName("PageRankRDD")
    sc = SparkContext(conf=conf)

    # Charger les données depuis Google Cloud Storage
    lines = sc.textFile(input_path)

    # Créer un RDD de liens
    links = lines.map(parse_neighbors).distinct().groupByKey().mapValues(list)

    # Appliquer le partitionnement si nécessaire
    if partitioning == "by-url":
        # Partitionner les données par URL (10 partitions, ajustable)
        links = links.partitionBy(10, lambda x: hash(x[0]) % 10)
    elif partitioning == "default":
        # Réduire à une seule partition pour simplifier
        links = links.coalesce(1)

    # Initialiser les rangs avec la valeur 1.0
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    # Algorithme PageRank
    for _ in range(iterations):
        # Calculer les contributions à partir des voisins
        contribs = links.join(ranks).flatMap(
            lambda url_neighbors_rank: [
                (neighbor, url_neighbors_rank[1][1] / len(url_neighbors_rank[1][0])) 
                for neighbor in url_neighbors_rank[1][0]
            ]
        ).reduceByKey(lambda a, b: a + b)

        # Calculer les nouveaux rangs
        ranks = contribs.mapValues(lambda contrib: contrib * 0.85 + 0.15)

    # Trier les rangs par ordre décroissant pour les résultats finaux
    ranks_sorted = ranks.sortBy(lambda x: x[1], ascending=False)

    # Enregistrer les résultats dans un fichier texte dans Google Cloud Storage
    ranks_sorted.map(lambda row: f"{row[0]} has rank: {row[1]}").coalesce(1).saveAsTextFile(output_path)

    # Arrêter le SparkContext
    sc.stop()

if __name__ == "__main__":
    # Lire les arguments de la ligne de commande
    input_path = sys.argv[1]  # Chemin vers le fichier de données
    output_path = sys.argv[2]  # Chemin pour enregistrer les résultats
    iterations = int(sys.argv[3])  # Nombre d'itérations
    partitioning = sys.argv[4]  # Type de partitionnement ("by-url" ou "default")
    
    # Exécuter la fonction principale
    main(input_path, output_path, iterations, partitioning)
