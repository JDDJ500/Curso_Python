import requests
from tkinter import Tk, LabelFrame, Frame, Label, Entry, END, Button, ttk, StringVar, messagebox

# Informações Base
pokemons        = []
next_pokemon_id = 1
opcoes      = ["Selecione" ,"Ano/s", "Mes/es", "Dia/s"]
Lista_Info = []

# Informações do pokemon
def get_name():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showerror("ERRO", "Selecione um pokemon!")
        return
    pokemon      = entry_pokemon.get()
    return pokemon


def INFO():
    name = get_name()
    if not name:
        messagebox.showerror("ERRO", "Nome do Treinador e Pokemon não inseridos!")
        return
    
    S_root = Tk()
    S_root.title("Informação do pokemon")
    S_root.geometry("800x500")

    # Frame
    frame_info = LabelFrame(S_root, text="Informações")
    frame_info_habilidades = LabelFrame(S_root, text="Habilidades")

    # Labels
    Label(frame_info, text="Pokemon:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    Label(frame_info, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    Label(frame_info, text="Tipo:").grid(row=2, column=0, padx=5, pady=5, sticky='e')

    # Mostrar
    frame_info.pack(pady=5, fill="x")
    frame_info_habilidades.pack(pady=5, fill="x")

    # Info Pokemon
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        Label(frame_info, text=(data['name'])).grid(row=0, column=1, padx=5, pady=5, sticky='e')
        Label(frame_info, text=(data['id'])).grid(row=1, column=1, padx=5, pady=5, sticky='e')
        for t in data['types']:
            Label(frame_info, text=(f" - {t['type']['name']}")).grid(row=2, column=1, padx=5, pady=5, sticky='e')
    
    # Info Hbilidades
    if response.status_code == 200:
        line = 0
        for ability in data['abilities']:
            Label(frame_info_habilidades, text=(f" - {ability['ability']['name']}")).grid(row=line, column=0, padx=5, pady=5, sticky='e')
            line += 1

# Funções dos Botões
def limpar():
    entry_treinador.delete(0, END)
    entry_pokemon.delete(0, END)
    entry_tipo.delete(0, END)
    entry_quantidade.delete(0, END)
    entry_idade.delete(0, END)
    opcao_selecionada.set("Selecione")

def Carregar_pokemon():
    for item in tree.get_children():
        tree.delete(item)
    for pokemon in pokemons:
        tree.insert('', 'end', values=(
            pokemon['id'],
            pokemon['treinador'],
            pokemon['pokemon'],
            pokemon['tipo'],
            pokemon['quantidade'],
            pokemon['idade']
        ))

def ADD_pokemon():
    global next_pokemon_id
    treinador    = entry_treinador.get()
    pokemon      = entry_pokemon.get()
    tipo         = entry_tipo.get()
    quantidade   = entry_quantidade.get()
    idade        = entry_idade.get()
    selecao      = opcao_selecionada.get()

    if not treinador or not pokemon:
        messagebox.showerror('Erro', 'Treinador e Pokemon são obrigatórios')
        return
    try:
        idade_int = int(idade) if idade else 0
    except ValueError:
        messagebox.showerror('Erro', 'Idade deve ser um numero inteiro')
        return
    
    novo_pokemon = {
        'id': next_pokemon_id,
        'treinador': treinador,
        'pokemon': pokemon,
        'tipo': tipo,
        'quantidade': quantidade,
        'idade': (idade +" "+ str(selecao)),
    }

    pokemons.append(novo_pokemon)
    next_pokemon_id += 1

    messagebox.showinfo('Sucesso', 'Pokemon cadastrado com exito')
    Carregar_pokemon()
    limpar()

def EDIT_pokemon():
    selecionado = tree.selection()
    if not selecionado:
        messagebox.showerror("ERRO", "Selecione um pokemon para editar!")
        return
    pokemon_id = tree.item(selecionado)['values'][0]
    treinador    = entry_treinador.get()
    pokemon      = entry_pokemon.get()
    tipo         = entry_tipo.get()
    quantidade   = entry_quantidade.get()
    idade        = entry_idade.get()
    selecao      = opcao_selecionada.get()

    if not treinador or not pokemon:
        messagebox.showerror("ERRO", "Treinador e Pokemon são obrigatórios!")
        return
    
    try:
        idade_int = int(idade) if idade else 0
    except ValueError:
        messagebox.showerror("ERRO", "Idade deve ser um numero inteiro!")
        return
    for pokemon in pokemons:
        if pokemon['id'] == pokemon_id:
            pokemon.update({
            'id': next_pokemon_id,
            'treinador': treinador,
            'pokemon': pokemon,
            'tipo': tipo,
            'quantidade': quantidade,
            'idade': (idade_int +" "+ str(selecao))
            })
            break
        messagebox.showinfo("Sucesso!", "Pokemon atualizado")
        Carregar_pokemon()

#Função da Tabela
def selecionar_pet(event):
    selecionado = tree.selection()
    if not selecionado:
        return
    
    values = tree.item(selecionado)['values']
    limpar()

    entry_treinador.insert(0, values[1])
    entry_pokemon.insert(0, values[2])
    entry_tipo.insert(0, values[3])
    entry_quantidade.insert(0, values[4])
    entry_idade.insert(0, values[5])

# Criar Janela

root = Tk()
root.title("Sistema de Cadastro de Pokemonss")
root.geometry("800x500")

# Frames
frame_form = LabelFrame(root, text="Formulario de Pokemon")
frame_form_btn = Frame(root)
frame_form_tabela = Frame(root)

# Tabela
    # Cabeçario
tree = ttk.Treeview(frame_form_tabela, columns=('ID', 'Treinador', 'Nome', 'Tipo', 'Quantidade', 'Idade'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Treinador', text='Treinador')
tree.heading('Nome', text='Nome')
tree.heading('Tipo', text='Tipo')
tree.heading('Quantidade', text='Quantidade')
tree.heading('Idade', text='Idade')
    # Colunas
tree.column('ID', width=50)
tree.column('Treinador', width=150)
tree.column('Nome', width=100)
tree.column('Tipo', width=100)
tree.column('Quantidade', width=100)
tree.column('Idade', width=50)

    # Scrollbar
scrollbar = ttk.Scrollbar(frame_form_tabela, orient="vertical", command=tree.yview)

    # Tree configuração
tree.configure(yscrollcommand=scrollbar.set)
tree.bind('<<TreeviewSelect>>', selecionar_pet)

# Configuração dos Nomes Apresentados
Label(frame_form, text="Treinador:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
Label(frame_form, text="Pokemon:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
Label(frame_form, text="Tipo:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
Label(frame_form, text="Quantidade:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
Label(frame_form, text="Idade:").grid(row=4, column=0, padx=5, pady=5, sticky='e')

# Receber Dados
entry_treinador    = Entry(frame_form, width=40)
entry_pokemon      = Entry(frame_form, width=40)
entry_tipo         = Entry(frame_form, width=40)
entry_quantidade   = Entry(frame_form, width=40)
entry_idade        = Entry(frame_form, width=40)



# Botões
btn_adicionar      = Button(frame_form_btn, text="Adicionar", command=ADD_pokemon, width=20).grid(row=0, column=0, padx=5, pady=5)
btn_editar         = Button(frame_form_btn, text="Editar", command=EDIT_pokemon, width=20).grid(row=0, column=1, padx=5, pady=5)
btn_remover        = Button(frame_form_btn, text="Remover", command=None, width=20).grid(row=0, column=3, padx=5, pady=5)
btn_limpar         = Button(frame_form_btn, text="Limpar", command=limpar, width=20).grid(row=0, column=4, padx=5, pady=5)
btn_info_pokemon   = Button(frame_form_btn, text="Informações", command=INFO, width=20).grid(row=0, column=5, padx=5, pady=5)
opcao_selecionada  = StringVar(frame_form)
menu_opcoes        = ttk.OptionMenu(frame_form, opcao_selecionada, "Selecione", *opcoes)

# Mostrar na Tela
frame_form            .pack(padx=10,pady=5,fill='x')
frame_form_btn        .pack(pady=5)
frame_form_tabela     .pack(padx=10, pady=5, fill='both', expand=True)
entry_treinador       .grid(row=0, column=1, padx=5, pady=5)
entry_pokemon         .grid(row=1, column=1, padx=5, pady=5)
entry_tipo            .grid(row=2, column=1, padx=5, pady=5)
entry_quantidade      .grid(row=3, column=1, padx=5, pady=5)
entry_idade           .grid(row=4, column=1, padx=5, pady=5)
menu_opcoes           .grid(row=4, column=2,pady=5)
tree                  .pack(side='left', fill='both', expand=True)
scrollbar             .pack(side='right', fill='y')

opcao_selecionada.set("Selecione")

# Loop da Janela
root.mainloop()
