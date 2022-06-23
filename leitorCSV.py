from dataView import *
from manipulaAquivo import ler_arquivos
from manipulaDataFame import *

NOMES_ARQUIVOS=['GOIANIA (A002)_2022-04-01_2022-04-30']
MES_DE_REFERENCIA='04/2022'
def main():

    # df = ler_arquivo('arquivos/','GOIANIA (A002)_2022-04-01_2022-04-30')
    dfs = ler_arquivos('arquivos/',NOMES_ARQUIVOS)
    df = concatenar_dfs(dfs)
    df = string_para_numerico(df)
    df = UTC_para_BRT(df)
    df = addTempMedia(df)
    df = KJ_to_KWh(df)

    # print(df)

    dicionario_de_meses = separar_dataframes(df)

    # for i in dicionario_de_meses:
    #     print('Referencia: ',i,'\n',dicionario_de_meses[i])
    

    radiacaoMediaValida(df, dicionario_de_meses, MES_DE_REFERENCIA)


    mediaPorHora, horasDoDia = mediaDia(dicionario_de_meses[MES_DE_REFERENCIA], 'Radiacao (Jh/m²)')
    geraGraficoBonito(horasDoDia, 'Hora (BRT)', mediaPorHora, 'Radiação (Jh/m²)', 'Gráfico da radiação média o do Mês')

def radiacaoMediaValida(df, dicionario_de_meses, mes):
    dias = listaDias(dicionario_de_meses[mes])

    for dia in dias:
        media = mediaDiaNotNull(df, 'Radiacao (Jh/m²)', dia)
        if media==0:
            print(dia, ' Dados insuficientes')
        else:
            print (dia, f' Incidencia média: {media:.3f} Jh/m²')


if __name__ == "__main__":
    main()
