# %%
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt  
from math import sqrt

# %% 

df = pd.read_csv('student-data-set.xls')


df.head()
# %%
df.info()
# %%
df.duplicated().sum()
# %%
df.nunique().sort_values()
# %%

# -=-=-=-= IDENTIFICAO DE OUTLIERS -=-=-=--==-
variaveis = ['age', 'absences', 'G1', 'G2', 'G3']

def identificar_outlier(colunas):
    resultado = []

    for coluna in colunas:
        Q1 = df[coluna].quantile(0.25)
        Q3 = df[coluna].quantile(0.75)
        IQR = Q3 - Q1

        limite_inferior = Q1 - (1.5 * IQR)
        limite_superior = Q3 + (1.5 * IQR)

        # resultado.append({"coluna": coluna, "li": limite_inferior, "ls": limite_superior})
        outliers = df[(df[coluna] < limite_inferior) | (df[coluna] > limite_superior)]

        resultado.append({
            'coluna': coluna,
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR,
            'limite_inferior': limite_inferior,
            'limite_superior': limite_superior,
            'n_outliers': len(outliers)
        })
    return pd.DataFrame(resultado)

outliers_df = identificar_outlier(variaveis)
outliers_df


# %%
# -=-=-=-=-=-=-=- VERIFICANDO CORRELACAO -=-=-=--=-=-=-=

df[['G1', 'G2', 'G3']].corr()

# %%
# -=-=-=-=-=-= HISTOGRAMA ABSENCES -=-=-=-=--=-=-=

bins = round(sqrt(len(df['absences'].dropna())))
bins
plt.hist(df['absences'], bins=bins)
plt.xlabel('Número de faltas')
plt.ylabel('Frequência')
plt.title('Distribuição de faltas')
plt.show()
# %%
# -=-=-=-=-=-=-=- HISTOGRAMA G3 -=-=--=-=-=-
bins_g3 = round(sqrt(len(df['G3'].dropna())))
bins_g3
plt.hist(df['G3'], bins=bins_g3)
plt.xlabel('Quantidade de Notas')
plt.ylabel('Frequencia')
plt.title('Distribuição de Notas')
plt.show()
# %%

df['absences'].skew()
# %%

# Estatistica descritiva para Absences e G3
for col in ['absences', 'G3']:
    print(f"=== Estatísticas: {col} ===")
    print(f"Média:          {df[col].mean():.2f}")
    print(f"Mediana:        {df[col].median():.2f}")
    print(f"Desvio Padrão:  {df[col].std():.2f}")
    print(f"Assimetria:     {df[col].skew():.2f}\n")

# %%

# -=-=-=-=-=--=-=-=---=- ANALISE BIVARIADA -=-=-=--=-=-=-=

# Hipotese: Alunos que faltam mais tendem a ter notas menores. 

plt.scatter(x=df['absences'], y=df['G3'], alpha=0.3)

# Visualmente nao podemos afirmar um relação linear. É notavel alunos com poucas faltas que tiraram notas boas e ruins, assim como alunos com bastante faltas ainda tiraram notas decentes
# %%
df[['absences','G3']].corr()

df[['absences','G3']].corr(method='spearman')

# %%
# Analise se outliers impactam a analise
def subconjunto_sem_outlier(colunas):

    sem_outliers = df.copy()
    for coluna in colunas:
        Q1 = df[coluna].quantile(0.25)
        Q3 = df[coluna].quantile(0.75)
        IQR = Q3 - Q1

        limite_inferior = Q1 - (1.5 * IQR)
        limite_superior = Q3 + (1.5 * IQR)

        # resultado.append({"coluna": coluna, "li": limite_inferior, "ls": limite_superior})
        sem_outliers = df[(df[coluna] >= limite_inferior) & (df[coluna] <= limite_superior)]

    return sem_outliers

df_sem_outliers = subconjunto_sem_outlier(['absences'])

df_sem_outliers

# %%
# Aplicando PEARSON e SPEARMAN 

plt.scatter(x=df_sem_outliers['absences'], y=df_sem_outliers['G3'], alpha=0.3)
# %%
df_sem_outliers[['absences', 'G3']].corr()
#%%
df_sem_outliers[['absences', 'G3']].corr('spearman')
# %%
