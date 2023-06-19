from tkinter import messagebox, Toplevel, Frame, Label, Button, Entry, StringVar

class DataModel:
    data_keys = (
            "valor_vendido", "comissao", "liquido_venda",
            "repasse", "total_da_ficha", "devolucao", "valor_pago"
        )
    messages = "O valor do REPASSE esta negativo."
    def __init__(self, values:tuple) -> None:
        self.valor_ficha = values[0]
        self.devolucao = values[1]
        self.valor_pago = values[2]
        self.restante = values[3]

        self.calculate = self.__calc__
        self.model = self.__data_model__

    def __calc__(self):
        self.valor_vendido = float(round(self.valor_ficha - self.devolucao))
        self.comissao = float(round(self.valor_vendido * 0.3))
        self.liquido_venda = float(round(self.valor_vendido - self.comissao))
        self.repasse = float(round(self.liquido_venda - self.valor_pago))

        if self.repasse < 0:
            self.repasse += self.restante
            
        return (
                self.valor_vendido, self.comissao, 
                self.liquido_venda, self.repasse, 
                self.valor_ficha, self.devolucao, 
                self.valor_pago)
            
    def __data_model__(self):
        return dict(zip(self.data_keys, self.calculate()))

class MessageWindow:
    def __init__(self):
        self.window = Toplevel()
        self.frm_0 = Frame(self.window)

        self.message_label = Label(self.frm_0, text=None)
        self.message_label.pack()
        self.value = StringVar(self.window)

        self.desc_label = Label(self.frm_0, text="Restante da ficha: ")
        self.entry = Entry(self.frm_0,textvariable=self.value)
        self.desc_label.pack(expand=False, fill="x", padx=4, pady=2)
        self.entry.pack(expand=False, fill="x", padx=6, pady=4)
        self.btn = Button(self.frm_0, text="Confirmar", command=lambda: self.__rep_value__)
        self.btn.pack()
        self.get_value = self.__rep_value__

        self.frm_0.pack()

        if isinstance(self.get_value, float):
            return self.value
            self.window.destroy() 
        
    def __rep_value__(self) -> float:
        self.window.mainloop()
        while self.get_value:
            self.get_value = round(float(self.entry.get()))
            return self.value
        
        self.window.destroy()


if __name__ == "__main__":
# valor_ficha - devolucao - valor_pago
    values = (200, 100, 100)
    processed = DataModel(values=values)
    print(processed.calculate())