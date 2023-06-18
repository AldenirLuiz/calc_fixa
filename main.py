from tkinter import Tk, Frame, Label, Entry, Button, END, Event, messagebox
from my_treeview import MyTable
from mainLayout import Layout
from modelData import DataModel
from manage import ViewCard

class ConfigLayout:
    key_events = [
        "<KeyRelease-Return>", "<KeyRelease-KP_Add>", "<KeyRelease-KP_Enter>"
    ]
    celulas = {
        "cobranca":[
            "total_cobrado",
            "repasse_novo",
            "comissao_venda",],
        "mercadoria":[
            "liquido_venda",
            "total_vendido",
            "devolucao",]}
    # "valor_vendido" "comissao" "liquido_venda" "repasse" "total_da_ficha" "devolucao" "valor_pago"
    view_keys = (
        "total_vendido", "comissao_venda", "liquido_venda",
        "repasse_novo", "total_da_ficha", "devolucao", "total_cobrado",)
    
    def __init__(self) -> None:
        self.window = Tk()

        self.primary = Frame(self.window)
        self.secondary = Frame(self.window)
        self.primary.pack(side="left",expand=True, fill="both")
        self.secondary.pack(side="left",expand=True, fill="both")
        # Container para visualizacao dos dados calculados
        self.dict_values = dict()
        # Container para colecao de widgets
        self.widgets = dict()
        # Container para os valores cauculados temporariamente
        self.values = tuple()

        self.temp_calc_session = dict()

        # Campo de insercao de dados; Valor Pago
        self.widgets.update(
            {"total_da_ficha": MyCard(self.secondary, "Total da Ficha",
                lambda: self.switch_event("total_da_ficha"))})
        # Campo de insercao de dados; Valor Pago
        self.widgets.update(
            {"devolucao": MyCard(self.secondary, "Devolucao",
                lambda: self.switch_event("devolucao"))})
        # Campo de insercao de dados; Valor Pago
        self.widgets.update(
            {"valor_pago": MyCard(self.secondary, "Valor Pago",
                lambda: self.switch_event("valor_pago"))})
        self.widgets.update(
            {"restante": MyCard(self.secondary, "Restante",
                lambda: self.switch_event("restante"))})
        # botoes
        self.widgets.update(
            {"button_c": Button(self.secondary, text="Finalizar", command=ViewCard().whrite(self.dict_values))})
        self.widgets.update(
            {"button": Button(self.secondary, text="Proxima", command=self.calculate)})
        # Listbox exibe fichas calculadas
        self.tree_columns_names = ["Valor da Ficha", "Devolucao", "Valor Vendido", "Valor Pago", "Saldo Devedor"]
        self.view_tree = MyTable(self.primary, self.tree_columns_names, font=("consolas", 8), _command=self.update_values).build_view()
        
        self.frame_view = Frame(self.primary)
        self.view_data = Layout.create_lay(self.frame_view, self.celulas, "label", font=("arial", 8))
        self.frame_view.pack()

        self.__build__()
        self.widgets["total_da_ficha"].focus()
        self.window.mainloop()



class MainLayout(ConfigLayout):

    def __build__(self):
        for widget in self.widgets.values():
            if isinstance(widget, MyCard):
                widget.build()
            else:
                for event in self.key_events:
                    widget.bind(event, self.calculate)
                widget.pack(side="left")
    
    def switch_event(self, name:str):
        if name != "restante":
            sequence = {
                "total_da_ficha": "devolucao",
                "devolucao": "valor_pago",
                "valor_pago": "restante"}
            self.widgets[sequence[name]].focus()
        else:
            self.calculate()
    
    def calculate(self):
        try:
            data = (
                float(self.widgets["total_da_ficha"].get()),
                float(self.widgets["devolucao"].get()),
                float(self.widgets["valor_pago"].get()),
                float(self.widgets["restante"].get()))
            
            model_val = DataModel(data)
            values = model_val.calculate()

            values_tree = (*data[:2], values[0], data[2], values[3])

            self.cache(data, values)
            self.clear_fields()
            self.insert_on(values_tree)
            self.update_values(values)
            self.widgets["total_da_ficha"].focus()
        except:
            return
        
    def cache(self, data, values):
        self.temp_calc_session.update(
            {f"{(f'{data[0]}', f'{data[1]}', f'{values[0]}', f'{data[2]}', f'{values[3]}')}": values})
        
    def clear_fields(self):
        for field in self.widgets.values():
            if isinstance(field, MyCard):
                field.clear()

    def insert_on(self, data):
        self.view_tree.insert("", 0, values=data)
    
    def update_values(self, values:tuple, reverse=False):
        if self.values != tuple():
            if reverse:
                self.values = tuple(x - y for x, y in zip(self.values, self.temp_calc_session[f"{values}"]))
            else:
                self.values = tuple(x + y for x, y in zip(self.values, values))
            self.dict_values = dict(zip(self.view_keys, self.values))
            ViewCard().whrite(self.dict_values)
            self.view_update()
        else: 
            self.values = values
            self.dict_values = dict(zip(self.view_keys, self.values))
            ViewCard().whrite(self.dict_values)
            self.view_update()

    def view_update(self):
        for value in self.dict_values.keys():
            if value in self.view_data.keys():
                self.view_data[value].configure(text=f"{self.dict_values[value]}")
        

        
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



if __name__ == "__main__":
    lay = MainLayout()