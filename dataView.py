import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as py
import numpy as np

#Plota um gráfico de linha a partir dos parametros passados
def geraGrafico(eixoX, legendaX, eixoY, legendaY, titulo):
    plt.title(titulo) # Titulo 
    plt.xlabel(legendaX) # Eixo x 
    plt.ylabel(legendaY) # Eixo y 
    plt.plot(eixoX, eixoY)
    plt.show()

#Plota gráfico utilizando recursos da biblioteca plotly
def geraGraficoBonito(eixoX, legendaX, eixoY, legendaY, titulo):

    max_value = max(eixoY)
    indx_max_values = np.where(eixoY == max_value)
    max_valuesY = [max_value]*len(indx_max_values[0])
    max_valuesX=[]
    for i in indx_max_values[0]:
        max_valuesX.append(eixoX[i])

    min_value = min(eixoY)
    indx_min_values= np.where(eixoY == min_value)
    min_valuesY=[min_value]*len(indx_min_values[0])
    min_valuesX=[]
    for i in indx_min_values[0]:
        min_valuesX.append(eixoX[i])
    
   
    layout = go.Layout(title=titulo, yaxis={'title':legendaY},xaxis={'title': legendaX})
    grafico = go.Scatter(x = eixoX, y = eixoY, mode = 'markers+lines', line=dict(color='rgb(0,0,0)'), name = titulo)

    fig = go.Figure(data=grafico, layout=layout)
    fig.add_trace(go.Scatter(x = max_valuesX, y = max_valuesY, mode = 'markers', marker_symbol = 'triangle-up', marker=dict(color='rgb(0,0,255)',size=10),name = 'Valor Máximo'))
    fig.add_trace(go.Scatter(x = min_valuesX, y = min_valuesY, mode = 'markers', marker_symbol = 'triangle-down', marker=dict(color='rgb(255,0,0)',size=10), name = 'Valor Mínimo'))

    py.plot(fig, auto_open=False)

#Plota um gráfico de linha a partir dos dois eixo dados
#NÃO USADA
def plot(df, eixo_x="Hora (BRT)", eixo_y="Radiacao (KJ/m²)"):

    # if (df.shape[0]/24) > 50:
    #     print('meses')

    if (df.shape[0]/24) > 1:
        # print('dias')
        eixo_x="Data"
    else:
        # print('horas')
        eixo_x="Hora (BRT)"

    df.plot(x=eixo_x, y=eixo_y, kind = 'line')
    plt.title(eixo_y+' / '+eixo_x)
    plt.show()

#NÃO USADA
#Associa valor escolhido com nome da coluna 
def switch_case(x):
    if x=='0':
        print('1- Data\n2- Hora (BRT)\n3- Temp. Ins. (C)\n4- Temp. Max. (C)\n5- Temp. Min. (C)\n6- Umi. Ins. (%)\n7- Umi. Max. (%)\n8- Umi. Min. (%)\n9- Pto Orvalho Ins. (C)\n10- Pto Orvalho Max. (C)\n11- Pto Orvalho Min. (C)\n12- Pressao Ins. (hPa)\n13- Pressao Max. (hPa)\n14- Pressao Min. (hPa)\n15- Vel. Vento (m/s)\n15- Dir. Vento (m/s)\n16- Raj. Vento (m/s)\n17- Radiacao (KJ/m²)\n18- Chuva (mm)\n')
    elif x=='1':
        print('1- Data\n')
        x="Data"
    elif x=='2':
        print('2- Hora (BRT)')
        x="Hora (BRT)"
    elif x=='3':
        print('3- Temp. Ins. (C)')
        x="Temp. Ins. (C)"
    elif x=='4':
        print('4- Temp. Max. (C)')
        x="Temp. Max. (C)"
    elif x=='5':
        print('5- Temp. Min. (C)')
        x="Temp. Min. (C)"
    elif x=='6':
        print('6- Umi. Ins. (%)')
        x="Umi. Ins. (%)"
    elif x=='7':
        print('7- Umi. Max. (%)')
        x="Umi. Max. (%)"
    elif x=='8':
        print('8- Umi. Min. (%)')
        x="Umi. Min. (%)"
    elif x=='9':
        print('9- Pto Orvalho Ins. (C)')
        x="Pto Orvalho Ins. (C)"
    elif x=='10':
        print('10- Pto Orvalho Max. (C)')
        x="Pto Orvalho Max. (C)"
    elif x=='11':
        print('11- Pto Orvalho Min. (C)')
        x="Pto Orvalho Min. (C)"
    elif x=='12':
        print('12- Pressao Ins. (hPa)')
        x="Pressao Ins. (hPa)"
    elif x=='13':
        print('13- Pressao Max. (hPa)')
        x="Pressao Max. (hPa)"
    elif x=='14':
        print('14- Pressao Min. (hPa)')
        x="Pressao Min. (hPa)"
    elif x=='15':
        print('15- Vel. Vento (m/s)')
        x="Vel. Vento (m/s)"
    elif x=='16':
        print('16- Raj. Vento (m/s)')
        x="Raj. Vento (m/s)"
    elif x=='17':
        print('17- Radiacao (KJ/m²)')
        x="Radiacao (KJ/m²)"
    elif x=='18':
        print('18- Chuva (mm)')
        x="Chuva (mm)"
    else:
        print('Coluna não encontrada...')
        x='0'
    return x

#NÃO USADA
#Selecionar as colunas que serão plotadas
def escolher_eixos_para_plot(df):
    while True:
        print('Qual o eixo X deseja plotar? (para ver as opções insira \'0\')\n')
        x=str(input('>'))
        x=switch_case(x)
        if x != '0': break

    while True:
        print('Qual o eixo Y deseja plotar? (para ver as opções insira \'0\')\n')
        y=str(input('>'))
        y=switch_case(y)
        if y != '0': break

    plot(df, x, y)