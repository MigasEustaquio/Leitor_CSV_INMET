from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import showinfo
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

def disable_event():
    messagebox.showinfo('Não funciona','Usar o botão do menu')
    pass

def destroyAndRecover(screen1, screen2):
        screen1.destroy()
        screen2.deiconify()

class GraphicInterface(object): 
    def __init__(self):

        self.dataFrame = pd.DataFrame
        self.dataFrames = pd.DataFrame

        self.fuso='-3'
        self.dataFrameSeparado=False

        self.mainScreen = Tk()

        # self.screen.geometry("900x640")
        # Grid.rowconfigure(self.screen, 0, weight=1)
        # Grid.columnconfigure(self.screen, 0, weight=1)

        self.mainScreen.title('Leitor CSV INMET')

        self.labelNomesDosArquivos = Label(self.mainScreen, text =  '')
        self.labelNomesDosArquivos.grid(column=1, row=2)
        self.infoLabelNomesDosArquivos = self.labelNomesDosArquivos.grid_info()

        textoSelecinarArquivos = Label(self.mainScreen, text = 'Arquivos selecionados:')
        textoSelecinarArquivos.grid(column=0, row=1)
        self.hidenLabelButton = Button(self.mainScreen, text = 'Ocultar', command = self.changeState)
        self.hidenLabelButton.grid(column = textoSelecinarArquivos.grid_info()["column"]+1, row = textoSelecinarArquivos.grid_info()["row"])
        self.infoHidenLabelButton=self.hidenLabelButton.grid_info()
        self.hidenLabelButton.grid_forget()
        
        self.fullDataFrameButton = Button(self.mainScreen, text='Intervalo Completo: ', command = lambda: self.toDfOpitions(self.mainScreen, self.dataFrame))
        self.fullDataFrameButton.grid(column=0, row=3, padx=10, pady=10)
        self.infoFullDataFrameButton = self.fullDataFrameButton.grid_info()
        self.fullDataFrameButton.grid_forget()

        self.splitDataFrameButton = Button(self.mainScreen, text='Separa Data Frame por mês', command = self.splitDataFrame)
        self.splitDataFrameButton.grid(column=0, row=4, padx=10, pady=10)
        self.infoSplitDataFrameButton=self.splitDataFrameButton.grid_info()
        self.splitDataFrameButton.grid_forget()
        
        setFusoButton= Button(self.mainScreen, text='Definir Fuso Horário', command = self.define_fuso_horario)
        setFusoButton.grid(row=0, column=100)
        self.entryFuso = Entry(self.mainScreen)
        self.entryFuso.grid(row=setFusoButton.grid_info()["row"], column=setFusoButton.grid_info()["column"]+1)
        

        
        selectFileButton = Button(self.mainScreen, text='Selecionar Arquivos', command = self.selectFile)
        selectFileButton.grid(column=0, row=100, padx=15, pady=15)

        exitButton = Button(self.mainScreen, text = 'tos2', command = lambda : self.s1_to_s2(self.mainScreen))
        exitButton.grid(column=3, row=100, padx=15, pady=15)

        self.mainScreen.mainloop()

    def s1_to_s2(self, closedScreen):
        self.screen2 = Tk()
        closedScreen.withdraw()
        self.btnBS1 = Button(self.screen2, text='volta para 1', command = lambda: destroyAndRecover(self.screen2, closedScreen))
        self.btnBS1.grid(column=2, row=1, padx=15, pady=15)
        self.screen2.protocol("WM_DELETE_WINDOW", disable_event)
        self.screen2.mainloop()

    def toDfOpitions(self, closedScreen, df):
        closedScreen.withdraw()

        dfOpitionsScreen = Tk()
        dfOpitionsScreen.title('Opções')
        dfOpitionsScreen.protocol("WM_DELETE_WINDOW", disable_event)
        btnBackToMain = Button(dfOpitionsScreen, text='Voltar para menu inicial', command = lambda: destroyAndRecover(dfOpitionsScreen, closedScreen))
        btnBackToMain.grid(column=100, row=0, padx=15, pady=15)
        
        print(df)
        dfLbels = list(df.columns.values)
        print(dfLbels)
 
        indxColumn = 0
        indxRow = 1
        aux = 0
        for label in dfLbels:
            if label == 'Data' or label == 'Hora (UTC)' or label == 'DateTime (UTC'+self.fuso+')' or label == 'Date (UTC'+self.fuso+')':
                pass
            else:
                aux += 1
                print(label)
                btn = Button(dfOpitionsScreen, text = label)
                btn.grid(column = indxColumn, row = indxRow)
                indxColumn += 1
                if (aux == 4):
                    print(aux)
                    indxRow += 1
                    indxColumn = 0
                    aux = 0
                
                
                    


        dfOpitionsScreen.mainloop


        #         for mes in list(self.dataFrames.keys()):
        #     # btn = Button(self.screen, text = mes)
        #     btnName=self.dataFrames[mes]['Date (UTC'+self.fuso+')'].values[0]+' a '+self.dataFrames[mes]['Date (UTC'+self.fuso+')'].values[-1]
        #     btn = Button(self.mainScreen, text = btnName, command= lambda j=mes: self.gerar_grafico(j, btnName))
        #     btns.append(btn)
        # for i, j in enumerate(btns):
        #     j.grid(column=self.infoSplitDataFrameButton["column"], row=self.infoSplitDataFrameButton["row"]+i+1)
      

# Recupera o fuso horário digitado e, se preciso, recarrega o dstaframe
    def define_fuso_horario(self):
        fuso=list(self.entryFuso.get())
        if len(fuso)>2: fuso[1]+=fuso[2]
        try:
            if fuso[0] == '+' or fuso[0] == '-':
                if fuso[1].isdigit() and int(fuso[1])<13:
                    self.fuso=self.entryFuso.get()
# Recarrega o dataframe caso o mesmo já tiver sido criado
                    if not self.dataFrame.empty:
                        self.selectFile(recarregar_dataframe=True)
                        if self.dataFrameSeparado:
                            self.splitDataFrame()
#
                    showinfo("Sucesso", "Fuso Horário alterado com sucesso! (UTC"+self.entryFuso.get()+")")
                else: showinfo("Erro", "Insira apenas números vállidos (1-12) após o sinal.")
            else: showinfo("Erro", "Insira um sinal positivo(+) ou negativo(-) seguido de um número.")
        except:
            showinfo("Erro", "Insira um formato de fuso horário, considere UTC como 0. (Ex:-3)")

# Lê os arquivos selecionados e prepara o Dataframe
    def selectFile(self, recarregar_dataframe=False):
        if not recarregar_dataframe:
            self.fileNames=filedialog.askopenfilenames(filetypes=[("CSV files", ".csv")])
            filedialog.askopenfile
        self.setDataFrame(self.fileNames)

        formatedNames = self.formatText(self.fileNames)
        self.labelNomesDosArquivos["text"] = formatedNames
        self.showElement(self.splitDataFrameButton, self.infoSplitDataFrameButton)
        self.showElement(self.hidenLabelButton, self.infoHidenLabelButton)

        fullInterval = self.dataFrame['Date (UTC'+self.fuso+')'].values[0]+' a '+self.dataFrame['Date (UTC'+self.fuso+')'].values[-1]
        self.fullDataFrameButton['text']+=fullInterval
        self.showElement(self.fullDataFrameButton, self.infoFullDataFrameButton)

# Chama as funções padrões para tratamento do Dataframe
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

# Separa o Dataframe completo em um df por mês de referência
    def splitDataFrame(self):
        self.dataFrames = separar_dataframes(self.dataFrame, self.fuso)
        self.dataFrameSeparado=True

# Criando lista de botões associados aos meses
        btns=[]
        for mes in list(self.dataFrames.keys()):
            # btn = Button(self.screen, text = mes)
            print('key: ', mes)
            btnName=self.dataFrames[mes]['Date (UTC'+self.fuso+')'].values[0]+' a '+self.dataFrames[mes]['Date (UTC'+self.fuso+')'].values[-1]
            btn = Button(self.mainScreen, text = btnName, command= lambda j=mes, nome = btnName: self.gerar_grafico(j, nome))
            btns.append(btn)
        for i, j in enumerate(btns):
            j.grid(column=self.infoSplitDataFrameButton["column"], row=self.infoSplitDataFrameButton["row"]+i+1)

# 
    def showElement(self, element, info):
        element.grid(row = info["row"],  column = info["column"],  padx = info["padx"], pady = info["pady"])

# Mostrar/Ocultar Arquivos
    def changeState(self):
        if(self.hidenLabelButton["text"] == 'Mostrar'):
            self.hidenLabelButton["text"] = 'Ocultar'
            self.showElement(self.labelNomesDosArquivos, self.infoLabelNomesDosArquivos)
        elif(self.hidenLabelButton["text"] == 'Ocultar'):
            self.labelNomesDosArquivos.grid_forget()
            self.hidenLabelButton["text"] = 'Mostrar'
        
# Gera uma janela com o gráfico do mês de referência
    def gerar_grafico(self, key_referencia, nome_referencia):
        mediaPorHora, horasDoDia = mediaDia(self.dataFrames[key_referencia], 'Radiacao (Jh/m²)', self.fuso)
        print(self.dataFrames[key_referencia])
        print('NOME: ', nome_referencia)
        geraGraficoBonito(horasDoDia, 'Hora '+'(UTC'+self.fuso+')' , mediaPorHora, 'Radiação (Jh/m²)', 'Gráfico da radiação '+nome_referencia)
        tSV.main()

    # def gerar_rafico_fullDf(self, label):
    #     mediaPorHora, horasDoDia = mediaDia(self.dataFrames[key_referencia], label, self.fuso)



	  
 
GraphicInterface()