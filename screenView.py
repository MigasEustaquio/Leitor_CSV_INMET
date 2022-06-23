from tkinter import *
from tkinter import filedialog
from click import command
import pandas as pd

def getFiles(fullpaths):
    dfs=[]
    for fullpath in fullpaths:
        df = pd.read_csv(fullpath, sep=";").fillna(0)
        df = df.replace(',', '.', regex=True)
        dfs.append(df)
    return dfs

# def selectFile():
#     fileNames=filedialog.askopenfilenames(filetypes=[("CSV files", ".csv")])
#     filedialog.askopenfile

#     dfs = getFiles(fileNames)
#     print (dfs)

    #nomesDosArquivos["text"] = fileNames




# screen = Tk()

# screen.title('banana?')
# texto = Label(screen, text='blablab')
# texto2 = Label(screen, text='blablab22222222222')
# texto.grid(column=0, row=0)
# texto2.grid(column=1, row=1)

# exitButton = Button(screen, text='Fechar', command=screen.destroy)
# exitButton.grid(column=3, row=4, padx=15, pady=15)

# selectFileButton = Button(screen, text='Selecionar Arquivos', command=selectFile)
# selectFileButton.grid(column=0, row=4, padx=15, pady=15)

# nomesDosArquivos = Label(screen, text='')
# nomesDosArquivos.grid(column=2, row=3)

# screen.mainloop()


class GraphicInterface(object): 
    def __init__(self): 
        self.screen = Tk()

        self.screen.title('Leitor CSV INMET')

        self.labelNomesDosArquivos = Label(self.screen, text =  '')
        self.labelNomesDosArquivos.grid(column=1, row=2)
        self.infoLabelNomesDosArquivos = self.labelNomesDosArquivos.grid_info()

        


        texto = Label(self.screen, text = 'Arquivos selecionados:')
        texto.grid(column=0, row=1)
        self.hidenLabelButton = Button(self.screen, text = 'Ocultar', command = self.changeState)
        self.hidenLabelButton.grid(column = texto.grid_info()["column"]+1, row = texto.grid_info()["row"])
        self.infoHidenLabelButton=self.hidenLabelButton.grid_info()
        self.hidenLabelButton.grid_forget()
        

        self.createDataFrameButton = Button(self.screen, text='Criar Data Frame')
        self.createDataFrameButton.grid(column=0, row=3, padx=10, pady=10)
        self.infoCreateDataFrameButton=self.createDataFrameButton.grid_info()
        self.createDataFrameButton.grid_forget()
        

        exitButton = Button(self.screen, text = 'Fechar', command = self.screen.destroy)
        exitButton.grid(column=3, row=4, padx=15, pady=15)

        selectFileButton = Button(self.screen, text='Selecionar Arquivos', command = self.selectFile)
        selectFileButton.grid(column=0, row=4, padx=15, pady=15)


        self.screen.mainloop()
    
    def selectFile(self):
        fileNames=filedialog.askopenfilenames(filetypes=[("CSV files", ".csv")])
        filedialog.askopenfile

        # dfs = getFiles(fileNames)
        # print (dfs)

        formatedNames = self.formatText(fileNames)
        self.labelNomesDosArquivos["text"] = formatedNames
        self.showElement(self.createDataFrameButton, self.infoCreateDataFrameButton)
        self.showElement(self.hidenLabelButton, self.infoHidenLabelButton)
        

    def formatText(self, fileNames):
        finalText=''
        for text in fileNames:
            finalText+=text+'\n'
        return finalText

    def showElement(self, element, info):
        element.grid(row = info["row"],  column = info["column"],  padx = info["padx"], pady = info["pady"])

    def changeState(self):
        if(self.hidenLabelButton["text"] == 'Mostrar'):
            self.hidenLabelButton["text"] = 'Ocultar'
            self.showElement(self.labelNomesDosArquivos, self.infoLabelNomesDosArquivos)
        elif(self.hidenLabelButton["text"] == 'Ocultar'):
            self.labelNomesDosArquivos.grid_forget()
            self.hidenLabelButton["text"] = 'Mostrar'
        

        
	  
 
GraphicInterface()





