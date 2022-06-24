from tkinter import *
from tkinter import filedialog
import pandas as pd

from manipulaDataFame import *
from dataView import *
import test_screenView as tSV


def getFiles(fullpaths):
    dfs=[]
    for fullpath in fullpaths:
        df = pd.read_csv(fullpath, sep=";").fillna(0)
        df = df.replace(',', '.', regex=True)
        dfs.append(df)
    return dfs

MES_DE_REFERENCIA='04/2022'
class GraphicInterface(object): 
    def __init__(self):

        self.dataFrame = pd.DataFrame
        self.dataFrames = pd.DataFrame

        self.fuso='-3'
        self.screen = Tk()

        # self.screen.geometry("900x640")
        # Grid.rowconfigure(self.screen, 0, weight=1)
        # Grid.columnconfigure(self.screen, 0, weight=1)

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
        

        self.splitDataFrameButton = Button(self.screen, text='Separa Data Frame por mês', command = self.splitDataFrame)
        self.splitDataFrameButton.grid(column=0, row=3, padx=10, pady=10)
        self.infoSplitDataFrameButton=self.splitDataFrameButton.grid_info()
        self.splitDataFrameButton.grid_forget()
        
        setFusoButton= Button(self.screen, text='Definir Fusos Horário', command = self.define_fuso_horario)
        setFusoButton.grid(row=0, column=100)
        # fusoLabel = Label(self.screen, text='bleb')
        self.entryFuso = Entry(self.screen)
        self.entryFuso.grid(row=setFusoButton.grid_info()["row"], column=setFusoButton.grid_info()["column"]+1)
        
        


        exitButton = Button(self.screen, text = 'Fechar', command = self.screen.destroy)
        exitButton.grid(column=3, row=100, padx=15, pady=15)

        selectFileButton = Button(self.screen, text='Selecionar Arquivos', command = self.selectFile)
        selectFileButton.grid(column=0, row=100, padx=15, pady=15)


        self.screen.mainloop()
    
    def define_fuso_horario(self):
        self.fuso=self.entryFuso.get()
        print(self.fuso)

    def selectFile(self):
        fileNames=filedialog.askopenfilenames(filetypes=[("CSV files", ".csv")])
        filedialog.askopenfile

        self.setDataFrame(fileNames)

        formatedNames = self.formatText(fileNames)
        self.labelNomesDosArquivos["text"] = formatedNames
        self.showElement(self.splitDataFrameButton, self.infoSplitDataFrameButton)
        self.showElement(self.hidenLabelButton, self.infoHidenLabelButton)

    def setDataFrame(self, fileNames):
        self.dataFrame = getFiles(fileNames)
        self.dataFrame = concatenar_dfs(self.dataFrame)
        self.dataFrame = string_para_numerico(self.dataFrame)
        self.dataFrame = definir_fuso_horario(self.dataFrame, self.fuso)
        self.dataFrame = addTempMedia(self.dataFrame)
        self.dataFrame = KJ_to_KWh(self.dataFrame)

    def formatText(self, fileNames):
        finalText=''
        for text in fileNames:
            finalText+=text+'\n'
        return finalText


    def splitDataFrame(self):
        self.dataFrames = separar_dataframes(self.dataFrame, self.fuso)

        btns=[]
        for mes in list(self.dataFrames.keys()):
            btn = Button(self.screen, text = mes)
            # btn = Button(self.screen, text = mes, command= lambda: self.gerar_grafico(btn['text']))
            btns.append(btn)
        for i, j in enumerate(btns):
            j.grid(column=self.infoSplitDataFrameButton["column"], row=self.infoSplitDataFrameButton["row"]+i+1)

    def showElement(self, element, info):
        element.grid(row = info["row"],  column = info["column"],  padx = info["padx"], pady = info["pady"])

    def changeState(self):
        if(self.hidenLabelButton["text"] == 'Mostrar'):
            self.hidenLabelButton["text"] = 'Ocultar'
            self.showElement(self.labelNomesDosArquivos, self.infoLabelNomesDosArquivos)
        elif(self.hidenLabelButton["text"] == 'Ocultar'):
            self.labelNomesDosArquivos.grid_forget()
            self.hidenLabelButton["text"] = 'Mostrar'
        
    def gerar_grafico(self, mes_referencia): #em teste
        print(mes_referencia)
        mediaPorHora, horasDoDia = mediaDia(self.dataFrames[mes_referencia], 'Radiacao (Jh/m²)', self.fuso)
        geraGraficoBonito(horasDoDia, 'Hora '+'(UTC'+self.fuso+')' , mediaPorHora, 'Radiação (Jh/m²)', 'Gráfico da radiação média o do Mês')
        tSV.main()


	  
 
GraphicInterface()





