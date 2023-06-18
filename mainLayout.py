from tkinter import Label, Entry, Frame, Widget


# ESTA CLASSE E RESPONSAVEL POR DISTRIBUIR O LAYOUT DINAMICAMENTE
class Layout:
    dictEntryWidget = dict()

    # define o tipo de widget para os dados como do tipo entrada
    @staticmethod
    def ret_entry(name: str, root: Widget | Frame, _font: tuple | None=None):
        if _font:
            font: tuple = _font
        else: font: tuple = ("arial", 12)
        widget = Entry(  # configuracoes do Entry
                root, width=21, relief='groove', name=name, justify="right")
        widget.pack(  # posicao de alocamento do widget na grade
                side='left', expand=0, fill='both', padx=2, pady=2, ipadx=2, ipady=2)
        return widget

    # define o tipo de widget para os dados como do tipo texto
    @staticmethod
    def ret_label(name: str, root: Widget | Frame, vtext: str, _font: tuple | None=None):
        if _font:
            font = _font
        else: font = ("arial", 12)
        widget = Label(  # configuracoes do Label
                root, font=font, text=vtext, width=16,
                relief='flat', name=name, justify="left", anchor="nw")
        widget.pack(  # posicao de alocamento na grade
                side='left', expand=0, fill='both', padx=2, pady=2, ipadx=2, ipady=2, anchor="nw")
        return widget

    # cria um widget opcional (usado para preencher o espaco reservado)
    @staticmethod
    def sub_widget(sb_widget: Widget | Frame):
        sb_widget.pack(  # alocando o subwidget na grade
                side='right', expand=1, fill='both', padx=2, pady=2, ipadx=2, ipady=2)

    # cria o card a receber os widgets
    @staticmethod
    def create_card(root: Widget | Frame, desc: str):
        # container de disposicao da grade frm0
        label = Label(root, text=desc.upper(), relief='groove')
        label.pack(expand=1, fill='x')

    # cria uma tarja de descricao acima do card quando solicitado
    @staticmethod
    def desc_widget(root: Widget | Frame, descricao: str):
        label_cobranca = Label(root, text=descricao.upper(), anchor='center')
        label_cobranca.pack()

    # cria o texto a ser exibido ao lado do widget de dados
    @staticmethod
    def ret_static_var(root: Widget | Frame, text_var: str, _font: tuple | None=None):
        if _font:
            font = _font
        else: font = ("arial", 12)
        texto_statico = Label(  # configuracoes do Label
                root, text=text_var, font=font, width=20, relief='flat', anchor='ne')
        texto_statico.pack(  # posicao de alocamento do widget na grade
                side='left', expand=1, fill='both', padx=2, pady=2, ipadx=2, ipady=2)

    @staticmethod
    def create_lay(*args, **misc) -> dict:
        """root:tk.Frame|tk.Widget, desc:str|bytes, subwidget:tk.Frame|tk.Widget"""
        root, celulas, type_wid = args
        desc:str|bytes|None = misc.get('desc')
        subwidget: Frame|Widget|None = misc.get('subwidget')
        data: dict|None = misc.get('data')
        font: tuple|None = misc.get('font')
        default: bool|None = misc.get('default')
        _exclude: list|None = misc.get('_exclude')

            
        #  percorre as celulas presentes no pacote
        for desc, celula in celulas.items():
            frm0 = Frame(root, relief='groove', bd=2)
            Layout.create_card(frm0, desc)
            # percorre os widgets presentes no pacote
            for widget in celula:
                # removendo caracteres desnecessarios
                name = str(widget)
                if data:
                    data_names = data.get(name)
                else:
                    data_names = ""
                frm1 = Frame(frm0, relief='flat')  # criando container da grade
                Layout.ret_static_var(
                    frm1, f"{widget}:".upper().replace('_', ' '), _font=font
                )
                
                if type_wid == 'entry': # filtro de tipo de widget para Entry
                    Layout.dictEntryWidget[name] = \
                        Layout.ret_entry(name=name, root=frm1, _font=font)
                    
                    if _exclude and name in _exclude:
                        Layout.dictEntryWidget[f'{name}'] = \
                            Layout.ret_label(
                                name=name, root=frm1, vtext=None, _font=font)
                    else:
                        Layout.dictEntryWidget[f'{name}'] = \
                            Layout.ret_entry(name=name, root=frm1, _font=font)
                        
                    if default:
                        if data.get(name):
                            Layout.dictEntryWidget[f'{name}'].insert(0, data.get(name))

                else:  # filtro de tipo de widget para Label
                    Layout.dictEntryWidget[f'{name}'] = \
                        Layout.ret_label(
                            name=name, root=frm1, vtext=data_names, _font=font
                        )
                frm1.pack( # alocando do container da grade
                    anchor='w', expand=1, fill='both', padx=2, pady=1, ipadx=2, ipady=1)
                
            if subwidget:  # aqui sera alocado um subwidget caso for solicitado.
                Layout.sub_widget(subwidget)

            frm0.pack(side='left', expand=1, fill='both', padx=4, pady=2, ipadx=2, ipady=1)

        # retorna os widgets configurados e enpacotados para uso
        return Layout.dictEntryWidget
    
    