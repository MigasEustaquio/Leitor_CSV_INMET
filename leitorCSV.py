from util.dataView import *
from util.manipulaAquivo import ler_arquivos
from util.manipulaDataFame import *

NOMES_ARQUIVOS=[ 'GOIANIA (A002)_2022-05-01_2022-05-31', 'GOIANIA (A002)_2022-04-01_2022-04-30']
MES_DE_REFERENCIA='04/2022'
FUSO_HORARIO='-3'
def main():

    dfs = ler_arquivos('arquivos/',NOMES_ARQUIVOS)
    df = concatenar_dfs(dfs)
    df = string_para_numerico(df)
    df = definir_fuso_horario(df, FUSO_HORARIO)
    df = addTempMedia(df)
    df = KJ_to_KWh(df)

    # print('COMPLETO ',df)

    dicionario_de_meses = separar_dataframes_mes(df, FUSO_HORARIO)
    # print(dicionario_de_meses)

    # print(list(dicionario_de_meses.keys()))
    

    # radiacaoMediaValida(df, dicionario_de_meses, MES_DE_REFERENCIA)

    # print(dicionario_de_meses[MES_DE_REFERENCIA])
    mediaPorHora, horasDoDia = mediaDia(dicionario_de_meses[MES_DE_REFERENCIA], 'Radiacao (Jh/m²)', FUSO_HORARIO)
    geraGraficoBonito([horasDoDia], 'Hora '+'(UTC'+FUSO_HORARIO+')' , [mediaPorHora], ['Radiação (Jh/m²)'], ['Gráfico da radiação média o do Mês' + MES_DE_REFERENCIA])

def radiacaoMediaValida(df, dicionario_de_meses, mes):
    dias = listaDias(dicionario_de_meses[mes], FUSO_HORARIO)

    for dia in dias:
        media = mediaDiaNotNull(df, 'Radiacao (Jh/m²)', dia, FUSO_HORARIO)
        if media==0:
            print(dia, ' Dados insuficientes')
        else:
            print (dia, f' Incidencia média: {media:.3f} Jh/m²')


if __name__ == "__main__":
    main()
