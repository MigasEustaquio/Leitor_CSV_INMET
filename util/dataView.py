import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as py

from util.funcoesDiversas import *

#Plota um gráfico de linha a partir dos parametros passados
def geraGrafico(eixoX, legendaX, eixoY, legendaY, titulo):
    plt.title(titulo) # Titulo 
    plt.xlabel(legendaX) # Eixo x 
    plt.ylabel(legendaY) # Eixo y 
    plt.plot(eixoX, eixoY)
    plt.show()

#Plota gráfico utilizando recursos da biblioteca plotly
def geraGraficoBonito(eixoX, legendaX, eixoY, legendaY, titulo, numero_curvas=1):
    titulos=''
    variaveis=''
    for i in titulo:
        titulos += i+'<br>'
    for i in legendaY:
        variaveis += i+'<br>'

    layout = go.Layout(title=titulos, yaxis={'title':variaveis},xaxis={'title': legendaX})
    
    for curva in range(numero_curvas):
        max_valuesX, max_valuesY, min_valuesX, min_valuesY = get_max_min(eixoX[curva], eixoY[curva])

        if curva == 0:
            grafico = go.Scatter(x = eixoX[curva], y = eixoY[curva], mode = 'markers+lines', line=dict(color='rgb(0,0,0)'), name = titulo[curva])

            fig = go.Figure(data=grafico, layout=layout)
            fig.add_trace(go.Scatter(x = max_valuesX, y = max_valuesY, mode = 'markers', marker_symbol = 'triangle-up', marker=dict(size=10),name = 'Valor Máximo '+titulo[curva]))
            fig.add_trace(go.Scatter(x = min_valuesX, y = min_valuesY, mode = 'markers', marker_symbol = 'triangle-down', marker=dict(size=10), name = 'Valor Mínimo '+titulo[curva]))

        else:

            fig.add_trace(go.Scatter(x = eixoX[curva], y = eixoY[curva], mode = 'markers+lines', name = titulo[curva]))
            
            fig.add_trace(go.Scatter(x = max_valuesX, y = max_valuesY, mode = 'markers', marker_symbol = 'triangle-up', marker=dict(size=10),name = 'Valor Máximo '+titulo[curva]))
            fig.add_trace(go.Scatter(x = min_valuesX, y = min_valuesY, mode = 'markers', marker_symbol = 'triangle-down', marker=dict(size=10), name = 'Valor Mínimo '+titulo[curva]))


    py.plot(fig, auto_open=False)


def geraGraficoHSP(eixoX, legendaX, eixoY, legendaY):

    eixoX=calculaHSP(eixoY)

    hoverinformation = str(round(eixoX[1], 3)) + ' HSP'

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['1000'],
        x=[eixoX[0]],
        name='',
        orientation='h',
        marker=dict(
        color='rgba(0, 0, 0, 0)',
        line=dict(color='rgba(0, 0, 0, 0)', width=3)
    )
    ))
    fig.add_trace(go.Bar(
        y=['1000'],
        x=[eixoX[1]],
        x0=[0],
        dx=2,
        name='HSP',
        orientation='h',
        text=hoverinformation,
        marker=dict(
        color='rgba(255, 255, 0, 1)',
        line=dict(color='rgba(255, 255, 0, 1.0)', width=3),
    )
    ))
    fig.add_trace(go.Bar(
        y=['1000'],
        x=[eixoX[2]],
        name='',
        orientation='h',
        marker=dict(
        color='rgba(0, 0, 0, 0)',
        line=dict(color='rgba(0, 0, 0, 0)', width=3)
    )
    ))

    fig.update_layout(barmode='stack', title="Horas de Sol Pleno",
    plot_bgcolor="#FFF",  # Sets background color to white
    xaxis=dict(
        title="Horas",
        linecolor="#BCCCDC",  # Sets color of X-axis line
        showgrid=False  # Removes X-axis grid lines
    ),
    yaxis=dict(
        title="Radiação",  
        linecolor="#BCCCDC",  # Sets color of Y-axis line
        showgrid=False,  # Removes Y-axis grid lines    
    ))

    py.plot(fig, auto_open=False)
