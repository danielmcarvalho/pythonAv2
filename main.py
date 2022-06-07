import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as msb
from tkinter import Tk, Label, StringVar, Entry, Button, Frame, Menu, Scrollbar, Toplevel, NO, TOP, X, Y, W, SOLID, LEFT, CENTER, RIGHT, BOTTOM, HORIZONTAL, VERTICAL


root = Tk()
root.title("ALUNOS MATRICULADOS")
width = 800
height = 600
sc_width = root.winfo_screenwidth()
sc_height = root.winfo_screenheight()
x = (sc_width/2) - (width/2)
y = (sc_height/2) - (height/2)
root.iconbitmap('E:\pythonProject\index\\favicon.ico')
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0,0)
root.config(bg='#FFFAFA')


nome = StringVar()
sobrenome = StringVar()
serie = StringVar()
turno = StringVar()
data_nascimento = StringVar()
matricula = None
update_window = None
new_window = None
caminho_db = 'E:\pythonProject\index\\alunos.db'


def database():
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    query = '''CREATE TABLE IF NOT EXISTS matriculados (
                matricula INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                sobrenome TEXT,
                data_nascimento TEXT,
                serie TEXT,
                turno TEXT
            )'''
    cursor.execute(query)
    cursor.execute('SELECT * FROM matriculados ORDER BY nome')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()


def submit():
    if nome.get() == '' or sobrenome.get() == '' or turno.get() == '' or serie.get() == '' or data_nascimento.get() == '':
        msb.showwarning('', 'Por favor, digite todos os campos.', icon='warning')
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        query = 'INSERT INTO matriculados (nome, sobrenome, data_nascimento, serie, turno) VALUES (?, ?, ?, ?, ?)'
        cursor.execute(query, (str(nome.get()), str(sobrenome.get()), str(data_nascimento.get()), str(serie.get()), str(turno.get())))
        conn.commit()
        cursor.execute('SELECT * FROM matriculados ORDER BY nome')
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        cursor.close()
        conn.close()
        nome.set('')
        sobrenome.set('')
        data_nascimento.set('')
        serie.set('')
        turno.set('')


def update():
    tree.delete(*tree.get_children())
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    cursor.execute('''UPDATE matriculados SET nome = ?, sobrenome = ?, data_nascimento = ?, serie = ?, turno = ? WHERE matricula = ?''',
                   (str(nome.get()), str(sobrenome.get()), str(data_nascimento.get()), str(serie.get()), str(turno.get()), int(matricula)))
    conn.commit()
    cursor.execute('SELECT * FROM matriculados ORDER BY nome')
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=data)
    cursor.close()
    conn.close()
    nome.set('')
    sobrenome.set('')
    data_nascimento.set('')
    serie.set('')
    turno.set('')
    update_window.destroy()


def selected(event):
    global matricula, update_window
    selected = tree.focus()
    conteudo = (tree.item(selected))
    itens_selecionados = conteudo['values']
    matricula = itens_selecionados[0]
    nome.set('')
    nome.set(itens_selecionados[1])
    sobrenome.set('')
    sobrenome.set(itens_selecionados[2])
    data_nascimento.set('')
    data_nascimento.set(itens_selecionados[3])
    serie.set('')
    serie.set(itens_selecionados[4])
    turno.set('')
    turno.set(itens_selecionados[5])

    update_window = Toplevel()
    update_window.title('ATUALIZAR')
    form_titulo = Frame(update_window)
    form_titulo.pack(side=TOP)
    form_alunos = Frame(update_window)
    form_alunos.pack(side=TOP, pady=10)
    width = 400
    height = 300
    sc_width = update_window.winfo_screenwidth()
    sc_height = update_window.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    update_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    update_window.resizable(0, 0)


    lbl_titulo = Label(form_titulo, text='Atualizando aluno', font=('calibri', 20),width=200)
    lbl_titulo.pack(fill=X)
    lbl_nome = Label(form_alunos, text='Nome', font=('calibri', 14))
    lbl_nome.grid(row=0, sticky=W)
    lbl_sobrenome = Label(form_alunos, text='Sobrenome', font=('calibri', 14))
    lbl_sobrenome.grid(row=1, sticky=W)
    lbl_nascimento = Label(form_alunos, text='Data de Nascimento', font=('calibri', 14))
    lbl_nascimento.grid(row=2, sticky=W)
    lbl_serie = Label(form_alunos, text='Série', font=('calibri', 14))
    lbl_serie.grid(row=3, sticky=W)
    lbl_turno = Label(form_alunos, text='Turno', font=('calibri', 14))
    lbl_turno.grid(row=4, sticky=W)


    ent_nome = Entry(form_alunos, textvariable=nome,  font=('calibri', 14))
    ent_nome.grid(row=0, column=1)
    ent_sobrenome = Entry(form_alunos, textvariable=sobrenome, font=('calibri', 14))
    ent_sobrenome.grid(row=1, column=1)
    ent_nascimento = Entry(form_alunos, textvariable=data_nascimento, font=('calibri', 14))
    ent_nascimento.grid(row=2, column=1)
    ent_serie = Entry(form_alunos, textvariable=serie, font=('calibri', 14))
    ent_serie.grid(row=3, column=1)
    ent_turno = Entry(form_alunos, textvariable=turno, font=('calibri', 14))
    ent_turno.grid(row=4, column=1)


    btn_atualizar = Button(form_alunos, text='Atualizar', foreground='white', bg='#228B22', width=50, command=update)
    btn_atualizar.grid(row=6, columnspan=2, pady=10)


def insert():
    global new_window
    nome.set('')
    sobrenome.set('')
    data_nascimento.set('')
    serie.set('')
    turno.set('')


    new_window = Toplevel()
    new_window.title("CADASTRO")
    form_titulo = Frame(new_window)
    form_titulo.pack(side=TOP)
    form_contato = Frame(new_window)
    form_contato.pack(side=TOP, pady=10)
    width = 400
    height = 300
    sc_width = new_window.winfo_screenwidth()
    sc_height = new_window.winfo_screenheight()
    x = (sc_width/2) - (width/2)
    y = (sc_height/2) - (height/2)
    new_window.geometry("%dx%d+%d+%d" % (width, height, x, y))
    new_window.resizable(0, 0)


    lbl_titulo = Label(form_titulo, text='Inserindo aluno', font=('calibri', 20), width=200)
    lbl_titulo.pack(fill=X)
    lbl_nome = Label(form_contato, text='Nome', font=('calibri', 14))
    lbl_nome.grid(row=0, sticky=W)
    lbl_sobrenome = Label(form_contato, text='Sobrenome', font=('calibri', 14))
    lbl_sobrenome.grid(row=1, sticky=W)
    lbl_nascimento = Label(form_contato, text='Data de Nascimento', font=('calibri', 14))
    lbl_nascimento.grid(row=2, sticky=W)
    lbl_serie = Label(form_contato, text='Série', font=('calibri', 14))
    lbl_serie.grid(row=3, sticky=W)
    lbl_turno = Label(form_contato, text='Turno', font=('calibri', 14))
    lbl_turno.grid(row=4, sticky=W)


    ent_nome = Entry(form_contato, textvariable=nome,  font=('calibri', 14))
    ent_nome.grid(row=0, column=1)
    ent_sobrenome = Entry(form_contato, textvariable=sobrenome, font=('calibri', 14))
    ent_sobrenome.grid(row=1, column=1)
    ent_nascimento = Entry(form_contato, textvariable=data_nascimento, font=('calibri', 14))
    ent_nascimento.grid(row=2, column=1)
    ent_serie = Entry(form_contato, textvariable=serie, font=('calibri', 14))
    ent_serie.grid(row=3, column=1)
    ent_turno = Entry(form_contato, textvariable=turno, font=('calibri', 14))
    ent_turno.grid(row=4, column=1)


    btn_atualizar = Button(form_contato, text='Cadastrar', foreground='white', bg='#228B22', width=50, command=submit)
    btn_atualizar.grid(row=6, columnspan=2, pady=10)


def delete():
    if not tree.selection():
        msb.showwarning('', 'Por favor, selecione um item da lista', icon='warning')
    else:
        resultado = msb.askquestion('', 'Tem certeza que deseja cancelar a matrícula?')
        if resultado == 'yes':
            item_selecionado = tree.focus()
            conteudo = (tree.item(item_selecionado))
            item = conteudo['values']
            tree.delete(item_selecionado)
            conn = sqlite3.connect(caminho_db)
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM matriculados WHERE matricula = {item[0]}')
            conn.commit()
            cursor.close()
            conn.close()


top = Frame(root, width=500)
top.pack(side=TOP)
mid = Frame(root, width=500, bg='#FFFAFA')
mid.pack(side=TOP)
midleft = Frame(mid, width=100)
midleft.pack(side=LEFT)
midleftPadding = Frame(mid, width=10, bg='#FFFAFA')
midleftPadding.pack(side=LEFT)
midrightPadding = Frame(mid, width=10, bg='#FFFAFA')
midrightPadding.pack(side=RIGHT)
midright = Frame(mid, width=100)
midright.pack(side=RIGHT)
bottom = Frame(root, width=500)
bottom.pack(side=BOTTOM)
tableMargin = Frame(root, width=500)
tableMargin.pack(side=TOP)


lbl_titulo = Label(top, text='INFORMAÇÕES ACADEMICAS', font=('calibri', 20), background='#FFFAFA', width=500)
lbl_titulo.pack(fill=X)

lbl_alterar = Label(bottom, text='Para alterar clique duas vezes no aluno desejado!', font=('calibri', 20), width=500)
lbl_alterar.pack(fill=X)


bttn_incluir = Button(midleft, text='INSERIR', foreground='white', bg='#228B22', command=insert)
bttn_incluir.pack()

bttn_excluir = Button(midright, text='EXCLUIR', foreground='white', bg='#FF0000', command=delete)
bttn_excluir.pack(side=RIGHT)


ScrollbarX = Scrollbar(tableMargin, orient=HORIZONTAL)
ScrollbarY = Scrollbar(tableMargin, orient=VERTICAL)

tree = ttk.Treeview(tableMargin, columns=('Matricula', 'Nome', 'Sobrenome', 'Data de Nascimento', 'Série', 'Turno'),
                    height=400, selectmode='extended', yscrollcommand=ScrollbarY.set, xscrollcommand=ScrollbarX.set)
ScrollbarY.config(command=tree.yview)
ScrollbarY.pack(side=RIGHT, fill=Y)
ScrollbarX.config(command=tree.xview)
ScrollbarX.pack(side=BOTTOM, fill=X)
tree.heading('Matricula', text='Matricula', anchor=W)
tree.heading('Nome', text='Nome', anchor=W)
tree.heading('Sobrenome', text='Sobrenome', anchor=W)
tree.heading('Data de Nascimento', text='Data de Nascimento', anchor=W)
tree.heading('Série', text='Série', anchor=W)
tree.heading('Turno', text='Turno', anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=1)
tree.column('#1', stretch=NO, minwidth=0, width=80)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=120)
tree.column('#5', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', selected)


menu_bar = Menu(root)
root.config(menu=menu_bar)


menu_arquivo = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=menu_arquivo)
menu_arquivo.add_command(label='Criar novo', command=insert)
menu_arquivo.add_separator()
menu_arquivo.add_command(label='Sair', command=root.destroy)

menu_sobre = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Sobre', menu=menu_sobre)
menu_sobre.add_command(label='Info')

if __name__ == '__main__':
    database()
    root.mainloop()