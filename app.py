import streamlit as st
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

# Set up the page using a wider layout.
st.set_page_config(layout="wide")

# Display a header image.
st.image('./Media/portada.png', use_column_width=True)

# Add some vertical space.
st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Set up sidebar for input.
with st.sidebar:
    st.header("Please provide the participant code(s) already confirmed for the room:")
    inquilino1 = st.text_input("Participant 1 (required)", key='p1')
    inquilino2 = st.text_input("Participant 2 (optional)", key='p2')
    inquilino3 = st.text_input("Participant 3 (optional)", key='p3')
    
    if st.button('Search for new roommate(s)'):
        id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3)
        if id_inquilinos:
            topn = 4 - len(id_inquilinos)  # Calculate how many more roommates to find
            if topn > 0:
                resultado, similitud_series = inquilinos_compatibles(id_inquilinos, topn)
            else:
                st.error("Maximum number of participants reached. No additional roommates needed.")

# Check results and display outside of the sidebar in the main body.
if 'resultado' in locals() and resultado:
    if isinstance(resultado, str):
        st.error(resultado)
    else:
        # Create columns for layout
        cols = st.columns((1, 2))
        with cols[0]:
            st.write("Compatibility level of each new roommate:")
            fig_grafico = generar_grafico_compatibilidad(similitud_series)
            st.pyplot(fig_grafico)
        with cols[1]:
            st.write("Comparison between roommates:")
            fig_tabla = generar_tabla_compatibilidad(resultado)
            st.plotly_chart(fig_tabla, use_container_width=True)
