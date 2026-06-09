import os, time
import json
from datetime import datetime

def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    agora = datetime.now()
    data_br = agora.strftime("%d/%m/%Y")
    hora_br = agora.strftime("%H:%M:%S")
    dadosDict[nome] = (pontos, data_br, hora_br)
    
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo
    
def maior_pontuador():
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    nome_maior = None
    dataJogada =  None
    horaJogada = None
    maior_pontos = -1

    for nome, info in dadosDict.items():

        pontos = info[0]
        dataJogada = info[1]
        horaJogada = info[2]
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            dataJogada = info[1]
            horaJogada = info[2]

    return nome_maior, maior_pontos, dataJogada, horaJogada