# logica.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def load_and_process_data(filepath):
    df = pd.read_csv(filepath, index_col='id_inquilino')
    df.columns = [
        'WakeUpTime', 'BedTime', 'PrayFrequency', 'PrayTime', 'StartDayWith', 
        'StudyWorkTime', 'DietType', 'FoodAllergies', 'CuisineType', 'ProfessionField', 
        'HobbiesInterests', 'FreeTimeSpent', 'EnvironmentPreference', 'SocialEvents', 
        'Tidiness', 'SharingItems', 'RoomTemperature', 'MusicPreference', 'MusicFrequency', 
        'RelaxationPreference'
    ]
    encoder = OneHotEncoder(sparse_output=False)
    df_encoded = encoder.fit_transform(df)
    return df, df_encoded

def calculate_similarity(df_encoded):
    similarity_matrix = np.dot(df_encoded, df_encoded.T)
    range_min, range_max = 0, 100
    min_original = np.min(similarity_matrix)
    max_original = np.max(similarity_matrix)
    rescaled_matrix = ((similarity_matrix - min_original) / (max_original - min_original)) * (range_max - range_min)
    return pd.DataFrame(rescaled_matrix)

def find_compatible_tenants(df_similarity, tenant_ids, topn):
    missing_ids = [id for id in tenant_ids if id not in df_similarity.index]
    if missing_ids:
        return f'The following tenant IDs were not found: {missing_ids}', None

    tenant_rows = df_similarity.loc[tenant_ids]
    average_similarity = tenant_rows.mean(axis=0)
    similar_tenants = average_similarity.sort_values(ascending=False).drop(tenant_ids)
    top_tenants = similar_tenants.head(topn)
    similar_records = df.loc[top_tenants.index]
    searched_records = df.loc[tenant_ids]
    result = pd.concat([searched_records.T, similar_records.T], axis=1)
    similarity_series = pd.Series(data=top_tenants.values, index=top_tenants.index, name='Similarity')

    return result, similarity_series
