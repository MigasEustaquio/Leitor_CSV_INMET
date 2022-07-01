from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import showinfo
import pandas as pd
import re

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

def disable_event():
    messagebox.showinfo('Não funciona','Usar o botão do menu')
    pass

def destroyAndRecover(screen1, screen2):
        screen1.destroy()
        screen2.deiconify()

def tratamento_formato_data(lista_entries):
    padrao_dia = re.compile("[0-9]{2}[/][0-9]{2}[/][0-9]{4}")
    padrao_mes = re.compile("[0-9]{2}[/][0-9]{4}")
    padrao_ano = re.compile("[0-9]{4}")

    datas=[]
    for entry in lista_entries:
        data=entry.get()

        # if data == '':
        #     print('Nenhuma data foi selecionada')
        # else:
        #     data_completa = data.split('/')
        #     if len(data_completa)==1:
        #         print('Ano')
        #     elif len(data_completa)==2:
        #         print('Mês')
        #     elif len(data_completa)==3:
        #         print('Dia')
        #     else:
        #         showinfo(title='Erro', message='Formato de data incorreto!')
        #         data = ''
        
        if not data:
            print('Nenhuma data foi selecionada')
        else:
            match_dia = padrao_dia.match(data)
            match_mes = padrao_mes.match(data)
            match_ano = padrao_ano.match(data)
            if match_dia:
                print(f'DIA {data}')
            elif match_mes:
                print(f'MÊS {data}')
            elif match_ano:
                print(f'ANO {data}')
            else:
                showinfo(title='Erro', message='Formato de data incorreto!')
                data = ''

            datas.append(data)

    return datas

class GraphicInterface(object): 
    def __init__(self):

        self.dataFrame = pd.DataFrame
        self.dataFrames = pd.DataFrame

        self.fuso='-3'
        self.dataFrameSeparado=False
        self.numeroEntriesData=0
        self.lista_entries=[]

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

        self.testeButton = Button(self.mainScreen, text='TESTE', command = lambda: self.toTesteScreen(self.mainScreen, self.dataFrame))
        self.testeButton.grid(column=4, row=100, padx=15, pady=15)
        self.infoTesteButton = self.testeButton.grid_info()
        self.testeButton.grid_forget()

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
        self.screen2.protocol("WM_DELETE_WINDOW",  lambda: destroyAndRecover(self.screen2, closedScreen))
        self.screen2.mainloop()

    def toDfOpitions(self, closedScreen, df):
        closedScreen.withdraw()

        dfOpitionsScreen = Tk()
        dfOpitionsScreen.title('Opções')
        dfOpitionsScreen.protocol("WM_DELETE_WINDOW", lambda: destroyAndRecover(dfOpitionsScreen, closedScreen))
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
                    indxRow += 1
                    indxColumn = 0
                    aux = 0


        dfOpitionsScreen.mainloop


    def toTesteScreen(self, closedScreen, df):
        if not self.dataFrameSeparado: self.splitDataFrame()

        closedScreen.withdraw()

        testeScreen = Tk()
        testeScreen.title('Opções')
        testeScreen.protocol("WM_DELETE_WINDOW", lambda: destroyAndRecover(testeScreen, closedScreen))
        btnBackToMain = Button(testeScreen, text='Voltar para menu inicial', command = lambda: destroyAndRecover(testeScreen, closedScreen))
        btnBackToMain.grid(column=101, row=0, padx=15, pady=15)
        btnConfirm = Button(testeScreen, text='Confirmar', command=self.itens_selecionados)
        btnConfirm.grid(column=100, row=100, padx=15, pady=15)

        self.labelTipoGrafico = Label(testeScreen, text =  'Tipo de Gráfico')
        self.labelTipoGrafico.grid(column=0, row=0)
        self.labelTipoGraficoInfo = self.labelTipoGrafico.grid_info()

        self.labelIntervalOP = Label(testeScreen, text = 'Opções')
        self.labelIntervalOP.grid(column=self.labelTipoGraficoInfo['column']+1, row=0)
        self.labelIntervalOPInfo = self.labelIntervalOP.grid_info()

        self.labelLabels = Label(testeScreen, text = 'Variável Analizada')
        self.labelLabels.grid(column=self.labelIntervalOPInfo['column']+2, row=0)
        self.labelLabelsInfo = self.labelLabels.grid_info()

        self.listboxTipoGrafico = Listbox(testeScreen, height=6, exportselection=0)
        self.listboxTipoGrafico.grid(column=self.labelTipoGraficoInfo['column'], row=self.labelTipoGraficoInfo['row']+1, sticky='nwes')
        self.listboxTipoGraficoInfo = self.listboxTipoGrafico.grid_info()

        self.listboxTipoGrafico.insert('end', 'Diário')
        self.listboxTipoGrafico.insert('end', 'Mensal')
        self.listboxTipoGrafico.insert('end', 'Anual')

        self.listboxLabels = Listbox(testeScreen, height=6, exportselection=0)
        self.listboxLabels.grid(column=self.labelLabelsInfo['column'], row=self.labelLabelsInfo['row']+1, sticky='nwes')
        self.listboxLabelsInfo = self.listboxLabels.grid_info()

        for label in list(df.columns.values):
            if label == 'Data' or label == 'Hora (UTC)' or label == 'DateTime (UTC'+self.fuso+')' or label == 'Date (UTC'+self.fuso+')':
                pass
            else:
                self.listboxLabels.insert('end', label)


        self.scrollbarLabels = Scrollbar(testeScreen, orient='vertical', command=self.listboxLabels.yview)
        self.listboxLabels['yscrollcommand'] = self.scrollbarLabels.set
        self.scrollbarLabels.grid(column=self.listboxLabelsInfo['column']+1, row=self.listboxLabelsInfo['row'], sticky='ns')
        self.scrollbarLabelInfos =  self.scrollbarLabels.grid_info()

        self.listBoxIntervalOp = Listbox(testeScreen, height=6, exportselection=0)
        self.listBoxIntervalOp.grid(column=self.labelIntervalOPInfo['column'], row=self.labelIntervalOPInfo['row']+1, sticky='nwes')
        self.listBoxIntervalOpInfo = self.listBoxIntervalOp.grid_info()

        self.scrollbarIntervalOp = Scrollbar(testeScreen, orient='vertical', command=self.listBoxIntervalOp.yview)
        self.listBoxIntervalOp['yscrollcommand'] = self.scrollbarIntervalOp.set
        self.scrollbarIntervalOp.grid(column=self.listBoxIntervalOpInfo['column']+1, row=self.listBoxIntervalOpInfo['row'], sticky='ns')
        self.scrollbarIntervalOpInfos = self.scrollbarIntervalOp.grid_info()

        self.labelEntrys = Label(testeScreen, text =  'Entradas')
        self.labelEntrys.grid(column=self.labelLabelsInfo['column']+2, row=0)
        self.labelEntrysInfo = self.labelEntrys.grid_info()
        
        self.listBoxEntrys = Listbox(testeScreen, height=6, exportselection=0)
        self.listBoxEntrys.grid(column=self.labelEntrysInfo['column'], row=self.labelEntrysInfo['row']+1, sticky='nwes')
        self.listBoxlabelEntrysInfo = self.listBoxEntrys.grid_info()

        self.scrollbarEntrys = Scrollbar(testeScreen, orient='vertical', command=self.listBoxEntrys.yview)
        self.listBoxEntrys['yscrollcommand'] = self.scrollbarEntrys.set
        self.scrollbarEntrys.grid(column=self.listBoxlabelEntrysInfo['column']+1, row=self.listBoxlabelEntrysInfo['row'], sticky='ns')
        self.scrollbarEntrysInfos = self.scrollbarIntervalOp.grid_info()
        
        self.btnLimpar = Button(testeScreen, text='Limpar')
        self.btnLimpar.grid(row = self.listBoxlabelEntrysInfo['row']+1, column = self.listBoxlabelEntrysInfo['column'])
        self.btnLimparInfo = self.btnLimpar.grid_info()
        

        self.btnAvancar = Button(testeScreen, text='Avançar', command = lambda: self.op_intervalo_data(self.listboxTipoGrafico))
        self.btnAvancar.grid(row = self.listboxTipoGraficoInfo['row']+1, column = self.listboxTipoGraficoInfo['column'])
        self.btnAvancarInfo = self.btnAvancar.grid_info()
    
        self.btnVoltar = Button(testeScreen, text = 'Voltar', command = lambda: print('voltar'))

        self.buttonAddEntry = Button(testeScreen, text='Adicionar Linha', command=lambda: self.cria_entry_data(testeScreen))
        self.buttonAddEntry.grid(row=self.btnLimparInfo['row']+1, column=self.labelEntrysInfo['column'])
        self.buttonAddEntryInfo = self.buttonAddEntry.grid_info()

        # self.entryDate = Entry(testeScreen)
        # self.entryDate.grid(row=1, column=3)
        self.cria_entry_data(testeScreen)


        testeScreen.mainloop

    def op_intervalo_data(self, listBox):
        self.opMes = None
        try:
            op = listBox.curselection()[0]
            print(listBox.get(op))
            if (len(self.btnVoltar.grid_info()) == 0):
                self.btnAvancar.grid_remove()

                self.btnVoltar.grid(row = self.listboxTipoGraficoInfo['row']+1, column = self.listboxTipoGraficoInfo['column'])
                self.btnVoltarInfo = self.btnVoltar.grid_info()

                self.btnAvancarInfo['column'] = self.labelIntervalOPInfo['column']
                self.showElement(self.btnAvancar, self.btnAvancarInfo)
            

            if op == 0:#dia
                self.carregaMes()
                print('nanana')
                if self.opMes is not None:
                    print('é pra ir')
                    self.btnAvancar.configure(command = lambda: self.carregarDia())
                print('chega ?')
                
                

            elif op == 1:#mes
                self.carregaMes()
                self.btnVoltar.configure(command = lambda: print('voltar ano mes'))

            elif op == 2:#ano
                self.selecionarAno()
                self.btnVoltar.configure(command = lambda: print('voltar ano ano'))
        except IndexError:
            showinfo(title='Erro', message='Selecione um tipo de intervalo de entrada')
            return
        
    def selecionarAno(self):
        self.labelIntervalOP['text'] = 'Selecione o Ano'
        self.listBoxIntervalOp.delete(0, END)
        self.listBoxIntervalOp.insert('end', 'ano')

    def carregaMes(self):
        self.labelIntervalOP['text'] = 'Selecione o Mês'
        self.listBoxIntervalOp.delete(0, END)
        self.dataFrameMeses = separar_dataframes(self.dataFrame, self.fuso)
        for dataMes in list(self.dataFrameMeses.keys()):
            self.listBoxIntervalOp.insert('end', dataMes)
        
        self.btnAvancar.configure(command = lambda: self.sececinarMes(self.listBoxIntervalOp))
            
    def sececinarMes(self, listBox):
        try: 
            op = listBox.curselection()[0]
            self.opMes = listBox.get(op)
            print (self.opMes)
            return
        except IndexError:
            showinfo(title='Erro', message='Selecione o mês')
            return
        
    def carregarDia(self):
        print(self.opMes, ' agora o dia')
        self.labelIntervalOP['text'] = 'Selecione o Dia'
        #self.listBoxIntervalOp.delete(0, END)
        self.dataFrameDias = self.dataFrameMeses[self.opMes]
        print(self.dataFrameDias)
        
        
    def selecionarDia(self, listBox):
        
        try:
            self.btnVoltar.configure(command = lambda: print('voltar dia'))
            
        except IndexError:
            showinfo(title='Erro', message='Selecione o dia')
            self.carregaMes()
            return
        
    
    def itens_selecionados(self):

        try:
            tipo_selecionado = self.listboxTipoGrafico.curselection()[0]
        except:
            showinfo(title='Erro', message='Nenhum tipo de gráfico foi selecionado')
            return

        try:
            variavel_selecionada = self.listboxLabels.get(self.listboxLabels.curselection())
        except:
            showinfo(title='Erro', message='Nenhuma variável foi selecionada')
            return
        

        datas= tratamento_formato_data(self.lista_entries)

        if not datas:
            showinfo(title='Erro', message='Nenhuma data foi selecionada')
            return

        msg = 'Tipo de Gráfico: '+str(tipo_selecionado)+'\nColuna: ' + variavel_selecionada + '\nData:'
        for data in datas: msg+=' '+data
        print(msg)

        try:
            self.gerar_grafico_qualquer_variavel(tipo_selecionado, datas, variavel_selecionada)
        except:
            showinfo(title='Erro', message='Erro ao gerar gráfico') #erro genérico provisório

        
        


    def cria_entry_data(self, testeScreen):

        self.numeroEntriesData+=1
        
        self.buttonAddEntry.grid_forget()

        entryDate = Entry(testeScreen)
        #entryDate.grid(row=self.numeroEntriesData+2, column=self.labelEntrysInfo['column'])
        self.showElement(entryDate, self.buttonAddEntryInfo)
        self.lista_entries.append(entryDate)

        
        self.buttonAddEntryInfo['row'] += 1 
        self.showElement(self.buttonAddEntry, self.buttonAddEntryInfo)
        
        # self.buttonAddEntry.destroy()
        # self.buttonAddEntry = Button(testeScreen, text='Adicionar Linha', command=lambda: self.cria_entry_data(testeScreen))
        # self.buttonAddEntry.grid(row=self.numeroEntriesData+3, column=self.labelEntrysInfo['column'])


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

        self.showElement(self.testeButton, self.infoTesteButton)

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
            # print('key: ', mes)
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


#Tornar possível fazer gráfico com várias variávei
    def gerar_grafico_qualquer_variavel(self, tipo_grafico, datas_referencia, variavel_referencia):

        for data in datas_referencia:
            print(data)

        # if tipo_grafico == 0: # Gráfico Diário
        #     showinfo(title='Erro', message='Não implementado')
        #     return

        # elif tipo_grafico == 1: # Gráfico Mensal
        #     eixoY, eixoX = mediaDia(self.dataFrames[data_referencia], variavel_referencia, self.fuso)

        # elif tipo_grafico == 2: # Gráfico Anual
        #     showinfo(title='Erro', message='Não implementado')
        #     return

        # geraGraficoBonito(eixoX, 'Hora '+'(UTC'+self.fuso+')' , eixoY, variavel_referencia, 'Gráfico de '+ variavel_referencia + ' ' + data_referencia)
        # tSV.main()





    # def gerar_rafico_fullDf(self, label):
    #     mediaPorHora, horasDoDia = mediaDia(self.dataFrames[key_referencia], label, self.fuso)



	  
 
GraphicInterface()