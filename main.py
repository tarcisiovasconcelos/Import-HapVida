from os import sep
import os
from tokenize import Double
import PySimpleGUI as sg
import pandas as pd
import func
from datetime import datetime
import calendar
import getpass



sg.theme("Default1")

# Layout
layout = [[sg.T("Olá, essa interface vai ajudar você a gerar o layout de importação do plano de saúde.\nApós escolher o arquivo de importação clique em 'Enviar' para enviar o mesmo para análise.\nPreste bastante atenção, depois de enviar, se houver algum problema com o CPF o sistema vai informar e encerrar\nQuando o processo de enviar for bem sucedido você pode gerar o layout  que ficará denominado de: layout.txt.\n")],
          [sg.Text("Escolha um arquivo: "), sg.Input(key="-IN2-" ,change_submits=True),
           sg.FileBrowse(key="-IN-", file_types=(("Text Files", "*.txt"),))],
           [sg.T("\n")],
          [sg.Button("Enviar"),sg.T("Se não houver arquivo selecionado a aplicação irá encerrar")],
          [sg.T("\n")],
          [sg.Button("Gerar"),sg.T("Só gera se o enviar ficar 100%")]]

# Janela
window = sg.Window('Assistente de importação HapVida', layout, size=(750,350))

# Eventos   
while True:
    event, values = window.read()
    #Primeiro evento, aqui ele permite fechar a aplicação
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    #Aqui precisamos fazer com que ele gere o novo txt para layout
    elif event == "Gerar":
        contador = 0
        username = getpass.getuser()      
        
        for linha in importRM:
            contador = contador + 1
            bigString = (f"{linha[0]};{linha[1]};{linha[2]};{linha[3]};{linha[4]};{linha[5]};{linha[6]};{linha[7]};{linha[8]};{linha[9]};{linha[10]};{linha[11]};{linha[12]};;;\n")
            with open("texto.txt", "a+") as arquivo:
                arquivo.writelines(bigString)
                arquivo.close
        with open("texto.txt", "r+") as arquivo:
            teste = arquivo.readlines()
            arquivo.close
        fpath = f"C:\\Users\\{username}\\Downloads\\"
        with open(fpath + f"layout{dataCompetencia}.txt", "w+") as arquivo:
            arquivo.writelines(teste)
            arquivo.close
        with open("texto.txt", "w+") as arquivo:
            arquivo.writelines("")
            arquivo.close
        sg.popup(f'Seu arquivo layout{dataCompetencia}.txt está pronto na pasta Downloads!')
    #Tratando o arquivo enviado
    elif event == "Enviar":
        #variavel para definir tamanho do cabeçalho
        texto1= pd.read_csv(values["-IN-"], header=None)
        #definindo tamanho do head
        for index, row in texto1.iterrows(): 
            a = row.str.contains('''Geracao em''')
            if a.any() == True:
                countHeader = a.name
        #definindo VENCIMENTO
        for index, row in texto1.iterrows(): 
            a = row.str.contains('''vencimento em''')
            if a.any() == True:
                linhaVencimento = row.array.astype(str)
                vencimento = " ".join(linhaVencimento).split(" ")
                data = 0
                for i in vencimento:
                    data = data + 1                    
                vencimento = vencimento[data-1]
                string_list = "".join(vencimento).split("/")
                int_list = list(map(int, string_list))
        test_date = datetime(int_list[2], int_list[1], int_list[0])
        res = calendar.monthrange(test_date.year, test_date.month)[1]
        mes = int_list[1]
        ano = int_list[2]
        dataCompetencia = [str(res), string_list[1], string_list[2]]
        dataCompetencia = "".join(dataCompetencia)

        #variavel para tratar os dados abaixo do cabeçalho separados por ; e salvando CPF e NOME das pessoas que estão com o plano 07F7F 
        texto = pd.read_csv(values["-IN-"], sep=";", header=(countHeader+1))
        titular = texto[texto.parentesco == 'TITULAR']
        dependente = texto[texto.parentesco != 'TITULAR']        
        titular_com_plano = titular.cpf[texto.empresa=='07F7F']
        dependente_com_plano = dependente.cpf[texto.empresa=='07F7F']
        dependenteRM = dependente.cobrado[texto.empresa=='07F7F']
        titularRM = titular.cobrado[texto.empresa=='07F7F']
        parentesco_dependente = dependente.parentesco[texto.empresa=='07F7F']
        parentesco_titular = titular.parentesco[texto.empresa=='07F7F']
        texto1 = texto[texto.empresa == '07F7F']        
        mix_matheus = [texto.cpf[texto.empresa=='07F7F'] ,texto.parentesco[texto.empresa=='07F7F']]
        dependentesArray = []
        titularesArray = []
        layoutPlanoDepend = []
        layoutPlanoTitular = []
        layoutPlano = []
        cobradosDepend = []
        cobradosTitular = []
        importRM = []
        novoDepend = []
        novoTitular = []

        #Alimentando Array's de  CPF Titular e Dependente
        for col in dependente_com_plano:
            x = col.replace("-", "")
            dependentesArray.append(x)
        
        for col in titular_com_plano:
            x = col.replace("-", "")
            titularesArray.append(x)

        for col in dependenteRM:
            #x = col.replace("-", "")
            cobradosDepend.append(col)

        for col in titularRM:
            #x = col.replace("-", "")
            cobradosTitular.append(col)

        #Tratamento de Array Dependente 
        print('\nIniciando tratamento de Dependentes')
        erro = 0
        j = 0 
        z = 0

        for object in dependentesArray:
            func.cursor.execute(func.sqlDependente, object)
            row = func.cursor.fetchone() 
            j = j+1 
            if row != None:
                add = [row[2],ano,mes,1,row[3],'8033',0,dataCompetencia,ano,mes,1,cobradosDepend[z]/100,cobradosDepend[z]/100]
                z = z + 1
                layoutPlano.append(add)
                print(f"CPF {object} SUCESSO!")       
                
            else:
                print(f"O CPF DO DEPENDENTE : {object} NÃO ESTÁ NO PLANO, FAVOR CHECAR")
                print('\nFinalizando procedimento para checagem !' )
                sg.popup(f"O CPF DO DEPENDENTE : {object} NÃO ESTÁ NO PLANO, ANOTE O CPF, A APLICAÇÃO VAI FECHAR. AO CORRIGIR É SÓ REPETIR O PROCESSO!")
                erro = erro + 1                
                break
        if erro != 0:
            print('Trate o erro para avançar')
            break
        else:    
            print('Iniciando tratamento de Titulares')
            h = 0
            f = 0
            for object in titularesArray:
                func.cursor.execute(func.sqlTitular, object)
                row = func.cursor.fetchone() 
                h = h+1         
                if row != None:
                    add = [row[2],ano,mes,1,row[3],'8033',0,dataCompetencia,ano,mes,1,cobradosTitular[f]/100,cobradosTitular[f]/100]
                    f = f + 1
                    layoutPlano.append(add)
                    print(f"CPF {object} SUCESSO!") 
                    
                else:
                    print(f"O CPF DO TITULAR : {object} NÃO ESTÁ NO PLANO, FAVOR CHECAR")
                    print('\nFinalizando procedimento para checagem !' )
                    sg.popup(f"O CPF DO TITULAR : {object} NÃO ESTÁ NO PLANO, ANOTE O CPF, A APLICAÇÃO VAI FECHAR. AO CORRIGIR É SÓ REPETIR O PROCESSO!")                     
                    break        
            
    
            for i in layoutPlano:
                cobaia1 = str (i[11])
                valorBeneficiario1 = cobaia1.replace(".", ",")
                chapa1 = str (i[0])
                novoDepend = [chapa1,int (i[1]),int (i[2]),int (i[3]),int (i[4]),int (i[5]),int (i[6]),int (i[7]),int (i[8]),int (i[9]),int (i[10]),valorBeneficiario1,valorBeneficiario1]
                importRM.append(novoDepend)
            
            sg.popup("PRONTO SE VOCÊ CHEGOU AQUI PODE GERAR O LAYOUT!!!\nEnviar 100% Concluído!")

      
#percorrendo cpf por cpf
#mix_matheus = texto.cpf[texto.empresa=='07F7F']
        #for object in mix_matheus:
        #    for l in object:
        #            print(l)

#sg.popup('Você carregou o arquivo:',texto)

#for index, row in texto1.iterrows(): 
#            print(row.name) < aqui conta quantas linhas tem 
#            print(row) < aqui conta as linhas

#print(texto1.str.startswith('Geraçao em'))
#ou palavra = "Geração em" e print(row.str.startswith(palavra))
