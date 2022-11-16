import re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
import webbrowser

from util.manipulaDataFame import *
from util.manipulaAquivo import *
from util.dataView import *
import util.graphicWindow as GW


FUSO_BR =  {
            '-5': 'Rio Branco (BRT-2) ', 
            '-4': 'Manaus (BRT-1) ',
            '-3': 'Brasília (BRT) ',
            '-2': 'Fernando de Noronha (BRT+1) '
            }

def showElement(element, info):
    element.grid(row = info["row"],  column = info["column"],  padx = info["padx"], pady = info["pady"])

def destroyAndRecover(screen1, screen2):
        screen1.destroy()
        screen2.deiconify()

def tratamento_formato_data(lista_entries):
    padrao_dia = re.compile("[0-9]{2}[/][0-9]{2}[/][0-9]{4}")
    padrao_mes = re.compile("[0-9]{2}[/][0-9]{4}")
    padrao_ano = re.compile("[0-9]{4}")

    datas=[]
    for i, entry in enumerate(lista_entries):
        print(entry.get())
        data=entry.get()
        
        if not data:
            print('Nenhuma data foi selecionada')
        else:
            if padrao_dia.fullmatch(data):
                print(f'DIA {data}')
                if i==0: tempo='Diário'
                else:
                    if tempo!='Diário':
                        showinfo(title='Erro', message='Apenas um formato de data é aceito por vez!')
                        data = tempo = ''
            elif padrao_mes.fullmatch(data):
                print(f'MÊS {data}')
                if i==0: tempo='Mensal'
                else:
                    if tempo!='Mensal':
                        showinfo(title='Erro', message='Apenas um formato de data é aceito por vez!')
                        data = tempo = ''
            elif padrao_ano.fullmatch(data):
                print(f'ANO {data}')
                if i==0: tempo='Anual'
                else:
                    if tempo!='Anual':
                        showinfo(title='Erro', message='Apenas um formato de data é aceito por vez!')
                        data = tempo = ''
            else:
                showinfo(title='Erro', message='Formato de data incorreto!')
                data, tempo = ''

            datas.append(data)

    return datas, tempo

def setListBox(listBox, list):
        listBox.delete(0, END)

        for element in list:
            listBox.insert('end', element)

def removeListBoxSelectedEntry(listBox):
    try:
        idxItem = listBox.curselection()[0]
        listBox.delete(idxItem)
    except IndexError:
        showinfo(title='Erro', message='Nenhuma entrada selecionada')
        return

def removeTreeViewSelectedEntry(tree):
    try:
        idxItem = tree.selection()[0]
        tree.delete(idxItem)
    except IndexError:
        showinfo(title='Erro', message='Nenhuma entrada selecionada')
        return    

def getTreeViewSelectedEntry(tree):
    try:
        idxItem = tree.selection()[0]
        return tree.item(idxItem, 'values')#tipo, data, variavel
    except IndexError:
       showinfo(title='Erro', message='Nenhuma entrada selecionada')

def getAllTreeViewEntrys(tree):
    listValues=[]
    if len(tree.get_children())==0:
        return
    else: 
        for idxItem in tree.get_children():
            listValues.append(tree.item(idxItem, 'values'))
    return listValues

def openInBrowser(url):
   webbrowser.open_new(url)
class GraphicUserInterface(object): 
    def __init__(self,  root):
        self.dataFrame = pd.DataFrame
        self.dataFrameDia = pd.DataFrame
        self.dataFrameMes = pd.DataFrame
        self.dataFrameAno = pd.DataFrame

        self.fuso='-3'
        self.dataFrameSeparadoDia=False
        self.dataFrameSeparadoMes=False
        self.dataFrameSeparadoAno=False
        self.numeroEntriesData=0
        
        self.externalOutput = True


        root.title('Leitor CSV INMET')
        topContainer = Frame(root)
        
        ajudaButton = Button(topContainer, text='Como usar?', command = lambda:self.helpScreen(root))
        ajudaButton.grid(column=0, row=0, padx=(15,600), pady=15)
        ajudaButtonInfo = ajudaButton.grid_info()

        setFusoButton = Button(topContainer, text='Definir Fuso Horário', command = self.define_fuso_horario)
        setFusoButton.grid(row=ajudaButtonInfo["row"], column=ajudaButtonInfo["column"]+5)
        setFusoButtonInfo=setFusoButton.grid_info()
        self.entryFuso = Entry(topContainer)
        self.entryFuso.grid(row=setFusoButtonInfo["row"], column=setFusoButtonInfo["column"]+1, padx=5,)

        topContainer.grid(row=0, column=0, ipadx=10)
        topContainerInfo=topContainer.grid_info()
        

        centerContainer = Frame(root)
        textoSelecinarArquivos = Label(centerContainer, text = 'Arquivos selecionados:')
        textoSelecinarArquivos.grid(column=0, row=0, padx=(15,0))
        textoSelecinarArquivosInfo=textoSelecinarArquivos.grid_info()

        
        self.hidenLabelButton = Button(centerContainer, text = 'Ocultar', command = self.changeState)
        self.hidenLabelButton.grid(column=textoSelecinarArquivosInfo["column"]+1, row =textoSelecinarArquivosInfo["row"])
        self.infoHidenLabelButton=self.hidenLabelButton.grid_info()
        self.hidenLabelButton.grid_forget()

        self.labelNomesDosArquivos = Label(centerContainer, text =  '')
        self.labelNomesDosArquivos.grid(column=self.infoHidenLabelButton['column'], row=self.infoHidenLabelButton['row']+1)
        self.infoLabelNomesDosArquivos = self.labelNomesDosArquivos.grid_info()

        centerContainer.grid(row=topContainerInfo['row']+1, column=topContainerInfo['column'], ipadx=10)
        centerContainerInfo=centerContainer.grid_info()


        botContainer = Frame(root)
        selectFileButton = Button(botContainer, text='Selecionar Arquivos', command = self.selectFile)
        selectFileButton.grid(column=0, row=0, padx=(0,100), pady=15)
        selectFileButtonInfo=selectFileButton.grid_info()

        self.toViewButton = Button(botContainer, text='Seguir para Visualização', command = lambda: self.toOptionsViewScreen(root, self.dataFrame))
        self.toViewButton.grid(column=selectFileButtonInfo["column"]+1, row=selectFileButtonInfo["row"])
        self.toViewButtonInfo = self.toViewButton.grid_info()
        self.toViewButton.grid_forget()

        configButton = Button(botContainer, text='Opções')
        #command = lambda:self.configScreen(root) "removido" pois o executavel não integra com agraphicWindow
        configButton.grid(column=self.toViewButtonInfo["column"]+1, row=self.toViewButtonInfo["row"], padx=(400,5))
        configButtonInfo = configButton.grid_info()
        

        suportButton = Button(botContainer, text='Suporte')
        suportButton.grid(column=configButtonInfo["column"]+1, row=selectFileButtonInfo["row"], )

        botContainer.grid(row=centerContainerInfo['row']+1, column=centerContainerInfo['column'], ipadx=10)
        botContainer=topContainer.grid_info()

    def toOptionsViewScreen(self, closedScreen, df):
        closedScreen.withdraw()
        optionsViewScreen = Tk()
        optionsViewScreen.title('Opções De Visualização')
        optionsViewScreen.protocol("WM_DELETE_WINDOW", lambda: destroyAndRecover(optionsViewScreen, closedScreen))
        
        print('Saída externa',self.externalOutput)
        btnBackToMain = Button(optionsViewScreen, text='Voltar para menu inicial', command = lambda: destroyAndRecover(optionsViewScreen, closedScreen))
        btnBackToMain.grid(column=100, row=0, padx=(0,15))

        labelTipoGrafico = Label(optionsViewScreen, text =  'Tipo de Gráfico')
        labelTipoGrafico.grid(column=0, row=0, pady=(20,0))
        labelTipoGraficoInfo = labelTipoGrafico.grid_info()

        self.labelIntervalOP = Label(optionsViewScreen, text = 'Opções')
        self.labelIntervalOP.grid(column=labelTipoGraficoInfo['column']+1, row=0, pady=(20,0))
        self.labelIntervalOPInfo = self.labelIntervalOP.grid_info()

        labelLabels = Label(optionsViewScreen, text = 'Variável Analizada')
        labelLabels.grid(column=self.labelIntervalOPInfo['column']+2, row=0, pady=(20,0))
        labelLabelsInfo = labelLabels.grid_info()

        self.listboxTipoGrafico = Listbox(optionsViewScreen, height=6, exportselection=0)
        self.listboxTipoGrafico.grid(column=labelTipoGraficoInfo['column'], row=labelTipoGraficoInfo['row']+1, sticky='nwes', padx=(15,0))
        self.listboxTipoGraficoInfo = self.listboxTipoGrafico.grid_info()

        self.listboxTipoGrafico.insert('end', 'Diário')
        self.listboxTipoGrafico.insert('end', 'Mensal')
        self.listboxTipoGrafico.insert('end', 'Anual')

        self.listboxLabels = Listbox(optionsViewScreen, height=6, exportselection=0)
        self.listboxLabels.grid(column=labelLabelsInfo['column'], row=labelLabelsInfo['row']+1, sticky='nwes')
        listboxLabelsInfo = self.listboxLabels.grid_info()

        for label in list(df.columns.values):
            if label == 'Data' or label == 'Hora (UTC)' or label == 'DateTime (UTC'+self.fuso+')' or label == 'Date (UTC'+self.fuso+')':
                pass
            else:
                self.listboxLabels.insert('end', label)
        self.listboxLabels.insert('end', 'Horas de Sol Pleno (HSP)')


        scrollbarLabels = Scrollbar(optionsViewScreen, orient='vertical', command=self.listboxLabels.yview)
        self.listboxLabels['yscrollcommand'] = scrollbarLabels.set
        scrollbarLabels.grid(column=listboxLabelsInfo['column']+1, row=listboxLabelsInfo['row'], sticky='ns')
        scrollbarLabelInfos =  scrollbarLabels.grid_info()

        self.listBoxIntervalOp = Listbox(optionsViewScreen, height=6, exportselection=0)
        self.listBoxIntervalOp.grid(column=self.labelIntervalOPInfo['column'], row=self.labelIntervalOPInfo['row']+1, sticky='nwes')
        listBoxIntervalOpInfo = self.listBoxIntervalOp.grid_info()

        scrollbarIntervalOp = Scrollbar(optionsViewScreen, orient='vertical', command=self.listBoxIntervalOp.yview)
        self.listBoxIntervalOp['yscrollcommand'] = scrollbarIntervalOp.set
        scrollbarIntervalOp.grid(column=listBoxIntervalOpInfo['column']+1, row=listBoxIntervalOpInfo['row'], sticky='ns')
        scrollbarIntervalOpInfos = scrollbarIntervalOp.grid_info()

        labelEntrys = Label(optionsViewScreen, text =  'Entradas')
        labelEntrys.grid(column=labelLabelsInfo['column']+2, row=0, pady=(20,0))
        labelEntrysInfo = labelEntrys.grid_info()
        
        self.treeViewEntrys = ttk.Treeview(optionsViewScreen, column=("c1", "c2", "c3"), show='headings', height=5)
        self.treeViewEntrys.column("# 1", anchor=CENTER, width = 50)
        self.treeViewEntrys.heading("# 1", text="Tipo")
        self.treeViewEntrys.column("# 2", anchor=CENTER, width = 100)
        self.treeViewEntrys.heading("# 2", text="Data")
        self.treeViewEntrys.column("# 3", anchor=CENTER,  width = 150)
        self.treeViewEntrys.heading("# 3", text="Variável")
        self.treeViewEntrys.grid(column=labelEntrysInfo['column'], row=labelEntrysInfo['row']+1, sticky='nwes', padx=(50,0))
        treeViewEntrysInfo = self.treeViewEntrys.grid_info()

        scrollbarTreeViewEntrys = Scrollbar(optionsViewScreen, orient='vertical', command = self.treeViewEntrys.yview)
        self.treeViewEntrys['yscrollcommand'] = self.treeViewEntrys.set
        scrollbarTreeViewEntrys.grid(column=treeViewEntrysInfo['column']+1, row=treeViewEntrysInfo['row'], sticky='ns')
        scrollbarTreeViewEntrysInfo = scrollbarTreeViewEntrys.grid_info()        

        btnsEntrysContainer = Frame(optionsViewScreen)
        btnsEntrysContainer.grid(row = scrollbarTreeViewEntrysInfo['row'], column = scrollbarTreeViewEntrysInfo['column']+1)
        btnsEntrysContainerInfo =  btnsEntrysContainer.grid_info()
        
        btnLimpar = Button(btnsEntrysContainer, text='Remover Todas Entradas', command = lambda: self.treeViewEntrys.delete(*self.treeViewEntrys.get_children()))
        btnLimpar.grid(row = 0, column = 0, sticky = NW)
        btnLimparInfo = btnLimpar.grid_info()
        
        btnRemoverElemento = Button(btnsEntrysContainer, text='Remover Entrada Selecionada', command = lambda: removeTreeViewSelectedEntry(self.treeViewEntrys))
        btnRemoverElemento.grid(row = btnLimparInfo['row']+1, column = 0, sticky = NW)
        btnRemoverElementoInfo = btnRemoverElemento.grid_info()

        btnGerarGraficoElemento = Button(btnsEntrysContainer, text='Plotar Gráfico para Entrada Selecionada', command = lambda : self.gera_grafico_unico(getTreeViewSelectedEntry(self.treeViewEntrys)))
        btnGerarGraficoElemento.grid(row = btnRemoverElementoInfo['row']+1, column = 0, sticky = NW)
        btnGerarGraficoElementoInfo = btnGerarGraficoElemento.grid_info()

        btnGerarGraficoTodosElementos = Button(btnsEntrysContainer, text='Plotar Gráfico com Todas Entradas', command = lambda: self.gera_grafico_multiplos(getAllTreeViewEntrys(self.treeViewEntrys)))
        btnGerarGraficoTodosElementos.grid(row = btnGerarGraficoElementoInfo['row']+1, column = 0, sticky = NW)
        btnGerarGraficoTodosElementosInfo = btnGerarGraficoTodosElementos.grid_info()
        

        self.btnAvancar = Button(optionsViewScreen, text='Avançar', command = lambda: self.op_intervalo_data(self.listboxTipoGrafico))
        self.btnAvancar.grid(row = self.listboxTipoGraficoInfo['row']+1, column = self.listboxTipoGraficoInfo['column'])
        self.btnAvancarInfo = self.btnAvancar.grid_info()
    
        self.btnVoltar = Button(optionsViewScreen, text = 'Voltar', command = lambda: print('voltar'))

        self.btnAdicionarListaEntradas = Button(optionsViewScreen, text = 'Adicionar Entrada')
        self.btnAdicionarListaEntradas.grid(row = listboxLabelsInfo['row']+1, column = listboxLabelsInfo['column'])
        self.btnAdicionarListaEntradasInfo = self.btnAdicionarListaEntradas.grid_info()
        self.btnAdicionarListaEntradas.grid_forget()

        entryDateContainer = Frame(optionsViewScreen)
        entryDate = Entry(entryDateContainer)
        #entryDate.grid(column=treeViewEntrysInfo['column'], row=treeViewEntrysInfo['row']+1)
        entryDate.grid(column=1, row=0)
        entryDateInfo = entryDate.grid_info()
        btnConfirm = Button(entryDateContainer, text='Adicionar nova entrada', command=lambda: self.addEntryToTreeViewEntrysBtn(entryDate))
        btnConfirm.grid(column=entryDateInfo['column']-1, row=entryDateInfo['row'], padx=(15,5))
        entryDateContainer.grid(column=treeViewEntrysInfo['column'], row=treeViewEntrysInfo['row']+1, pady=(15, 20))

        optionsViewScreen.mainloop

    def addEntryToTreeViewEntrys(self, tipo, data, BtnVoltar=False):
        try:
            idxItem = self.listboxLabels.curselection()[0]
            variavel = self.listboxLabels.get(idxItem)

            if(tipo == 'Diário' and data in self.dataFrameDia):
                self.treeViewEntrys.insert('','end', values=(tipo, data, variavel))

            elif(tipo == 'Mensal' and data in self.dataFrameMes):
                self.treeViewEntrys.insert('','end', values=(tipo, data, variavel))
                    
            elif(tipo == 'Anual' and data in self.dataFrameAno):
                self.treeViewEntrys.insert('','end', values=(tipo, data, variavel))

            else:
                showinfo(title='Erro', message='Data não encontrada')
            
            if not BtnVoltar: self.voltarDefault()

        except IndexError:
            showinfo(title='Erro', message='Selecione uma Variável')
            return

    def addEntryToTreeViewEntrysBtn(self, entryDate):
        if not self.dataFrameSeparadoDia: self.splitDataFrameDia()
        if not self.dataFrameSeparadoMes: self.splitDataFrameMes()
        if not self.dataFrameSeparadoAno: self.splitDataFrameAno()
        datas, tipo = tratamento_formato_data([entryDate])
        self.addEntryToTreeViewEntrys(tipo, datas[0], BtnVoltar=True)

    def op_intervalo_data(self, listBox):
        self.opState = 'Inicio'
        try:
            op = listBox.curselection()[0]
            self.tipoGrafico = listBox.get(op)
            print(self.tipoGrafico)
            if (len(self.btnVoltar.grid_info()) == 0):
                self.btnAvancar.grid_remove()

                self.btnVoltar.grid(row = self.listboxTipoGraficoInfo['row']+1, column = self.listboxTipoGraficoInfo['column'])
                self.btnVoltarInfo = self.btnVoltar.grid_info()

                self.btnAvancarInfo['column'] = self.labelIntervalOPInfo['column']
                showElement(self.btnAvancar, self.btnAvancarInfo)

            if op == 0:#dia
                if not self.dataFrameSeparadoMes: self.splitDataFrameMes()
                if not self.dataFrameSeparadoDia: self.splitDataFrameDia()
                self.opState = 'DataDia'
                self.carregaMes()
                self.btnVoltar.configure(command = lambda: self.voltarDefault())

            elif op == 1:#mes
                if not self.dataFrameSeparadoMes: self.splitDataFrameMes()
                self.carregaMes()
                self.btnVoltar.configure(command = lambda: self.voltarDefault())

            elif op == 2:#ano
                if not self.dataFrameSeparadoAno: self.splitDataFrameAno()
                self.carregaAno()
                self.btnVoltar.configure(command = lambda: self.voltarDefault())
        except IndexError:
            showinfo(title='Erro', message='Selecione um tipo de intervalo de entrada')
            return
        
    def voltarDefault(self):
        self.btnAdicionarListaEntradas.grid_remove()
        self.labelIntervalOP['text'] = 'Opções'
        self.listBoxIntervalOp.delete(0, END)
        self.btnVoltar.grid_remove()
        self.btnAvancar.grid_remove()
        showElement(self.btnAvancar, self.btnVoltarInfo)
        self.btnAvancar.configure(command = lambda: self.op_intervalo_data(self.listboxTipoGrafico))

    def carregaAno(self):
        self.labelIntervalOP['text'] = 'Selecione o Ano'
        self.listBoxIntervalOp.delete(0, END)
        setListBox(self.listBoxIntervalOp, self.dataFrameAno.keys())
        self.btnAvancar.configure(command = lambda: self.selecionarAno(self.listBoxIntervalOp))
        self.btnVoltar.configure(command = lambda: self.voltarDefault())
        self.btnAdicionarListaEntradas.grid_forget()

    def selecionarAno(self, listBox):
        try: 
            op = listBox.curselection()[0]
            self.opAno = listBox.get(op)
            print (self.opAno)
            showElement(self.btnAdicionarListaEntradas, self.btnAdicionarListaEntradasInfo)
            self.btnAdicionarListaEntradas.configure(command = lambda: self.addEntryToTreeViewEntrys(self.tipoGrafico, self.opAno))
                
        except IndexError:
            showinfo(title='Erro', message='Selecione o Ano')
            return

    def carregaMes(self):
        self.labelIntervalOP['text'] = 'Selecione o Mês'
        setListBox(self.listBoxIntervalOp, self.dataFrameMes.keys())
        
        self.btnAvancar.configure(command = lambda: self.selecionarMes(self.listBoxIntervalOp))
        self.btnVoltar.configure(command = lambda: self.voltarDefault())
        self.btnAdicionarListaEntradas.grid_forget()
            
    def selecionarMes(self, listBox):
        try: 
            op = listBox.curselection()[0]
            self.opMes = listBox.get(op)
            print (self.opMes)
            if(self.opState=='DataDia'):
                self.carregarDia()
            else:
                showElement(self.btnAdicionarListaEntradas, self.btnAdicionarListaEntradasInfo)
                self.btnAdicionarListaEntradas.configure(command = lambda: self.addEntryToTreeViewEntrys(self.tipoGrafico, self.opMes))
                
        except IndexError:
            showinfo(title='Erro', message='Selecione o Mês')
            return
        
    def carregarDia(self):
        print(self.opMes, ' agora o dia')
        self.labelIntervalOP['text'] = 'Selecione o Dia'
        self.dataFrameDiasDoMes = self.dataFrameMes[self.opMes]    
        dias=listaDias(self.dataFrameDiasDoMes, self.fuso)
        setListBox(self.listBoxIntervalOp, dias)
        self.btnAvancar.configure(command = lambda: self.selecionarDia(self.listBoxIntervalOp))
    
    def selecionarDia(self, listBox):
        try:
            op = listBox.curselection()[0]
            self.opDia = listBox.get(op)
            print (self.opDia)

            self.btnVoltar.configure(command = lambda: self.carregaMes())
            showElement(self.btnAdicionarListaEntradas, self.btnAdicionarListaEntradasInfo)
            self.btnAdicionarListaEntradas.configure(command = lambda: self.addEntryToTreeViewEntrys(self.tipoGrafico, self.opDia))
        except IndexError:
            showinfo(title='Erro', message='Selecione o dia')
            return 
         
    def gera_grafico_unico(self, values):
        tipo, data, variavel = values
        addInfo = []

        print(tipo, data, variavel)  
        df = pd.DataFrame
        if tipo == 'Diário':
            df = self.dataFrameDia[data]
        elif tipo == 'Mensal':
            df = self.dataFrameMes[data]
        elif tipo == 'Anual':
            df = self.dataFrameAno[data]
        else:
            showinfo(title='Erro', message='Entrada Não identificada')
            return
        print(df)
        if variavel == 'Horas de Sol Pleno (HSP)': 
            mediaPorHora, horasDoDia = mediaDia(df, 'Radiacao (Wh/m²)', self.fuso)
        else: 
            mediaPorHora, horasDoDia = mediaDia(df, variavel, self.fuso)
        titulo=f'Gráfico {variavel}, média {tipo}: {data}'

        if variavel == 'Radiacao (Wh/m²)':
            valor_medio_dia = data+': '+str(round(sum(mediaPorHora)/1000, 2))+' KWh/m².dia'
            addInfo.append(valor_medio_dia)
        
        legendaX='Hora '
        try:
            legendaX=legendaX+FUSO_BR[self.fuso]
        except:
            legendaX=legendaX+'(UTC'+self.fuso+')'

        geraGraficoBonito([horasDoDia], legendaX, [mediaPorHora], [variavel], [titulo], self.externalOutput, addInfo)
        if (not self.externalOutput):
            GW.main()

    def gera_grafico_multiplos(self, listValues):
        print(listValues)
        listMediaPorHora = []
        listHorasDoDia = []
        listTitulo = []
        listVariaveis = []
        addInfos = []

        for value in (listValues):
            tipo, data, variavel = value
            df = pd.DataFrame
            if tipo == 'Diário':
                df = self.dataFrameDia[data]
            elif tipo == 'Mensal':
                df = self.dataFrameMes[data]
            elif tipo == 'Anual':
                df = self.dataFrameAno[data]
            else:
                showinfo(title='Erro', message='Entrada(s) Não identificada(s)')
                return
            
            if variavel == 'Horas de Sol Pleno (HSP)': 
                mediaPorHora, horasDoDia = mediaDia(df, 'Radiacao (Wh/m²)', self.fuso)
            else: 
                mediaPorHora, horasDoDia = mediaDia(df, variavel, self.fuso)

            if variavel == 'Radiacao (Wh/m²)':
                valor_medio_dia = data+': '+str(round(sum(mediaPorHora)/1000, 2))+' KWh/m².dia'
                addInfos.append(valor_medio_dia)
            else:
                addInfos.append('')

            listVariaveis.append(variavel)
            listMediaPorHora.append(mediaPorHora)
            listHorasDoDia.append(horasDoDia)
            titulo= f'Gráfico {variavel}, média {tipo}: {data}'
            listTitulo.append(titulo)

        legendaX='Hora '
        try:
            legendaX=legendaX+FUSO_BR[self.fuso]
        except:
            legendaX=legendaX+'(UTC'+self.fuso+')'
        geraGraficoBonito(listHorasDoDia, legendaX, listMediaPorHora, listVariaveis, listTitulo, self.externalOutput, addInfos)
        if (not self.externalOutput):
            GW.main()


# Lê os arquivos selecionados e prepara o Dataframe
    def selectFile(self, recarregar_dataframe=False):
        if not recarregar_dataframe:
            self.fileNames=filedialog.askopenfilenames(filetypes=[("CSV files", ".csv")])
            filedialog.askopenfile
        self.setDataFrame(self.fileNames)

        formatedNames = self.formatText(self.fileNames)
        self.labelNomesDosArquivos["text"] = formatedNames
        showElement(self.hidenLabelButton, self.infoHidenLabelButton)

        showElement(self.toViewButton, self.toViewButtonInfo)

    # Chama as funções padrões para tratamento do Dataframe
    def setDataFrame(self, fileNames):
        self.dataFrame = getFiles(fileNames)
        self.dataFrame = concatenar_dfs(self.dataFrame)
        self.dataFrame = string_para_numerico(self.dataFrame)
        self.dataFrame = definir_fuso_horario(self.dataFrame, self.fuso)
        self.dataFrame = addTempMedia(self.dataFrame)
        self.dataFrame = KJ_to_Wh(self.dataFrame)

    def formatText(self, fileNames):
        finalText=''
        for text in fileNames:
            finalText+=text+'\n'
        return finalText

# Recupera o fuso horário digitado e, se preciso, recarrega o dstaframe
    def define_fuso_horario(self):
        fuso=list(self.entryFuso.get())
        self.dataFrameSeparadoDia=False
        self.dataFrameSeparadoMes=False
        self.dataFrameSeparadoAno=False
        if len(fuso)>2: fuso[1]+=fuso[2]
        try:
            if fuso[0] == '+' or fuso[0] == '-':
                if fuso[1].isdigit() and int(fuso[1])<13:
                    self.fuso=self.entryFuso.get()
# Recarrega o dataframe caso o mesmo já tiver sido criado
                    if not self.dataFrame.empty:
                        self.selectFile(recarregar_dataframe=True)

                    showinfo("Sucesso", "Fuso Horário alterado com sucesso! (UTC"+self.entryFuso.get()+")")
                else: showinfo("Erro", "Insira apenas números vállidos (1-12) após o sinal.")
            else: showinfo("Erro", "Insira um sinal positivo(+) ou negativo(-) seguido de um número.")
        except ValueError:
            print(ValueError)
            showinfo("Erro", "Insira um formato de fuso horário, considere UTC como 0. (Ex:-3)")

# Mostrar/Ocultar Arquivos
    def changeState(self):
        if(self.hidenLabelButton["text"] == 'Mostrar'):
            self.hidenLabelButton["text"] = 'Ocultar'
            showElement(self.labelNomesDosArquivos, self.infoLabelNomesDosArquivos)
        elif(self.hidenLabelButton["text"] == 'Ocultar'):
            self.labelNomesDosArquivos.grid_forget()
            self.hidenLabelButton["text"] = 'Mostrar'

# Separa o Dataframe completo em um df por mês de referência
    def splitDataFrameMes(self):
        self.dataFrameMes = separar_dataframes_mes(self.dataFrame, self.fuso)
        self.dataFrameSeparadoMes=True
    
    def splitDataFrameDia(self):
        self.dataFrameDia = separar_dataframes_dia(self.dataFrame, self.fuso)
        self.dataFrameSeparadoDia=True
    
    def splitDataFrameAno(self):
        self.dataFrameAno = separar_dataframes_ano(self.dataFrame, self.fuso)
        self.dataFrameSeparadoAno=True

    def boxbChanged(self, x):
        print(x.get())
        
    def configScreen(self, root):
        opScreen = Toplevel(root)
        
        listScreenToCloseOnComfirm=[opScreen]
        
        opScreen.title('Opções de Configuração')
        
        outputCheck = BooleanVar()

        outCheckBtn = Checkbutton(opScreen,
                        text='Saída No Seu Browser Padrão',
                        # command=lambda:self.boxbChanged(outputCheck),
                        variable=outputCheck,
                        onvalue=True,
                        offvalue=False)
        outCheckBtn.grid(row=0, column=0, padx=(30, 5), pady=(20, 30), columnspan=2)

        toBind = {
                    'externalOutput' : outputCheck
                }
        
        comfirmButton = Button(opScreen, text='Comfirmar', command = lambda:self.confrimScreen(toBind, listScreenToCloseOnComfirm))
        comfirmButton.grid(row=1, column=3, padx=(50, 30), pady=(0, 30))
        
        opScreen.grab_set()
        opScreen.mainloop()
        
    def confrimScreen(self, dataBind, listScreenToCloseOnComfirm):
        screen = Tk()
        screen.title('Confirmação')
        listScreenToCloseOnComfirm.append(screen)
        
        textLabel = Label(screen, text='Deseja salvar as altereções?')
        textLabel.grid(row=0, column=0, padx=(30, 30), pady=(30, 50), columnspan=2)

        comfirmButton = Button(screen, text='Salvar', command = lambda:self.confrimBind(listScreenToCloseOnComfirm, dataBind))
        comfirmButton.grid(row=1, column=0, padx=(30, 50), pady=(0, 30))

        refuseButton = Button(screen, text='Descartar', command = screen.destroy)
        refuseButton.grid(row=1, column=1, padx=(50, 30), pady=(0, 30))
        
        screen.mainloop()
        
    def confrimBind(self, listScreenToClose, dataBind):    
        self.externalOutput=dataBind['externalOutput'].get()
        
        for screen in reversed(listScreenToClose):
            screen.destroy()
            
        messagebox.showinfo(title='Alterado', message='Alterações concluidas')

    def helpScreen(self, root):
        helpScreen = Toplevel(root)
        helpScreen.title('Informações')

        infoText = Label(helpScreen, text="Informações: \n")
        infoText.grid(row=0, column=0, padx=(100, 100), pady=(50, 0))
        infoTextInfo=infoText.grid_info()  

        container = Frame(helpScreen)

        
        userGuide = Label(container, text="   •Guia de Usuário", fg="blue", cursor="hand2")
        userGuide.grid(row=0, column=0, sticky = NW)
        userGuideInfo=userGuide.grid_info()
        userGuide.bind("<Button-1>", lambda e: openInBrowser("https://docs.google.com/document/d/16LtWiOdAq1zBPLJj3_9v3I3rdGzFP5cKeywaL3hJAGQ"))

        repositorio = Label(container, text="   •Repositório GitHub", fg="blue", cursor="hand2")
        repositorio.grid(row=userGuideInfo["row"]+1, column=userGuideInfo["column"], sticky=userGuideInfo["sticky"])
        repositorioInfo=repositorio.grid_info()
        repositorio.bind("<Button-1>", lambda e: openInBrowser("https://github.com/MigasEustaquio/Leitor_CSV_INMET"))

        container.grid(row=infoTextInfo["row"]+1, column=infoTextInfo["column"],padx=(0, 100), pady=(0, 50))



        
mainScreen = Tk()
GraphicUserInterface(mainScreen)
mainScreen.mainloop()