import streamlit as st
import pandas as pd
from logica import find_compatible_tenants, load_and_process_data, calculate_similarity
from ayudantes import generate_compatibility_chart, generate_compatibility_table, get_tenant_ids

# Configurar la página para utilizar un layout más amplio.
st.set_page_config(layout="wide")

resultado = None

# Mostrar una gran imagen en la parte superior.
st.image('./Media/portada.png', use_column_width=True)

# Insertar un espacio vertical de 60px
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Configurar el sidebar con inputs y un botón.
with st.sidebar:
    st.header("¿Quién está viviendo ya en el piso?")
    inquilino1 = st.text_input("Inquilino 1")
    inquilino2 = st.text_input("Inquilino 2")
    inquilino3 = st.text_input("Inquilino 3")
    
    if st.button('BUSCAR NUEVOS COMPAÑEROS'):
        topn = 4  # Número fijo de nuevos compañeros de habitación
        # Obtener los identificadores de inquilinos utilizando la función
        id_inquilinos = get_tenant_ids(inquilino1, inquilino2, inquilino3)

        if id_inquilinos:
            # Llama a la función find_compatible_tenants con los parámetros correspondientes
            df, df_encoded = load_and_process_data('dataset_inquilinos.csv')
            df_similarity = calculate_similarity(df_encoded)
            result, similarity_series = find_compatible_tenants(df, df_similarity, id_inquilinos, topn)
            if isinstance(result, str):
                st.error(result)
            else:
                resultado = (result, similarity_series)

# Verificar si 'resultado' contiene un mensaje de error (cadena de texto)
if isinstance(resultado, str):
    st.error(resultado)
# Si no, y si 'resultado' no es None, mostrar el gráfico de barras y la tabla
elif resultado is not None:
    cols = st.columns((1, 2))  # Divide el layout en 2 columnas
    
    with cols[0]:  # Esto hace que el gráfico y su título aparezcan en la primera columna
        st.write("Nivel de compatibilidad de cada nuevo compañero:")
        fig_grafico = generate_compatibility_chart(resultado[1])
        st.pyplot(fig_grafico)
    
    with cols[1]:  # Esto hace que la tabla y su título aparezcan en la segunda columna
        st.write("Comparativa entre compañeros:")
        fig_tabla = generate_compatibility_table(resultado)
        st.plotly_chart(fig_tabla, use_container_width=True)
