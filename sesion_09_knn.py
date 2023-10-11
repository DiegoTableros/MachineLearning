# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:48:47 2023

@author: hp
"""

'''
###############################################################################
################                                          #####################
################              Algoritmos knn              #####################
################                                          #####################
###############################################################################
'''


import os
import pandas as pd
import numpy as np
from siuba import *
from siuba.dply.vector import * 
from plotnine import *


#%%

os.chdir("C:\\Users\\diego\\Desktop\\MachineLearning")
mi_data = pd.read_csv("datos_peliculas.csv")

#%%

mi_data.head()
mi_data.columns
mi_data.shape

peliculas = mi_data >> select(_.pelicula)
mi_data = mi_data >> select(-_.pelicula)

#%%

from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

#%%
'''
CLASIFICACIÓN

Probamos KNN para clasificación; en concreto vamos a suponer que queremos 
predecir el género de una película en función de las otras columnas
'''

sorted(mi_data["genero"].unique())

mi_data.shape

#Seleccionamos la columna de GENERO, que es la que queremos predecir
variable_objetivo_clasificacion = mi_data >> select(_.genero)
#Seleccionamos todas las columnas MENOS la que queremos predecir, de los datos
variables_independientes_clasificacion = mi_data >> select(-_.genero)

#DIVIDIR EN ENTRENAMIENTO Y PRUEBA
X_train, X_test, y_train, y_test = train_test_split(
    variables_independientes_clasificacion,
    variable_objetivo_clasificacion, test_size=0.20,random_state=2023)

#Mostrar los datos GENERO de la sección de ENTRENAMIENTO
sorted(y_train["genero"].unique())

'''Utilizando pesos uniformes'''
#CONSTRUCTOR DEL CLASIFICADOR con el entrenamiento
clasificador_knn_uniforme = KNeighborsClassifier(n_neighbors=3, weights="uniform")
clasificador_knn_uniforme.fit(X_train, y_train["genero"])

#Calcular las predicciones con el clasificador
preds_uniforme = clasificador_knn_uniforme.predict(X_test)
#Average MICRO por multiclase
#Calculo del f1 entre los datos reales y los predichos
f1_score(y_test, preds_uniforme, average="micro")

'''Utilizando pesos = "distancias" '''
#CONSTRUCTOR DEL CLASIFICADOR con el entrenamiento
clasificador_knn_distancias = KNeighborsClassifier(n_neighbors=100, weights="distance")
clasificador_knn_distancias.fit(X_train, y_train["genero"])

preds_distancias = clasificador_knn_distancias.predict(X_test)
f1_score(y_test, preds_distancias, average="micro")

#%%
'''Selección de k'''

def clasificadores_knn(k):
    knn_uniforme = KNeighborsClassifier(n_neighbors=k, weights="uniform")
    knn_distancias = KNeighborsClassifier(n_neighbors=k, weights="distance")
    knn_uniforme.fit(X_train, y_train["genero"])
    knn_distancias.fit(X_train, y_train["genero"])
    preds_uniforme = knn_uniforme.predict(X_test)
    preds_distancias = knn_distancias.predict(X_test)
    f1_uniforme = f1_score(y_test, preds_uniforme, average="micro")
    f1_distancias = f1_score(y_test, preds_distancias, average="micro")
    return (k,f1_uniforme,f1_distancias)

clasificacion_evaluaciones =[ clasificadores_knn(k) for k in range(1,151,2)]

clasificacion_evaluaciones = pd.DataFrame(clasificacion_evaluaciones,
                                          columns = ["k","F1_uniforme","F1_distancias"])
#%%
clasificaciones_evaluaciones_tidy = clasificacion_evaluaciones >> gather("F1_tipo",
                                                                         "F1_score",
                                                                         -_.k)

(ggplot(data = clasificaciones_evaluaciones_tidy) +
    geom_point(mapping=aes(x="k",y="F1_score",color="F1_tipo")) +
    geom_line(mapping=aes(x="k",y="F1_score",color="F1_tipo"))
)


(ggplot(data = clasificacion_evaluaciones) +
    geom_point(mapping=aes(x="k",y="F1_uniforme"),color = "red") +
    geom_line(mapping=aes(x="k",y="F1_uniforme"),color = "red") +
    geom_point(mapping=aes(x="k",y="F1_distancias"),color = "blue") +
    geom_line(mapping=aes(x="k",y="F1_distancias"),color = "blue")
)

mi_data.shape[0]**0.5

(clasificacion_evaluaciones >> 
    filter((_.F1_uniforme == _.F1_uniforme.max()) | (_.F1_distancias == _.F1_distancias.max()))
)

#%%

'''Utilizando pesos uniformes'''
mejor_clasificador_knn_uniforme = KNeighborsClassifier(n_neighbors=15, weights="uniform")
mejor_clasificador_knn_uniforme.fit(X_train, y_train["genero"])

mejor_preds_uniforme = mejor_clasificador_knn_uniforme.predict(X_test)
f1_score(y_test, mejor_preds_uniforme, average="micro")

'''Utilizando pesos = "distancias" '''
mejor_clasificador_knn_distancias = KNeighborsClassifier(n_neighbors=7, weights="distance")
mejor_clasificador_knn_distancias.fit(X_train, y_train["genero"])

mejor_preds_distancias = mejor_clasificador_knn_distancias.predict(X_test)
f1_score(y_test, mejor_preds_distancias, average="micro")

#%%









