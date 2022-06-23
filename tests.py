# from matplotlib import pyplot as plt


# def divideDias(df):
#     numDias = len(df)/24
#     listaDias = []

#     inicio=0
#     fim=24
#     for dia in range(int(numDias)):
#         listaDias.append(df.iloc[inicio:fim,:])
#         inicio+=24
#         fim+=24
    
#     return listaDias
    
# def mediaDoMes(listaDf):
#     listaMediaHr=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#     for dfDia in listaDf:
#         for i in range(len(dfDia['Radiacao (KJ/m²)'])):
#             listaMediaHr[i]+=dfDia.iloc[i]['Radiacao (KJ/m²)']
#         # break
    
#     # print(listaMediaHr)
        
#     listaMediaHr = [round(x/24, 2) for x in listaMediaHr]
#     return listaMediaHr

# def GeraGrafico(mediaMes):

#     novoMediaMes=mediaMes
#     print('Anterior', novoMediaMes)
#     for i in range (3):
#         novoMediaMes.append(novoMediaMes.pop(0))
    
#     print('Novo', novoMediaMes)


#     hrsDoDia=[]
#     for i in range(24):
#         hrsDoDia.append(i)
#     print(hrsDoDia)

#     plt.title('Grafico Media de radiação do Mês') # Titulo 
#     plt.xlabel('Hora (BRT)') # Eixo x 
#     plt.ylabel('Radiacao (KJ/m²)') # Eixo y 
#     plt.plot(hrsDoDia, novoMediaMes)
#     plt.show()

import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np

def graficoBonito():
    # Gráfico usando apenas marcadores
    trace1 = go.Scatter(x = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y = [1, 2, 3, 4, 5],
                        mode = 'markers',
                        name = 'Apenas marcadores')
    # Gráfico de apenas linhas
    trace2 = go.Scatter(x = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y = [11, 12, 13, 14, 15],
                        mode = 'lines',
                        name = 'Apenas linhas')
    # Criando gráfico com marcadores e linhas
    trace3 = go.Scatter(x = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio'],
                        y = [6, 7, 8, 9, 10],
                        mode = 'markers+lines',
                        name = 'Marcadores e Linhas')
    data = [trace1, trace2, trace3]
    py.plot(data, auto_open=False)


import test_screenView as testSV
from manipulaDataFame import *
from manipulaAquivo import *

def test():

    dfs = ler_arquivos('arquivos/',['GOIANIA (A002)_2022-04-01_2022-04-30'])
    df = concatenar_dfs(dfs)
    df = string_para_numerico(df)

    df = definir_fuso_horario(df, '-5')

    print(df)

if __name__ == '__main__':

    test()
