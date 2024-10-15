#####################################################################
############################### LIB's ###############################
#####################################################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.ticker import PercentFormatter
import seaborn as sb


#####################################################################
################### INPUTS E TRATAMENTO DOS DADOS ###################
#####################################################################


################################################################################################################# INPUT's
caminho = "C://Users//Dell latitude//Desktop//Estudo Python - Éric//Aulas//Analise_De_Dados//PLANILHAS//caso_estudo.xlsx"

clientes = pd.read_excel(caminho, sheet_name= 'clientes')
lojas = pd.read_excel(caminho, sheet_name= 'lojas')
produtos = pd.read_excel(caminho, sheet_name= 'produtos')
vendas = pd.read_excel(caminho, sheet_name= 'vendas')
pagamentos = pd.read_excel(caminho, sheet_name= 'pagamentos')

planilha_principal = vendas.join(clientes.set_index('id'), on= ['id_cliente'])
planilha_principal = planilha_principal.join(lojas.set_index('id'), on= ['id_loja'])

produtos.loc[9, 'valor'] = produtos.valor[9]/10000
planilha_principal = planilha_principal.join(produtos.set_index('id'), on= ['id_produto'])

pagamentos = pagamentos.drop(columns=['id'])
planilha_principal = planilha_principal.join(pagamentos.set_index('id_venda'), on= ['id'])
#########################################################################################################################


############################################################################################################################################################# TRATAMENTO DOS DADOS
# Retirando Colunas Desnecessárias
planilha_principal = planilha_principal.drop(columns=['id','id_cliente','id_loja','id_produto'])

# Renomeando Colunas
planilha_principal.rename(columns={'dt_nasc': 'dt_nascimento', 'dt_pgto': 'dt_pagamento', 'produto_valor': 'valor'}, inplace=True)

# Data Nascimento
planilha_principal.dt_nascimento = pd.to_datetime(planilha_principal.dt_nascimento, format='%m/%d/%Y')
#planilha_principal.dt_nascimento = planilha_principal.dt_nascimento.dt.strftime('%d/%m/%Y')

# Data Pagamnto
planilha_principal.dt_pagamento = pd.to_datetime(planilha_principal.dt_pagamento, format='%Y/%m/%d')
#planilha_principal.dt_pagamento = planilha_principal.dt_pagamento.dt.strftime('%d/%m/%Y')

# Data Venda
planilha_principal.dt_venda = pd.to_datetime(planilha_principal.dt_venda, format='%Y/%m/%d')
#planilha_principal.dt_venda = planilha_principal.dt_venda.dt.strftime('%d/%m/%Y')

##################################################################################################################################################################################


#####################################################################
########### FEATURE ENGINEERING (CRIAÇÃO DE NOVOS DADOS) ############
#####################################################################


# Variável de Identificação do Pagamento
planilha_principal['houve_pgto'] = planilha_principal.dt_pagamento.apply(lambda x: 'Sim' if pd.notna(x) else 'Não')

# Variável de Tempo Média do Pagamento
planilha_principal['tma_pgto'] = (planilha_principal.dt_pagamento - planilha_principal.dt_venda).dt.days

# Idade dos Clientes
planilha_principal['idade'] = np.floor((pd.to_datetime('today') - planilha_principal.dt_nascimento).dt.days / 365)


#####################################################################
##################### ANÁLISE DE DADOS (GRÁFICOS) ###################
#####################################################################


Qtd_Vendas_Loja = planilha_principal.groupby('cidade').count().dt_venda.sort_values(ascending=False)

plt.figure(figsize=(15,5))
plt.bar(Qtd_Vendas_Loja.index, Qtd_Vendas_Loja.values)
plt.title('Vendas Por Loja')
plt.show()


Receita_Vendas_Loja = planilha_principal.groupby('cidade').valor.sum().sort_values(ascending=False)

plt.figure(figsize=(15,5))
plt.bar(Receita_Vendas_Loja.index, Receita_Vendas_Loja.values)
plt.title('Receita Por Loja')
plt.show()


Vendas_Produto = planilha_principal.groupby('produto').count().dt_venda.sort_values(ascending=False)

plt.figure(figsize=(15,5))
plt.bar(Vendas_Produto.index, Vendas_Produto.values)
plt.title('Produtos Que Mais Vendem')
plt.show()


Produtos_Renda = planilha_principal.groupby('produto').valor.sum().sort_values(ascending=False)

plt.figure(figsize=(15,5))
plt.bar(Produtos_Renda.index, Produtos_Renda.values)
plt.title('Produtos Que Mais Vendem')
plt.show()


ind = planilha_principal[planilha_principal.houve_pgto == "Não"]
Inadimplecia_Qtd = ind.groupby('produto').count().dt_venda.sort_values(ascending=False)

plt.figure(figsize=(15,5))
plt.bar(Inadimplecia_Qtd.index, Inadimplecia_Qtd.values)
plt.title('Produtos Com Mais Inadimplencia')
plt.show()


Inadimplecia_Valor = ind.groupby('produto').valor.sum().sort_values(ascending=False)

plt.figure(figsize=(15,5))
plt.bar(Inadimplecia_Valor.index, Inadimplecia_Valor.values)
plt.title('Produtos Com Mais Inadimplencia')
plt.show()


#####################################################################
################ ANÁLISE DE DADOS (GRÁFICOS - SUBPLOTS) #############
#####################################################################


################################################################################ Visão Vendas Gerais
plt.figure(figsize=(10,7))

plt.subplot(2,2,1)

Qtd_Vendas_Loja = planilha_principal.groupby('cidade').count().dt_venda.sort_values(ascending=False)
plt.bar(Qtd_Vendas_Loja.index, Qtd_Vendas_Loja.values)
plt.title('Vendas Por Loja')
plt.xticks(rotation=90)

plt.subplot(2,2,2)

Receita_Vendas_Loja = planilha_principal.groupby('cidade').valor.sum().sort_values(ascending=False)
plt.bar(Receita_Vendas_Loja.index, Receita_Vendas_Loja.values)
plt.title('Receita Por Loja')
plt.xticks(rotation=90)

plt.subplot(2,2,3)

Vendas_Produto = planilha_principal.groupby('produto').count().dt_venda.sort_values(ascending=False)
plt.bar(Vendas_Produto.index, Vendas_Produto.values)
plt.title('Produtos Que Mais Vendem')
plt.xticks(rotation=90)

plt.subplot(2,2,4)

Produtos_Renda = planilha_principal.groupby('produto').valor.sum().sort_values(ascending=False)
plt.bar(Produtos_Renda.index, Produtos_Renda.values)
plt.title('Receita Dos Produtos')
plt.xticks(rotation=90)

# Corrige o Layout dos Gráficos
plt.tight_layout()
plt.show()
######################################################################################################


################################################################################## Visão Inadimplência
plt.figure(figsize=(15,10))

plt.subplot(2,2,1)

ind = planilha_principal[planilha_principal.houve_pgto == "Não"]
Inadimplecia_Qtd = ind.groupby('produto').count().dt_venda.sort_values(ascending=False)
plt.bar(Inadimplecia_Qtd.index, Inadimplecia_Qtd.values)
plt.title('Produtos Com Mais Inadimplencia')
plt.xticks(rotation=90)

plt.subplot(2,2,2)

Inadimplecia_Valor = ind.groupby('produto').valor.sum().sort_values(ascending=False)
plt.bar(Inadimplecia_Valor.index, Inadimplecia_Valor.values)
plt.title('Valor de Prejuizo Por Produto')
plt.xticks(rotation=90)

# Corrige o Layout dos Gráficos
plt.tight_layout()
plt.show()
######################################################################################################


#####################################################################
################# ANÁLISE DE DADOS (MESCLANDO GRÁFICOS) #############
#####################################################################


############################################################################# Visão Geral dos Clientes
fig, ax = plt.subplots(figsize=(15, 5))
Receita_Clientes = planilha_principal[['nome', 'valor']].groupby('nome').sum().valor.sort_values(ascending=False)

ax.plot(Receita_Clientes.index, Receita_Clientes.values, color='C0')

ax2 = ax.twinx()
receita_acumulada = Receita_Clientes.values.cumsum()/Receita_Clientes.values.sum()
ax2.plot(Receita_Clientes.index, receita_acumulada*100, color='C1')
ax2.yaxis.set_major_formatter(PercentFormatter())

# Retira a Poluição Visual do Gráfico
ax.axes.get_xaxis().set_visible(False)
ax2.axes.get_xaxis().set_visible(False)

plt.title('Receita Por Cliente')
plt.show()
######################################################################################################


########################################################## Percepção dos Produtos que Mais Geram Renda
fig, ax = plt.subplots(figsize=(15, 5))

ax.bar(Produtos_Renda.index, Produtos_Renda.values, color='C0')

ax2 = ax.twinx()
renda_acumulada_produtos = Produtos_Renda.values.cumsum()/Produtos_Renda.values.sum()
ax2.plot(Produtos_Renda.index, renda_acumulada_produtos*100, color='C1', marker='D')
ax2.yaxis.set_major_formatter(PercentFormatter())
# Configurando os Limites Percentuais do Gráfico
plt.ylim(0,110)
plt.title('Renda Acumulada Por Produtos')
plt.show()
######################################################################################################


Graf_Dados = pd.DataFrame(columns=('loja','produto','receita'))
for cidade in lojas.cidade:
    for produto in produtos.produto:
        Graf_Dados = Graf_Dados._append({
            'loja': cidade,
            'produto': produto,
            'receita': planilha_principal.valor[(planilha_principal.cidade == cidade) & (planilha_principal.produto == produto)].sum()
        }, ignore_index=True)

# Transformando em Tabela Dinâmica
Graf_Dados = Graf_Dados.pivot_table(index='loja', columns='produto', values='receita', aggfunc='sum')
sb.heatmap(Graf_Dados)
plt.show()


#####################################################################
################# ANÁLISE DE DADOS DO TMA DE PAGAMENTO ##############
#####################################################################


########################################################################## Média do Tempo de Pagamento
planilha_principal.tma_pgto.mean()

sb.histplot(data= planilha_principal.tma_pgto, kde=True)    # 'kde=True' --> Traz a Curva de Densidade no Gráfico
plt.title('Histograma Para Tempo de Pagamento')
plt.show()

# CONCLUSÃO:
# Este Gráfico Mostra que não Há uma Média Certa Nesta Variável, Sendo Impossivel Traçar uma Previsibilidade
######################################################################################################


############################################### EXISTE ALGUMA LOJA QUE O TMA DE PAGAMENTO É MAIS ALTO?
TMA_Loja = planilha_principal[['cidade','tma_pgto']].groupby('cidade').mean().tma_pgto.sort_values(ascending=False)

plt.figure(figsize=(7, 10))
TMA_Loja = planilha_principal[['cidade','tma_pgto']].groupby('cidade').boxplot('tma_pgto')
plt.xticks(rotation=90)
plt.show()
######################################################################################################















# ------------------------------------------------------------------------------------------------- OBS ------------------------------------------------------------------------------------ #

# 'plt.bar()' --> Grafico de Barras
# 'plt.plot()' --> Grafico de Linhas
# 'sb.heatmap()' --> Mapa de Calor (Identificação de Problemas de Forma Simplificada)
# 'sb.histplot()' --> Histograma Com Curva De Densidade (Entendendo Se Os Dados Estão Dentro dos Conformes Para Variáveis Estatísticas)

# Média Movel --> Media_Movel = planilha_principal[['dt_venda', 'valor']].groupby('dt_venda').sum().rolling(30).mean().sort_values(ascending=True, by='dt_venda')
