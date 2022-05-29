import pandas as pd
import matplotlib.pyplot as plt

# NOME_DO_ARQUIVO = "GOIANIA (A002)_2022-05-06_2022-05-06"
NOME_DO_ARQUIVO = "GOIANIA (A002)_2022-04-01_2022-04-30"

#Lê o arquvo csv e substitui "," por "."
def ler_arquivo():
    df = pd.read_csv("arquivos/" + NOME_DO_ARQUIVO + ".csv", sep=";").fillna(0)
    df = df.replace(',', '.', regex=True)
    return df

#Muda o tipo dos dados do df de string para numerico
def string_para_numerico(df):
    for coluna in df:
        if coluna == "Data": pass
        else: df[coluna] = pd.to_numeric(df[coluna])
    return(df)

#Muda o formato do horário militar em UTC para o comum em BRT
# def UTC_para_BRT(df):
#     df["Hora (UTC)"] = df["Hora (UTC)"].apply(lambda x: (x/100)-3)
#     df.rename(columns = {"Hora (UTC)":"Hora (BRT)"}, inplace = True)
#     return df

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

def main():

    df = ler_arquivo()
    df = string_para_numerico(df)    
    dfsEmdias=divideDias(df)

    mediaMes=mediaDoMes(dfsEmdias)
    GeraGrafico(mediaMes)

if __name__ == "__main__":
    main()