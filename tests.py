from matplotlib import pyplot as plt


def divideDias(df):
    numDias = len(df)/24
    listaDias = []

    inicio=0
    fim=24
    for dia in range(int(numDias)):
        listaDias.append(df.iloc[inicio:fim,:])
        inicio+=24
        fim+=24
    
    return listaDias
    
def mediaDoMes(listaDf):
    listaMediaHr=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for dfDia in listaDf:
        for i in range(len(dfDia['Radiacao (KJ/m²)'])):
            listaMediaHr[i]+=dfDia.iloc[i]['Radiacao (KJ/m²)']
        # break
    
    # print(listaMediaHr)
        
    listaMediaHr = [round(x/24, 2) for x in listaMediaHr]
    return listaMediaHr

def GeraGrafico(mediaMes):

    novoMediaMes=mediaMes
    print('Anterior', novoMediaMes)
    for i in range (3):
        novoMediaMes.append(novoMediaMes.pop(0))
    
    print('Novo', novoMediaMes)


    hrsDoDia=[]
    for i in range(24):
        hrsDoDia.append(i)
    print(hrsDoDia)

    plt.title('Grafico Media de radiação do Mês') # Titulo 
    plt.xlabel('Hora (BRT)') # Eixo x 
    plt.ylabel('Radiacao (KJ/m²)') # Eixo y 
    plt.plot(hrsDoDia, novoMediaMes)
    plt.show()