import pandas as pd

#Lê o arquvo csv e substitui "," por "."
def ler_arquivo(path, nomeDoArquivo):
    df = pd.read_csv(path + nomeDoArquivo + ".csv", sep=";").fillna(0)
    df = df.replace(',', '.', regex=True)
    return df