from tkinter import *
from tkinter import ttk
from tkinter import tix
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser



root = tix.Tk()

class Relatorios():
    def print_clienntes(self):
        webbrowser.open("clientes.pdf")
    def gerar_relatorio(self):
        self.c = canvas.Canvas('clientes.pdf')
        self.codigo_rel = self.codigo_entry.get()
        self.nome_rel = self.nome_entry.get()
        self.telefone_rel = self.telefone_entry.get()
        self.cidade_rel = self.cidade_entry.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont('Helvetica', 18)
        self.c.drawString(100, 700, 'Codigo: ' + self.codigo_rel)
        self.c.drawString(100, 670, 'Nome: ' + self.nome_rel)
        self.c.drawString(100, 630, 'Telefone: ' + self.telefone_rel)
        self.c.drawString(100, 600, 'Cidade: ' + self.cidade_rel)

        self.c.showPage()
        self.c.save()
        self.print_clienntes()
class Funcs():
    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor(); print('Conectando ao Banco de Dados')
    def desconecta_bd(self):
        self.conn.close(); print('Desconectando ao Banco de Dados')
    def monta_tabelas(self):
        self.conecta_bd();
        ### Criar tabela
        self.cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS clientes ( 
        cod INTEGER PRIMARY KEY,
        nome_clientes CHAR(40) NOT NULL,
        telefone INTERGER(20),
        cidade CHAR(40)
        );
    """)
        self.conn.commit(); print('Banco de Dados criado')
        self.desconecta_bd()
    def variavel_cadastro(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
    def add_cliente(self):
        self.variavel_cadastro()
        self.conecta_bd()

        self.cursor.execute("""
        INSERT INTO clientes (nome_clientes, telefone, cidade)
        VALUES(?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_clientes, telefone, cidade FROM clientes
         ORDER BY nome_clientes ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd
    def OnDoubleClik(self, event):
        self.limpa_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    def deleta_cliente(self):
        self.variavel_cadastro()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_cliente(self):
        self.variavel_cadastro()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_clientes = ?, telefone = ?, cidade = ?
        WHERE cod = ?""", (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(""" SELECT cod, nome_clientes, telefone,
        cidade FROM clientes WHERE nome_clientes LIKE '%s' ORDER BY 
        nome_clientes ASC
        """ % nome)
        busca_nomeCli = self.cursor.fetchall()
        for i in busca_nomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()
class Aplication(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame_1()
        self.lista_frame_2()
        self.monta_tabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='#000003')
        self.root.geometry('700x500')
        self.root.resizable(True, True)
        self.root.maxsize(width=1200, height=900)
        self.root.minsize(width=500, height=400)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#040c13', highlightbackground='#081922',
                             highlightthickness=4)
        self.frame_1.place(relx=0.02, rely=0.02, relheight=0.46, relwidth=0.960)

        self.frame_2 = Frame(self.root, bd=4, bg='#040c13', highlightbackground='#081922',
                             highlightthickness=4,)
        self.frame_2.place(relx=0.02, rely=0.5, relheight=0.46, relwidth=0.960)
    def widgets_frame_1(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba_1 = Frame(self.abas)
        self.aba_2  = Frame(self.abas)

        self.aba_1.configure(background= "#040c13")
        self.aba_2.configure(background='#040c13')

        self.abas.add(self.aba_1, text='Clientes')
        self.abas.add(self.aba_2, text='Produtos')

        self.abas.place(relx=0, rely=0, relwidth=0.9999, relheight=0.9999)


        ### Criação do botão 'limpar'
        self.bt_limpar = Button(self.aba_1, text="Limpar", bd=3, bg='#103141', fg='white',
                                command=self.limpa_tela, activebackground='#103058',
                                activeforeground='white'
                                )
        self.bt_limpar.place(relx=0.2, rely=0.10, relwidth=0.1, relheight=0.15)

        ### Criação do botão 'buscar'
        self.bt_buscar = Button(self.aba_1, text="Buscar", bd=3, bg='#103141', fg='white',
                                command=self.busca_cliente, activebackground='#103058',
                                activeforeground='white')
        self.bt_buscar.place(relx=0.31, rely=0.10, relwidth=0.1, relheight=0.15)

            ## Criando balâo de texto
        text_balao_buscar = 'Digite no campo "Nome" o nome do cliente que deseja buscar'
        self.balao_buscar = tix.Balloon(self.aba_1)
        self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg = text_balao_buscar)


        ### Criação do botão 'cadastrar'
        self.bt_cadastar = Button(self.aba_1, text="Cadastrar", bd=3, bg='#103141', fg='white',
                                command=self.add_cliente, activebackground='#103058',
                                activeforeground='white')
        self.bt_cadastar.place(relx=0.6, rely=0.10, relwidth=0.1, relheight=0.15)

        ### Criação do botão 'Alterar'
        self.bt_alterar = Button(self.aba_1, text="Alterar", bd=3, bg='#103141', fg='white',
                                 command=self.altera_cliente, activebackground='#103058',
                                 activeforeground='white')
        self.bt_alterar.place(relx=0.71, rely=0.10, relwidth=0.1, relheight=0.15)

        ### Criação do botão 'Apagar'
        self.bt_apagar = Button(self.aba_1, text="Apagar", bd=3, bg='#103141', fg='white',
                                command=self.deleta_cliente, activebackground='#103058',
                                activeforeground='white')
        self.bt_apagar.place(relx=0.82, rely=0.10, relwidth=0.1, relheight=0.15)

        ### Criação da label e entrada do codigo
        self.lb_codigo = Label(self.aba_1, text='Código',bg='#040c13', fg='#1ca2d8')
        self.lb_codigo.place(relx= 0.05, rely=0.033)

        self.codigo_entry = Entry(self.aba_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        ### Criação da label e entrada da nome
        self.lb_nome = Label(self.aba_1, text="Nome", bg='#040c13', fg='#1ca2d8')
        self.lb_nome.place(relx=0.05, rely=0.33)

        self.nome_entry = Entry(self.aba_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.85)

        ### Criação da label e entrada do telefone
        self.lb_telefone = Label(self.aba_1, text="Telefone",bg='#040c13', fg='#1ca2d8')
        self.lb_telefone.place(relx=0.05, rely=0.63)

        self.telefone_entry = Entry(self.aba_1)
        self.telefone_entry.place(relx=0.05, rely=0.75, relwidth=0.4)

        ### Criação da label e entrada da Cidade
        self.lb_cidade = Label(self.aba_1, text="Cidade",bg='#040c13', fg='#1ca2d8')
        self.lb_cidade.place(relx=0.5, rely=0.63)

        self.cidade_entry = Entry(self.aba_1)
        self.cidade_entry.place(relx=0.5, rely=0.75, relwidth=0.4)
    def lista_frame_2(self):
        ###criando a listagem dos objetos
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=('col1, col2, col3, col4'))
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Código')
        self.listaCli.heading('#2', text='Nome do Cliente')
        self.listaCli.heading('#3', text='Telefone')
        self.listaCli.heading('#4', text='Cidade')

        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=50)
        self.listaCli.column('#2', width=200)
        self.listaCli.column('#3', width=150)
        self.listaCli.column('#4', width=150)

        self.listaCli.place(relx=0, rely=0, relwidth=0.999, relheight=0.999)
        ###criando o scrool da lista
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscrollcommand=self.frame_2,)
        self.scroolLista.place(relx=0.96, rely=0.01, relwidth=0.03, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClik)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label='Opções', menu=filemenu)
        menubar.add_cascade(label='Relatorio', menu=filemenu2)

        filemenu.add_command(label='Sair', command=Quit)
        filemenu2.add_command(label='Gerar Relatorio', command=self.gerar_relatorio)




Aplication()