from tkinter import Tk, Label, Entry, Button

#              TELA
root          = Tk()
root.title("Hello Word gráfico")
root.geometry("700x500")

#        O QUE TEM NA TELA
labelFrase    = Label(root,text='Bem-Vindo ao\ndigite seu nome!!', font=('Courier New', 32), fg='#007070', bg='lightblue')
labelFrase2   = Label(root,text='Digite seu nome', font=('Courier New', 32), fg='#007070', bg='lightblue')
entryNome     = Entry(root,width=25, font=('Courier New', 32))
buttonGravar  = Button(root, text='GRAVAR', command=None, font=('Courier New', 25), fg='#007070')
labelFrase.pack(padx=5,pady=5)
labelFrase2.pack(padx=5,pady=5)
entryNome.pack(padx=5,pady=5)
buttonGravar.pack(padx=5,pady=5)

#     LOOP PARA A TELA FUNCIONAR
root.mainloop()