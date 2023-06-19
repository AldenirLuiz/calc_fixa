from tkinter import messagebox

class DataModel:
    data_keys = (
            "valor_vendido", "comissao", "liquido_venda",
            "repasse", "total_da_ficha", "devolucao", "valor_pago"
        )
    messages = {
        "msg_rep_tit": "Verifique os Dados!",
        "msg_rep_inf": "O valor do REPASSE esta negativo!\n VALOR DO REPASSE: {}",
        "msg_rep_add": "Existe restante na ficha? Caso haja restante na ficha adicione o valor no campo corespondente."
    }
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
            if messagebox.askyesno(
                self.messages["msg_rep_tit"], 
                self.messages["msg_rep_inf"].format(self.repasse)+self.messages["msg_rep_add"],
                icon="question"):
                return
            else:
                self.repasse = 0

        return (
                self.valor_vendido, self.comissao, 
                self.liquido_venda, self.repasse, 
                self.valor_ficha, self.devolucao, 
                self.valor_pago)
            
    def __data_model__(self):
        return dict(zip(self.data_keys, self.calculate()))


if __name__ == "__main__":
# valor_ficha - devolucao - valor_pago
    values = (200, 100, 100)
    processed = DataModel(values=values)
    print(processed.calculate())