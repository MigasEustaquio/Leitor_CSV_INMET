from dataView import geraGrafico
from manipulaAquivo import ler_arquivos
from manipulaDataFame import *

def main():

    # df = ler_arquivo('arquivos/','GOIANIA (A002)_2022-04-01_2022-04-30')
    dfs = ler_arquivos('arquivos/',['GOIANIA (A002)_2022-02-03_2022-03-02','GOIANIA (A002)_2022-04-01_2022-06-02'])
    df = concatenar_dfs(dfs)
    df = string_para_numerico(df)
    df = UTC_para_BRT(df)
    df = addTempMedia(df)
    df = KJ_to_KWh(df)

    dicionario_de_meses = separar_dataframes(df)

    dias = listaDias(dicionario_de_meses['02/2022'])

    for dia in dias:
        media = meidaDiaNotNull(df, 'Radiacao (Jh/m²)', dia)
        if media==0:
            print(dia, ' Dados insuficientes')
        else:
            print (dia, f' Incidencia média: {media:.3f} Jh/m²')


    # dfMediaDia=mediaDia(df, 'Radiacao (Jh/m²)')
    # horasDoDia=[]
    # for i in range(24):
    #     horasDoDia.append(i)
    # geraGrafico(horasDoDia, 'Hora (BRT)', dfMediaDia, 'Radiacao (Jh/m²)', 'Gráfico da radiaçã média o do Mês')


if __name__ == "__main__":
    main()