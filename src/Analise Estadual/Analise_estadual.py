# Pacotes 
from database import *
import  numpy as np
import plotly.express as px
import logging
import os
import sys
import csv
import pathlib 

# Definindo a função de deflação 
def deflação(serie):
    IPCA = {'2013':5.91068325533108,'2014':6.40747079590815,'2015':10.6730281339751,'2016':6.28798821322138,'2017':2.94742132043471,'2018':3.74558117019155,'2019':4.30615161715953}
    deflation = {}
    inflação={'2019':1}
    a=[]
    for i in range(2018,2012,-1):
        a.append(IPCA[str(i)]/100)
        inflação[str(i)] = (1-sum(a))
    for ano in serie.keys():
        if ano not in ['Estado','IDH','Porte','Região']:
            lista = []  
            for series in serie[ano]:
                lista.append(series*inflação[ano])
            deflation[ano]= lista
        else:
            deflation[ano]= serie[ano]
    return(deflation)

# Exportando os dados para csv 
def list_csv(dic,to):
    data =[]
    for keys in dic.keys():
        row = [str(keys)]
        for value in dic[keys]:
            row.append(str(value))
        data.append(row)

    f = open('outputs_N_NE/'+to+'.csv','w')
    writer = csv.writer(f)
    writer.writerows(data)
    f.close()
        
# Importando os dados 
try:
   dados_apuração = (Populacao.select(Populacao.Estado,Populacao.Ano,Populacao.População,Populacao.IDH,Populacao.Porte,Receitas_apuracao_sps_estadual.campo,Receitas_apuracao_sps_estadual.Receitas_realizadas_Bimestre).distinct().join(Receitas_apuracao_sps_estadual, on=((Populacao.Estado == Receitas_apuracao_sps_estadual.estado) &(Populacao.Ano == Receitas_apuracao_sps_estadual.ano))))
   dados_adicionais = (Populacao.select(Populacao.Estado,Populacao.Ano,Populacao.População,Populacao.IDH,Populacao.Porte,Receitas_adicionais_financiamento_estadual.campo,Receitas_adicionais_financiamento_estadual.Receitas_realizadas_Bimestre).distinct().join(Receitas_adicionais_financiamento_estadual, on=((Populacao.Estado == Receitas_adicionais_financiamento_estadual.estado) &(Populacao.Ano == Receitas_adicionais_financiamento_estadual.ano))))
except Exception as e:
   print(e)

# Segregando os dados por regiões 
# Nordeste 
Apuração_Nordeste =[]
for dados in list(dados_apuração.dicts()):
    Nordeste = ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']
    if dados.get("Estado") in Nordeste:
        Apuração_Nordeste.append(dados)

Adicionais_Nordeste =[]
for dados in list(dados_adicionais.dicts()):
    Nordeste = ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']
    if dados.get("Estado") in Nordeste:
        Adicionais_Nordeste.append(dados)

# Norte
Apuração_Norte =[]
for dados in list(dados_apuração.dicts()):
    Norte = ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']
    if dados.get("Estado") in Norte:
        Apuração_Norte.append(dados)

Adicionais_Norte =[]
for dados in list(dados_adicionais.dicts()):
    Norte = ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']
    if dados.get("Estado") in Norte:
        Adicionais_Norte.append(dados)

# Norte e Nordeste
Apuração_Norte_Nordeste =[]
for dados in list(dados_apuração.dicts()):
    Norte = ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins','Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']
    if dados.get("Estado") in Norte:
        Apuração_Norte_Nordeste.append(dados)

Adicionais_Norte_Nordeste =[]
for dados in list(dados_adicionais.dicts()):
    Norte = ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins','Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']
    if dados.get("Estado") in Norte:
        Adicionais_Norte_Nordeste.append(dados)

# 1 Receita Total por Estado da Região Norte para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, em milhões de reais
# Receita Estadual Total
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Apuração_Norte:
       if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Estado'] == estado:
            tabela[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(deflação(tabela),'Receita Total - Norte')


# 2 Receita Total por Estado da Região Norte para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, em milhões de reais
# Receita Estadual Total
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
       if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Estado'] == estado:
            tabela[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(deflação(tabela),'Receita Total - Nordeste')

# 3 Receita Total por IDH nos Estado da Região Norte e Nordeste para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, em milhões de reais
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for IDH in ['Médio','Alto','Muito Alto']:
    for anos in range(2013,2020):
        numerador = []
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['IDH'] == IDH and dados['Ano']== anos:
                numerador.append(dados['Receitas_realizadas_Bimestre']/1000000)
        tabela[str(anos)].append(sum(numerador))
    tabela['IDH'].append(IDH)
list_csv(deflação(tabela),'Receita Total - IDH')

# 4 Receita Total por Porte nos Estado da Região Norte e Nordeste para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, em milhões de reais
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador = []
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['IDH'] == IDH and dados['Porte']== int(Porte):
                numerador.append(dados['Receitas_realizadas_Bimestre']/1000000)
        tabela[str(anos)].append(sum(numerador))
    tabela['Porte'].append(Porte)

list_csv(deflação(tabela),'Receita Total - Porte')


# 5 Receita Total por Estado da Região Norte para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, per capita.
# Receita Estadual Total
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Apuração_Norte:
        if dados['Estado'] == estado:
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Estado'] == estado:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)


# Exportando os dados
list_csv(tabela,'Receita Total per capita - Norte')

# 6 Receita Total por Estado da Região Nordeste para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, per capita.
# Receita Estadual Total
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
        if dados['Estado'] == estado:
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Estado'] == estado:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Receita Total per capita - Nordeste')

# 7 Receita Total por IDH por estados da Região Nordeste e Norte para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, per capita.
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for IDH in ['Médio','Alto','Muito Alto']:
    for anos in range(2013,2020):
        numerador = []
        print(numerador)
        denominador =[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['IDH'] == IDH and dados['Ano']==anos :
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                print(numerador)
                denominador.append(int(dados['População']))
        try:
            tabela[str(anos)].append(sum(numerador)/sum(denominador))
        except Exception as e:
            print(e)
    tabela['IDH'].append(IDH)
list_csv(tabela,'Receita Total per capita - IDH')


# 8 Receita Total por Porte por estados da Região Nordeste e Norte para apuração da aplicação em ações e serviços públicos de saúde, no agregado de 2013 a 2019, per capita.
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador = []
        denominador =[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Porte'] == Porte and dados['Ano']==anos :
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                print(numerador)
                denominador.append(int(dados['População']))
        try:
            tabela[str(anos)].append(sum(numerador)/sum(denominador))
        except Exception as e:
            tabela[str(anos)].append(0)
    tabela['Porte'].append(Porte)
list_csv(tabela,'Receita Total per capita - Porte')

# 9 Receita líquida de impostos das Regiões Norte/Nordeste, 2013 a 2019, em milhões de reais
# Receita Estadual liquido
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Apuração_Norte:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                numerador = dados['Receitas_realizadas_Bimestre']
                tabela[str(dados['Ano'])].append(numerador/1000000)
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(deflação(tabela),'Receita líquida de impostos- Norte')

# 10 Receita líquida de impostos das Regiões Norte/Nordeste, 2013 a 2019, em milhões de reais
# Receita Estadual Liquida 
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                numerador = dados['Receitas_realizadas_Bimestre']
                tabela[str(dados['Ano'])].append(numerador/1000000)
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(deflação(tabela),'Receita líquida de impostos- Nordeste')

# 11 Receita líquida de impostos por IDH das Regiões Norte/Nordeste, 2013 a 2019, em milhões de reais
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for IDH in ['Médio','Alto','Muito Alto']:
    for anos in range(2013,2020):
        numerador =[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['IDH']==IDH and dados['Ano'] == anos :
                numerador.append(dados['Receitas_realizadas_Bimestre'])
        tabela[str(anos)].append(sum(numerador)/1000000)
    tabela['IDH'].append(IDH)

list_csv(deflação(tabela),'Receita líquida de impostos - IDH')

# 12 Receita líquida de impostos por Porte das Regiões Norte/Nordeste, 2013 a 2019, em milhões de reais
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador =[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Porte']==Porte and dados['Ano'] == anos :
                numerador.append(dados['Receitas_realizadas_Bimestre'])
        tabela[str(anos)].append(sum(numerador)/1000000)
    tabela['Porte'].append(Porte)

list_csv(deflação(tabela),'Receita líquida de impostos - Porte')

# 13 Receita líquida estadual de impostos dos estados da Região Norte, no agregado de 2013 a 2019, per capita
# Receita Estadual liquida
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Apuração_Norte:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Receita liquida per capita - Norte')

# 14 Receita líquida estadual de impostos dos estados da Região Nordeste, no agregado de 2013 a 2019, per capita
# Receita Estadual liquida
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Receita liquida per capita - Nordeste')

# 15 Receita líquida estadual de impostos por IDH dos estados da Região Norte e Nordeste, no agregado de 2013 a 2019, per capita
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for IDH in ['Médio','Alto','Muito Alto']:
    for anos in range(2013,2020):
        numerador =[]
        denominador = []
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Ano']==anos and dados['IDH']==IDH: 
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)
    tabela['IDH'].append(IDH)

# Exportando os dados
list_csv(tabela,'Receita liquida per capita - IDH')

# 16 Receita líquida estadual de impostos por Porte dos estados da Região Norte e Nordeste, no agregado de 2013 a 2019, per capita
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador =[]
        denominador = []
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Ano']==anos and dados['Porte']==Porte: 
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)
    tabela['Porte'].append(Porte)

# Exportando os dados
list_csv(tabela,'Receita liquida per capita - Porte')

# 17 – Receita de Transferências Constitucionais e Legais da União para os Estados da Região Norte, 2013 a 2019, em milhões de reais.
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Apuração_Norte:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
                numerador = dados['Receitas_realizadas_Bimestre']
                tabela[str(dados['Ano'])].append(numerador/1000000)
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Receita de transferência constitucional e legais - Norte')

# 18 - Receita de Transferências Constitucionais e Legais da União para os Estados da Região Nordeste, 2013 a 2019, em milhões de reais.
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
                numerador = dados['Receitas_realizadas_Bimestre']
                tabela[str(dados['Ano'])].append(numerador/1000000)
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Receita de transferência constitucional e legais - Nordeste')

# 19 - Receita de Transferências Constitucionais e Legais da União por IDH dos Estados da Região Nordeste, 2013 a 2019, em milhões de reais.
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for IDH in ['Médio','Alto','Muito Alto']:    
    for anos in range(2013,2020):
        numerador=[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Ano']==anos and dados['IDH']==IDH:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
        tabela[str(anos)].append(sum(numerador)/1000000)
    tabela['IDH'].append(IDH)

list_csv(tabela,'Receita de transferência constitucional e legais - IDH')

# 20 - Receita de Transferências Constitucionais e Legais da União por IDH dos Estados da Região Nordeste, 2013 a 2019, em milhões de reais.
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador =[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Ano']==anos and dados['Porte']==Porte:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
        tabela[str(anos)].append(sum(numerador)/1000000)
    tabela['Porte'].append(Porte)

list_csv(deflação(tabela),'Receita de transferência constitucional e legais - Porte')


# 21 Receita de Transferências Constitucionais e Legais da União para os Estados da Região Norte, 2013 a 2019, per capita
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Apuração_Norte:
       if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
          if dados['Estado'] == estado:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Receita de transferência constitucional e legais per capita - Norte')

# 22 Receita de Transferências Constitucionais e Legais da União para os Estados da Região Nordeste, 2013 a 2019, per capita.
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
                    numerador = dados['Receitas_realizadas_Bimestre']
                    denominador = int(dados['População'])
                    tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Receita de transferência constitucional e legais per capita - Nordeste')

# 23 - Receita de Transferências Constitucionais e Legais da União por IDH dos Estados da Região Nordeste, 2013 a 2019, em milhões de reais per capita. 
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for IDH in ['Médio','Alto','Muito Alto']:    
    for anos in range(2013,2020):
        numerador=[]
        denominador=[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Ano']==anos and dados['IDH']==IDH:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)
    tabela['IDH'].append(IDH)

list_csv(tabela,'Receita de transferência constitucional e legais - IDH')

# 24 - Receita de Transferências Constitucionais e Legais da União por Porte dos Estados da Região Nordeste, 2013 a 2019, em milhões de reais.
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for Porte in ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador=[]
        denominador=[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Ano']==anos and dados['Porte']==Porte:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)
    tabela['Porte'].append(Porte)

list_csv(tabela,'Receita de transferência constitucional e legais - Porte')

# 25 Percentual médio da receita líquida de impostos na receita total dos estados da Região Norte, no agregado de 2013 a 2019
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Apuração_Norte:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = int(dados['Receitas_realizadas_Bimestre'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Indicador Capacidade - Norte')

# 26 Percentual médio da receita líquida de impostos na receita total dos estados da Região Nordeste, no agregado de 2013 a 2019
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = int(dados['Receitas_realizadas_Bimestre'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Indicador Capacidade - Nordeste')

# 27 Percentual médio da receita líquida de impostos na receita total por IDH dos estados da Região Norte e Nordeste, no agregado de 2013 a 2019
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for IDH in ['Médio','Alto','Muito Alto']:    
    for anos in range(2013,2020):
        numerador=[]
        denominador=[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Ano']==anos and dados['IDH']==IDH:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Ano']==anos and dados['IDH']==IDH:
                denominador.append(int(dados['Receitas_realizadas_Bimestre']))
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)
    tabela['IDH'].append(IDH)
list_csv(tabela,'Indicador Capacidade - IDH')

# 28 Percentual médio da receita líquida de impostos na receita total dos estados da Região Nordeste, no agregado de 2013 a 2019
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:    
    for anos in range(2013,2020):
        numerador=[]
        denominador=[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Ano']==anos and dados['Porte']==Porte:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Ano']==anos and dados['Porte']==Porte:
                denominador.append(int(dados['Receitas_realizadas_Bimestre']))
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)
    tabela['Porte'].append(Porte)

list_csv(tabela,'Indicador Capacidade - Porte')

# 29 - Percentual Médio da receita de transferências na receita total dos estados da Região Norte, no agregado de 2013 a 2019
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Apuração_Norte:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = int(dados['Receitas_realizadas_Bimestre'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Indicador Dependencia - Norte')

# 30 - Percentual Médio da receita de transferências na receita total dos estados da Região Norte, no agregado de 2013 a 2019 
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = int(dados['Receitas_realizadas_Bimestre'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)
list_csv(tabela,'Indicador Dependencia - Nordeste')

# 31 - Percentual Médio da receita de transferências na receita total dos estados da Região Norte e Nortdeste - IDH, no agregado de 2013 a 2019 
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for IDH in ['Médio','Alto','Muito Alto']:    
    for anos in range(2013,2020):
        numerador=[]
        denominador=[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Ano']==anos and dados['IDH']==IDH:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Ano']==anos and dados['IDH']==IDH:
                denominador.append(int(dados['Receitas_realizadas_Bimestre']))
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)
    tabela['IDH'].append(IDH)
list_csv(tabela,'Indicador Dependencia - IDH')

# 32 - Percentual Médio da receita de transferências na receita total dos estados da Região Norte e Nortdeste - Porte, no agregado de 2013 a 2019 
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:   
    for anos in range(2013,2020):
        numerador=[]
        denominador=[]
        for dados in Apuração_Norte_Nordeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Ano']==anos and dados['Porte']==Porte:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III' and dados['Ano']==anos and dados['Porte']==Porte:
                denominador.append(int(dados['Receitas_realizadas_Bimestre']))
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)
    tabela['Porte'].append(Porte)
list_csv(tabela,'Indicador Dependencia - Porte')

# 33 - Percentual Médio da receita de transferências na receita total dos estados da Região Norte, no agregado de 2013 a 2019 
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Apuração_Nordeste:
        if dados['Estado'] == estado:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = int(dados['Receitas_realizadas_Bimestre'])
                tabela[str(dados['Ano'])].append(round(numerador/denominador,2))
    tabela['Estado'].append(estado)

# Exportando os dados
list_csv(tabela,'Indicador Dependencia - Nordeste')

# 34 - Receitas adicionais vinculadas ao SUS dos Estados da Região Norte, no agregado de 2013 a 2019, em milhões de reais per capita
tabela={'IDH':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for IDH in ['Médio','Alto','Muito Alto']:    
    for anos in range(2013,2020):
        numerador=[] 
        denominador=[]
        for dados in Adicionais_Norte_Nordeste:
            if dados['campo'] =='Provenientes da União' and dados['Ano']==anos and dados['IDH']==IDH:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
        try:
            tabela[str(anos)].append(sum(numerador)/1000000)
        except:
            tabela[str(anos)].append(0)
    tabela['IDH'].append(IDH)

list_csv(deflação(tabela),'Indicador Dependencia Sus - IDH')

# 35 - Receitas adicionais vinculadas ao SUS dos Estados da Região Norte, no agregado de 2013 a 2019, em milhões de reais per capita
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:   
    for anos in range(2013,2020):
        numerador=[] 
        denominador=[]
        for dados in Adicionais_Norte_Nordeste:
            if dados['campo'] =='Provenientes da União' and dados['Ano']==anos and dados['Porte']==Porte:
                numerador.append(dados['Receitas_realizadas_Bimestre']),
        try:
            tabela[str(anos)].append(sum(numerador)/1000000)
        except:
            tabela[str(anos)].append(0)
    tabela['Porte'].append(Porte)

list_csv(deflação(tabela),'Indicador Dependencia Sus - Porte')

# 36 – Receita líquida de impostos das Regiões Norte/Nordeste, 2013 a 2019, em milhões de reais.
tabela={'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Apuração_Nordeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))

    tabela[str(ano)].append(sum(Numerador)/1000000)
tabela['Região'].append('Nordeste')


for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Apuração_Norte):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))

    tabela[str(ano)].append(sum(Numerador)/1000000)
tabela['Região'].append('Norte')

list_csv(deflação(tabela),'Receita líquida de impostos das Regiões Norte_Nordeste')

# 37 – Receita de Transferências Constitucionais e Legais da União das Regiões Norte/Nordeste, 2013 a 2019, em milhões de reais.
tabela={'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Apuração_Nordeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))

    tabela[str(ano)].append(sum(Numerador)/1000000)
tabela['Região'].append('Nordeste')

for ano in range(2013,2020):
    Numerador =[]
    for dados in list(Apuração_Norte):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])

    tabela[str(ano)].append(sum(Numerador)/1000000)
tabela['Região'].append('Norte')

list_csv(deflação(tabela),'Receita líquida de impostos das Regiões Norte_Nordeste')


# 38 - Valores de Receitas Adicionais (SUS) 
tabela={'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Porte in ['1000000','5000000','10000000','15000000','20000000']:   
    for anos in range(2013,2020):
        numerador=[] 
        denominador=[]
        for dados in Adicionais_Norte_Nordeste:
            if dados['campo'] =='Provenientes da União' and dados['Ano']==anos and dados['Porte']==Porte:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
        try:
            tabela[str(anos)].append(sum(numerador)/1000000)
        except:
            tabela[str(anos)].append(0)
    tabela['Porte'].append(Porte)

list_csv(deflação(tabela),'Indicador Dependencia Sus - Porte')


# 39 - Receita total do SUS da Região Norte, 2013 a 2019, em milhões de reais
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:   
    for anos in range(2013,2020):
        numerador=[] 
        for dados in Adicionais_Norte:
            if dados['campo'] =='TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Ano']==anos and dados['Estado']==Estado:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
        
        tabela[str(anos)].append(sum(numerador)/1000000)
    tabela['Estado'].append(Estado)

list_csv(deflação(tabela),'Receita Total do SUS - Região Norte')

# 40 - Receita total do SUS da Região Norte, 2013 a 2019, em milhões de reais
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        numerador=[] 
        for dados in Adicionais_Norte:
            if dados['campo'] =='TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Ano']==anos and dados['Estado']==Estado:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
=        
        tabela[str(anos)].append(sum(numerador)/1000000)
    tabela['Estado'].append(Estado)

list_csv(deflação(tabela),'Receita Total do SUS - Região Nordeste')

# 41 - Indicador de Dependência do Sus da Região Norte, 2013 a 2019, em milhões de reais
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        numerador=[] 
        denominador=[]
        for dados in Adicionais_Norte:
            if dados['campo'] == 'Provenientes da União' and dados['Ano']==anos and dados['Estado']== Estado:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] =='TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Ano']==anos and dados['Estado']==Estado:
                denominador.append(dados['Receitas_realizadas_Bimestre'])
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)

    tabela['Estado'].append(Estado)

list_csv(tabela,'Indicador de Dependência do Sus 1 - Região Norte')


# 42 - Indicador de Dependência do Sus da Região Nordeste, 2013 a 2019, em milhões de reais
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        numerador=[] 
        denominador=[]
        for dados in Adicionais_Nordeste:
            if dados['campo'] == 'Provenientes da União' and dados['Ano']==anos and dados['Estado']== Estado:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] =='TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Ano']==anos and dados['Estado']==Estado:
                denominador.append(dados['Receitas_realizadas_Bimestre'])
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)

    tabela['Estado'].append(Estado)

list_csv(tabela,'Indicador de Dependência do Sus 1 - Região Nordeste')


# 43 - Indicador de Dependência do Sus da Região Norte, 2013 a 2019, em milhões de reais
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        numerador=[] 
        denominador=[]
        for dados in Adicionais_Norte:
            if dados['campo'] == 'Outras Receitas do SUS' and dados['Ano']==anos and dados['Estado']== Estado:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] =='TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Ano']==anos and dados['Estado']==Estado:
                denominador.append(dados['Receitas_realizadas_Bimestre'])
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)

    tabela['Estado'].append(Estado)

list_csv(tabela,'Indicador de Dependência do Sus 2 - Região Norte')


# 44 - Indicador de Dependência do Sus da Região Nordeste, 2013 a 2019, em milhões de reais
tabela={'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for Estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        numerador=[] 
        denominador=[]
        for dados in Adicionais_Nordeste:
            if dados['campo'] == 'Outras Receitas do SUS' and dados['Ano']==anos and dados['Estado']== Estado:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] =='TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Ano']==anos and dados['Estado']==Estado:
                denominador.append(dados['Receitas_realizadas_Bimestre'])
        try:
            tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except:
            tabela[str(anos)].append(0)

    tabela['Estado'].append(Estado)

list_csv(tabela,'Indicador de Dependência do Sus 2 - Região Nordeste')
