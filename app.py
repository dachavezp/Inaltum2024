import streamlit as st
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

st.set_page_config(layout="wide")
st.image('./Media/portada.png', use_column_width=True)
st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Por favor indicar el código de participante de las personas ya confirmadas en la habitación")
    inquilino1 = st.text_input("Inquilino 1 (opcional)")
    inquilino2 = st.text_input("Inquilino 2 (opcional)")
    inquilino3 = st.text_input("Inquilino 3 (opcional)")
    
    if st.button('Buscar nuevos compañeros'):
        id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3)
        if id_inquilinos:
            topn = 4 - len(id_inquilinos)  # Calculate how many more roommates to find
            resultado = inquilinos_compatibles(id_inquilinos, topn)
            if isinstance(resultado, str):
                st.error(resultado)
            elif resultado is not None:
                cols = st.columns((1, 2))
                with cols[0]:
                    st.write("Nivel de compatibilidad de cada nuevo compañero:")
                    fig_grafico = generar_grafico_compatibilidad(resultado[1])
                    st.pyplot(fig_grafico)
                with cols[1]:
                    st.write("Comparativa entre compañeros:")
                    fig_tabla = generar_tabla_compatibilidad(resultado)
                    st.plotly_chart(fig_tabla, use_container_width=True)