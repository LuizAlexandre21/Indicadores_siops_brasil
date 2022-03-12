<h1 align=center> Indicadores Siops</h1>
<h2 align=center> Tratamento e analise de dados do SIOPS - Datasus</h2>

--- 
O SIOPS é o sistema informatizado, de alimentação obrigatória e acesso público, operacionalizado pelo Ministério da Saúde, instituído para coleta, recuperação, processamento, armazenamento, organização, e disponibilização de informações referentes às receitas totais e às despesas com saúde dos orçamentos públicos em saúde. O sistema possibilita o acompanhamento e monitoramento da aplicação de recursos em saúde, no âmbito da  União, Estados, Distrito Federal e Municípios, sem prejuízo das atribuições próprias dos Poderes Legislativos e dos Tribunais de Contas.

---
## Informação sobre a analise

### Histórico das versões 

- [x] Versão para o estado do Ceará
- [x] Analise para tabelas de Receitas  
- [x] Calculo dos indicadores: Capacidade e Dependencia (Sus e Governo)
### Versão 0.1 

- Analise das Receitas de Apuração e Adicionais dos Municipios Cearenses 
- Calculo dos indicadores de Capacidade 
- Calculo dos indicadores de Dependência Estadual e Federal 
- Calculo dos indicadores de Dependência do SUS 


## Executando 

### Instalando bibliotecas 

Antes da execução das analises, é necessaria a instalação de um conjunto de bibliotecas para a linguagem python. Para isso basta executar o seguinte comando:

```python 
sudo pip install requirements.txt
```

### Estrutura da Analise

#### 1. Analise por município 

Para a visualização da analise em nivel municipal, basta acessar a pasta *Indices_Municipais*, que é composta pelos seguintes códigos:

- database --> Responsavel pela conexão entre o banco de dados e a analise, através do formato ORM
- Indice de capacidade do Municipio CPM --> Calculo do indice de capacidade de recursos do municipio 
- Indice de Dependência Municipal - IDM --> Calculo do nivel de dependência de recursos governamentais (Estadual e Federal)
- Indice de Dependência Municipal_SUS - IDMS --> Calculo do nivel de dependência de recursos governamentais (Estadual e Federal) para o SUS
- table_schemas -> Conjunto de instruções para construção de tabelas do banco de dados 

Logo para a execução dos códigos, basta executar o seguinte comando:

```python
python <nome do arquivo>.py 
```
Para a criação das tabelas no banco de dados MySQL:

```sql
mysql -u <nome de usuario> -p <Senha> -e table_schemas.sql
```

#### 2. Indicadores por Agregação

Para a visualização da analise ao nivel de agregação de saúde, basta acessar a pasta *Indices_Regiões_Saúde*, que é composta pelos seguintes códigos:

- database --> Responsavel pela conexão entre o banco de dados e a analise, através do formato ORM
- Indicadores_IDH
- Indicadores_Região_Saúde 
- Indicadores_Região_Saúde_2 

:warning: - Essa parte está em construção, logo não é recomendada a sua utilização para analises 


Logo para a execução dos códigos, basta executar o seguinte comando:

```python
python <nome do arquivo>.py 
```
#### 3. Analises dos Indicadores







## Contato 

:bust_in_silhouette: Luiz Alexandre Moreira Barros 

:mailbox_with_mail:	 luizalexandremoreira21@outlook.com

:octocat: https://github.com/LuizAlexandre21

:notebook_with_decorative_cover: http://lattes.cnpq.br/9458204748985902
