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
def deflação(serie,ano_base):
    IPCA = {'2013':5.91068325533108,'2014':6.40747079590815,'2015':10.6730281339751,'2016':6.28798821322138,'2017':2.94742132043471,'2018':3.74558117019155,'2019':4.30615161715953}
    a=[]
    inflação=[1,]
    for i in range(2019,2013,-1):
        a.append(IPCA[str(i)]/100)
        inflação.append(1-sum(a))
    infla = pd.DataFrame({'ano':[2019,2018,2017,2016,2015,2014,2013],'valor':inflação})    
    for i in infla:
        deflac =[]
        for i in range(0,len(serie)):
            row = serie.loc[i]
            ano = row['ano']
            x = (infla[infla['ano']==2019]['valor'].iloc[0]/infla[infla['ano']==ano]['valor'].iloc[0])*serie.loc[i]['Receitas_realizadas_Bimestre']
            deflac.append(x)
        
    return(deflac)

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
        
# Configurando o log  
# Detectando uso de terminal 
if sys.stdout.isatty():
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
else:
    LOG_FORMAT = "%(name)s - %(levelname)s - %(message)s"
    
# Ajustando as configurações do logging 
logging.basicConfig(level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()), format=LOG_FORMAT, datefmt="%Y-%m-%dT%H:%M:%S") 
# Definição de loggers para outros modulos 
# Geral
logger = logging.getLogger("Analise_Norte_Nordeste")

# Importando os dados 
try:
   dados_apuração = (Populacao.select(Populacao.Estado,Populacao.Ano,Populacao.População,,Receitas_apuracao_sps_estadual.campo,Receitas_apuracao_sps_estadual.Receitas_realizadas_Bimestre).join(Receitas_apuracao_sps_estadual, on=((Populacao.Estado == Receitas_apuracao_sps_estadual.estado) &(Populacao.Ano == Receitas_apuracao_sps_estadual.ano))))
   dados_adicionais = (Populacao.select(Populacao.Estado,Populacao.Ano,Populacao.População,Receitas_adicionais_financiamento_estadual.campo,Receitas_adicionais_financiamento_estadual.Receitas_realizadas_Bimestre).join(Receitas_adicionais_financiamento_estadual, on=((Populacao.Estado == Receitas_adicionais_financiamento_estadual.estado) &(Populacao.Ano == Receitas_adicionais_financiamento_estadual.ano))))
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

# Sudeste 
Apuração_Sudeste =[]
for dados in list(dados_apuração.dicts()):
    Sudeste = ['São Paulo','Rio de Janeiro','Espírito Santo','Minas Gerais']
    if dados.get("Estado") in Sudeste:
        Apuração_Sudeste.append(dados)

Adicionais_Sudeste =[]
for dados in list(dados_adicionais.dicts()):
    Sudeste = ['São Paulo','Rio de Janeiro','Espírito Santo','Minas Gerais']
    if dados.get("Estado") in Sudeste:
        Adicionais_Sudeste.append(dados)

# Sul 
Apuração_Sul =[]
for dados in list(dados_apuração.dicts()):
    Sul = ['Rio Grande do Sul','Paraná','Santa Catarina']
    if dados.get("Estado") in Sul:
        Apuração_Sul.append(dados)

Adicionais_Sul =[]
for dados in list(dados_adicionais.dicts()):
    Sul = ['Rio Grande do Sul','Paraná','Santa Catarina']
    if dados.get("Estado") in Sul:
        Adicionais_Sul.append(dados)

# Centro_oeste 
Apuração_Centro =[]
for dados in list(dados_apuração.dicts()):
    Centro = ['Goiás','Distrito Federal','Mato Grosso do Sul','Mato Grosso']
    if dados.get("Estado") in Centro:
        Apuração_Centro.append(dados)

Adicionais_Centro =[]
for dados in list(dados_adicionais.dicts()):
    Centro = ['Goiás','Distrito Federal','Mato Grosso do Sul','Mato Grosso']
    if dados.get("Estado") in Centro:
        Adicionais_Centro.append(dados)

# Receita Estadual Total
tabela={'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

# Receita Estadual Total - Nordeste 
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Apuração_Nordeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Nordeste')

# Receita Estadual Total - Norte 
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Apuração_Norte):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Norte')

# Receita Estadual Total - Sul 
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Apuração_Sul):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Sul')

# Receita Estadual Total - Sudeste 
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Apuração_Sudeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Sudeste')

# Receita Estadual Total - Centro- Oeste
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Apuração_Centro):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Centro-Oeste')

# Exportando dados 
list_csv(tabela,'Receita Estadual Total ')

# Receita Estadual Total - Per_Capita
tabela={'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

# Receita Estadual Total - Nordeste 
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Apuração_Nordeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))
    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Nordeste')

# Receita Estadual Total - Norte
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Apuração_Norte):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))
    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Norte')

# Receita Estadual Total - Sul
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Apuração_Sul):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))
    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Sul')

# Receita Estadual Total - Sudeste
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Apuração_Sudeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))
    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Sudeste')

# Receita Estadual Total - Centro Oeste
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Apuração_Centro):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))
    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Centro-Oeste')

# Exportando dados 
list_csv(tabela,'Receita Estadual per capita')

# Capacidade Estadual
tabela={'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

# Capacidade Estadual Total - Nordeste 
for ano in range(2013,2020):
    Num =[]
    Den =[]
    Capacidade=[]
    for dados in list(Apuração_Nordeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                numerador = dados['Receitas_realizadas_Bimestre']
                Num.append(numerador)
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = dados['Receitas_realizadas_Bimestre']
                Den.append(denominador)
    Capacidade = sum(Num)/sum(Den)
    tabela[str(ano)].append(Capacidade)
tabela['Região'].append('Nordeste')

# Capacidade Estadual Total - Norte
for ano in range(2013,2020):
    Num =[]
    Den =[]
    for dados in list(Apuração_Norte):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                numerador = dados['Receitas_realizadas_Bimestre']
                Num.append(numerador)
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = dados['Receitas_realizadas_Bimestre']
                Den.append(denominador)
    Capacidade = sum(Num)/sum(Den)
    tabela[str(ano)].append(Capacidade)
tabela['Região'].append('Norte')

# Capacidade Estadual Total - Sul
for ano in range(2013,2020):
    Num =[]
    Den =[]
    for dados in list(Apuração_Sul):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                numerador = dados['Receitas_realizadas_Bimestre']
                Num.append(numerador)
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = dados['Receitas_realizadas_Bimestre']
                Den.append(denominador)
    Capacidade = sum(Num)/sum(Den)
    tabela[str(ano)].append(Capacidade)
tabela['Região'].append('Sul')

# Capacidade Estadual Total - Sudeste
for ano in range(2013,2020):
    Num =[]
    Den =[]
    for dados in list(Apuração_Sudeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                numerador = dados['Receitas_realizadas_Bimestre']
                Num.append(numerador)
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = dados['Receitas_realizadas_Bimestre']
                Den.append(denominador)
    Capacidade = sum(Num)/sum(Den)
    tabela[str(ano)].append(Capacidade)
tabela['Região'].append('Sudeste')

# Capacidade Estadual Total - Centro-Oeste
for ano in range(2013,2020):
    Num =[]
    Den =[]
    for dados in list(Apuração_Centro):
        if dados['Ano'] == ano :
            if dados['campo'] == 'RECEITA DE IMPOSTOS LÍQUIDA (I)': 
                numerador = dados['Receitas_realizadas_Bimestre']
                Num.append(numerador)
            if dados['campo'] == 'TOTAL DAS RECEITAS PARA APURAÇÃO DA APLICAÇÃO EM AÇÕES E SERVIÇOS PÚBLICOS DE SAÚDE (IV) = I + II - III':
                denominador = dados['Receitas_realizadas_Bimestre']
                Den.append(denominador)
    Capacidade = sum(Num)/sum(Den)
    tabela[str(ano)].append(Capacidade)
tabela['Região'].append('Centro')

# Exportando dados 
list_csv(tabela,'Capacidade')

# Receita Estadual Adicional - total 
tabela={'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

# Receita Estadual Adicional - Nordeste 
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Adicionais_Nordeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Nordeste')

# Receita Estadual Adicional - Norte
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Adicionais_Norte):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Norte')

# Receita Estadual Adicional - Sul
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Adicionais_Sul):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Sul')

# Receita Estadual Adicional - Sudeste
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Adicionais_Sudeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Sudeste')

# Receita Estadual Adicional - Centro-oeste
for ano in range(2013,2020):
    Receita =[]
    for dados in list(Adicionais_Centro):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Receita.append(dados['Receitas_realizadas_Bimestre'])
    tabela[str(ano)].append(sum(Receita))
tabela['Região'].append('Centro')

# Exportando dados 
list_csv(tabela,'Receita Estadual Adicional Total')

# Receita Estadual Adicional - percapita 
tabela={'Região':[],'2013':[],'2014':[],'2015':[],'2016':[],'2017':[],'2018':[],'2019':[]}

# Receita Estadual Adicional - Nordeste 
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Adicionais_Nordeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))

    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Nordeste')

# Receita Estadual Adicional - Norte
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Adicionais_Norte):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))

    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Norte')

# Receita Estadual Adicional - Sul
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Adicionais_Sul):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))

    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Sul')                Denominador.append(int(dados['População']))

    Numerador =[]
    Denominador =[]
    for dados in list(Adicionais_Sudeste):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))

    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Sudeste')

# Receita Estadual Adicional - Centro-Oeste
for ano in range(2013,2020):
    Numerador =[]
    Denominador =[]
    for dados in list(Adicionais_Centro):
        if dados['Ano'] == ano :
            if dados['campo'] == 'TOTAL RECEITAS ADICIONAIS PARA FINANCIAMENTO DA SAÚDE':
                Numerador.append(dados['Receitas_realizadas_Bimestre'])
                Denominador.append(int(dados['População']))

    tabela[str(ano)].append(sum(Numerador)/sum(Denominador))
tabela['Região'].append('Centro-Oeste')

# Exportando dados 
list_csv(tabela,'Receita Estadual Adicional - Percapita')


