#data cleaning script
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
