from tkinter import TclError
from tqdm import tqdm
from time import sleep
import psutil
import datetime
import sys
import PySimpleGUI as sg
import os
import ctypes
ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
from configparser import ConfigParser

janelamenu = True

#LEITURA DO ARQUIVO#
config_object = ConfigParser()
config_object.read("config.ini")
userinfo = config_object["USERINFO"]
limite = (userinfo["limit"])

ultima_verificacao = datetime.datetime.now().second

conv = int(limite)
print(type(limite))
print(type(conv))
print(limite)
print(conv)

#LAYOUT MENU#
layout_menu = [
[sg.Text("Monitoramento - RAM/CPU",font=('Arial',25))],
[sg.Text("RAM",font=('Arial',18))],
[sg.Text(psutil.virtual_memory,key='ram')],
[sg.Text("-------------------------------------------------------------------------------------------------------")],
[sg.Text("CPU",font=('Arial',18))],
[sg.Text(psutil.cpu_percent,key='cpu')],
[sg.Button("Sair",key='sair',size=(18,2)),sg.Button("Iniciar",key='iniciar',size=(22,2)),sg.Button("Configuracoes",key='conf',size=(18,2))],
]

#LAYOUT CONFIG#
layout_config = [
    [sg.Text('Limite - Ram: '), sg.InputText(''+limite)], 
    [sg.Button('Salvar'), sg.Button('Voltar')]
]

while janelamenu:
    windowMenu = sg.Window('Ram - Check', layout_menu, finalize=True, disable_close=False,element_justification='c')
    windowConf = sg.Window('Configuracoes', layout_config, finalize=True, disable_close=True,element_justification='c')
    windowConf.Hide()
    event, values = windowMenu.read()
    if event in (sg.WINDOW_CLOSED, 'sair'):
        janelamenu = False
        break
        windowMenu.Close()

    if event == 'conf':
        windowMenu.Hide()
        windowConf.UnHide()
        event, values = windowConf.read()
        conv = (values[0])

        if event == 'Salvar':
            windowConf.Hide()
            windowMenu.UnHide()
            event, values = windowMenu.read()

            config_object = ConfigParser()
            config_object.read("config.ini")

            userinfo = config_object["USERINFO"]

            userinfo["limit"] = conv

            with open('config.ini', 'w') as conf:
                config_object.write(conf)
            conv = int(limite)
            print(type(limite))
            print(type(conv))
            print(limite)
            print(conv)
        if event == 'Voltar':
            windowConf.Hide()
            windowMenu.UnHide()
            event, values = windowMenu.read()
            conv = int(limite)
            print(type(limite))
            print(type(conv))
            print(limite)
            print(conv)

    if event == "iniciar":
        windowMenu['sair'].update(visible=False)
        windowMenu['conf'].update(visible=False)
        windowMenu['iniciar'].update(visible=False)
        windowMenu.refresh()
        windowConf.Close()

    while True:
        verifica_pasta = os.path.exists('log')
        if verifica_pasta == False:
            os.mkdir('log')
        try:
            ultima_verificacao = datetime.datetime.now().second
            ram_info = psutil.virtual_memory().percent
            cpu_percent = psutil.cpu_percent()
            sleep(0.5)
            windowMenu.refresh()
            windowMenu['ram'].update(psutil.virtual_memory().percent)
            windowMenu['cpu'].update(psutil.cpu_percent())
            if psutil.virtual_memory().percent >= conv:
                if ultima_verificacao != datetime.datetime.now().second:
                    sys.stdout = open("log\log.txt", "a")
                    print("--Memoria | Passou de 90%\nData: ",datetime.datetime.now(),'\n')
                    sys.stdout.close()
                    windowMenu['ram'].update(text_color='red')
                    continue
            if psutil.cpu_percent() >= conv:
                if ultima_verificacao != datetime.datetime.now().second:
                    windowMenu['cpu'].update(text_color='red')
                    continue
            if psutil.cpu_percent() < conv:
                if ultima_verificacao != datetime.datetime.now().second:
                    windowMenu['cpu'].update(text_color='white')
                    continue
            if psutil.virtual_memory().percent <= conv:
                if ultima_verificacao != datetime.datetime.now().second:
                    windowMenu['ram'].update(text_color='white')
                    continue
            windowMenu.refresh()

        except (TclError):
            sg.Popup("Encerrado")
            janelamenu = False
            break
            windowMenu.Close()
        except Exception as e:
            sg.Popup(f"Erro ao consultar | {e}")
            janelamenu = False
            break
            windowMenu.Close()

    windowMenu.close()

windowMenu.close()
