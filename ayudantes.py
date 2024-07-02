import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

# FUNCIÓN PARA GENERAR EL GRÁFICO DE COMPATIBILIDAD
def generar_grafico_compatibilidad(compatibilidad):
    fig, ax = plt.subplots(figsize=(5, 4))
    compatibilidad = compatibilidad.abs()
    sns.barplot(x=compatibilidad.index, y=compatibilidad.values, ax=ax, color='lightblue')
    sns.despine()
    ax.set_xlabel('Identificador de Inquilino', fontsize=10)
    ax.set_ylabel('Similitud (%)', fontsize=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_yticklabels(['{:.1f}%'.format(y * 1) for y in ax.get_yticks()])
    for p in ax.patches:
        ax.annotate(f'{p.get_height()*1:.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    return fig

# FUNCIÓN PARA GENERAR LA TABLA DE COMPAÑEROS
def generar_tabla_compatibilidad(resultado):
    resultado_0_with_index = resultado[0].reset_index()
    resultado_0_with_index.rename(columns={'index': 'ATRIBUTO'}, inplace=True)
    fig_table = go.Figure(data=[go.Table(
        columnwidth = [20] + [10] * (len(resultado_0_with_index.columns) - 1),
        header=dict(values=list(resultado_0_with_index.columns), fill_color='paleturquoise', align='left'),
        cells=dict(values=[resultado_0_with_index[col] for col in resultado_0_with_index.columns], fill_color='lavender', align='left')
    )])
    fig_table.update_layout(width=700, height=320, margin=dict(l=0, r=0, t=0, b=0))
    return fig_table

# FUNCIÓN PARA OBTENER LOS ID DE LOS INQUILINOS
def obtener_id_inquilinos(inquilino1, inquilino2, inquilino3):
    id_inquilinos = []
    for inquilino in [inquilino1, inquilino2, inquilino3]:
        try:
            if inquilino:
                id_inquilinos.append(int(inquilino))
        except ValueError:
            st.error(f"El identificador del inquilino '{inquilino}' no es un número válido.")
            return []  # Retorna una lista vacía para detener la ejecución
    return id_inquilinos
