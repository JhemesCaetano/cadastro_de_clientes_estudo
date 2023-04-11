#amnos os imports é para armarzenar as imagens no codigo
#_________________________________
import base64
from PIL import ImageTk, Image
#_________________________________


##### armazenado imagens no codigo
def imagens_base64(self):
    self.btbovo_base64 ='utilize o conversor do site base64.guru'



### criando Menus
def Menus(self):
    menubar = Menu(self.root)
    self.root.config(menu=menubar)
    filemenu = Menu(menubar)
    filemenu2 = Menu(menubar)

    def Quit(): self.root.destroy()

    menubar.add_cascade(label='Opções', menu=filemenu)
    menubar.add_cascade(label='Sobre', menu=menubar)

    filemenu.add_command(label='Sair', command=Quit)
    filemenu2.add_command(label='limpa cliente', command=self.limpa_tela)
### criando botões estilizazdos
    self.img_novo = PhotoImage(file='botaonovo.gif')
    self.img_novo = self.img_novo.subsample((2, 2))

    self.style = ttk.Style()
    self.style.configure('BW.TButton', relwidth=1, relheigth=1, foreground='gay',
     borderwidth=0, bordercolor='gay', background='#103058',
     image=self.img_novo)

