import numpy as np
import datetime

def calculaHSP(vertices):

    area_grafico=0

    for i in range(len(vertices)-1):
        area_grafico+=(vertices[i]+vertices[i+1])/2

    HSP=area_grafico/1000

    tamanho_horizontal_grafico = HSP/2

    return [12-tamanho_horizontal_grafico, HSP, 12-tamanho_horizontal_grafico]

def mediaDia(df, label, fuso):
    mediaHoras=[]
    horasDoDia=[]

    formato_fuso='(UTC'+fuso+')'

    for i in range(24):
        if (i<10):
            hora='-0'+str(i)
        else:
            hora='-'+str(i)
        valoresDia = df[df['DateTime '+formato_fuso].str.endswith(hora)][label].values
        if(len(valoresDia)>0):
            mediaHoras.append(round(sum(valoresDia)/len(valoresDia),3))
            horasDoDia.append(i)

    return mediaHoras,horasDoDia

    #media no dia, descarta valores nulos
def mediaDiaNotNull(df, label, data, fuso):
    valoresValidos=[]

    formato_fuso='(UTC'+fuso+')'

    valores=df[df['Date '+formato_fuso].str.match(data)][label].values

    for valor in valores:
        if valor != 0:
            valoresValidos.append(valor)

    if len(valoresValidos) == 0:
        return 0
    else:
        return sum(valoresValidos)/len(valoresValidos)

def listaDias(df, fuso):

    formato_fuso='(UTC'+fuso+')'

    dias = df['Date '+formato_fuso].values
    listaDias=list(set(dias))
    
    return sorted(listaDias, key=lambda date: datetime.datetime.strptime(date, "%d/%m/%Y"))


def listaDiasNovo(df, data, fuso):

    formato_fuso='(UTC'+fuso+')'

    valores=df[df['Date '+formato_fuso].str.endswith(data)]['Date '+formato_fuso].values

    dias = [x.split('/')[0] for x in valores]
    
    return sorted(list(set(dias)))

def valores_um_dia(df, label, fuso, dia):

    valoresDia = df[df['DateTime (UTC'+fuso+')'].str.startswith(dia)][label].values

    horasDoDia=[i for i in range(len(valoresDia))]

    return valoresDia, horasDoDia

def get_max_min(eixoX, eixoY):
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

    return max_valuesX, max_valuesY, min_valuesX, min_valuesY