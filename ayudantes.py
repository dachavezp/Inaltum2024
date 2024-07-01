# ayudantes.py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

def generar_grafico_compatibilidad(compatibility_series):
    if compatibility_series.empty:
        st.error("Datos de compatibilidad están vacíos.")
        return None

    compatibility_series /= 100  # Escalar a 0-1 para porcentaje

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=compatibility_series.index, y=compatibility_series.values, ax=ax, palette='Blues_d')
    sns.despine(top=True, right=True, left=False, bottom=False)
    ax.set_xlabel('Identificador de Inquilino', fontsize=12)
    ax.set_ylabel('Similitud (%)', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(['{:.0f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=10)
    
    for p in ax.patches:
        ax.annotate('{:.0f}%'.format(p.get_height() * 100), (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 10), textcoords='offset points', fontsize=10)
    plt.title('Gráfico de Compatibilidad de Inquilinos', fontsize=14)
    st.pyplot(fig)

def generar_tabla_compatibilidad(results):
    if results[0].empty:
        st.error("Datos de resultados están vacíos.")
        return None

    results_with_index = results[0].reset_index()
    results_with_index.rename(columns={'index': 'Atributo'}, inplace=True)
    fig_table = go.Figure(data=[go.Table(
        header=dict(values=list(results_with_index.columns), fill_color='brown', align='left', font=dict(color='white')),
        cells=dict(values=[results_with_index[col] for col in results_with_index.columns], fill_color='lightblue', align='left'))
    ])
    fig_table.update_layout(width=800, height=400, title='Tabla Detallada de Compatibilidad de Inquilinos')
    st.plotly_chart(fig_table)

def obtener_id_inquilinos(*tenants):
    tenant_ids = []
    for tenant in tenants:
        if tenant:
            try:
                tenant_ids.append(int(tenant))
            except ValueError:
                st.error(f"El identificador '{tenant}' no es un número válido.")
                return []
    return tenant_ids
