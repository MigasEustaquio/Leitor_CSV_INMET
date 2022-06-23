from dataView import geraGrafico
from manipulaAquivo import ler_arquivos
from manipulaDataFame import *
from tests import geraGraficoBonito

NOMES_ARQUIVOS = ['GOIANIA (A002)_2022-04-01_2022-04-30']

def main():

    dfs = ler_arquivos('arquivos/', NOMES_ARQUIVOS)
    df = concatenar_dfs(dfs)
    df = string_para_numerico(df)
    df = UTC_para_BRT(df)
    df = addTempMedia(df)
    df = KJ_to_KWh(df)

    print(df)

    dicionario_de_meses = separar_dataframes(df)

    # for i in dicionario_de_meses:
    #     print('Referencia: ',i,'\n',dicionario_de_meses[i])
    

    # dias = listaDias(dicionario_de_meses['03/2022'])

    # for dia in dias:
    #     media = meidaDiaNotNull(df, 'Radiacao (Jh/m²)', dia)
    #     if media==0:
    #         print(dia, ' Dados insuficientes')
    #     else:
    #         print (dia, f' Incidencia média: {media:.3f} Jh/m²')


    mediaPorHora, horasDoDia = mediaDia(dicionario_de_meses['04/2022'], 'Radiacao (Jh/m²)')
    geraGraficoBonito(horasDoDia, 'Hora (BRT)', mediaPorHora, 'Radiacao (Jh/m²)', 'Gráfico da radiação média o do Mês')


if __name__ == "__main__":
    main()
