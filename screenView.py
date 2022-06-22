from tkinter import *
from tkinter import filedialog
import pandas as pd

def getFiles(fullpaths):
    dfs=[]
    for fullpath in fullpaths:
        df = pd.read_csv(fullpath, sep=";").fillna(0)
        df = df.replace(',', '.', regex=True)
        dfs.append(df)
    return dfs

def selectFile():
    fileNames=filedialog.askopenfilenames(filetypes=[("CSV files", ".csv")])
    filedialog.askopenfile

    dfs = getFiles(fileNames)
    print (dfs)

    nomesDosArquivos["text"] = fileNames




screen = Tk()

screen.title('banana?')
texto = Label(screen, text='blablab')
texto2 = Label(screen, text='blablab22222222222')
texto.grid(column=0, row=0)
texto2.grid(column=1, row=1)

exitButton = Button(screen, text='Fechar', command=screen.destroy)
exitButton.grid(column=3, row=4, padx=15, pady=15)

selectFileButton = Button(screen, text='Selecionar Arquivos', command=selectFile)
selectFileButton.grid(column=0, row=4, padx=15, pady=15)

nomesDosArquivos = Label(screen, text='')
nomesDosArquivos.grid(column=2, row=3)

screen.mainloop()





