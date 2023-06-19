# Construct Personalized ttk.TreeView Object
# Author: Aldenir Luiz 12/03/2023

from tkinter import Tk, Frame
from tkinter.ttk import Treeview, Style
from ctypes import Union

class MyTable:
    """
A classe MyTable tem três atributos de instância: font, style e max_width, 
estes armazenam a fonte do texto da tabela, o estilo da tabela e a largura máxima da tabela, 
A classe tem um método __init__ que recebe um objeto Tk, uma lista de nomes de colunas e um valor opcional de largura, e inicializa a instância da classe.
O método build_view é responsável por criar a tabela. Ele configura o estilo das colunas e adiciona as colunas e os cabeçalhos da tabela. 
Em seguida, ele adiciona as linhas de dados na tabela e so entao o método retorna a tabela criada."""
    def __init__(self, _root: Tk, _columns: list, _width: int=100, font:tuple=('arial', 12), _command=None) -> None:
        self.font:tuple = font
        self.style: Style = Style()
        self.master: Tk = _root
        self.columns: Union[list:str] = _columns
        self.max_width: int = _width
        self.font_bold = (*self.font, 'bold')

        self.command = _command
        
        self.main_table = Treeview(
            master = self.master,
            selectmode = 'extended',
            columns=self.columns, 
            show='headings',
            ); self.build_view(),
        self.main_table.bind("<Double-1>", self.get_items)
            

    def build_view(self):
        self.style.configure("Treeview.Heading", font=self.font_bold)
        self.style.configure("Treeview", font=self.font)
        index_count = 0
        for column_name in self.columns:
            self.main_table.column(
                column_name, minwidth=50, width=self.max_width, anchor='n'
            )
            self.main_table.heading(
                index_count, text=column_name, anchor='n'
            )
            index_count+=1
        self.main_table.pack(expand=1, fill='both')
        return self.main_table
    
    def get_items(self, event):
        try:
            item = self.main_table.selection()[0]
            values = self.main_table.item(item, 'values')

            self.command(values, reverse=True)
            self.main_table.delete(item)
        except:
            return event



if __name__ == "__main__":
    tree_columns_names = ["Nome", "Idade", "Sexo", "Id"]
    tree_data = [
        ['Aldenir', '29', 'Masculino', '#3231'],
        ['Jeronimo', '41', 'Masculino', '#4561'],
        ['Francisco', '34', 'Masculino', '#7895']
    ]

    my_window = Tk()
    view = MyTable(my_window, tree_columns_names, 120).build_view()

    for (_nome, _idade,_sexo, _id) in tree_data:
        view.insert('', 'end', values=(_nome, _idade, _sexo, _id))

    my_window.mainloop()
