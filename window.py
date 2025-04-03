from tkinter import*

root = Tk()
root.title("window")
root.geometry("800x600")


def mostarnome():
    valor = entryTxt.get()
    labelFrase2.config(text=valor)
    labelFrase2.pack(padx=5,pady=5)


def apagarnome():
    labelFrase2.config(text='')
     

labelFrase2 = Label(root, text='', font=('Courier New',32), fg='#FaFfaa', bg='#AaAaAa')
labelFrase1 = Label(root, text='Bem-vindo ao digite seu nome!!', font=('Courier New',32), fg='#FaFfaa', bg='#AaAaAa', width=800)
labelFrase = Label(root, text='Digite seu nome:', font=('Courier New',32), fg='#FaFfaa', bg="#AaAaAa", width=800)
entryTxt = Entry(root, font=('Courier New',32))
buttonGravar = Button(root, text='GRAVAR', command=(mostarnome), font=('Courier New',20), fg='#FaFfaa', bg='#AaAaAa')
buttonGravar1 = Button(root, text='APAGAR', command=apagarnome, font=('Courier New',20), fg='#FaFfaa', bg='#AaAaAa')
labelFrase2 = Label(root, text='', font=('Courier New',32), fg='#FaFfaa', bg='#AaAaAa')

labelFrase1.pack(padx=5,pady=5)
labelFrase.pack(padx=5,pady=5)
entryTxt.pack(padx=5,pady=5)
buttonGravar.pack(padx=5,pady=5)
buttonGravar1.pack(padx=5,pady=5)

root.mainloop()