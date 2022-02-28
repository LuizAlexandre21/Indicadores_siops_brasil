# Pacotes 
from database import *
import  numpy as np
#import plotly.express as px
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
        if ano not in ['Estado','IDH','Estado','Região']:
            lista = []  
            for series in serie[ano]:
                lista.append(series*inflação[ano])
            deflation[ano]= lista
        else:
            deflation[ano]= serie[ano]
    return deflation

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
   dados_apuração = (Populacao.select(Populacao.Estado,Populacao.Ano,Populacao.População,Populacao.IDH,Populacao.Estado,Receitas_apuracao_sps_estadual.campo,Receitas_apuracao_sps_estadual.Receitas_realizadas_Bimestre).distinct().join(Receitas_apuracao_sps_estadual, on=((Populacao.Estado == Receitas_apuracao_sps_estadual.estado) &(Populacao.Ano == Receitas_apuracao_sps_estadual.ano))))
   dados_adicionais = (Populacao.select(Populacao.Estado,Populacao.Ano,Populacao.População,Populacao.IDH,Populacao.Estado,Receitas_adicionais_financiamento_estadual.campo,Receitas_adicionais_financiamento_estadual.Receitas_realizadas_Bimestre).distinct().join(Receitas_adicionais_financiamento_estadual, on=((Populacao.Estado == Receitas_adicionais_financiamento_estadual.estado) &(Populacao.Ano == Receitas_adicionais_financiamento_estadual.ano))))
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

# Sul 
Apuração_Sul =[]
for dados in list(dados_apuração.dicts()):
    Sul = ['Rio Grande do Sul','Paraná','Santa Catarina']
    if dados.get("Estado") in Sul:
        Apuração_Sul.append(dados)

Adicionais_Sul = []
for dados in list(dados_adicionais.dicts()):
    Sul = ['Rio Grande do Sul','Paraná','Santa Catarina']
    if dados.get("Estado") in Sul:
        Adicionais_Sul.append(dados)

# Sudeste 
Apuração_Sudeste =[]
for dados in list(dados_apuração.dicts()):
    Sudeste = ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']
    if dados.get("Estado") in Sudeste:
        Apuração_Sudeste.append(dados)

Adicionais_Sudeste = []
for dados in list(dados_adicionais.dicts()):
    Sudeste = ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']
    if dados.get("Estado") in Sudeste:
        Adicionais_Sudeste.append(dados)

# Centro Oeste
Apuração_Centro_Oeste =[]
for dados in list(dados_apuração.dicts()):
    Centro = ['Goiás','Mato Grosso','Mato Grosso do Sul']
    if dados.get("Estado") in Centro:
        Apuração_Centro_Oeste.append(dados)

Adicionais_Centro_Oeste = []
for dados in list(dados_adicionais.dicts()):
    Centro = ['Goiás','Mato Grosso','Mato Grosso do Sul']
    if dados.get("Estado") in Centro:
        Adicionais_Centro_Oeste.append(dados)

# 1. Receita Total por Região - Milhoes
# 1.1 Norte 
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Apuração_Norte:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                denominador = dados['Receitas_realizadas_Bimestre']
        Tabela_Norte[str(anos)].append((numerador+denominador)/1000000)
    Tabela_Norte['Estado'].append(estado)

list_csv(deflação(Tabela_Norte),"Receita Total por Região - Norte")

# 1.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        for dados in Apuração_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                denominador = dados['Receitas_realizadas_Bimestre']
        Tabela_Nordeste[str(anos)].append((numerador+denominador)/1000000)
    Tabela_Nordeste['Estado'].append(estado)

list_csv(deflação(Tabela_Nordeste),"Receita Total por Região - Nordeste")

# 1.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Apuração_Sudeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                denominador = dados['Receitas_realizadas_Bimestre']
        Tabela_Sudeste[str(anos)].append((numerador+denominador)/1000000)
    Tabela_Sudeste['Estado'].append(estado)

list_csv(deflação(Tabela_Sudeste),"Receita Total por Região - Sudeste")

# 1.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        for dados in Apuração_Centro_Oeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                denominador = dados['Receitas_realizadas_Bimestre']
        Tabela_Centro[str(anos)].append((numerador+denominador)/1000000)
    Tabela_Centro['Estado'].append(estado) 

list_csv(deflação(Tabela_Centro),"Receita Total por Região - Centro Oeste")

# 1.5 Sul 

Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
        for dados in Apuração_Sul:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                denominador = dados['Receitas_realizadas_Bimestre']
        Tabela_Sul[str(anos)].append((numerador+denominador)/1000000)
    Tabela_Sul['Estado'].append(estado) 

list_csv(deflação(Tabela_Sul),"Receita Total por Região - Sul")

# 1.6 Brasil 
Regiões = {'Sul':Tabela_Sul,'Sudeste':Tabela_Sudeste,'Nordeste':Tabela_Nordeste,'Norte':Tabela_Norte,'Centro Oeste':Tabela_Centro}

Tabela_Brasil = {'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for região in Regiões.keys():
    for ano in range(2013,2020):
        Tabela_Brasil[str(ano)].append(sum(Regiões[região][str(ano)]))
    Tabela_Brasil['Região'].append(região)

list_csv(deflação(Tabela_Brasil),"Receita Total por Região - Brasil")

# 2. Receita Total por Região - Per Capita 
# 2.1 Norte
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Apuração_Norte:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                campo3 = int(int(dados['População']))
        Tabela_Norte[str(anos)].append(round((campo1 + campo2)/campo3,2))
    Tabela_Norte['Estado'].append(estado)

list_csv(deflação(Tabela_Norte),"Receita Total por Região per capita - Norte")

# 2.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        for dados in Apuração_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                campo3 = int(int(dados['População']))
        Tabela_Nordeste[str(anos)].append(round((campo1 + campo2)/campo3,2))
    Tabela_Nordeste['Estado'].append(estado)

list_csv(deflação(Tabela_Nordeste),"Receita Total por Região per capita - Nordeste")

# 2.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Apuração_Sudeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                campo3 = int(int(dados['População']))
        Tabela_Sudeste[str(anos)].append(round((campo1 + campo2)/campo3,2))
    Tabela_Sudeste['Estado'].append(estado)

list_csv(deflação(Tabela_Sudeste),"Receita Total por Região per capita - Sudeste")

# 2.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        for dados in Apuração_Centro_Oeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                campo3 = int(int(dados['População']))
        Tabela_Centro[str(anos)].append(round((campo1 + campo2)/campo3,2))
    Tabela_Centro['Estado'].append(estado)  # TODO: Corrigir esse detalhe
        
list_csv(deflação(Tabela_Centro),"Receita Total por Região per capita - Centro Oeste")

# 2.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
        for dados in Apuração_Sul:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                campo3 = int(int(dados['População']))
        Tabela_Sul[str(anos)].append(round((campo1 + campo2)/campo3,2))
    Tabela_Sul['Estado'].append(estado)  # TODO: Corrigir esse detalhe

list_csv(deflação(Tabela_Sul),"Receita Total por Região per capita - Sul")

# 2.6 Brasil 
Tabela_Brasil = {'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for anos in range(2013,2020):
    Sudeste = {'Total':[],'População':[]}
    Sul = {'Total':[],'População':[]}
    Centro = {'Total':[],'População':[]}
    Norte = {'Total':[],'População':[]}
    Nordeste = {'Total':[],'População':[]}
    for dados in list(dados_apuração.dicts()):
        for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Norte['Total'].append(campo1+campo2)
                Norte['População'].append(int(dados['População']))
        for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Nordeste['Total'].append(campo1+campo2)
                Nordeste['População'].append(int(dados['População']))
        for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Sul['Total'].append(campo1+campo2)
                Sul['População'].append(int(dados['População']))
        for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Centro['Total'].append(campo1+campo2)
                Centro['População'].append(int(dados['População']))
        for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Sudeste['Total'].append(campo1+campo2)
                Sudeste['População'].append(int(dados['População']))
    Tabela_Brasil[str(anos)].append(sum(Sudeste['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Sul['Total'])/sum(Sul['População']))
    Tabela_Brasil[str(anos)].append(sum(Centro['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Norte['Total'])/sum(Norte['População']))
    Tabela_Brasil[str(anos)].append(sum(Nordeste['Total'])/sum(Nordeste['População']))
Tabela_Brasil['Região'] = ['Sudeste','Sul','Centro','Norte','Nordeste']

list_csv(deflação(Tabela_Brasil),"Receita Total por Região per capita - Brasil")

# 3. Receita Líquida - Milhões
# 3.1 Norte 
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Apuração_Norte:
           if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                Tabela_Norte[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Norte['Estado'].append(estado)

list_csv(deflação(Tabela_Norte),"Receita Líquida - Norte")

# 3.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        for dados in Apuração_Nordeste:
           if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                Tabela_Nordeste[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Nordeste['Estado'].append(estado)

list_csv(deflação(Tabela_Nordeste),"Receita Líquida - Nordeste")

# 3.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Apuração_Sudeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                Tabela_Sudeste[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Sudeste['Estado'].append(estado)

list_csv(deflação(Tabela_Sudeste),"Receita Líquida - Sudeste")

# 3.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        for dados in Apuração_Centro_Oeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA' :
                if dados['Estado'] == estado and dados['Ano']==anos:
                    Tabela_Centro[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Centro['Estado'].append(estado)  # TODO: Corrigir esse detalhe

list_csv(deflação(Tabela_Centro),"Receita Líquida - Centro Oeste")

# 3.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
        for dados in Apuração_Sul:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                Tabela_Sul[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Sul['Estado'].append(estado)

list_csv(deflação(Tabela_Sul),"Receita Líquida - Sul")

# 3.6 Brasil 
Regiões = {'Sul':Tabela_Sul,'Sudeste':Tabela_Sudeste,'Nordeste':Tabela_Nordeste,'Norte':Tabela_Norte,'Centro Oeste':Tabela_Centro}
Tabela_Brasil = {'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for região in Regiões.keys():
    for ano in range(2013,2020):
        Tabela_Brasil[str(ano)].append(sum(Regiões[região][str(ano)]))
    Tabela_Brasil['Região'].append(região)
    
list_csv(deflação(Tabela_Brasil),"Receita Líquida - Brasil")

# 4. Receita Líquida - per capita
# 4.1 Norte
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Apuração_Norte:
           if dados['campo'] =='RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                Tabela_Norte[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Norte['Estado'].append(estado)

list_csv(deflação(Tabela_Norte),"Receita Líquida per capita - Norte")

# 4.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        for dados in Apuração_Nordeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                Tabela_Nordeste[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Nordeste['Estado'].append(estado)

list_csv(deflação(Tabela_Nordeste),"Receita Líquida per capita - Nordeste")

# 4.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Apuração_Sudeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos: 
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                Tabela_Sudeste[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Sudeste['Estado'].append(estado)
list_csv(deflação(Tabela_Sudeste),"Receita Líquida per capita - Sudeste")

# 4.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        for dados in Apuração_Centro_Oeste:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA':
                if dados['Estado'] == estado and dados['Ano']==anos:
                    numerador = dados['Receitas_realizadas_Bimestre']
                    denominador = int(dados['População'])
                    Tabela_Centro[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Centro['Estado'].append(estado)  # TODO: Corrigir esse detalhe

list_csv(deflação(Tabela_Centro),"Receita Líquida per capita - Centro Oeste")

# 4.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
        for dados in Apuração_Sul:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano'] == anos:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                Tabela_Sul[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Sul['Estado'].append(estado)

list_csv(deflação(Tabela_Sul),"Receita Líquida per capita - Sul")

# 4.6 Brasil 
Tabela_Brasil = {'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for anos in range(2013,2020):
    Sudeste = {'Total':[],'População':[]}
    Sul = {'Total':[],'População':[]}
    Centro = {'Total':[],'População':[]}
    Norte = {'Total':[],'População':[]}
    Nordeste = {'Total':[],'População':[]}
    for dados in list(dados_apuração.dicts()):
        for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                Norte['Total'].append(dados['Receitas_realizadas_Bimestre'])
                Norte['População'].append(int(dados['População']))
        for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                Nordeste['Total'].append(dados['Receitas_realizadas_Bimestre'])       
                Nordeste['População'].append(int(dados['População']))
        for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                Sul['Total'].append(dados['Receitas_realizadas_Bimestre'])     
                Sul['População'].append(int(dados['População']))

        for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and dados['Estado'] == estado and dados['Ano']==anos:
                Sudeste['Total'].append(dados['Receitas_realizadas_Bimestre'])     
                Sudeste['População'].append(int(dados['População']))
    Tabela_Brasil[str(anos)].append(sum(Sudeste['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Sul['Total'])/sum(Sul['População']))
    Tabela_Brasil[str(anos)].append(sum(Centro['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Norte['Total'])/sum(Norte['População']))
    Tabela_Brasil[str(anos)].append(sum(Nordeste['Total'])/sum(Nordeste['População']))
Tabela_Brasil['Região'] = ['Sudeste','Sul','Centro','Norte','Nordeste']

list_csv(deflação(Tabela_Brasil),"Receita Líquida per capita - Brasil")

# 5.Receita de Transferências Constitucionais e Legais da União - Milhões 
# 5.1 Norte 
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Apuração_Norte:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                Tabela_Norte[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Norte['Estado'].append(estado)

list_csv(deflação(Tabela_Norte),"Receita de Transferências Constitucionais e Legais da União - Norte")

# 5.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        for dados in Apuração_Nordeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                Tabela_Nordeste[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Nordeste['Estado'].append(estado)

list_csv(deflação(Tabela_Nordeste),"Receita de Transferências Constitucionais e Legais da União - Nordeste")

# 5.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Apuração_Sudeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                Tabela_Sudeste[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Sudeste['Estado'].append(estado)

list_csv(deflação(Tabela_Sudeste),"Receita de Transferências Constitucionais e Legais da União - Sudeste")

# 5.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        for dados in Apuração_Centro_Oeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' or dados['campo']=='RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':
                if dados['Estado'] == estado and dados['Ano'] == anos:
                    Tabela_Centro[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Centro['Estado'].append(estado)  # TODO: Corrigir esse detalhe
list_csv(deflação(Tabela_Centro),"Receita de Transferências Constitucionais e Legais da União - Centro")

# 5.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
        for dados in Apuração_Sul:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                Tabela_Sul[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Sul['Estado'].append(estado)

list_csv(deflação(Tabela_Sul),"Receita de Transferências Constitucionais e Legais da União - Sul")

# 5.6 Brasil 
Regiões = {'Sul':Tabela_Sul,'Sudeste':Tabela_Sudeste,'Nordeste':Tabela_Nordeste,'Norte':Tabela_Norte,'Centro Oeste':Tabela_Centro}

Tabela_Brasil = {'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for região in Regiões.keys():
    for ano in range(2013,2020):
        Tabela_Brasil[str(ano)].append(sum(Regiões[região][str(ano)]))
    Tabela_Brasil['Região'].append(região)
    
list_csv(deflação(Tabela_Brasil),"Receita de Transferências Constitucionais e Legais da União - Brasil")

# 6 Receita de Transferências Constitucionais e Legais da União - Per Capita
# 6.1 Norte
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Apuração_Norte:
           if dados['campo'] =='RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                Tabela_Norte[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Norte['Estado'].append(estado)

list_csv(deflação(Tabela_Norte),"Receita de Transferências Constitucionais e Legais da União per capita - Sul")


# 6.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        for dados in Apuração_Nordeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                Tabela_Nordeste[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Nordeste['Estado'].append(estado)

list_csv(deflação(Tabela_Nordeste),"Receita de Transferências Constitucionais e Legais da União per capita - Nordeste")

# 6.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Apuração_Sudeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)'  and dados['Estado'] == estado:
                numerador = dados['Receitas_realizadas_Bimestre']
                denominador = int(dados['População'])
                Tabela_Sudeste[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Sudeste['Estado'].append(estado)

list_csv(deflação(Tabela_Sudeste),"Receita de Transferências Constitucionais e Legais da União per capita - Sudeste")

# 6.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        for dados in Apuração_Centro_Oeste:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' or dados['campo']=='RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':  
                if dados['Estado'] == estado and dados['Ano'] == anos:
                    numerador = dados['Receitas_realizadas_Bimestre']
                    denominador = int(dados['População'])
                    Tabela_Centro[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Centro['Estado'].append(estado)  # TODO: Corrigir esse detalhe

list_csv(deflação(Tabela_Centro),"Receita de Transferências Constitucionais e Legais da União per capita - Centro Oeste")

# 6.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
       for dados in Apuração_Sul:
        if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)'  and dados['Estado'] == estado:
            numerador = dados['Receitas_realizadas_Bimestre']
            denominador = int(dados['População'])
            Tabela_Sul[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Sul['Estado'].append(estado)

list_csv(deflação(Tabela_Sul),"Receita de Transferências Constitucionais e Legais da União per capita - Sul")

# 6.6 Brasil 
Tabela_Brasil = {'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for anos in range(2013,2020):
    Sudeste = {'Total':[],'População':[]}
    Sul = {'Total':[],'População':[]}
    Centro = {'Total':[],'População':[]}
    Norte = {'Total':[],'População':[]}
    Nordeste = {'Total':[],'População':[]}
    for dados in list(dados_apuração.dicts()):
        for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)'  and dados['Estado'] == estado and dados['Ano']==anos:
                Norte['Total'].append(dados['Receitas_realizadas_Bimestre'])
                Norte['População'].append(int(dados['População']))
        for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)'  and dados['Estado'] == estado and dados['Ano']==anos:
                Nordeste['Total'].append(dados['Receitas_realizadas_Bimestre'])       
                Nordeste['População'].append(int(dados['População']))
        for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
            if dados['campo'] =='RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)'  and dados['Estado'] == estado and dados['Ano']==anos:
                Sul['Total'].append(dados['Receitas_realizadas_Bimestre'])     
                Sul['População'].append(int(dados['População']))
        for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' or dados['campo']=='RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':
                if dados['Estado'] == estado and dados['Ano']==anos:
                    Centro['Total'].append(dados['Receitas_realizadas_Bimestre'])     
                    Centro['População'].append(int(dados['População']))
        for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
            if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)'  and dados['Estado'] == estado and dados['Ano']==anos:
                Sudeste['Total'].append(dados['Receitas_realizadas_Bimestre'])     
                Sudeste['População'].append(int(dados['População']))
    Tabela_Brasil[str(anos)].append(sum(Sudeste['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Sul['Total'])/sum(Sul['População']))
    Tabela_Brasil[str(anos)].append(sum(Centro['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Norte['Total'])/sum(Norte['População']))
    Tabela_Brasil[str(anos)].append(sum(Nordeste['Total'])/sum(Nordeste['População']))
Tabela_Brasil['Região'] = ['Sudeste','Sul','Centro','Norte','Nordeste']

list_csv(deflação(Tabela_Brasil),"Receita de Transferências Constitucionais e Legais da União per capita - Brasil")

# 7 Indicador de Capacidade 
# 7.1 Norte 
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Apuração_Norte:
           if dados['Estado'] == estado and dados['Ano']:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador = campo1
                    Tabela_Norte[str(dados['Ano'])].append(round(numerador/(campo1+campo2),2))
    Tabela_Norte['Estado'].append(estado)

list_csv(Tabela_Norte,"Indicador de Capacidade - Norte")

# 7.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        for dados in Apuração_Nordeste:
            if dados['Estado'] == estado:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador = campo1
                    Tabela_Nordeste[str(dados['Ano'])].append(round(numerador/(campo1+campo2),2))
    Tabela_Nordeste['Estado'].append(estado)

list_csv(Tabela_Nordeste,"Indicador de Capacidade - Nordeste")

# 7.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Apuração_Sudeste:
            if dados['Estado'] == estado:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador =campo1
                    Tabela_Sudeste[str(dados['Ano'])].append(round(numerador/(campo1+campo2),2))
    Tabela_Sudeste['Estado'].append(estado)

list_csv(Tabela_Sudeste,"Indicador de Capacidade - Sudeste")

# 7.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        for dados in Apuração_Centro_Oeste:
            if dados['Estado'] == estado:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador = campo1
                    Tabela_Centro[str(dados['Ano'])].append(round(numerador/(campo1+campo2),2))
    Tabela_Centro['Estado'].append(estado)

list_csv(Tabela_Centro,"Indicador de Capacidade_Centro")


# 7.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
        for dados in Apuração_Sul:
            if dados['Estado'] == estado:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador = campo1 
                    Tabela_Sudeste[str(dados['Ano'])].append(round(numerador/(campo1+campo2),2))
    Tabela_Sul['Estado'].append(estado)

list_csv(Tabela_Sul,"Indicador de Capacidade - Sul")

# 7.6 Brasil 
Tabela_Brasil = {'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for anos in range(2013,2020):
    Sudeste = {'Total':[],'População':[]}
    Sul = {'Total':[],'População':[]}
    Centro = {'Total':[],'População':[]}
    Norte = {'Total':[],'População':[]}
    Nordeste = {'Total':[],'População':[]}
    for dados in list(dados_apuração.dicts()):
        for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Norte['Total'].append(campo1/(campo1+campo2))
                Norte['População'].append(int(dados['População']))
        for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Nordeste['Total'].append(campo1/(campo1+campo2))
                Nordeste['População'].append(int(dados['População']))
        for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Sul['Total'].append(campo1/(campo1+campo2))
                Sul['População'].append(int(dados['População']))
        for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Centro['Total'].append(campo1/(campo1+campo2))
                Centro['População'].append(int(dados['População']))
        for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Sudeste['Total'].append(campo1/(campo1+campo2))
                Sudeste['População'].append(int(dados['População']))
    Tabela_Brasil[str(anos)].append(sum(Sudeste['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Sul['Total'])/sum(Sul['População']))
    Tabela_Brasil[str(anos)].append(sum(Centro['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Norte['Total'])/sum(Norte['População']))
    Tabela_Brasil[str(anos)].append(sum(Nordeste['Total'])/sum(Nordeste['População']))
Tabela_Brasil['Região'] = ['Sudeste','Sul','Centro','Norte','Nordeste']

list_csv(Tabela_Brasil,"Indicador de Capacidade - Brasil")


# 8.Indicador Dependencia 
# 8.1 Norte
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Apuração_Norte:
           if dados['Estado'] == estado and dados['Ano']:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    Tabela_Norte[str(dados['Ano'])].append(round(campo2/(campo1+campo2),2))
    Tabela_Norte['Estado'].append(estado)

list_csv(Tabela_Norte,"Indicador de Dependencia - Norte")

# 8.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        numerador = []
        denominador = []
        for dados in Apuração_Nordeste:
            if dados['Estado'] == estado:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador.append(campo1)
        Tabela_Nordeste[str(dados['Ano'])].append(round(campo2/(campo1+campo2),2))
    Tabela_Nordeste['Estado'].append(estado)

list_csv(Tabela_Nordeste,"Indicador de Dependencia - Nordeste")

# 8.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        numerador = []
        denominador = []
        for dados in Apuração_Sudeste:
            if dados['Estado'] == estado:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador.append(campo1)
                    Tabela_Sudeste[str(dados['Ano'])].append(round(campo2/(campo1+campo2),2))
    Tabela_Sudeste['Estado'].append(estado)

list_csv(Tabela_Sudeste,"Indicador de Dependencia - Sudeste")

# 7.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        numerador = []
        denominador = []        
        for dados in Apuração_Centro_Oeste:
            if dados['Estado'] == estado:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador.append(campo1)
                    Tabela_Centro[str(dados['Ano'])].append(round(campo2/(campo1+campo2),2))
    Tabela_Centro['Estado'].append(estado)

list_csv(Tabela_Centro,"Indicador de  Dependencia Centro")


# 7.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
        numerador = []
        denominador = []        
        for dados in Apuração_Sul:
            if dados['Estado'] == estado:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano'] == anos :
                    campo1 = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano'] == anos:
                    campo2 = dados['Receitas_realizadas_Bimestre']
                    numerador.append(campo1)
                    Tabela_Sudeste[str(dados['Ano'])].append(round(campo2/(campo1+campo2),2))
    Tabela_Sul['Estado'].append(estado)

list_csv(Tabela_Sul,"Indicador de  Dependencia - Sul")

# 7.6 Brasil 
Tabela_Brasil = {'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for anos in range(2013,2020):
    Sudeste = {'Total':[],'População':[]}
    Sul = {'Total':[],'População':[]}
    Centro = {'Total':[],'População':[]}
    Norte = {'Total':[],'População':[]}
    Nordeste = {'Total':[],'População':[]}
    for dados in list(dados_apuração.dicts()):
        for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Norte['Total'].append(campo2/(campo1+campo2))
                Norte['População'].append(int(dados['População']))
        for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Nordeste['Total'].append(campo2/(campo1+campo2))
                Nordeste['População'].append(int(dados['População']))
        for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Sul['Total'].append(campo2/(campo1+campo2))
                Sul['População'].append(int(dados['População']))
        for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Centro['Total'].append(campo2/(campo1+campo2))
                Centro['População'].append(int(dados['População']))
        for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' and  dados['Estado'] == estado and dados['Ano']==anos:
                campo1 = dados['Receitas_realizadas_Bimestre']
            elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' and dados['Estado'] == estado and dados['Ano']==anos:
                campo2 = dados['Receitas_realizadas_Bimestre']
                Sudeste['Total'].append(campo2/(campo1+campo2))
                Sudeste['População'].append(int(dados['População']))
    Tabela_Brasil[str(anos)].append(sum(Sudeste['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Sul['Total'])/sum(Sul['População']))
    Tabela_Brasil[str(anos)].append(sum(Centro['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Norte['Total'])/sum(Norte['População']))
    Tabela_Brasil[str(anos)].append(sum(Nordeste['Total'])/sum(Nordeste['População']))
Tabela_Brasil['Região'] = ['Sudeste','Sul','Centro','Norte','Nordeste']

list_csv(Tabela_Brasil,"Indicador de  Dependencia - Brasil")

# 9.Indicador Dependencia Sus
# 9.1 Norte
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for anos in range(2013,2020):
        for dados in Adicionais_Norte:
            if dados['Estado'] == estado and dados['Ano']==anos:
                if dados['campo'] == 'Provenientes da União':
                    numerador = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                    denominador = dados['Receitas_realizadas_Bimestre']
                    Tabela_Norte[str(dados['Ano'])].append(round(numerador/denominador,2))
        Tabela_Norte['Estado'].append(estado)

list_csv(Tabela_Norte,"Indicador de Dependencia Sus - Norte")

# 9.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for anos in range(2013,2020):
        for dados in Adicionais_Nordeste:
            if dados['Estado'] == estado and dados['Ano']==anos:
                if dados['campo'] == 'Provenientes da União':
                    numerador = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                    denominador = dados['Receitas_realizadas_Bimestre']
                    Tabela_Nordeste[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Nordeste['Estado'].append(estado)

list_csv(Tabela_Nordeste,"Indicador de Dependencia Sus - Nordeste")

# 9.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Adicionais_Sudeste:
            if dados['Estado'] == estado and dados['Ano']==anos:
                if dados['campo'] == 'Provenientes da União':
                    numerador = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] ==  'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                    denominador = dados['Receitas_realizadas_Bimestre']
                    Tabela_Sudeste[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Sudeste['Estado'].append(estado)

list_csv(Tabela_Sudeste,"Indicador de Dependencia Sus - Sudeste")

# 9.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for anos in range(2013,2020):
        for dados in Adicionais_Centro_Oeste:
            if dados['Estado'] == estado and dados['Ano']==anos:
                if dados['campo'] == 'Provenientes da União':
                    numerador = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                    denominador = dados['Receitas_realizadas_Bimestre']
                    try:
                        Tabela_Centro[str(dados['Ano'])].append(round(numerador/denominador,2))
                    except:
                        Tabela_Centro[str(dados['Ano'])].append(0.0000001)
    Tabela_Centro['Estado'].append(estado)


list_csv(Tabela_Centro,"Indicador de Dependencia Sus - Centro Oeste")

# 9.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for anos in range(2013,2020):
        for dados in Adicionais_Norte:
            if dados['Estado'] == estado and dados['Ano']==anos:
                if dados['campo'] == 'Provenientes da União':
                    numerador = dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                    denominador = dados['Receitas_realizadas_Bimestre']
                    Tabela_Sul[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Sul['Estado'].append(estado)

list_csv(Tabela_Sul,"Indicador de Dependencia Sus - Sul")

# 9.6 Brasil 
Tabela_Brasil = {'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for anos in range(2013,2020):
    Sudeste = {'numerador':[],'denominador':[]}
    Sul = {'numerador':[],'denominador':[]}
    Centro = {'numerador':[],'denominador':[]}
    Norte = {'numerador':[],'denominador':[]}
    Nordeste = {'numerador':[],'denominador':[]}
    for dados in list(dados_adicionais.dicts()):
        for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
            if dados['campo'] =='Provenientes da União' and dados['Estado'] == estado and dados['Ano']==anos:
                Norte['numerador'].append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Norte['denominador'].append(dados['Receitas_realizadas_Bimestre'])
        for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
            if dados['campo'] =='Provenientes da União' and dados['Estado'] == estado and dados['Ano']==anos:
                Nordeste['numerador'].append(dados['Receitas_realizadas_Bimestre'])       
            elif dados['campo'] ==  'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Nordeste['denominador'].append(dados['Receitas_realizadas_Bimestre'])
        for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
            if dados['campo'] =='Provenientes da União'  and dados['Estado'] == estado and dados['Ano']==anos :
                Sul['numerador'].append(dados['Receitas_realizadas_Bimestre'])     
            elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Sul['denominador'].append(dados['Receitas_realizadas_Bimestre'])
        for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']:
            if dados['campo'] == 'Provenientes da União' and dados['Estado'] == estado and dados['Ano']==anos:
                Centro['numerador'].append(dados['Receitas_realizadas_Bimestre'])     
            elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Centro['denominador'].append(dados['Receitas_realizadas_Bimestre'])
        for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
            if dados['campo'] == 'Provenientes da União' and dados['Estado'] == estado and dados['Ano']==anos:
                Sudeste['numerador'].append(dados['Receitas_realizadas_Bimestre'])     
            elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE'  and dados['Estado'] == estado and dados['Ano']==anos:
                Sudeste['denominador'].append(dados['Receitas_realizadas_Bimestre'])
    Tabela_Brasil[str(anos)].append(sum(Sudeste['numerador'])/sum(Sudeste['denominador']))
    Tabela_Brasil[str(anos)].append(sum(Sul['numerador'])/sum(Sul['denominador']))
    Tabela_Brasil[str(anos)].append(sum(Centro['numerador'])/sum(Sudeste['denominador']))
    Tabela_Brasil[str(anos)].append(sum(Norte['numerador'])/sum(Norte['denominador']))
    Tabela_Brasil[str(anos)].append(sum(Nordeste['numerador'])/sum(Nordeste['denominador']))
Tabela_Brasil['Região'] = ['Sudeste','Sul','Centro','Norte','Nordeste']

list_csv(Tabela_Brasil,"Indicador de Dependencia Sus - Brasil")

# 10. Receitas Adicionais Totais 
# 10.1 Norte 
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Adicionais_Norte:
       if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            Tabela_Norte[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Norte['Estado'].append(estado)

list_csv(deflação(Tabela_Norte),"Receitas Adicionais Totais - Norte")

# 10.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Adicionais_Nordeste:
       if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            Tabela_Nordeste[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Nordeste['Estado'].append(estado)

list_csv(deflação(Tabela_Nordeste),"Receitas Adicionais Totais - Nordeste")

# 10.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for anos in range(2013,2020):
        for dados in Adicionais_Sudeste:
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Tabela_Sudeste[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Sudeste['Estado'].append(estado)

list_csv(deflação(Tabela_Sudeste),"Receitas Adicionais Totais - Sudeste")

# 10.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for dados in Adicionais_Centro_Oeste:
        if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            Tabela_Centro[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Centro['Estado'].append(estado)  # TODO: Corrigir esse detalhe

list_csv(deflação(Tabela_Centro),"Receitas Adicionais Totais - Centro Oeste")

# 10.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for dados in Adicionais_Sul:
        if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            Tabela_Sul[str(dados['Ano'])].append(dados['Receitas_realizadas_Bimestre']/1000000)
    Tabela_Sul['Estado'].append(estado)

list_csv(deflação(Tabela_Sul),"Receitas Adicionais Totais - Sul")

# 10.6 Brasil 
Regiões = {'Sul':Tabela_Sul,'Sudeste':Tabela_Sudeste,'Nordeste':Tabela_Nordeste,'Norte':Tabela_Norte,'Centro Oeste':Tabela_Centro}

Tabela_Brasil = {'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for região in Regiões.keys():
    for ano in range(2013,2020):
        Tabela_Brasil[str(ano)].append(sum(Regiões[região][str(ano)]))
    Tabela_Brasil['Região'].append(região)
list_csv(deflação(Tabela_Brasil),"Receitas Adicionais Totais - Brasil")

# 11. Receitas Adicionais per capita 
# 11.1 Norte 
Tabela_Norte = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in  ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
    for dados in Adicionais_Norte:
       if dados['campo'] =='TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            numerador = dados['Receitas_realizadas_Bimestre']
            denominador = int(dados['População'])
            Tabela_Norte[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Norte['Estado'].append(estado)

list_csv(deflação(Tabela_Norte),"Receitas Adicionais Totais per capita - Norte")

# 11.2 Nordeste 
Tabela_Nordeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
    for dados in Adicionais_Nordeste:
        if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            numerador = dados['Receitas_realizadas_Bimestre']
            denominador = int(dados['População'])
            Tabela_Nordeste[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Nordeste['Estado'].append(estado)

list_csv(deflação(Tabela_Nordeste),"Receitas Adicionais Totais per capita - Nordeste")

# 11.3 Sudeste 
Tabela_Sudeste = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
    for dados in Adicionais_Sudeste:
        if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            numerador = dados['Receitas_realizadas_Bimestre']
            denominador = int(dados['População'])
            Tabela_Sudeste[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Sudeste['Estado'].append(estado)

list_csv(deflação(Tabela_Sudeste),"Receitas Adicionais Totais per capita - Sudeste")

# 11.4 Centro Oeste 
Tabela_Centro = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']: 
    for dados in Adicionais_Centro_Oeste:
        if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            numerador = dados['Receitas_realizadas_Bimestre']
            denominador = int(dados['População'])
            Tabela_Centro[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Centro['Estado'].append(estado)  # TODO: Corrigir esse detalhe

list_csv(deflação(Tabela_Centro),"Receitas Adicionais Totais per capita - Centro Oeste")

# 11.5 Sul 
Tabela_Sul = {'Estado':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
    for dados in Adicionais_Sul:
        if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado:
            numerador = dados['Receitas_realizadas_Bimestre']
            denominador = int(dados['População'])
            Tabela_Sul[str(dados['Ano'])].append(round(numerador/denominador,2))
    Tabela_Sul['Estado'].append(estado)

list_csv(deflação(Tabela_Sul),"Receitas Adicionais Totais per capita - Sul")

# 11.6 Brasil 
Tabela_Brasil = {'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}
for anos in range(2013,2020):
    Sudeste = {'Total':[],'População':[]}
    Sul = {'Total':[],'População':[]}
    Centro = {'Total':[],'População':[]}
    Norte = {'Total':[],'População':[]}
    Nordeste = {'Total':[],'População':[]}
    for dados in list(dados_adicionais.dicts()):
        for estado in ['Acre','Amapá','Amazonas','Roraima','Rondônia','Pará','Tocantins']:
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE'and dados['Estado'] == estado and dados['Ano']==anos:
                Norte['Total'].append(dados['Receitas_realizadas_Bimestre'])
                Norte['População'].append(int(dados['População']))
        for estado in ['Bahia','Ceará','Piauí','Maranhão','Rio Grande do Norte','Paraíba','Pernambuco','Sergipe','Alagoas']:
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Nordeste['Total'].append(dados['Receitas_realizadas_Bimestre'])       
                Nordeste['População'].append(int(dados['População']))
        for estado in ['Rio Grande do Sul','Paraná','Santa Catarina']:
            if dados['campo'] =='TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Sul['Total'].append(dados['Receitas_realizadas_Bimestre'])     
                Sul['População'].append(int(dados['População']))
        for estado in ['Goiás','Mato Grosso','Mato Grosso do Sul']:
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Centro['Total'].append(dados['Receitas_realizadas_Bimestre'])     
                Centro['População'].append(int(dados['População']))
        for estado in ['Rio de Janeiro','Minas Gerais','São Paulo','Espírito Santo']:
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Estado'] == estado and dados['Ano']==anos:
                Sudeste['Total'].append(dados['Receitas_realizadas_Bimestre'])     
                Sudeste['População'].append(int(dados['População']))
    Tabela_Brasil[str(anos)].append(sum(Sudeste['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Sul['Total'])/sum(Sul['População']))
    Tabela_Brasil[str(anos)].append(sum(Centro['Total'])/sum(Sudeste['População']))
    Tabela_Brasil[str(anos)].append(sum(Norte['Total'])/sum(Norte['População']))
    Tabela_Brasil[str(anos)].append(sum(Nordeste['Total'])/sum(Nordeste['População']))
Tabela_Brasil['Região'] = ['Sudeste','Sul','Centro','Norte','Nordeste']

list_csv(deflação(Tabela_Brasil),"Receitas Adicionais Totais per capita - Brasil")
