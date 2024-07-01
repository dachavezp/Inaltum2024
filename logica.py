# 1. SETUP
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# 2. CARGA DE DATOS
# Load the dataset
df = pd.read_csv('dataset_inquilinos.csv', index_col='id_inquilino')

# Rename columns to meaningful names
df.columns = [
    'WakeUpTime', 'BedTime', 'PrayFrequency', 'PrayTime', 'StartDayWith', 
    'StudyWorkTime', 'DietType', 'FoodAllergies', 'CuisineType', 'ProfessionField', 
    'HobbiesInterests', 'FreeTimeSpent', 'EnvironmentPreference', 'SocialEvents', 
    'Tidiness', 'SharingItems', 'RoomTemperature', 'MusicPreference', 'MusicFrequency', 
    'RelaxationPreference'
]

# 3. ONE HOT ENCODING
# Perform one-hot encoding
encoder = OneHotEncoder(sparse_output=False)
df_encoded = encoder.fit_transform(df)

# Get the names of the encoded features
encoded_feature_names = encoder.get_feature_names_out()

# 4. MATRIZ DE SIMILIARIDAD
# Compute the similarity matrix using dot product
matriz_s = np.dot(df_encoded, df_encoded.T)

# Define the target range
rango_min = -100
rango_max = 100

# Find the minimum and maximum values in matriz_s
min_original = np.min(matriz_s)
max_original = np.max(matriz_s)

# Rescale the matrix
matriz_s_reescalada = ((matriz_s - min_original) / (max_original - min_original)) * (rango_max - rango_min) + rango_min

# Convert to Pandas DataFrame
df_similaridad = pd.DataFrame(matriz_s_reescalada, index=df.index, columns=df.index)

# 5. BÚSQUEDA DE INQUILINOS COMPATIBLES
'''
Input:
* id_inquilinos: the current tenant(s) MUST BE A LIST even if it contains only one element
* topn: the number of compatible tenants to search for

Output:
List with 2 elements.
Element 0: the characteristics of the compatible tenants
Element 1: the similarity data
'''

def inquilinos_compatibles(id_inquilinos, topn):
    # Check if all tenant IDs exist in the similarity matrix
    for id_inquilino in id_inquilinos:
        if id_inquilino not in df_similaridad.index:
            return 'At least one of the tenants was not found'

    # Get the rows corresponding to the given tenants
    filas_inquilinos = df_similaridad.loc[id_inquilinos]

    # Calculate the average similarity between tenants
    similitud_promedio = filas_inquilinos.mean(axis=0)

    # Sort tenants based on average similarity
    inquilinos_similares = similitud_promedio.sort_values(ascending=False)

    # Exclude the reference tenants (the ones in the input list)
    inquilinos_similares = inquilinos_similares.drop(id_inquilinos)

    # Get the top n most similar tenants
    topn_inquilinos = inquilinos_similares.head(topn)

    # Get the records of the similar tenants
    registros_similares = df.loc[topn_inquilinos.index]

    # Get the records of the searched tenants
    registros_buscados = df.loc[id_inquilinos]

    # Concatenate the searched records with the similar records in columns
    resultado = pd.concat([registros_buscados.T, registros_similares.T], axis=1)

    # Create a Series object with the similarity of the found similar tenants
    similitud_series = pd.Series(data=topn_inquilinos.values, index=topn_inquilinos.index, name='Similitud')

    # Return the result and the Series object
    return resultado, similitud_series
