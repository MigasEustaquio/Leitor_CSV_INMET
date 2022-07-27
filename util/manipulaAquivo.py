import pandas as pd

#Lê o arquvo csv e substitui "," por "."
def ler_arquivos(path, nomesDosArquivos):
    dfs=[]
    for arquivo in nomesDosArquivos:
        df = pd.read_csv(path + arquivo + ".csv", sep=";").fillna(0)
        df = df.replace(',', '.', regex=True)
        dfs.append(df)
    return dfs

def getFiles(fullpaths):
    dfs=[]
    for fullpath in fullpaths:
        df = pd.read_csv(fullpath, sep=";").fillna(0)
        df = df.replace(',', '.', regex=True)
        dfs.append(df)
    return dfs