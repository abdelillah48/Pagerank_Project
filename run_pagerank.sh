#!/bin/bash

# Variables de configuration
PROJECT_ID="pagerank-441218"      # Remplacez par le ID de projet Google Cloud
REGION="europe-west1"              # Région pour Dataproc en France
BUCKET_NAME="pagerankbuck"       # Nom de bucket GCS
SCRIPT_PATH="gs://$BUCKET_NAME/pagerank_dataframe.py"  # Chemin vers le script PySpark
DATA_FILE="gs://public_lddm_data/small_page_links.nt"  # Chemin vers le fichier de données dans le bucket public
OUTPUT_PATH="gs://$BUCKET_NAME/pagerank_results"  # Chemin pour les résultats

# Liste des configurations de cluster (nombre de nœuds)
declare -a NODE_COUNTS=(1 2 4)  

# Supprimer les résultats précédents
rm -f execution_times.txt

# Boucle pour chaque configuration de nœuds
for NUM_NODES in "${NODE_COUNTS[@]}"; do
    for PARTITIONING in "by-url"; do  # Types de partitionnement
        CLUSTER_NAME="pagerank-cluster-${NUM_NODES}-${PARTITIONING}"  # Nom du cluster

        # Vérifier et supprimer le cluster s'il existe déjà
        if gcloud dataproc clusters describe "$CLUSTER_NAME" --region "$REGION" >/dev/null 2>&1; then
            echo "Le cluster $CLUSTER_NAME existe déjà. Suppression..."
            gcloud dataproc clusters delete "$CLUSTER_NAME" --region "$REGION" --quiet
        fi

        # Créer le cluster Dataproc
        if [[ "$NUM_NODES" -ge 2 ]]; then
            echo "Création du cluster $CLUSTER_NAME avec $NUM_NODES nœuds et partitionnement $PARTITIONING."
            gcloud dataproc clusters create "$CLUSTER_NAME" \
                --enable-component-gateway --region="$REGION" \
                --zone="$REGION-b" --master-machine-type="n1-standard-4" \
                --master-boot-disk-size=50 --master-boot-disk-type=pd-standard \
                --num-workers="$NUM_NODES" --public-ip-address \
                --worker-machine-type="n1-standard-4" --worker-boot-disk-size=50 \
                --worker-boot-disk-type=pd-standard \
                --image-version="2.0-debian10" \
                --project="$PROJECT_ID"
        else
            echo "Création du cluster $CLUSTER_NAME avec 1 nœud."
            gcloud dataproc clusters create "$CLUSTER_NAME" --single-node \
                --enable-component-gateway --region="$REGION" \
                --zone="$REGION-c" --master-machine-type="n1-standard-4" \
                --master-boot-disk-size=50 --master-boot-disk-type=pd-standard \
                --image-version="2.0-debian10" \
                --project="$PROJECT_ID" --public-ip-address
        fi

        # Vérifiez si le cluster a été créé avec succès
        if [ $? -ne 0 ]; then
            echo "Échec de la création du cluster $CLUSTER_NAME. Vérifiez les messages d'erreur ci-dessus."
            continue
        fi

        # Supprimer les résultats précédents dans le bucket
        echo "Suppression des résultats précédents à l'emplacement $OUTPUT_PATH/$PARTITIONING/*"
        gsutil -m rm -r gs://$BUCKET_NAME/pagerank_results/$PARTITIONING/*

        # Soumettre le job PySpark à Google Cloud Dataproc
        echo "Soumission du job PySpark au cluster $CLUSTER_NAME."
        start_time=$(date +%s)
        gcloud dataproc jobs submit pyspark "$SCRIPT_PATH" \
            --region="$REGION" \
            --cluster="$CLUSTER_NAME" \
            --properties="spark.executor.memory=8g,spark.executor.cores=4,spark.driver.memory=8g,spark.executor.memoryOverhead=4g" \
            --project="$PROJECT_ID" \
            -- "$DATA_FILE" "$OUTPUT_PATH/$PARTITIONING" 10 "$PARTITIONING"  # Passer le fichier de données, le chemin de sortie, le nombre d'itérations et le type de partitionnement
        end_time=$(date +%s)

        # Calcul et stockage du temps d'exécution
        echo "${NUM_NODES} nodes, Partitioning: $PARTITIONING, Execution time: $(($end_time - $start_time)) seconds" >> execution_times.txt

        # Supprimer le cluster après exécution
        echo "Suppression du cluster $CLUSTER_NAME."
        gcloud dataproc clusters delete "$CLUSTER_NAME" --region "$REGION" --quiet
    done
done
