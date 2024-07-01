import streamlit as st
import pandas as pd
from logica import find_compatible_tenants, load_and_process_data, calculate_similarity
from ayudantes import generate_compatibility_chart, generate_compatibility_table, get_tenant_ids

# Set up the page using a wider layout.
st.set_page_config(layout="wide")

# Display a header image.
st.image('./Media/portada.png', use_column_width=True)

# Add some vertical space.
st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Set up sidebar for input.
with st.sidebar:
    st.header("Please provide the participant code(s) already confirmed for the room:")
    participant1 = st.text_input("Participant 1 (required)", key='p1')
    participant2 = st.text_input("Participant 2 (optional)", key='p2')
    participant3 = st.text_input("Participant 3 (optional)", key='p3')
    
    if st.button('Search for new roommate(s)'):
        tenant_ids = get_tenant_ids(participant1, participant2, participant3)
        if tenant_ids:
            topn = 4 - len(tenant_ids)  # Calculate how many more roommates to find
            if topn > 0:
                df, df_encoded = load_and_process_data('dataset_inquilinos.csv')
                df_similarity = calculate_similarity(df_encoded)
                results = find_compatible_tenants(df_similarity, tenant_ids, topn)
                if isinstance(results, str):  # Check if the function returned an error message.
                    st.error(results)
                else:
                    result, similarity_series = results
            else:
                st.error("Maximum number of participants reached. No additional roommates needed.")

# Check results and display outside of the sidebar in the main body.
if 'result' in locals() and result:
    # Create columns for layout
    cols = st.columns((1, 2))
    with cols[0]:
        st.write("Compatibility level of each new roommate:")
        fig_graph = generate_compatibility_chart(similarity_series)
        st.pyplot(fig_graph)
    with cols[1]:
        st.write("Comparison between roommates:")
        fig_table = generate_compatibility_table(result)
        st.plotly_chart(fig_table, use_container_width=True)
