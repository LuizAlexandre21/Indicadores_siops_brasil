# Bibliotecas 
from peewee import *
from playhouse.db_url import connect 
import logging 

# Definindo o Logger 
logger = logging.getLogger("Database")

# Estabelecendo a conexão 
try:
    database = connect("mysql://alexandre:34340012@localhost:3306/Data_saude")
    logger.info("Database successfully connected")
except:
    logger.error("Database connection failed")

# Criando a classe de conexão mysql 
class MySQLBitField(Field):
    field_type = "bit" 
    
    def __init__(self,*_,**__):
        pass

# Criando a classe do modelo basico 
class BaseModel(Model):
    class Meta:
        database = database 

# Tabela de Receitas Apuração 
class Receitas_apuracao_sps_estadual(BaseModel):
    estado = TextField()
    ano = TextField()
    campo = TextField()
    previsao_inicial = FloatField()
    previsao_atualizada = FloatField()
    Receitas_realizadas_Bimestre = FloatField()
    Receitas_realizadas_Porcentagem = FloatField() 
    class Meta:
        primary_key = False 
        table_name = "Receitas_apuracao_sps_estadual"

# Tabela de Receitas Adicionais
class Receitas_adicionais_financiamento_estadual(BaseModel):
    estado = TextField()
    ano = TextField()
    campo = TextField()
    previsao_inicial = FloatField()
    previsao_atualizada = FloatField()
    Receitas_realizadas_Bimestre = FloatField()
    Receitas_realizadas_Porcentagem = FloatField() 
    class Meta:
        primary_key = False
        table_name = "Receitas_adicionais_financiamento_estadual"

# Tabela de Despesas em Saude por Natureza 
class Despesas_saude_natureza_estadual(BaseModel):
    estado = TextField()
    ano = TextField()
    campo = TextField()
    dotação_inicial = FloatField()
    dotação_atualizada = FloatField()
    despesas_executadas_liquidadas = FloatField()
    despesas_executadas_liquidadas = FloatField()
    class Meta:
        primary_key = False 
        table_name = "Despesas_saude_natureza_estadual"

# Tabela de Despesas de saúde não computadas
class Despesas_saude_nao_computadas_estadual(BaseModel):
    estado = TextField()
    ano = TextField()
    campo = TextField()
    dotação_inicial = FloatField()
    dotação_atualizada = FloatField()
    despesas_executadas_liquidadas = FloatField()
    despesas_executadas_liquidadas = FloatField()
    class Meta:
        primary_key = False 
        table_name = "Despesas_saude_nao_computadas_estadual"

# Tabela de Despesas de saúde subfunção
class Despesas_saude_subfuncao_estadual(BaseModel):
    estado = TextField()
    ano = TextField()
    campo = TextField()
    dotação_inicial = FloatField()
    dotação_atualizada = FloatField()
    despesas_executadas_liquidadas = FloatField()
    despesas_executadas_liquidadas = FloatField()
    class Meta:
        primary_key = False 
        table_name = "Despesas_saude_subfuncao_estadual"

# Tabela de população 
class Populacao(BaseModel):
    Estado = TextField()
    Ano = IntegerField()
    População = IntegerField()
    IDH = IntegerField()
    Porte = IntegerField()
    class Meta:
        primary_key = False
        table_name = "pop_csv"

