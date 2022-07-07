import re
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo


from util.manipulaDataFame import *
from util.dataView import *
import util.graphicWindow as GW


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
    for i, entry in enumerate(lista_entries):
        print(entry.get())
        data=entry.get()
        
        if not data:
            print('Nenhuma data foi selecionada')
        else:
            if padrao_dia.match(data):
                print(f'DIA {data}')
                if i==0: tempo='dia'
                else:
                    if tempo!='dia':
                        showinfo(title='Erro', message='Apenas um formato de data é aceito por vez!')
                        data = tempo = ''
            elif padrao_mes.match(data):
                print(f'MÊS {data}')
                if i==0: tempo='mes'
                else:
                    if tempo!='mes':
                        showinfo(title='Erro', message='Apenas um formato de data é aceito por vez!')
                        data = tempo = ''
            elif padrao_ano.match(data):
                print(f'ANO {data}')
                if i==0: tempo='ano'
                else:
                    if tempo!='ano':
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
    #print(tree.get_children())
    listValues=[]
    if len(tree.get_children())==0:
        return
    else: 
        for idxItem in tree.get_children():
            listValues.append(tree.item(idxItem, 'values'))
    return listValues
   


class GraphicInterface(object): 
    def __init__(self):

        self.dataFrame = pd.DataFrame
        self.dataFrameDia = pd.DataFrame
        self.dataFrameMes = pd.DataFrame
        self.dataFrameAno = pd.DataFrame

        self.fuso='-3'
        self.dataFrameSeparadoDia=False
        self.dataFrameSeparadoMes=False
        self.dataFrameSeparadoAno=False
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

        self.splitDataFrameButton = Button(self.mainScreen, text='Separa Data Frame por mês', command = self.splitDataFrameMes)
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

        self.listboxLabels.insert('end', 'Horas de Sol Pleno (HSP)')


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
        
        self.treeViewEntrys = ttk.Treeview(testeScreen, column=("c1", "c2", "c3"), show='headings', height=5)
        self.treeViewEntrys.column("# 1", anchor=CENTER, width = 50)
        self.treeViewEntrys.heading("# 1", text="Tipo")
        self.treeViewEntrys.column("# 2", anchor=CENTER, width = 100)
        self.treeViewEntrys.heading("# 2", text="Data")
        self.treeViewEntrys.column("# 3", anchor=CENTER,  width = 150)
        self.treeViewEntrys.heading("# 3", text="Variável")
        self.treeViewEntrys.grid(column=self.labelEntrysInfo['column'], row=self.labelEntrysInfo['row']+1, sticky='nwes')
        self.treeViewEntrysInfo = self.treeViewEntrys.grid_info()

        self.scrollbarTreeViewEntrys = Scrollbar(testeScreen, orient='vertical', command = self.treeViewEntrys.yview)
        self.treeViewEntrys['yscrollcommand'] = self.treeViewEntrys.set
        self.scrollbarTreeViewEntrys.grid(column=self.treeViewEntrysInfo['column']+1, row=self.treeViewEntrysInfo['row'], sticky='ns')
        self.scrollbarTreeViewEntrysInfo = self.scrollbarTreeViewEntrys.grid_info()


        # self.listBoxEntrys = Listbox(testeScreen, height=6, exportselection=0, width = 60)
        # self.listBoxEntrys.grid(column=self.labelEntrysInfo['column'], row=self.labelEntrysInfo['row']+1, sticky='nwes')
        # self.listBoxlabelEntrysInfo = self.listBoxEntrys.grid_info()

        # self.scrollbarEntrys = Scrollbar(testeScreen, orient='vertical', command=self.listBoxEntrys.yview)
        # self.listBoxEntrys['yscrollcommand'] = self.scrollbarEntrys.set
        # self.scrollbarEntrys.grid(column=self.listBoxlabelEntrysInfo['column']+1, row=self.listBoxlabelEntrysInfo['row'], sticky='ns')
        # self.scrollbarEntrysInfo = self.scrollbarEntrys.grid_info()
        

        self.btnsEntrysContainer = Frame(testeScreen)
        self.btnsEntrysContainer.grid(row = self.scrollbarTreeViewEntrysInfo['row'], column = self.scrollbarTreeViewEntrysInfo['column']+1)
        self.btnsEntrysContainerInfo =  self.btnsEntrysContainer.grid_info()
        
        self.btnLimpar = Button(self.btnsEntrysContainer, text='Remover Todas Entradas', command = lambda: self.treeViewEntrys.delete(*self.treeViewEntrys.get_children()))
        self.btnLimpar.grid(row = 0, column = 0, sticky = NW)
        self.btnLimparInfo = self.btnLimpar.grid_info()
        
        self.btnRemoverElemento = Button(self.btnsEntrysContainer, text='Remover Entrada Selecionada', command = lambda: removeTreeViewSelectedEntry(self.treeViewEntrys))
        self.btnRemoverElemento.grid(row = self.btnLimparInfo['row']+1, column = 0, sticky = NW)
        self.btnRemoverElementoInfo = self.btnRemoverElemento.grid_info()

        self.btnGerarGraficoElemento = Button(self.btnsEntrysContainer, text='Plotar Gráfico para Entrada Selecionada', command = lambda : self.gera_grafico_unico(getTreeViewSelectedEntry(self.treeViewEntrys)))
        self.btnGerarGraficoElemento.grid(row = self.btnRemoverElementoInfo['row']+1, column = 0, sticky = NW)
        self.btnGerarGraficoElementoInfo = self.btnGerarGraficoElemento.grid_info()

        self.btnGerarGraficoTodosElementos = Button(self.btnsEntrysContainer, text='Plotar Gráfico com Todas Entradas', command = lambda: self.gera_grafico_multiplos(getAllTreeViewEntrys(self.treeViewEntrys)))
        self.btnGerarGraficoTodosElementos.grid(row = self.btnGerarGraficoElementoInfo['row']+1, column = 0, sticky = NW)
        self.btnGerarGraficoTodosElementosInfo = self.btnGerarGraficoTodosElementos.grid_info()
        

        self.btnAvancar = Button(testeScreen, text='Avançar', command = lambda: self.op_intervalo_data(self.listboxTipoGrafico))
        self.btnAvancar.grid(row = self.listboxTipoGraficoInfo['row']+1, column = self.listboxTipoGraficoInfo['column'])
        self.btnAvancarInfo = self.btnAvancar.grid_info()
    
        self.btnVoltar = Button(testeScreen, text = 'Voltar', command = lambda: print('voltar'))

        self.buttonAddEntry = Button(testeScreen, text='Adicionar Linha', command=lambda: self.cria_entry_data(testeScreen))
        self.buttonAddEntry.grid(row=self.treeViewEntrysInfo['row']+1, column=self.treeViewEntrysInfo['column'])
        self.buttonAddEntryInfo = self.buttonAddEntry.grid_info()

        self.btnAdicionarListaEntradas = Button(testeScreen, text = 'Adicionar Entrada')
        self.btnAdicionarListaEntradas.grid(row = self.listboxLabelsInfo['row']+1, column = self.listboxLabelsInfo['column'])
        self.btnAdicionarListaEntradasInfo = self.btnAdicionarListaEntradas.grid_info()
        self.btnAdicionarListaEntradas.grid_forget()

        self.cria_entry_data(testeScreen)

        testeScreen.mainloop

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
                self.showElement(self.btnAvancar, self.btnAvancarInfo)

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
        self.showElement(self.btnAvancar, self.btnVoltarInfo)
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
            self.showElement(self.btnAdicionarListaEntradas, self.btnAdicionarListaEntradasInfo)
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
                self.showElement(self.btnAdicionarListaEntradas, self.btnAdicionarListaEntradasInfo)
                #self.btnAdicionarListaEntradas.configure(command = lambda: self.addEntryToListBox([self.tipoGrafico, self.opMes], self.listboxLabels, self.listBoxEntrys))
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
            self.showElement(self.btnAdicionarListaEntradas, self.btnAdicionarListaEntradasInfo)
            #self.btnAdicionarListaEntradas.configure(command = lambda: self.addEntryToListBox([self.tipoGrafico, self.opDia], self.listboxLabels, self.listBoxEntrys))
            self.btnAdicionarListaEntradas.configure(command = lambda: self.addEntryToTreeViewEntrys(self.tipoGrafico, self.opDia))
        except IndexError:
            showinfo(title='Erro', message='Selecione o dia')
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
        

        datas, tempo = tratamento_formato_data(self.lista_entries)

        if tempo == '': return

        if not datas:
            showinfo(title='Erro', message='Nenhuma data foi selecionada')
            return

        msg = 'Tipo de Gráfico: '+str(tipo_selecionado)+'\nColuna: ' + variavel_selecionada + '\nData:'
        for data in datas: msg+=' '+data
        print(msg)

        if variavel_selecionada == 'Horas de Sol Pleno (HSP)':
            if len(datas)>1:
                showinfo(title='Erro', message='Para verificar as horas de sol pleno selecione apenas uma data')
                return

        # try:
        #     self.gerar_grafico_qualquer_variavel(tipo_selecionado, datas, variavel_selecionada)
        # except:
        #     showinfo(title='Erro', message='Erro ao gerar gráfico') #erro genérico provisório
        self.gerar_grafico_qualquer_variavel(tipo_selecionado, datas, variavel_selecionada, tempo)



    # def addEntryToListBox(self, info, listBoxCheck, listBoxInsert):
    #     try:
    #         op = listBoxCheck.curselection()[0]
    #         entry = [info, listBoxCheck.get(op)]
    #         entryText = 'Informaçoes; Data: '
    #         for i in info:
    #             entryText += i+' '
    #         entryText +='; Variavel: '+listBoxCheck.get(op)
    #         listBoxInsert.insert('end', entryText)
    #         print(entryText)
    #         self.voltarDefault()
    #     except IndexError:
    #         showinfo(title='Erro', message='Selecione o parâmetro indicado')
    #         return
    
    def addEntryToTreeViewEntrys(self, tipo, data):
        try:
           idxItem = self.listboxLabels.curselection()[0]
           variavel = self.listboxLabels.get(idxItem)
           self.treeViewEntrys.insert('','end', values=(tipo, data, variavel))
           self.voltarDefault()
        except IndexError:
            showinfo(title='Erro', message='Selecione uma Variável')
            return

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
                        if self.dataFrameSeparadoMes:
                            self.splitDataFrameMes()
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
    def splitDataFrameMes(self):
        self.dataFrameMes = separar_dataframes_mes(self.dataFrame, self.fuso)
        self.dataFrameSeparadoMes=True
    
    def splitDataFrameDia(self):
        self.dataFrameDia = separar_dataframes_dia(self.dataFrame, self.fuso)
        self.dataFrameSeparadoDia=True
    
    def splitDataFrameAno(self):
        self.dataFrameAno = separar_dataframes_ano(self.dataFrame, self.fuso)
        self.dataFrameSeparadoAno=True

# Criando lista de botões associados aos meses
        btns=[]
        for mes in list(self.dataFrameMes.keys()):
            # print('key: ', mes)
            btnName=self.dataFrameMes[mes]['Date (UTC'+self.fuso+')'].values[0]+' a '+self.dataFrameMes[mes]['Date (UTC'+self.fuso+')'].values[-1]
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
        mediaPorHora, horasDoDia = mediaDia(self.dataFrameMes[key_referencia], 'Radiacao (KWh/m²)', self.fuso)
        print(self.dataFrameMes[key_referencia])
        print('NOME: ', nome_referencia)
        geraGraficoBonito(horasDoDia, 'Hora '+'(UTC'+self.fuso+')' , mediaPorHora, 'Radiação (KWh/m²)', 'Gráfico da radiação '+nome_referencia)
        GW.main()

    def gera_grafico_unico(self, values):
        tipo, data, variavel = values
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
            mediaPorHora, horasDoDia = mediaDia(df, 'Radiacao (KWh/m²)', self.fuso)
        else: 
            mediaPorHora, horasDoDia = mediaDia(df, variavel, self.fuso)
        titulo=f'Gráfico {variavel}, média {tipo}: {data}'
        geraGraficoBonito([horasDoDia], 'Hora '+'(UTC'+self.fuso+')', [mediaPorHora], [variavel], [titulo])
        GW.main()

    def gera_grafico_multiplos(self, listValues):
        print(listValues)
        listMediaPorHora = []
        listHorasDoDia = []
        listTitulo = []
        listVariaveis = []
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
                mediaPorHora, horasDoDia = mediaDia(df, 'Radiacao (KWh/m²)', self.fuso)
            else: 
                mediaPorHora, horasDoDia = mediaDia(df, variavel, self.fuso)

            listVariaveis.append(variavel)
            listMediaPorHora.append(mediaPorHora)
            listHorasDoDia.append(horasDoDia)
            titulo= f'Gráfico {variavel}, média {tipo}: {data}'
            listTitulo.append(titulo)

        geraGraficoBonito(listHorasDoDia, 'Hora '+'(UTC'+self.fuso+')', listMediaPorHora, listVariaveis, listTitulo)
        GW.main()


#Tornar possível fazer gráfico com várias variávei
    def gerar_grafico_qualquer_variavel(self, tipo_grafico, datas_referencia, variavel_referencia, tempo):

        eixoY=[]
        eixoX=[]

        if tipo_grafico == 0: # Gráfico Diário

            if tempo == 'dia':
                for data_referencia in datas_referencia:

                    nome_df = data_referencia.split('/')
                    if len(nome_df)>2: nome_df=nome_df[1]+'/'+nome_df[2]

                    if variavel_referencia == 'Horas de Sol Pleno (HSP)':
                        y, x = valores_um_dia(self.dataFrameMes[nome_df], 'Radiacao (KWh/m²)', self.fuso, data_referencia)
                    else:
                        y, x = valores_um_dia(self.dataFrameMes[nome_df], variavel_referencia, self.fuso, data_referencia)
                    eixoX.append(x)
                    eixoY.append(y)

            elif tempo == 'mes':
                for data_referencia in datas_referencia:
                    if variavel_referencia == 'Horas de Sol Pleno (HSP)':
                        y, x = mediaDia(self.dataFrameMes[data_referencia], 'Radiacao (KWh/m²)', self.fuso)
                    else:
                        y, x = mediaDia(self.dataFrameMes[data_referencia], variavel_referencia, self.fuso)
                    eixoX.append(x)
                    eixoY.append(y)

            elif tempo == 'ano':
                showinfo(title='Erro', message='Não implementado!')
                return

        elif tipo_grafico == 1: # Gráfico Mensal

            if tempo == 'dia': showinfo(title='Erro', message='Não pode ser feito um gráfico mensal de apenas um dia!')

            elif tempo == 'mes':
                for data_referencia in datas_referencia:
                    x=[]
                    y=[]
                    dias = listaDiasNovo(self.dataFrameMes[data_referencia], data_referencia, self.fuso)
                    for dia in dias:
                        media = mediaDiaNotNull(self.dataFrameMes[data_referencia], variavel_referencia, dia+'/'+data_referencia, self.fuso)
                        x.append(dia)
                        y.append(media)
                    eixoX.append(x)
                    eixoY.append(y)

            elif tempo == 'ano':
                showinfo(title='Erro', message='Não implementado!')
                return


        elif tipo_grafico == 2: # Gráfico Anual

            if tempo == 'dia': showinfo(title='Erro', message='Não pode ser feito um gráfico anual de apenas um dia!')

            elif tempo == 'mes': showinfo(title='Erro', message='Não pode ser feito um gráfico anual de apenas um mês!')
            
            elif tempo == 'ano':
                showinfo(title='Erro', message='Não implementado!')
                return

        numero_curvas=len(eixoY)
        legendaX='Hora '+'(UTC'+self.fuso+')'

        if variavel_referencia == 'Horas de Sol Pleno (HSP)':
            geraGraficoHSP(eixoX, legendaX, eixoY[0], variavel_referencia)
        else:
            geraGraficoBonito(eixoX, legendaX, eixoY, variavel_referencia, 'Gráfico de '+ variavel_referencia + ' ' + data_referencia, numero_curvas)
        GW.main()


	  
 
GraphicInterface()