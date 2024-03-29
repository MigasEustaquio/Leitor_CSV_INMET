import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as py
from plotly.subplots import make_subplots
from util.funcoesDiversas import*


#Plota um gráfico de linha a partir dos parametros passados
def geraGrafico(eixoX, legendaX, eixoY, legendaY, titulo):
    plt.title(titulo) # Titulo 
    plt.xlabel(legendaX) # Eixo x 
    plt.ylabel(legendaY) # Eixo y 
    plt.plot(eixoX, eixoY)
    plt.show()

#Plota gráfico utilizando recursos da biblioteca plotly
def geraGraficoBonito(eixoX, legendaX, eixoY, legendaY, titulo, browserOpen = False, addInfo = False):
    variaveis=legendaY.copy()
    addSecondary_y = False
    titulos=''

    for i in titulo:
        titulos += i+'<br>'
    strLegendaY=''
    secondary_y_title=False
    for i in set(variaveis):
        if i == 'Horas de Sol Pleno (HSP)':
            secondary_y_title=True
            if(len(set(variaveis)) > 1):
                addSecondary_y=True
        else:
            strLegendaY += i+'<br>'

    figureData = make_subplots(specs=[[{"secondary_y": addSecondary_y}]])

    for curva in range(len(legendaY)):
        if(legendaY[curva]=='Horas de Sol Pleno (HSP)'):
            _, hsp, _ =calculaHSP(eixoY[curva])
            max_valuesX, _, _, _ = get_max_min(eixoX[curva], eixoY[curva])
            hoverinformation = str(round(hsp, 3)) + ' HSP'
            centro=12
            
            trace1=go.Scatter(x = [0, eixoX[curva][-1]], y = [0, 0], mode = 'markers', showlegend = False, marker_color = 'rgba(255, 255, 0, 0)')
            trace2=go.Bar(
                yaxis='y2',
                y = [1000],
                x = [centro],
                width=hsp,
                name=hoverinformation+'.<br>'+titulo[curva],
                orientation='v',
                text=hoverinformation,
                insidetextanchor = 'middle',
                textposition='inside',
                textangle=-90,
                marker=dict(color='rgba(255, 255, 0, 0.4)')
            )

            figureData.add_trace(trace1, secondary_y=addSecondary_y)
            figureData.add_trace(trace2, secondary_y=addSecondary_y)
            
        else:
         
            max_valuesX, max_valuesY, min_valuesX, min_valuesY = get_max_min(eixoX[curva], eixoY[curva])
            if addInfo[curva]:
                mainData = go.Scatter(x = eixoX[curva], y = eixoY[curva], mode = 'markers+lines', name = titulo[curva]+'<br>'+addInfo[curva])
            else:
                mainData = go.Scatter(x = eixoX[curva], y = eixoY[curva], mode = 'markers+lines', name = titulo[curva])
            maxValuesData = go.Scatter(x = max_valuesX, y = max_valuesY, mode = 'markers', marker_symbol = 'triangle-up', marker=dict(size=10), name = 'Valor Máximo '+titulo[curva])
            minValuesData = go.Scatter(x = min_valuesX, y = min_valuesY, mode = 'markers', marker_symbol = 'triangle-down', marker=dict(size=10), name = 'Valor Mínimo '+titulo[curva])
            
            figureData.add_trace(minValuesData)
            figureData.add_trace(maxValuesData)
            figureData.add_trace(mainData)

    fig = go.Figure(data=figureData)
    fig.update_layout(barmode='group', plot_bgcolor="#FFF", title=titulos)
    fig.update_yaxes(title=strLegendaY,showline=True, linewidth=1, linecolor='black', ticks='inside')
    fig.update_xaxes(title= legendaX, showline=True, linewidth=1, linecolor='black', ticks='inside')
    #tickmode='auto', nticks=6
    # fig.update_layout(
    #     xaxis_tickformatstops = [
    #         dict(dtickrange=[None, None], value= "%H Hrs")
    #     ]
    # )
    #tickmode = 'linear', tick0 = 0, dtick = 4
    #ticklabelstep=1
    if secondary_y_title == True:
        fig.update_yaxes(title_text='Irradiância (W/m²)', secondary_y=addSecondary_y)
    py.plot(fig, auto_open = browserOpen)


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
