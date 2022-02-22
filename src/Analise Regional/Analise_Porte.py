# Pacotes 
from database import *
import  numpy as np
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

# Segregando os dados por Porte 
## 1. Receita Total por IDH - Milhoes
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador =[]
        denominador =[]
        for dados in list(dados_apuração.dicts()):
            if  dados['Porte'] == porte and dados['Ano']==anos:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA':
                    numerador.append(dados['Receitas_realizadas_Bimestre'])
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)'  or dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':
                    denominador.append(dados['Receitas_realizadas_Bimestre'])
        Tabela[str(anos)].append((sum(numerador)+sum(denominador))/1000000)
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Receita Total por Porte")

# 2. Receita Total por IDH - Per Capita 
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador =[]
        denominador =[]
        pop = []
        for dados in list(dados_apuração.dicts()):
            if  dados['Porte'] == porte and dados['Ano']==anos:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA':
                    numerador.append(dados['Receitas_realizadas_Bimestre'])
                    pop.append(int(dados['População']))
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)'  or dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':
                    denominador.append(dados['Receitas_realizadas_Bimestre'])
        Tabela[str(anos)].append(round((sum(numerador)+sum(denominador))/sum(pop),2))
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Receita Total per capita por Porte")

# 3. Receita Líquida - Milhões
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    numerador = []
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['Porte'] == porte and dados['Ano']==anos:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA' :
                    numerador.append(dados['Receitas_realizadas_Bimestre']/1000000)
        Tabela[str(anos)].append(round(sum(numerador),2))
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Receita Liquida por IDH")

# 4. Receita Total por IDH - Per Capita 
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['Porte'] == porte and dados['Ano']==anos:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA':
                    numerador.append(dados['Receitas_realizadas_Bimestre'])
                    denominador.append(int(dados['População']))
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Receita Liquida por Porte")

# 5.Receita de Transferências Constitucionais e Legais da União 
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador = []
        denominador =[]
        for dados in list(dados_apuração.dicts()):
            if dados['Porte'] == porte and dados['Ano']==anos:
                if dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' or dados['campo'] == 'RECEITAS DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':
                    numerador.append(dados['Receitas_realizadas_Bimestre'])
                    denominador.append(int(dados['População']))

        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['Porte'].append(porte)
list_csv(Tabela,"Receita de Transferências Constitucionais e Legais da União por Porte")

# 6. Receita Total por IDH - Per Capita 
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador = []
        denominador =[]
        for dados in list(dados_apuração.dicts()):
            if dados['Porte'] == porte and dados['Ano']==anos:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo']=='RECEITA DE IMPOSTOS LÍQUIDA': 
                    campo1=dados['Receitas_realizadas_Bimestre']
                    numerador.append(campo1)
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' or dados['campo'] == 'RECEITAS DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':
                    campo2=dados['Receitas_realizadas_Bimestre']
                    denominador.append(campo1+campo2)
        try:
            Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
        except Exception as e:
            print(e)
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Receita de Transferências Constitucionais e Legais da União per capita por porte")

# 7.Indicador de Capacidade 
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_apuração.dicts()):
            if dados['Porte'] == porte and dados['Ano']==anos:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo']=='RECEITA DE IMPOSTOS LÍQUIDA': 
                    campo1=dados['Receitas_realizadas_Bimestre']
                    numerador.append(campo1)
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' or dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':
                    campo2=dados['Receitas_realizadas_Bimestre']
                    denominador.append(campo1+campo2)
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Indicador de Capacidade por Porte")

# 8. Indicador de Depêndencia
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    for anos in range(2013,2020):
        numerador = []
        denominador =[]
        for dados in list(dados_apuração.dicts()):
            if dados['Porte'] == porte and dados['Ano']==anos:
                if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)' or dados['campo']=='RECEITA DE IMPOSTOS LÍQUIDA': 
                    campo1=dados['Receitas_realizadas_Bimestre']
                elif dados['campo'] == 'RECEITA DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS (II)' or dados['campo'] == 'RECEITAS DE TRANSFERÊNCIAS CONSTITUCIONAIS E LEGAIS':
                    campo2=dados['Receitas_realizadas_Bimestre']
                    numerador.append(campo2)
                    denominador.append(campo1+campo2)
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Indicador de Dependencia por Porte")


# 9. Indicador Dependencia Sus
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_adicionais.dicts()):
            if dados['campo'] == 'Provenientes da União' and dados['Porte'] == porte and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
            elif dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Porte'] == porte and dados['Ano']==anos:
                denominador.append(dados['Receitas_realizadas_Bimestre'])
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Indicador de Dependência do SUS por Porte")

# 10. Receitas Adicionais Totais 
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in  ['1000000','5000000','10000000','15000000','20000000']:
    numerador = []
    for anos in range(2013,2020):
        for dados in list(dados_adicionais.dicts()):
            if dados['campo'] == 'Provenientes da União' and dados['Porte'] == porte and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre']/1000000)
        Tabela[str(anos)].append(sum(numerador))
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Receitas Adicionais Totais por Porte")

# 11. Receitas Adicionais per capita 
Tabela = {'Porte':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

for porte in ['1000000','5000000','10000000','15000000','20000000']:
    numerador = []
    denominador =[]
    for anos in range(2013,2020):
        for dados in list(dados_adicionais.dicts()):
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE' and dados['Porte'] == porte and dados['Ano']==anos:
                numerador.append(dados['Receitas_realizadas_Bimestre'])
                denominador.append(int(dados['População']))
        Tabela[str(anos)].append(round(sum(numerador)/sum(denominador),2))
    Tabela['Porte'].append(porte)

list_csv(Tabela,"Receitas Adicionais per capita por Porte")