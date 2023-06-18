import json


class ViewCard:
    json_file: str = "tempData.json"
    with open(json_file, "r") as cell_names:
        layers = json.load(cell_names)

    def ret_card(self, card: str, celula: str = None):
        if celula:
            return self.layers[card][celula]
        return self.layers[card]

    @property
    def __layers__(self):
        return self.layers
    
    def whrite(self, data:dict):
        with open("tempData.json", mode='w', encoding="utf-8") as fp:
            json.dump(data, fp)



if __name__ == "__main__":
    
    dict_values = {
        "total_vendido": 10,
        "comissao_venda": 50,
        "liquido_venda": 11,
        "repasse_novo": 98,
        "total_da_ficha": 0,
        "devolucao": 22,
        "total_cobrado": 41}
    ViewCard().whrite(dict_values)
    
    print(ViewCard().layers)

