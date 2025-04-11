from tkinter import Tk, LabelFrame, Frame, Label, Entry, END, Button, ttk

pets        = []
next_pet_id = 1

# Criar Janela

root = Tk()
root.title("Sistema de Cadastro de Pets")
root.geometry("800x500")

# Frames
frame_form = LabelFrame(root, text="Formulario de Pet")
frame_form.pack(padx=10,pady=5,fill='x')

frame_form_btn = Frame(root)
frame_form_btn.pack(pady=5)

frame_form_tabela = Frame(root)
frame_form_tabela.pack(padx=10, pady=5, fill='both', expand=True)

#Tabela
tree = ttk.Treeview(frame_form_tabela, columns=('ID', 'Tutor', 'Nome', 'Espécie', 'Raça', 'Idade'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Tutor', text='Tutor')
tree.heading('Nome', text='Nome')
tree.heading('Espécie', text='Espécie')
tree.heading('Raça', text='Raça')
tree.heading('Idade', text='Idade')

# Receber Dados
Label(frame_form, text="Tutor:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_tutor = Entry(frame_form, width=40)
entry_tutor.grid(row=0, column=1, padx=5, pady=5)

Label(frame_form, text="Pet:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_pet = Entry(frame_form, width=40)
entry_pet.grid(row=1, column=1, padx=5, pady=5)

Label(frame_form, text="Especie:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
entry_especie = Entry(frame_form, width=40)
entry_especie.grid(row=2, column=1, padx=5, pady=5)

Label(frame_form, text="Raça:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
entry_raca = Entry(frame_form, width=40)
entry_raca.grid(row=3, column=1, padx=5, pady=5)

Label(frame_form, text="Idade:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
entry_idade = Entry(frame_form, width=40)
entry_idade.grid(row=4, column=1, padx=5, pady=5)

#Coleta de Dados
tutor    = entry_tutor.get()
pet      = entry_pet.get()
especie  = entry_especie.get()
raca     = entry_raca.get()
idade    = entry_idade.get()

# Funções dos Botões
def limpar():
    entry_tutor.delete(0, END)
    entry_pet.delete(0, END)
    entry_especie.delete(0, END)
    entry_raca.delete(0, END)
    entry_idade.delete(0, END)

# Botões
btn_adicionar  = Button(frame_form_btn, text="Adicionar", command=None).grid(row=0, column=0, padx=5, pady=5)
btn_editar     = Button(frame_form_btn, text="Editar", command=None).grid(row=0, column=1, padx=5, pady=5)
btn_remover    = Button(frame_form_btn, text="Remover", command=None).grid(row=0, column=3, padx=5, pady=5)
btn_limpar     = Button(frame_form_btn, text="Limpar", command=limpar).grid(row=0, column=4, padx=5, pady=5)

# Loop da Janela
root.mainloop()