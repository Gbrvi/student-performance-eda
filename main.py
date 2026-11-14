# %%
import pandas as pd
from scipy import stats

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
