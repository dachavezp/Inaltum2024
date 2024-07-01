# ayudantes.py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

def generate_compatibility_chart(compatibility_series):
    if compatibility_series.empty:
        st.error("Compatibility data is empty.")
        return None

    compatibility_series /= 100  # Scale to 0-1 for percentage

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=compatibility_series.index, y=compatibility_series.values, ax=ax, palette='Blues_d')
    sns.despine(top=True, right=True, left=False, bottom=False)
    ax.set_xlabel('Tenant Identifier', fontsize=12)
    ax.set_ylabel('Similarity (%)', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(['{:.0f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=10)
    
    for p in ax.patches:
        ax.annotate('{:.0f}%'.format(p.get_height() * 100), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10)
    plt.title('Tenant Compatibility Chart', fontsize=14)
    st.pyplot(fig)

def generate_compatibility_table(results):
    if results[0].empty:
        st.error("Results data is empty.")
        return None

    results_with_index = results[0].reset_index()
    results_with_index.rename(columns={'index': 'Attribute'}, inplace=True)
    fig_table = go.Figure(data=[go.Table(
        header=dict(values=list(results_with_index.columns), fill_color='brown', align='left', font=dict(color='white')),
        cells=dict(values=[results_with_index[col] for col in results_with_index.columns], fill_color='lightblue', align='left'))
    ])
    fig_table.update_layout(width=800, height=400, title='Detailed Tenant Compatibility Table')
    st.plotly_chart(fig_table)

def get_tenant_ids(*tenants):
    tenant_ids = []
    for tenant in tenants:
        if tenant:
            try:
                tenant_ids.append(int(tenant))
            except ValueError:
                st.error(f"The identifier '{tenant}' is not a valid number.")
                return []
    return tenant_ids
