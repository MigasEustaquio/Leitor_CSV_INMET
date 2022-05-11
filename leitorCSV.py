import pandas as pd
import matplotlib.pyplot as plt

NOME_DO_ARQUIVO = "GOIANIA (A002)_2022-05-04_2022-05-11"

#Muda o tipo dos dados do df de string para numerico
def string_para_numerico(df):
    for coluna in df:
        if coluna == "Data": pass
        else: df[coluna] = pd.to_numeric(df[coluna])

    df["Hora (UTC)"] = df["Hora (UTC)"].apply(lambda x: (x/100)-3)
    df.rename(columns = {"Hora (UTC)":"Hora (BRT)"}, inplace = True)

    return(df)

#Lê o arquvo csv e substitui "," por ".". Chama a função string_para_numerico antes de retornar
def ler_e_formatar():
    df = pd.read_csv("arquivos/" + NOME_DO_ARQUIVO + ".csv", sep=";").fillna(0)
    df = df.replace(',', '.', regex=True)
    return string_para_numerico(df)

#Plota um gráfico de linha a partir dos dois eixo dados
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

#Selecionar as colunas que serão plotadas
def escolher_eixos_para_plot(df):
    # while True:
    #     print('Qual o eixo X deseja plotar? (para ver as opções insira \'0\')\n')
    #     x=str(input('>'))
    #     x=switch_case(x)
    #     if x != '0': break

    # while True:
    #     print('Qual o eixo Y deseja plotar? (para ver as opções insira \'0\')\n')
    #     y=str(input('>'))
    #     y=switch_case(y)
    #     if y != '0': break

    # plot(df, x, y)
    plot(df)

def main():

    df = ler_e_formatar()

    escolher_eixos_para_plot(df)

if __name__ == "__main__":
    main()