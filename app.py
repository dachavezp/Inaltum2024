import streamlit as st
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

# Configure the page to use a wider layout.
st.set_page_config(layout="wide")

# Display a large image at the top.
st.image('./Media/portada.png', use_column_width=True)

# Insert a vertical space of 60px.
st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Configure the sidebar with inputs and a button.
with st.sidebar:
    st.header("¿Quién está viviendo ya en el piso?")
    inquilino1 = st.text_input("Inquilino 1 (opcional)")
    inquilino2 = st.text_input("Inquilino 2 (opcional)")
    inquilino3 = st.text_input("Inquilino 3 (opcional)")
    
    if st.button('BUSCAR NUEVOS COMPAÑEROS'):
        # Obtain tenant identifiers using the function
        id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3)

        # Calculate how many more roommates to find to make up a group of 4
        if id_inquilinos:
            topn = 4 - len(id_inquilinos)
            if topn > 0:
                resultado = inquilinos_compatibles(id_inquilinos, topn)
            else:
                st.error("Ya has introducido 4 inquilinos, no se necesitan más.")

# Check if 'resultado' contains an error message (string)
if isinstance(resultado, str):
    st.error(resultado)
# If not, and if 'resultado' is not None, display the bar graph and the table
elif resultado is not None:
    cols = st.columns((1, 2))  # Split the layout into 2 columns
    
    with cols[0]:  # This makes the graph and its title appear in the first column
        st.write("Nivel de compatibilidad de cada nuevo compañero:")
        fig_grafico = generar_grafico_compatibilidad(resultado[1])
        st.pyplot(fig_grafico)
    
    with cols[1]:  # This makes the table and its title appear in the second column
        st.write("Comparativa entre compañeros:")
        fig_tabla = generar_tabla_compatibilidad(resultado)
        st.plotly_chart(fig_tabla, use_container_width=True)
