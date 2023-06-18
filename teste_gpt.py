class DataModel:

    data_keys = (
            "valor_vendido","comissao","liquido_venda","repasse","total_da_ficha","devolucao","valor_pago"
        )
    def __init__(self, values:tuple) -> None:
        self.valor_ficha = values[0]
        self.devolucao = values[1]
        self.valor_pago = values[2]
        self.calculate = self.__calc__
        self.model = self.__data_model__

    def __calc__(self):
        self.valor_vendido = self.valor_ficha - self.devolucao
        self.comissao = self.valor_vendido * 0.3
        self.liquido_venda = self.valor_vendido - self.comissao
        self.repasse = self.liquido_venda - self.valor_pago
        return (self.valor_vendido, self.comissao, self.liquido_venda, self.repasse)

    def __data_model__(self):
        return dict(zip(self.data_keys, self.calculate()))


# valor_ficha - devolucao - valor_pago
values = (200, 100, 50)
processed = DataModel(values=values)
print(processed.model())