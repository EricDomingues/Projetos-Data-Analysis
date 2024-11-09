#####################################################################
############################### LIB's ###############################
#####################################################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, classification_report, accuracy_score
from sklearn.metrics import recall_score, precision_score, f1_score, confusion_matrix, auc
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import metrics, tree

import statsmodels.api as sm
import statsmodels.formula.api as smf

from xgboost import XGBClassifier


#####################################################################
################### INPUTS E TRATAMENTO DOS DADOS ###################
#####################################################################


################################################################################################################# INPUT's
caminho = "C://Users//Dell//OneDrive//Área de Trabalho//Estudo Python//Aulas//Analise_De_Dados//PLANILHAS//caso_estudo.xlsx"

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
planilha_principal['houve_pgto'] = planilha_principal.dt_pagamento.apply(lambda x: 1 if pd.notna(x) else 0)

# Variável de Tempo Média do Pagamento
planilha_principal['tma_pgto'] = (planilha_principal.dt_pagamento - planilha_principal.dt_venda).dt.days

# Idade dos Clientes
planilha_principal['idade'] = np.floor((pd.to_datetime('today') - planilha_principal.dt_nascimento).dt.days / 365)


#####################################################################
############## MACHINE LEARNING (CRIANDO UM DATAFRAME) ##############
#####################################################################


dfML = planilha_principal[['sexo', 'cidade', 'produto', 'valor', 'idade', 'houve_pgto']]
dfML = dfML.replace([' ','-'], '_', regex=True)


# Normalizando os Dados quantitativos (Deixando entre 0 e 1)
dfML['valor'] = dfML['valor'] / dfML['valor'].max()
dfML['idade'] = dfML['idade'] / dfML['idade'].max()

# Normalizando os Dados qualitativos (Deixando entre 0 e 1)
col_quali = ['sexo','cidade','produto']
dfML_dummies = pd.get_dummies(dfML[col_quali], drop_first=False)
dfML_dummies = dfML_dummies.astype(int) # Transforma em binario

# Concatenando Tabelas Normalizadas
dfML = pd.concat([dfML, dfML_dummies], axis=1)
dfML = dfML.drop(col_quali, axis=1)

y = dfML.houve_pgto # Definindo coluna target (coluna foco)
x = dfML.drop(['houve_pgto'], axis=1) # Definindo variaveis
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42) # 70% dos dados em teste e 30% em treino

# TESTE PARA PREVISÃO
X_teste = x.loc[[2997,2998]]


#####################################################################
######### MACHINE LEARNING (MODELO DE REGRESSÃO LOGISTICA) ##########
#####################################################################


#################################################################################### CRIANDO RESUMO DO MODELO
somando_colunas = ' + '.join(dfML.drop(['houve_pgto'], axis=1).columns)
modelo = smf.glm(formula='houve_pgto ~ ' + somando_colunas, data=dfML, family = sm.families.Binomial()).fit()

print(modelo.summary())
#############################################################################################################


############################################################################################ CRIANDO O MODELO
model = LogisticRegression(penalty=None)
model.fit(x_train, y_train)

print('- Matriz de Confusão')
print(confusion_matrix(y_test, model.predict(x_test)))

print('\n- Reporte completo')
print(classification_report(y, model.predict(x)))

print('\n- Reporte teste')
print(classification_report(y_test, model.predict(x_test)))
#############################################################################################################


#####################################################################
############### MACHINE LEARNING (ARVORE DE DECISÃO) ################
#####################################################################


model = DecisionTreeClassifier(criterion="entropy", max_depth=5)
model = model.fit(x_train,y_train)
fig = plt.figure(figsize=(20,10))
_ = tree.plot_tree(model, feature_names=x.columns, class_names=['targetNo','targetYes'], filled=True)
fig.show()

# MATRIZ DE CONFUSÃO
print('- Matriz de Confusão')
print(confusion_matrix(y_test, model.predict(x_test)))
print('\n- Reporte completo')
print(classification_report(y, model.predict(x)))
print('\n- Reporte teste')
print(classification_report(y_test, model.predict(x_test)))

# TESTANDO MODELO DE ARVORE DE DECISÃO
model.predict(X_teste)


#####################################################################
##################### MACHINE LEARNING (XGBOOST) ####################
#####################################################################


model = XGBClassifier()
model.fit(x_train, y_train)

# MATRIZ DE CONFUSÃO
print('- Matriz de Confusão')
print(confusion_matrix(y_test, model.predict(x_test)))
print('\n- Reporte completo')
print(classification_report(y, model.predict(x)))
print('\n- Reporte teste')
print(classification_report(y_test, model.predict(x_test)))

# TESTANDO MODELO DE XGBOOST
model.predict(X_teste)










# Precisão: Dos valores preditos o quanto o seu algoritmo acertou
# Modelos de Regressão Linear e Regressão Logistica
# NO MODELO DE REGRESSÃO LOGISTICA QUANDO O "P" FOR MENOR QUE 5% (0.05) SIGNIFICA QUE A VARIAVEL EXPRESSA É SIGNIFICATIVA PARA O PROBLEMA QUE DEVE SER SOLUCIONADO
