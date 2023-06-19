
from tkinter import END, Entry, Frame, Label, messagebox, Event



class MyCard:
    key_events = [
        "<KeyRelease-Return>", "<KeyRelease-KP_Add>", "<KeyRelease-KP_Enter>"
    ]
    descriptions = {
        "total da ficha": "Valor Total das mercadorias na ficha",
        "devolucao": "Valor Total das mercadorias devolvidas pela cliente.",
        "valor pago": "Valor pago pela cliente em dinheiro e ou pix",
        "title_error": "Erro. Dados inseridos Invalidos.", 
        "message_error": "Os dados Inseridos estao incorretos! Verifique os dados inseridos e tente novamente.",
        "restante": "Preencha este campo somente se houver restante na ficha"
    }
    def __init__(self, _master:Frame, _name:str, _command) -> None:
        # Campo de insercao de dados
        self.name = _name.lower().strip()
        self.mainframe = Frame(_master, bd=1, relief="ridge")
        # Criando a entrada de dados e sua descricao
        self.label = Label(self.mainframe, text=_name)
        self.entry = Entry(self.mainframe, name=self.name)
        self.label_desc = Label(self.mainframe, text=self.descriptions[self.name])
        
        # Adicionando eventos de tecla ao entry
        self.bind_events()
        # Entregando o container principal a instancia para chamada posterior
        self.build = self.__build__
        # Defininndo o retorno de dados da entry
        self.get = self.__get_value__
        # Definindo o clear
        self.clear = self.__clear_field__
        # Definido o evento de foco na entry
        self.focus = self.__focus__
        self.command = _command
        self.pack()

    # Funcao responsavel por posicionar o caontainer principal na janela
    def __build__(self) -> None:
        return self.mainframe.pack(expand=True, fill="both")
    # Funcao responsavel por obter o valor digitado na entry
    def __get_value__(self) -> str:
        try:
            self.entry.configure(fg="black")
            return float(self.clean_field(self.entry.get()))
        except:
            messagebox.showwarning(self.descriptions["title_error"], self.descriptions["message_error"])
            self.entry.configure(fg="red")
            self.entry.focus()
            return
    
    def clean_field(self, value: str):
        my_string = str()
        for char in value:
            if char.isnumeric():
                my_string += char
            elif char in ".,":
                my_string += "."
        return my_string

    # Limpar campo
    def __clear_field__(self):
        self.entry.delete(0, END)
        if self.name == "restante":
            self.entry.insert(0, "0")

    # Chama a funcao respectiva passado como argumento em _command
    def key_event(self, event:Event):
        self.command()

    # Define o foco para a entry
    def __focus__(self):
        self.entry.focus()
    # Alocando eventos
    def bind_events(self):
        for event in self.key_events:
            self.entry.bind(event, self.key_event)
    def pack(self):
        self.label.config(justify="left", padx=4, pady=2, anchor="nw")
        if self.name == "restante":
            self.label_desc.configure(fg="black", font=('arial', 8), wraplength=122)
            self.entry.insert(0, "0")
        else:
            self.label_desc.configure(fg="green", font=('arial', 8), wraplength=122)
        self.label.pack(expand=False, fill="x", padx=4, pady=2)
        self.entry.pack(expand=False, fill="x", padx=4, pady=2)
        self.label_desc.pack(expand=False, fill="x", padx=4, pady=2)