import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st

# FUNCTION TO GENERATE COMPATIBILITY GRAPH
def generate_compatibility_chart(compatibility):
    compatibility = compatibility / 100  # Scale to 0-1 for percentage

    # Configure the Seaborn bar chart
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the size as needed
    
    # Create the bar chart with values converted to percentages
    sns.barplot(x=compatibility.index, y=compatibility.values, ax=ax, palette='Blues_d')
    
    # Remove borders
    sns.despine(top=True, right=True, left=False, bottom=False)
    
    # Set axis labels and rotate x-axis labels
    ax.set_xlabel('Tenant Identifier', fontsize=12)
    ax.set_ylabel('Similarity (%)', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    # Adjust y-axis labels to display percentages correctly
    ax.set_yticklabels(['{:.0f}%'.format(y * 100) for y in ax.get_yticks()], fontsize=10)

    # Add percentage labels over each bar
    for p in ax.patches:
        height = p.get_height()
        ax.annotate('{:.0f}%'.format(height * 100),
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='center',
                    xytext=(0, 10),
                    textcoords='offset points', fontsize=10)

    plt.title('Tenant Compatibility Chart', fontsize=14)
    return(fig)


# FUNCTION TO GENERATE COMPATIBILITY TABLE
def generate_compatibility_table(results):
    # Modify the 'index' column name and adjust column widths
    results_with_index = results[0].reset_index()
    results_with_index.rename(columns={'index': 'Attribute'}, inplace=True)
    
    # Configure the Plotly table
    fig_table = go.Figure(data=[go.Table(
        columnwidth = [180] + [120] * (len(results_with_index.columns) - 1),  # Adjust the first value for 'Attribute' column width
        header=dict(values=list(results_with_index.columns),
                    fill_color='brown',  # Header background color
                    align='left',
                    font=dict(color='white')),  # Header text color
        cells=dict(values=[results_with_index[col] for col in results_with_index.columns],
                   fill_color='lightblue',  # Cell background color
                   align='left'))
    ])
    
    # Adjust table layout
    fig_table.update_layout(
        width=800, height=400,  # Adjust as per your needs
        margin=dict(l=0, r=0, t=0, b=0),
        title='Detailed Tenant Compatibility Table'
    )

    return(fig_table)


# FUNCTION TO OBTAIN SEED TENANT IDS
def get_tenant_ids(*tenants):
    # Create a list with entered tenant identifiers, converting to integers
    tenant_ids = []
    for tenant in tenants:
        try:
            if tenant:  # If there's text in the input
                tenant_ids.append(int(tenant))  # Convert to integer and add to the list
        except ValueError:
            st.error(f"The identifier '{tenant}' is not a valid number.")
            tenant_ids = []  # Clear the list if there's an error
            break  # Exit the loop

    return tenant_ids
