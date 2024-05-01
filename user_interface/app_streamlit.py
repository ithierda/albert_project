import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from sklearn.decomposition import PCA
from kmodes.kprototypes import KPrototypes
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# Header
st.header("Albert Counting App")

st.image('/Users/ithierdaramon/Desktop/python/B2/projet_ml/albertcounting_logo.png', caption='logo')

# Introduction Text
st.markdown("""
Cette app va nous permettre de mieux comprendre notre clustering pour choisir notre meilleur bénéficiaire
""")


# Charger vos données, supposons que 'x' est déjà chargé avec vos données
df = pd.read_csv('/Users/ithierdaramon/Desktop/python/B2/projet_ml/EXPERT_COMPTABLE_AVANT_DERNIER.csv')

def percentage_ebitda(x,y):
    return (y*100/x)

df['EBITDA %'] = percentage_ebitda(df['CA'],df['ebitda'])

x = pd.read_csv('/Users/ithierdaramon/Desktop/python/B2/projet_ml/data_clean.csv')


test = df[['age','city','nb_employe (pappers)','nb_EC','EBITDA %']]
test.dropna(inplace=True)
import re

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
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
test['city_encoded'] = le.fit_transform(test['city'])
y = test['EBITDA %']
x = test.drop(columns=['EBITDA %','city'])
x = x.astype('float64')

costs = []
K = range(1, 10)  
x['city_encoded'] = x['city_encoded'].astype(int).astype('category')
x_array = x.values
categorical_indices= [1]

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x_array)

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
st.pyplot(plt)


# Effectuer le clustering avec le nombre optimal de clusters
categorical_indices = [1]  
kproto = KPrototypes(n_clusters=3, init='Cao', verbose=2)
clusters_prototype = kproto.fit_predict(x_array, categorical=categorical_indices)

# Afficher les résultats du clustering dans un DataFrame
result_df = pd.DataFrame({'Data Point': range(len(x)), 'Cluster': clusters_prototype})
st.subheader("Cluster Results")
st.write(result_df)


# Perform PCA to reduce the dimensionality to 2D
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)

# Plot the clusters on a scatter plot
optimal_num_clusters = 3
st.subheader("Cluster Visualization with K-Prototype and PCA")
plt.figure(figsize=(8, 6))
for cluster in range(optimal_num_clusters):
    plt.scatter(x_pca[clusters_prototype == cluster, 0], 
                x_pca[clusters_prototype == cluster, 1], 
                label=f'Cluster {cluster}', 
                alpha=0.5)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Visualization of Clusters with K-Prototype and PCA')
plt.legend()
st.pyplot(plt)


# Calcul des statistiques des clusters
test['cluster'] = clusters_prototype
median_ebitda_by_cluster = test.groupby('cluster')['EBITDA %'].median().sort_values(ascending=False)
st.subheader("Median EBITDA % by Cluster")
st.write(median_ebitda_by_cluster)

# Sélection des données pour le cluster choisi
df_cluster_choisi = test[test['cluster'] == 2]
st.subheader("Data for the Chosen Cluster")
st.write(df_cluster_choisi)


# Filtrer les données du cluster choisi selon les critères donnés
df_cluster_choisi = df_cluster_choisi[(df_cluster_choisi['EBITDA %'] < 100) & (df_cluster_choisi['EBITDA %'] > -100)]

# Afficher la distribution de la variable cible pour le cluster choisi
plt.figure(figsize=(10, 6))
sns.histplot(df_cluster_choisi['EBITDA %'], kde=True)
plt.title('Distribution de la variable cible')
plt.xlabel('EBITDA %')
plt.ylabel('Nombre de données')
st.pyplot(plt)
                  
region_parisienne = ['COURBEVOIE', 'ASNIERES-SUR-SEINE', 'EVRY', 'CHAMPS-SUR-MARNE',
       'DRAVEIL','BOULOGNE-BILLANCOURT', 'EVREUX', 'CLICHY', 'ARGENTEUIL',
       'ALFORTVILLE', 'COLOMBES', 'FONTAINEBLEAU', 'EAUBONNE',
       'ENGHIEN-LES-BAINS', 'ARPAJON',
       'ARCACHON', 'CHATILLON','ANTONY',
       'CHANTILLY', 'FONTENAY-SOUS-BOIS', 'BRETIGNY-SUR-ORGE',
       'EMERAINVILLE', 'EVRY-COURCOURONNES', 'ETAMPES',  'CHAMPIGNY-SUR-MARNE', 'BOISEMONT',
       'BOUGIVAL',
       'COURDIMANCHE-SUR-ESSONNE', 
       'BEAUVAIS', 'BESANCON', 'COLOMBE',
       'CERGY', 'BOULOGNE-SUR-MER', 
       'CHARENTON-LE-PONT', 
       'BRY-SUR-MARNE','BOIS-COLOMBES', 'DEUIL-LA-BARRE', 'BUSSY-SAINT-GEORGES',
       'BOIS-LE-ROI', 'AUBERVILLIERS',
       'BAILLY-ROMAINVILLIERS',
       'FRANCONVILLE', 'CHOISY-LE-ROI', 
       'BOURG-LA-REINE', 
       'ERMONT',  'CORMEILLES-EN-PARISIS',
       'AULNAY-SOUS-BOIS', 
       'BONDY', 'CRETEIL',
       'CHENNEVIERES-SUR-MARNE', 'CARRIERES-SUR-SEINE']

# Filtrer les données du cluster choisi pour les villes de la région parisienne avec un EBITDA % supérieur à 40
df_region_paris = df_cluster_choisi[df_cluster_choisi['city'].isin(region_parisienne)].sort_values(by='EBITDA %', ascending=False)
st.subheader("Data for Paris Region in the Chosen Cluster with EBITDA % > 40")
st.write(df_region_paris[df_region_paris['EBITDA %'] > 40])

# Afficher les informations des entreprises dans la région parisienne avec un EBITDA % supérieur à 40
st.subheader("Data for Companies in Paris Region in the Chosen Cluster with EBITDA % > 40")
st.write(df[(df['age'].isin(df_region_paris['age'])) & (df['city'].isin(region_parisienne)) & (df['EBITDA %'] > 40)])
