from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import re
import sys

def main(input_path, output_path, iterations, partitioning):
    # Initialiser la session Spark
    spark = SparkSession.builder \
        .appName("PageRankDataFrame") \
        .getOrCreate()

    # Charger les données depuis Google Cloud Storage
    lines = spark.read.text(input_path)

    # Fonction pour parser les voisins
    def parseNeighbors(urls):
        parts = re.split(r'\s+', urls)
        return parts[0], parts[2]

    # Créer un DataFrame de liens
    links_rdd = lines.rdd.map(lambda urls: parseNeighbors(urls[0])).distinct()
    links_df = links_rdd.toDF(["url", "neighbor"]).groupBy("url") \
        .agg(F.collect_list("neighbor").alias("neighbors"))

    # Initialiser les rangs
    ranks_df = links_df.select("url").withColumn("rank", F.lit(1.0))

    # Algorithme PageRank
    for i in range(iterations):
        contribs_df = links_df.join(ranks_df, "url") \
            .withColumn("contrib", F.expr("transform(neighbors, x -> rank / size(neighbors))")) \
            .select(F.explode(F.col("contrib")).alias("neighbor"), F.col("url"), F.col("rank")) \
            .groupBy("neighbor").agg(F.sum("rank").alias("total_contrib"))

        # Calculer les nouveaux rangs
        ranks_df = contribs_df.withColumn("rank", (F.col("total_contrib") * 0.85 + 0.15)).withColumnRenamed("neighbor", "url")

    # Enregistrer les résultats dans un format Parquet avec partitionnement par URL
    if partitioning == "by-url":
        ranks_df.write \
            .partitionBy("url") \
            .format("parquet") \
            .save(output_path)
    elif partitioning == "default":
        ranks_df.coalesce(1).write \
            .format("parquet") \
            .save(output_path)

    # Arrêter la session Spark
    spark.stop()

if __name__ == "__main__":
    # Lire les arguments de la ligne de commande
    input_path = sys.argv[1]  # Chemin vers le fichier de données
    output_path = sys.argv[2]  # Chemin pour enregistrer les résultats
    iterations = int(sys.argv[3])  # Nombre d'itérations
    partitioning = sys.argv[4]  # Type de partitionnement
    main(input_path, output_path, iterations, partitioning)
