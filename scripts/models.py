#training models for the project and saving the model

#Libairies
from sklearn.preprocessing import LabelEncoder
from kmodes.kprototypes import KPrototypes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import re
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('EXPERT_COMPTABLE_AVANT_DERNIER.csv')

def percentage_ebitda(x,y):
    return (y*100/x)

df['EBITDA %'] = percentage_ebitda(df['CA'],df['ebitda'])

test = df[['age','city','nb_employe (pappers)','nb_EC','EBITDA %']]
test.dropna(inplace=True)

def moyenne_nombre_employes(text):
    # Utiliser une expression régulière pour trouver tous les nombres dans le texte
    nombres = re.findall(r'\d+', text)
    
    # Convertir les résultats de texte à entier
    nombres = [int(n) for n in nombres]
    
    # Calculer la moyenne si on a exactement deux nombres
    if len(nombres) == 2:
        return sum(nombres) / 2
    else:
        return nombres[0]
        
test['estimation employe'] = test['nb_employe (pappers)'].apply(moyenne_nombre_employes)
test.drop(columns='nb_employe (pappers)', inplace=True)

le = LabelEncoder()
test['city_encoded'] = le.fit_transform(test['city'])
y = test['EBITDA %']
x = test.drop(columns=['EBITDA %','city'])

# convert type in numeric
x = x.astype('float64')
x.info()
x.to_csv('data_clean.csv', index=False)

# KMEANS
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Standardisation des données
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# Calcul du coût pour différents nombres de clusters
costs = []
K = range(1, 10)
for k in K:
    kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
    kmeans.fit(x_scaled)
    # Le coût est le WCSS (Within-Cluster Sum of Square)
    costs.append(kmeans.inertia_)

# Visualisation des coûts
plt.figure(figsize=(8, 4))
plt.plot(K, costs, 'bx-')
plt.xlabel('Nombre de Clusters')
plt.ylabel('Coût (WCSS)')
plt.title('La Méthode du Coude pour Déterminer le Nombre Optimal de Clusters')
plt.show()

# kmeans with 5 clusters

kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42)
kmeans.fit(x_scaled)
clusters_kmeans = kmeans.predict(x_scaled)
test['cluster'] = clusters_kmeans

test['cluster'].value_counts()
test
# KMEANS prototypes
from kmodes.kprototypes import KPrototypes
costs = []
K = range(1, 10)  
x['city_encoded'] = x['city_encoded'].astype(int).astype('category')
x_array = x.values
categorical_indices= [1]

for k in K:
    kproto = KPrototypes(n_clusters=k, init='Cao', verbose=1)
    kproto.fit_predict(x_array, categorical=categorical_indices)
    costs.append(kproto.cost_)

# Visualisation des coûts
plt.figure(figsize=(8, 4))
plt.plot(K, costs, 'bx-')
plt.xlabel('Nombre de Clusters')
plt.ylabel('Coût (Distortion)')
plt.title('La Méthode du Coude pour Déterminer le Nombre Optimal de Clusters')
plt.show()
categorical_indices = [1]  
kproto = KPrototypes(n_clusters=3, init='Cao', verbose=2)
clusters_prototype = kproto.fit_predict(x_array, categorical=categorical_indices)
print("Centres des Clusters:\n", kproto.cluster_centroids_)
print("Affectations des clusters:", clusters_prototype)
test['cluster'] = clusters_prototype
test['cluster'].value_counts()
test
# DBSCAN
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# Normalisation des données - important pour DBSCAN
x_scaled = StandardScaler().fit_transform(x_array)

# Tester différents eps
eps_values = np.linspace(0.1, 2.0, 20)  # Vous pouvez ajuster ces valeurs
min_samples = 5  # Ajustez ce paramètre selon la densité attendue de vos données
silhouette_scores = []

for eps in eps_values:
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(x_scaled)
    # Calculer le coefficient de silhouette
    if len(set(labels)) > 1:  # Éviter de calculer si un seul cluster
        score = silhouette_score(x_scaled, labels)
        silhouette_scores.append(score)
    else:
        silhouette_scores.append(-1)  # Cas où il y a moins de 2 clusters valides

# Visualisation des coefficients de silhouette
plt.figure(figsize=(8, 4))
plt.plot(eps_values, silhouette_scores, 'bx-')
plt.xlabel('Valeur de Eps')
plt.ylabel('Score de Silhouette')
plt.title('Optimisation de DBSCAN par Score de Silhouette')
plt.show()


x_scaled = StandardScaler().fit_transform(x)

dbscan = DBSCAN(eps=1.80, min_samples=5)
clusters_dbscan = dbscan.fit_predict(x_scaled)

n_clusters = len(set(clusters_dbscan)) - (1 if -1 in clusters_dbscan else 0)

print(f'Nombre de clusters formés : {n_clusters}')
print(f'Points considérés comme bruit : {np.sum(clusters_dbscan == -1)}')

from scipy.spatial.distance import cdist

x_scaled_df = pd.DataFrame(x_scaled, index=x.index)  # Assurez-vous que les indices correspondent

# Application de DBSCAN
dbscan = DBSCAN(eps=1.80, min_samples=5)
clusters_dbscan = dbscan.fit_predict(x_scaled_df)

# Trouver les centroïdes réels (point le plus central de chaque cluster)
real_centroids = []
labels = np.unique(clusters_dbscan)

for label in labels:
    if label != -1:  # Exclure le bruit
        points_in_cluster = x_scaled_df[clusters_dbscan == label]
        # Calculer la distance entre tous les points du cluster
        pairwise_distances = cdist(points_in_cluster, points_in_cluster)
        # Somme des distances de chaque point à tous les autres points du cluster
        sum_distances = pairwise_distances.sum(axis=1)
        # Trouver l'indice du point qui a la somme des distances la plus faible
        centroid_index = np.argmin(sum_distances)
        # Trouver le centroïde correspondant dans le tableau original non normalisé
        real_centroids.append(x.loc[points_in_cluster.index[centroid_index]])

# Affichage des centroïdes
print("Centroïdes réels des clusters :")
for centroid in real_centroids:
    print(centroid)

test['cluster'] = clusters_dbscan
# Créer un DataFrame à partir de la liste des centroïdes
centroids_df = pd.DataFrame(real_centroids)
# Fusionner les centroïdes avec le DataFrame 'test' en utilisant les indices
# Assurez-vous que 'test' a un index qui peut être utilisé pour la fusion
test_centroids = test.loc[centroids_df.index]

test_centroids.sort_values(by='EBITDA %', ascending=False)
test['cluster'].value_counts()
test[test['cluster'] == 1]

# BEST IS KMEANS PROTOTYPE
