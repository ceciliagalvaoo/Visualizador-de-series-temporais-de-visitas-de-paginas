import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
# Importar os dados e definir o índice como a coluna 'date'
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')
# Limpar os dados: Remover os 2,5% maiores e menores valores
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]
# Função para desenhar o gráfico de linhas
def draw_line_plot():
    # Desenhar o gráfico de linhas
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    # Salvar a imagem e retornar o gráfico
    fig.savefig('line_plot.png')
    return fig
# Função para desenhar o gráfico de barras
def draw_bar_plot():
    # Copiar e modificar os dados para o gráfico de barras mensal
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()  # Usar nomes completos dos meses
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    # Reordenar as colunas para garantir a ordem correta dos meses
    df_bar = df_bar[['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']]
    # Desenhar o gráfico de barras
    fig = df_bar.plot(kind='bar', figsize=(12, 6), legend=True).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    # Salvar a imagem e retornar o gráfico
    fig.savefig('bar_plot.png')
    return fig
# Função para desenhar os diagramas de caixa
def draw_box_plot():
    # Preparar os dados para os diagramas de caixa
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')
    df_box['month_num'] = df_box['date'].dt.month
    df_box = df_box.sort_values('month_num')
    # Desenhar os diagramas de caixa (usando Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    # Diagrama de caixas por ano (tendência)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    # Diagrama de caixas por mês (sazonalidade)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    # Salvar a imagem e retornar o gráfico
    fig.savefig('box_plot.png')
    return fig