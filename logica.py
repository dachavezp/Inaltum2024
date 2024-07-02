import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Load and prepare data
df = pd.read_csv('dataset_inquilinos.csv', index_col='id_inquilino')
df.columns = [
    'horario', 'bioritmo', 'nivel_educativo', 'leer', 'animacion',
    'cine', 'mascotas', 'cocinar', 'deporte', 'dieta', 'fumador',
    'visitas', 'orden', 'musica_tipo', 'musica_alta', 'plan_perfecto', 'instrumento'
]

# One-hot encoding
encoder = OneHotEncoder(sparse=False)
df_encoded = encoder.fit_transform(df)
encoded_feature_names = encoder.get_feature_names_out()

# Similarity matrix
matriz_s = np.dot(df_encoded, df_encoded.T)
min_original = np.min(matriz_s)
max_original = np.max(matriz_s)
rango_min, rango_max = -100, 100
matriz_s_reescalada = ((matriz_s - min_original) / (max_original - min_original)) * (rango_max - rango_min) + rango_min
df_similaridad = pd.DataFrame(matriz_s_reescalada, index=df.index, columns=df.index)

# Function to find compatible tenants
def inquilinos_compatibles(id_inquilinos):
    # Verify each ID in the similarity matrix
    if not set(id_inquilinos).issubset(df_similaridad.index):
        return "At least one of the tenants was not found", None
    
    # Get rows for the given tenants
    filas_inquilinos = df_similaridad.loc[id_inquilinos]

    # Calculate average similarity
    similitud_promedio = filas_inquilinos.mean(axis=0)

    # Sort tenants based on average similarity and exclude known tenants
    topn = 4 - len(id_inquilinos)  # Determine how many more tenants are needed
    inquilinos_similares = similitud_promedio.drop(id_inquilinos).sort_values(ascending=False).head(topn)

    # Get records for similar and existing tenants
    registros_similares = df.loc[inquilinos_similares.index]
    registros_buscados = df.loc[id_inquilinos]

    # Concatenate results
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)
    similitud_series = pd.Series(data=inquilinos_similares.values, index=inquilinos_similares.index, name='Similitud')

    return resultado, similitud_series

