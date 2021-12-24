# Pacotes
import plotly.graph_objects as go
from colour import Color 


# Criando a classe de graficos 
class plots:
    # Gerando os gradientes 
    def colour_gradient(start_color,stop_color,num):
        start = Color(start_color)
        colors = list(start.range_to(Color("green"),num))
        vector =[]
        for color in colors:
            vector.append(color)
        return vector


    # Preparando os dados
    def data_preparation(dicionario):
        dic = {}
        for num in range(len(dicionario[list(dicionario.keys())[0]])):
            for key in dicionario:
                data = dicionario[key]
                print(data)
                if key == "Região":
                    dic[data[num]] = []
                else:
                    chave = list(dic.keys())
                    dic[chave[num]].append(data[num])
        return dic       

    # Grafico de evolução 
    def evolution_plot(dicionario,range_year,metadata,preparation = False):
        if preparation == True:
            data = data_preparation(dicionario)
        else:
            data = dicionario
        #colors = colour_gradient("blue","white",len(data.keys()))
        keys = list(data.keys())
        if range_year is not list:
            range_list = list(range(0,len(dicionario)))
        else:
            range_list = range_year
        fig = go.Figure()
        for loc in range(0,len(data)):
            fig.add_trace(go.Scatter(x=range_list,y=data[keys[loc]],name=keys[loc]))
        fig.update_layout(title=metadata["title"],xaxis_title=metadata["xaxis_title"],yaxis_title=metadata["yaxis_title"])
        
        return fig 

    # Grafico de barras 
    def comparative_plot(dicionario,range_year,metadata,preparation = False):
        if preparation == True:
            data = data_preparation(dicionario)
        else:
            data = dicionario
        #colors = colour_gradient("blue","white",len(data.keys()))
        keys = list(data.keys())
        if range_year is list:
            range_list = range_year
        else:
            range_list = list(range(0,len(dicionario)))

        fig = go.Figure()
        for loc in range(0,len(data)):
            fig.add_trace(go.Bar(x=range_list,y=data[keys[loc]],name=keys[loc]))
        fig.update_layout(title=metadata["title"],xaxis_title=metadata["xaxis_title"],yaxis_title=metadata["yaxis_title"])
        
        return fig 