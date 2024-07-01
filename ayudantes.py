import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

# FUNCTION TO GENERATE COMPATIBILITY GRAPH
def generate_compatibility_chart(compatibility):
    if compatibility.empty:
        st.error("Compatibility data is empty.")
        return None

    compatibility = compatibility / 100  # Scale to 0-1 for percentage

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=compatibility.index, y=compatibility.values, ax=ax, palette='Blues_d')
    sns.despine(top=True, right=True, left=False, bottom=False)
    
    ax.set_xlabel('Tenant Identifier', fontsize=12)
    ax.set_ylabel('Similarity (%)', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(['{:.0f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=10)
    
    for p in ax.patches:
        height = p.get_height()
        ax.annotate('{:.0f}%'.format(height * 100),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 10),
                    textcoords='offset points', fontsize=10)
    
    plt.title('Tenant Compatibility Chart', fontsize=14)
    st.pyplot(fig)  # Show the plot in Streamlit

# FUNCTION TO GENERATE COMPATIBILITY TABLE
def generate_compatibility_table(results):
    if results[0].empty:
        st.error("Results data is empty.")
        return None

    results_with_index = results[0].reset_index()
    results_with_index.rename(columns={'index': 'Attribute'}, inplace=True)
    
    fig_table = go.Figure(data=[go.Table(
        columnwidth = [180] + [120] * (len(results_with_index.columns) - 1),
        header=dict(values=list(results_with_index.columns), fill_color='brown', align='left', font=dict(color='white')),
        cells=dict(values=[results_with_index[col] for col in results_with_index.columns], fill_color='lightblue', align='left'))
    ])
    
    fig_table.update_layout(
        width=800, height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        title='Detailed Tenant Compatibility Table'
    )
    
    st.plotly_chart(fig_table)  # Show the table in Streamlit

# FUNCTION TO OBTAIN SEED TENANT IDS
def get_tenant_ids(*tenants):
    tenant_ids = []
    for tenant in tenants:
        if tenant:  # Check if the input is non-empty
            try:
                tenant_ids.append(int(tenant))
            except ValueError:
                st.error(f"The identifier '{tenant}' is not a valid number.")
                return []
    return tenant_ids
