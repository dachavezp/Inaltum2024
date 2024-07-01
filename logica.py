# logica.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def load_and_process_data(filepath='dataset_inquilinos.csv'):
    df = pd.read_csv(filepath, index_col='id_inquilino')
    
    # Verificar la cantidad de columnas
    expected_columns = [
        'WakeUpTime', 'BedTime', 'PrayFrequency', 'PrayTime', 'StartDayWith', 
        'StudyWorkTime', 'DietType', 'FoodAllergies', 'CuisineType', 'ProfessionField', 
        'HobbiesInterests', 'FreeTimeSpent', 'EnvironmentPreference', 'SocialEvents', 
        'Tidiness', 'SharingItems', 'RoomTemperature', 'MusicPreference', 'MusicFrequency', 
        'RelaxationPreference'
    ]

    if len(df.columns) != len(expected_columns):
        raise ValueError(f"El archivo CSV debe tener exactamente {len(expected_columns)} columnas: {expected_columns}")

    # Actualizar nombres de columnas
    df.columns = expected_columns

    # Convertir todas las columnas a tipo string
    df = df.astype(str)

    # Mostrar los tipos de datos de cada columna para verificar
    st.write("Tipos de datos de cada columna:", df.dtypes)

    # Verificar que los datos sean válidos para el OneHotEncoder
    if not all(df.dtypes == object):
        raise ValueError("Todos los datos deben ser de tipo string (object) para el OneHotEncoder.")

    # Realizar el one-hot encoding
    encoder = OneHotEncoder(sparse_output=False)
    df_encoded = encoder.fit_transform(df)

    return df, df_encoded

def calculate_similarity(df_encoded):
    # Calcular la matriz de similaridad utilizando el producto punto
    matriz_s = np.dot(df_encoded, df_encoded.T)

    # Definir el rango de destino
    rango_min = -100
    rango_max = 100

    # Encontrar el mínimo y máximo valor en matriz_s
    min_original = np.min(matriz_s)
    max_original = np.max(matriz_s)

    # Reescalar la matriz
    matriz_s_reescalada = ((matriz_s - min_original) / (max_original - min_original)) * (rango_max - rango_min) + rango_min

    # Convertir a Pandas DataFrame
    return pd.DataFrame(matriz_s_reescalada, index=df.index, columns=df.index)

def inquilinos_compatibles(id_inquilinos, topn):
    df, df_encoded = load_and_process_data()
    df_similarity = calculate_similarity(df_encoded)
    
    # Verificar si todos los ID de inquilinos existen en la matriz de similaridad
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df_similarity.index:
            return 'Al menos uno de los inquilinos no encontrado'

    # Obtener las filas correspondientes a los inquilinos dados
    filas_inquilinos = df_similarity.loc[id_inquilinos]

    # Calcular la similitud promedio entre los inquilinos
    similitud_promedio = filas_inquilinos.mean(axis=0)

    # Ordenar los inquilinos en función de su similitud promedio
    inquilinos_similares = similitud_promedio.sort_values(ascending=False)

    # Excluir los inquilinos de referencia (los que están en la lista)
    inquilinos_similares = inquilinos_similares.drop(id_inquilinos)

    # Tomar los topn inquilinos más similares
    topn_inquilinos = inquilinos_similares.head(topn)

    # Obtener los registros de los inquilinos similares
    registros_similares = df.loc[topn_inquilinos.index]

    # Obtener los registros de los inquilinos buscados
    registros_buscados = df.loc[id_inquilinos]

    # Concatenar los registros buscados con los registros similares en las columnas
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)

    # Crear un objeto Series con la similitud de los inquilinos similares encontrados
    similitud_series = pd.Series(data=topn_inquilinos.values, index=topn_inquilinos.index, name='Similitud')

    # Devolver el resultado y el objeto Series
    return resultado, similitud_series
print(df)