# SETUP
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# CARGA DE DATOS
df = pd.read_csv('dataset_inquilinos.csv', index_col='id_inquilino')

df.columns = [
        'Wake Up Time', 'Bed Time', 'Pray Frequency', 'Pray Time', 'Start Day With',
    'Study/Work Time', 'Diet Type', 'Food Allergies', 'Cuisine Type',
    'Profession/Field of Study', 'Hobbies/Interests', 'Free Time Spent',
    'Environment Preference', 'Social Events Attendance', 'Tidiness',
    'Sharing Personal Items', 'Room Temperature Preference'
]

# ONE HOT ENCODING
# Realizar el one-hot encoding para convertir categorías en variables binarias
encoder = OneHotEncoder(sparse=False)
df_encoded = encoder.fit_transform(df)
encoded_feature_names = encoder.get_feature_names_out()  # Nombres de características después del encoding

# MATRIZ DE SIMILARIDAD
# Calcular la matriz de similaridad usando producto punto
matriz_s = np.dot(df_encoded, df_encoded.T)

# Escala de la matriz para valores entre -100 y 100
rango_min, rango_max = -100, 100
min_original, max_original = np.min(matriz_s), np.max(matriz_s)
matriz_s_reescalada = ((matriz_s - min_original) / (max_original - min_original)) * (rango_max - rango_min) + rango_min

# Convertir a DataFrame para fácil manipulación
df_similaridad = pd.DataFrame(matriz_s_reescalada, index=df.index, columns=df.index)

# FUNCIÓN PARA ENCONTRAR INQUILINOS COMPATIBLES
def inquilinos_compatibles(id_inquilinos, topn):
    """
    Encuentra inquilinos compatibles basados en similaridad.
    
    Args:
    - id_inquilinos (list): IDs de los inquilinos actuales.
    - topn (int): Número de inquilinos compatibles a buscar.
    
    Returns:
    - tuple: Contiene dos elementos, un DataFrame con las características de los inquilinos compatibles
             y una Serie con los datos de similaridad.
    """
    # Verificar existencia de IDs de inquilinos
    if not set(id_inquilinos).issubset(df_similaridad.index):
        return 'Al menos uno de los inquilinos no encontrado'

    # Calcular similaridad promedio
    filas_inquilinos = df_similaridad.loc[id_inquilinos]
    similitud_promedio = filas_inquilinos.mean(axis=0)
    inquilinos_similares = similitud_promedio.sort_values(ascending=False).drop(id_inquilinos)

    # Seleccionar los topn más similares, excluyendo los ya presentes
    topn_inquilinos = inquilinos_similares.head(topn)
    registros_similares = df.loc[topn_inquilinos.index]

    # Combinar datos de inquilinos actuales y similares
    registros_buscados = df.loc[id_inquilinos]
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)

    # Serie de similaridad para los inquilinos seleccionados
    similitud_series = pd.Series(topn_inquilinos.values, index=topn_inquilinos.index, name='Similitud')

    return (resultado, similitud_series)
