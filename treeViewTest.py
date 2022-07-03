from tkinter import *
from tkinter import ttk

from numpy import empty

def addTreeEntrys(tree, tipo, data, variavel):
    tree.insert('', END, values=(tipo, data, variavel))

def getElemet(tree):
    try:
        # idxItem = tree.selection()[0]
        # print(idxItem)
        # print(tree.item(idxItem, 'values'))
        print(len(tree.get_children()))
        print(tree.get_children())
        for i in tree.get_children():
            print(tree.item(i, 'values'))
    except IndexError:
        pass

def deleteElement(tree):
    try:
        # idxItem = tree.selection()[0]
        # print(idxItem)
        # tree.delete(idxItem)
        tree.delete(*tree.get_children())
    except IndexError:
        pass    



win = Tk()

#tipo data variável
entrysContainer = Frame(win)
entrysContainer.grid(row = 0, column = 0)

treeEntrys = ttk.Treeview(entrysContainer, column=("c1", "c2", "c3"), show='headings', height=3)
treeEntrys.column("# 1", anchor=CENTER)
treeEntrys.heading("# 1", text="Tipo")
treeEntrys.column("# 2", anchor=CENTER)
treeEntrys.heading("# 2", text="Data")
treeEntrys.column("# 3", anchor=CENTER)
treeEntrys.heading("# 3", text="Variavel")
treeEntrys.grid(row = 0, column = 0)
scrollbar = Scrollbar(entrysContainer, orient='vertical', command = treeEntrys.yview)
treeEntrys['yscrollcommand'] = treeEntrys.set
scrollbar.grid(row=0, column = 1 ,sticky='ns')

treeEntrys.insert



#entry=['tipo', 'data', 'variavel']
btn = Button(win, text='Add', command = lambda: addTreeEntrys(treeEntrys, 'tipo', 'data', 'variavel'))
btn.grid(row = 1, column = 0)

btn = Button(win, text='Get', command = lambda: getElemet(treeEntrys))
btn.grid(row = 1, column = 1)

btn = Button(win, text='Deleta', command = lambda: deleteElement(treeEntrys))
btn.grid(row = 1, column = 2)

win.mainloop()