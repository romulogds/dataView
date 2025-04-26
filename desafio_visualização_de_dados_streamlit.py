# Importação de bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Cabeçalho da Página ---
st.title("📈 Análise de Crescimento de Vendas - 1º Trimestre 2024")
st.markdown("""
Este painel apresenta uma análise do crescimento de vendas da empresa no início de 2024,
com gráficos e insights focados no desempenho diário, mensal e por categoria de produto.
""")

# --- Carregar o Dataset ---
st.header("1. Carregando os Dados")

csv_path = 'sales_data.csv'  # Ajuste para caminhos locais ou onde você subir

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    df.drop_duplicates(inplace=True)
    df['Date_Sold'] = pd.to_datetime(df['Date_Sold'])

    st.write("Primeiras linhas do dataset:")
    st.dataframe(df.head())

    # --- Informações Iniciais ---
    st.header("2. Informações do Dataset")
    total_registros = len(df)
    data_inicial = df['Date_Sold'].min()
    data_final = df['Date_Sold'].max()

    st.success(f"Total de registros: **{total_registros}**")
    st.success(f"Período coberto: **{data_inicial.date()} até {data_final.date()}**")

    # --- Comparação de Vendas Mensais ---
    st.header("3. Comparação de Vendas Mensais (Jan, Fev, Mar)")

    df['Month'] = df['Date_Sold'].dt.to_period('M')
    vendas_mensais = df[df['Date_Sold'] < '2024-04-01'].groupby('Month')['Total_Sales'].sum()

    meses = ['Jan 2024', 'Fev 2024', 'Mar 2024']
    totais = [vendas_mensais.loc['2024-01'], vendas_mensais.loc['2024-02'], vendas_mensais.loc['2024-03']]

    fig2, ax2 = plt.subplots(figsize=(8,5))
    barras = ax2.bar(meses, totais, color='#4c78a8')
    ax2.set_title('Vendas Totais Mensais - 1º Trimestre 2024')
    ax2.set_xlabel('Mês')
    ax2.set_ylabel('Vendas Totais (R$)')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    for barra in barras:
        altura = barra.get_height()
        ax2.annotate(f'R$ {altura:,.0f}',
                     xy=(barra.get_x() + barra.get_width()/2, altura), xytext=(0,5),
                     textcoords="offset points", ha='center', va='bottom')

    st.pyplot(fig2)

    # --- Análise de Vendas por Categoria ---
    st.header("4. Análise de Vendas por Categoria")

    vendas_cat_mensal = df[df['Date_Sold'] < '2024-04-01'].groupby(['Month','Category'])['Total_Sales'].sum().unstack(fill_value=0)

    colors = ['#4c78a8', '#f58518', '#54a24b', '#b279a2']
    fig3, ax3 = plt.subplots(figsize=(8,5))
    vendas_cat_mensal.plot(kind='bar', stacked=True, color=colors, ax=ax3)

    ax3.set_title('Vendas Mensais por Categoria - 1º Tri 2024')
    ax3.set_xlabel('Mês')
    ax3.set_ylabel('Vendas Totais (R$)')
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    ax3.legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot(fig3)

    # --- Conclusão ---
    st.header("5. Conclusão 📌")
    st.markdown("""
    - As vendas aumentaram mês a mês, com destaque para **março de 2024**, que superou todos os meses anteriores.
    - **Clothing** e **Grocery** foram as categorias que mais impulsionaram o crescimento no trimestre.
    - **Toys** teve crescimento sólido, enquanto **Electronics** caiu um pouco em março, indicando necessidade de monitoramento.
    """)
else:
    st.error(f"Arquivo '{csv_path}' não encontrado. Por favor, verifique o caminho do arquivo!")
