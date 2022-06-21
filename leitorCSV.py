from dataView import geraGrafico
from manipulaAquivo import ler_arquivo
from manipulaDataFame import KJ_to_KWh, UTC_para_BRT, addTempMedia, listaDias, mediaDia, meidaDiaNotNull, separar_dataframes, string_para_numerico

def main():

    # df = ler_arquivo('arquivos/','GOIANIA (A002)_2022-04-01_2022-04-30')
    df = ler_arquivo('arquivos/','GOIANIA (A002)_2022-04-01_2022-06-02')
    df = string_para_numerico(df)
    df = UTC_para_BRT(df)
    df = addTempMedia(df)
    df = KJ_to_KWh(df)

    dicionario_de_meses = separar_dataframes(df)

    dias = listaDias(dicionario_de_meses['06/2022'])

    for dia in dias:
        media = meidaDiaNotNull(df, 'Radiacao (Jh/m²)', dia)
        print (dia, ' Incidencia média: ', round(media, 3), 'Jh/m²')

    # dfMediaDia=mediaDia(df, 'Radiacao (Jh/m²)')
    # horasDoDia=[]
    # for i in range(24):
    #     horasDoDia.append(i)
    # geraGrafico(horasDoDia, 'Hora (BRT)', dfMediaDia, 'Radiacao (Jh/m²)', 'Gráfico da radiaçã média o do Mês')


if __name__ == "__main__":
    main()