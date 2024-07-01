import streamlit as st
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

st.set_page_config(layout="wide")
st.image('./Media/top_image.png', use_column_width=True)
st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Please provide the participant code(s) already confirmed for the room:")
    inquilino1 = st.text_input("Participant 1 (required)")
    inquilino2 = st.text_input("Participant 2 (optional)")
    inquilino3 = st.text_input("Participant 3 (optional)")
    
    if st.button('Search for new roommate(s)'):
        id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3)
        if id_inquilinos:
            topn = 4 - len(id_inquilinos)  # Calculate how many more roommates to find
            result = inquilinos_compatibles(id_inquilinos, topn)

# Check results and display outside of the sidebar in the main body.
if 'result' in locals() and not result.empty:
    if isinstance(result, str):
        st.error(result)
    else:
        cols = st.columns((1, 2))
        with cols[0]:
            st.write("Compatibility level of each new roommate:")
            fig_grafico = generar_grafico_compatibilidad(result[1])
            st.pyplot(fig_grafico)
        with cols[1]:
            st.write("Comparison between roommates:")
            fig_tabla = generar_tabla_compatibilidad(result)
            st.plotly_chart(fig_tabla, use_container_width=True)
