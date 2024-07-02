import streamlit as st
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

# Configurar la página para utilizar un layout más amplio.
st.set_page_config(layout="wide")

resultado = None

# Mostrar una gran imagen en la parte superior.
st.image('./Media/portada.png', use_column_width=True)

# Insertar un espacio vertical de 60px
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Configurar el sidebar con inputs y un botón.
with st.sidebar:
    st.header("Who is alredy in the house?")
    inquilino1 = st.text_input("Participant ID 1 (Required)")
    inquilino2 = st.text_input("Participant ID 2 (Optional)")
    inquilino3 = st.text_input("Participant ID 3 (Optional)")
    
    if st.button('Look for new mate'):
        # Verifica que al menos un inquilino haya sido introducido
        if not inquilino1:
            st.error("Introduce i ID please.")
        else:
            # Obtener los identificadores de inquilinos utilizando la función
            id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3)

            # Calcula cuántos nuevos compañeros se necesitan para llegar a 4
            num_presentes = len([i for i in [inquilino1, inquilino2, inquilino3] if i])
            topn = 4 - num_presentes

            if id_inquilinos and topn > 0:
                # Llama a la función inquilinos_compatibles con los parámetros correspondientes
                resultado = inquilinos_compatibles(id_inquilinos, topn)

# Verificar si 'resultado' contiene un mensaje de error (cadena de texto)
if isinstance(resultado, str):
    st.error(resultado)
# Si no, y si 'resultado' no es None, mostrar el gráfico de barras y la tabla
elif resultado is not None:
    cols = st.columns((1, 2))  # Divide el layout en 2 columnas
    
    with cols[0]:  # Esto hace que el gráfico y su título aparezcan en la primera columna
        st.write("Compatibility level among participants:")
        fig_grafico = generar_grafico_compatibilidad(resultado[1])
        st.pyplot(fig_grafico)
    
    with cols[1]:  # Esto hace que la tabla y su título aparezcan en la segunda columna
        st.write("Comparative between participants:")
        fig_tabla = generar_tabla_compatibilidad(resultado)
        st.plotly_chart(fig_tabla, use_container_width=True)
