#training models for the project and saving the model

#Libairies
from sklearn.preprocessing import LabelEncoder
from kmodes.kprototypes import KPrototypes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('EXPERT_COMPTABLE_AVANT_DERNIER.csv')

test['estimation employe'] = test['nb_employe (pappers)'].apply(moyenne_nombre_employes)

test.drop(columns='nb_employe (pappers)', inplace=True)


le = LabelEncoder()
test['city_encoded'] = le.fit_transform(test['city'])
x = test[['age','city_encoded','estimation employe','nb_EC']]
# convert type in numeric

x = x.astype('float64')
x.info()
x

costs = []
K = range(1, 10)  # Testez de 1 à 9 clusters, par exemple

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
clusters = kproto.fit_predict(x_array, categorical=categorical_indices)
print("Centres des Clusters:\n", kproto.cluster_centroids_)
print("Affectations des clusters:", clusters)
x
y = test['ebitda']
# regression lineaire 



x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)



regressor = LinearRegression()

regressor.fit(x_train, y_train)

y_pred = regressor.predict(x_test)


print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
print('R2 Score:', r2_score(y_test, y_pred))

