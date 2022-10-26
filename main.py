import PySimpleGUI as sg
import mysql.connector
from datetime import datetime
from dateutil.relativedelta import relativedelta


banco = mysql.connector.connect(
    host='localhost',
    user='root',
    password='i!ggRv265Vm43HC',
    database='levantamento_ginecologico'
)
cursor = banco.cursor()
SQl_use = 'use levantamento_ginecologico'
cursor.execute(SQl_use)
banco.commit()
print('Banco de Dados Conectado!')

# Janelas
def janela_inicial():
    layout_inical = [
        [sg.Button('Nova Tabela', size=(20,1))],
        [sg.Button('Carregar Tabela', size=(20,1))],
        [sg.Button('Excluir Tabela', size=(20,1))]
    ]
    return sg.Window('Levantamento Ginecológico', layout=layout_inical, finalize=True)

def nova_tabela():
    layout_nova = [
        [sg.Text('Nome', size=(5,1)), sg.Input(size=(10,1), key='nome')],
        [sg.Text('Dia da Inseminação', size=(17,1)), sg.Input(size=(10,1), key='inseminacao')],
        [sg.Button('Salvar'), sg.Button('Cancelar')]
    ]
    return sg.Window('Nova Tabela', layout=layout_nova, finalize=True)

def carregar_tabela():
    layout_carregar = [
        [sg.Output(size=(20,10), key='carregar')],
        [sg.Button('Mostrar'), sg.Button('Voltar')]
    ]
    return sg.Window('Carregar Tabelas', layout=layout_carregar, finalize=True)

def excluir_tabela():
    layout_excluir = [
        [sg.Text('Digite o Id', size=(11,1)), sg.Input(size=(5,1), key='excluir_id')],
        [sg.Button('Excluir'), sg.Button('Cancelar')]
    ]
    return sg.Window('Excluir Tabela', layout=layout_excluir, finalize=True)

janela1, janela2, janela3, janela4 = janela_inicial(), None, None, None

#SQL
def criando_tabelas():
    cursor = banco.cursor()
    SQL_create = (f"insert into vacas (Nome, Dia_Inseminacao, Estimativa_parto) values (%s, %s, %s);")
    dados = (str(values['nome']), dia_inseminacao, estimativa_parto)
    cursor.execute(SQL_create, dados)
    banco.commit()
    [sg.Popup('Tabela criada com sucesso!')]

def mostrando_tabelas():
    cursor = banco.cursor()
    SQL_select = 'select * from vacas;'
    cursor.execute(SQL_select)
    result = cursor.fetchall()

    window['carregar'].update(result)

def excluindo_tabelas():
    cursor = banco.cursor()
    SQL_delete = (f"delete from vacas where id = {values['excluir_id']};")
    cursor.execute(SQL_delete)
    banco.commit()
    [sg.Popup('Tabela excluída com sucesso!')]

while(True):
    window, event, values = sg.read_all_windows()

    if(janela1):
        if(event == sg.WINDOW_CLOSED):
            break

        if(event == 'Nova Tabela'):
            janela2 = nova_tabela()
            janela1.hide()

        if(event == 'Carregar Tabela'):
            janela3 = carregar_tabela()
            janela1.hide()


        if(event == 'Excluir Tabela'):
            janela4 = excluir_tabela()
            janela1.hide()

    if(janela2):
        if (event == 'Cancelar'):
            janela2.hide()
            janela1.un_hide()

        if(event == 'Salvar'):
            dia_inseminacao = datetime.strptime(values['inseminacao'], '%Y-%m-%d')
            estimativa_parto = dia_inseminacao + relativedelta(months=9)

            if(estimativa_parto < datetime.today()):
                [sg.Popup('Data Inválida')]
            else:
                criando_tabelas()

    if(janela3):
        if(event == 'Voltar'):
            janela3.hide()
            janela1.un_hide()

        if(event == 'Mostrar'):
            mostrando_tabelas()

    if(janela4):
        if(event == 'Cancelar'):
            janela4.hide()
            janela1.un_hide()

        if(event == 'Excluir'):
            excluindo_tabelas()

banco.close()