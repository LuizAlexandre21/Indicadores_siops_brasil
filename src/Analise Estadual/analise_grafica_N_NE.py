# Pacotes 
import numpy as np
import plots
import logging
import os
import sys
import csv

# Função de importação de csv 
def import_csv(path):
    dic = {}
    data = open(path,mode='r') 
    csv_reader = csv.DictReader(data)
    line_count =0
    for row in csv_reader:
        for key in row.keys():
            if line_count ==0:
                dic[key] = []
                dic[key].append(row[key])
            else:
                dic[key].append(row[key])
        line_count +=1
    return dic 

# Importando os indicadores 
list_dir = os.listdir('outputs_N_NE')

# Abrindo indicadores 
local = {}
for files in list_dir:
    local[str(files).replace(".csv","")]=[]
    local[str(files).replace(".csv","")].append(import_csv('outputs_N_NE/'+files))

# Gradiente de cores 
cores = plots.plots.colour_gradient('#535fb2','#a5b5ee',7)

# Gráfico 1 – Evolução da Receita Total das Regiões Norte/Nordeste para apuração da aplicação em ações e serviços públicos de saúde, 2013 a 2019, em milhões de reais
#data_range = local['Receita Estadual Total '][0]['Região']
#local['Receita Estadual Total '][0].pop('Região')
#dicionario = local['Receita Estadual Total '][0]
#metadata ={'title':'Evolução da Receita Total - Norte/Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
#fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 2 – Receita Total por Estado da Região Norte para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, em milhões de reais.
data_range = local['Receita Total - Norte'][0]['Estado']
local['Receita Total - Norte'][0].pop('Estado')
dicionario = local['Receita Total - Norte'][0]
metadata ={'title':'Receita Total - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 3 -Receita Total por Estado da Região Nordeste para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, em milhões de reais
data_range = local['Receita Total - Nordeste'][0]['Estado']
local['Receita Total - Nordeste'][0].pop('Estado')
dicionario = local['Receita Total - Nordeste'][0]
metadata ={'title':'Receita Total - Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 4 – Receita Total por Estado da Região Norte para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, per capita.
data_range = local['Receita Total per capita - Norte'][0]['Estado']
local['Receita Total per capita - Norte'][0].pop('Estado')
dicionario = local['Receita Total per capita - Norte'][0]
metadata ={'title':'Receita Total per capita - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 5 – Receita Total por Estado da Região Nordeste para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, per capita.
data_range = local['Receita Total per capita - Nordeste'][0]['Estado']
local['Receita Total per capita - Nordeste'][0].pop('Estado')
dicionario = local['Receita Total per capita - Nordeste'][0]
metadata ={'title':'Receita Total per capita - Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 6 – Receita líquida de impostos das Regiões Norte/Nordeste, 2013 a 2019, em milhões de reais.
#data_range = local['Receita líquida de impostos das Regiões Norte_Nordeste'][0]['Região']
#local['Receita líquida de impostos das Regiões Norte_Nordeste'][0].pop('Região')
#dicionario = local['Receita líquida de impostos das Regiões Norte_Nordeste'][0]
#metadata ={'title':'Receita líquida de impostos das Regiões Norte_Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
#fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 7 – Receita líquida estadual de impostos dos estados da Região Norte, no agregado de 2013 a 2019, em milhões de reais.
#data_range = local['Receita liquida - Norte'][0]['Estado']
#local['Receita liquida - Norte'][0].pop('Estado')
#dicionario = local['Receita liquida - Norte'][0]
#metadata ={'title':'Receita liquida - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
#fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 8 - Receita líquida estadual de impostos dos estados da Região Nordeste, no agregado de 2013 a 2019, em milhões de reais.
#data_range = local['Receita liquida - Nordeste'][0]['Estado']
#local['Receita liquida - Nordeste'][0].pop('Estado')
#dicionario = local['Receita liquida - Nordeste'][0]
#metadata ={'title':'Receita liquida - Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
#fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 9 – Receita líquida estadual de impostos dos estados da Região Norte, no agregado de 2013 a 2019, per capita.
data_range = local['Receita liquida per capita - Norte'][0]['Estado']
local['Receita liquida per capita - Norte'][0].pop('Estado')
dicionario = local['Receita liquida per capita - Norte'][0]
metadata ={'title':'Receita liquida per capita - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 10 – Receita líquida estadual de impostos dos estados da Região Nordeste, no agregado de 2013 a 2019, per capita
data_range = local['Receita liquida per capita - Nordeste'][0]['Estado']
local['Receita liquida per capita - Nordeste'][0].pop('Estado')
dicionario = local['Receita liquida per capita - Nordeste'][0]
metadata ={'title':'Receita liquida per capita - Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 11 – Receita de Transferências Constitucionais e Legais da União das Regiões Norte/Nordeste, 2013 a 2019, em milhões de reais.

# Gráfico 12 –Receita de Transferências Constitucionais e Legais da União para os Estados da Região Norte, 2013 a 2019, em milhões de reais.
data_range = local['Receita de transferência constitucional e legais - Norte'][0]['Estado']
local['Receita de transferência constitucional e legais - Norte'][0].pop('Estado')
dicionario = local['Receita de transferência constitucional e legais - Norte'][0]
metadata ={'title':'Receita de transferência constitucional e legais - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 13 –Receita de Transferências Constitucionais e Legais da União para os Estados da Região Nordeste, 2013 a 2019, em milhões de reais.
data_range = local['Receita de transferência constitucional e legais - Nordeste'][0]['Estado']
local['Receita de transferência constitucional e legais - Nordeste'][0].pop('Estado')
dicionario = local['Receita de transferência constitucional e legais - Nordeste'][0]
metadata ={'title':'Receita de transferência constitucional e legais- Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 14 –Receita de Transferências Constitucionais e Legais da União para os Estados da Região Norte, 2013 a 2019, per capita.
data_range = local['Receita de transferência constitucional e legais per capita - Norte'][0]['Estado']
local['Receita de transferência constitucional e legais per capita - Norte'][0].pop('Estado')
dicionario = local['Receita de transferência constitucional e legais per capita - Norte'][0]
metadata ={'title':'Receita de transferência constitucional e legais per capita- Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 15 –Receita de Transferências Constitucionais e Legais da União para os Estados da Região Nordeste, 2013 a 2019, per capita
data_range = local['Receita de transferência constitucional e legais per capita - Nordeste'][0]['Estado']
local['Receita de transferência constitucional e legais per capita - Nordeste'][0].pop('Estado')
dicionario = local['Receita de transferência constitucional e legais per capita - Nordeste'][0]
metadata ={'title':'Receita de transferência constitucional e legais per capita- Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 15 – Percentual médio da receita líquida de impostos na receita total dos estados da Região Norte, no agregado de 2013 a 2019. 
data_range = local['Indicador Capacidade - Norte'][0]['Estado']
local['Indicador Capacidade - Norte'][0].pop('Estado')
dicionario = local['Indicador Capacidade - Norte'][0]
metadata ={'title':'Indicador Capacidade - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 16 – Percentual médio da receita líquida de impostos na receita total dos estados da Região Norte, no agregado de 2013 a 2019. 
data_range = local['Indicador Capacidade - Nordeste'][0]['Estado']
local['Indicador Capacidade - Nordeste'][0].pop('Estado')
dicionario = local['Indicador Capacidade - Nordeste'][0]
metadata ={'title':'Indicador Capacidade - Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 17 - Percentual Médio da receita de transferências na receita total dos estados da Região Norte, no agregado de 2013 a 2019.
data_range = local['Indicador Dependencia - Norte'][0]['Estado']
local['Indicador Dependencia - Norte'][0].pop('Estado')
dicionario = local['Indicador Dependencia - Norte'][0]
metadata ={'title':'Indicador Dependencia - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 18 – Percentual Médio da receita de transferências na receita total dos estados da Região Nordeste, no agregado de 2013 a 2019.
data_range = local['Indicador Dependencia - Nordeste'][0]['Estado']
local['Indicador Dependencia - Nordeste'][0].pop('Estado')
dicionario = local['Indicador Dependencia - Nordeste'][0]
metadata ={'title':'Indicador Dependencia - Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 19 - Receitas adicionais vinculadas ao SUS dos Estados da Região Norte, no agregado de 2013 a 2019, em milhões de reais.
data_range = local['Indicador Dependencia Sus - Norte'][0]['Estado']
local['Indicador Dependencia Sus - Norte'][0].pop('Estado')
dicionario = local['Indicador Dependencia Sus - Norte'][0]
metadata ={'title':'Indicador Dependencia Sus - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 20 - Receitas adicionais vinculadas ao SUS dos Estados da Região Nordeste, no agregado de 2013 a 2019, em milhões de reais.
data_range = local['Indicador Dependencia Sus - Nordeste'][0]['Estado']
local['Indicador Dependencia Sus - Nordeste'][0].pop('Estado')
dicionario = local['Indicador Dependencia Sus - Nordeste'][0]
metadata ={'title':'Indicador Dependencia Sus - Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 21 – Receitas adicionais vinculadas ao SUS dos Estados da Região Norte, no agregado de 2013 a 2019, per capita.
data_range = local['Indicador Dependencia Sus per capita - Norte'][0]['Estado']
local['Indicador Dependencia Sus per capita - Norte'][0].pop('Estado')
dicionario = local['Indicador Dependencia Sus per capita - Norte'][0]
metadata ={'title':'Indicador Dependencia Sus per capita - Norte','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)

# Gráfico 22 – Receitas adicionais vinculadas ao SUS dos Estados da Região Nordeste, no agregado de 2013 a 2019, per capita.
data_range = local['Indicador Dependencia Sus per capita - Nordeste'][0]['Estado']
local['Indicador Dependencia Sus per capita - Nordeste'][0].pop('Estado')
dicionario = local['Indicador Dependencia Sus per capita - Nordeste'][0]
metadata ={'title':'Indicador Dependencia Sus per capita - Nordeste','xaxis_title':'Ano','yaxis_title':'Bilhões'}
fig = plots.plots.comparative_plot(dicionario,data_range,cores,metadata,preparation = False)