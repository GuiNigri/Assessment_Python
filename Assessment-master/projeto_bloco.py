import pygame,sys,os, time,psutil, netifaces
from datetime import datetime , timedelta
from pytz import timezone
from mostrar_conteudo import *
from conta_clock import *
from mostrar_grafico import *
pygame.mixer.init()

pygame.font.init()

lista = os.listdir("./")

dic = {}
dic2 = {}
formato = "%d/%m/%Y %H:%M:%S"

for i in lista:
    if os.path.isfile(i):
        dic[i] = []
        timestamp_criacao = os.stat(i).st_atime
        timestamp_modificacao = os.stat(i).st_mtime
        data_criacao = time.strftime(formato, time.localtime(timestamp_criacao))
        data_mod = time.strftime(formato, time.localtime(timestamp_modificacao))
        dic[i].append(os.stat(i).st_size)
        dic[i].append(data_criacao)
        dic[i].append(data_mod)
print(dic)

terminou = False
def conteudo_aba1():
    soma_percent = 0
    soma_indices = 0

    try:
        soma_v, soma_r = pega_processos("somas")
        #print(soma_vms)
        lista_processos_ordenados = []
        for elemento in sorted(psutil.process_iter(), key=lambda x : x.memory_info().rss, reverse = True):
            lista_processos_ordenados.append(elemento)
        for p in lista_processos_ordenados:
            if p.status() == 'running':
                pid = p.pid
                nome = p.name()
                rss = p.memory_info().rss/1024/1024
                vms = p.memory_info().vms/1024/1024
                status = p.status()
                montar_tabela(f'{pid}',10,220+soma_indices*20)
                montar_tabela(f'{nome}',70,220+soma_indices*20)
                montar_tabela(f'{round(vms,2)} MB',250,220+soma_indices*20)
                montar_tabela(f'{round(rss,2)} MB',350,220+soma_indices*20)
                montar_tabela(f'{round(vms/round(soma_v,2),4)} %',450,220+soma_indices*20)
                montar_tabela(f'{round(rss/round(soma_r,2),4)} %',550,220+soma_indices*20)
                soma_indices = soma_indices + 1
    except psutil.NoSuchProcess:
        pass
        
    montar_tabela(f'Total de uso do sistema: {soma_percent/100}  %',10,150)
    montar_tabela(f'Total de uso do vms: {round(soma_v,2)}  MB',10,130)
    montar_tabela(f'Total de uso do rss: {round(soma_r,2)}  MB',10,110)
    
    montar_tabela("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",0,175)
    montar_tabela("pid",10,190)
    montar_tabela("rms",70,190)
    montar_tabela("vms",250,190)
    montar_tabela("rss",350,190)
    montar_tabela("% do vms",450,190)
    montar_tabela("% do rss",550,190)
    """for item in lista_de_dicionario:
        montar_tabela(f'{item["pid"]}',10,155+soma_indices*20)
        montar_tabela(f'{item["nome"]}',50,155+soma_indices*20)
        montar_tabela(f'{round(item["vms"]/1024/1024,2)} MB',200,155+soma_indices*20)
        montar_tabela(f'{round(item["rss"]/1024/1024,2)} MB',300,155+soma_indices*20)
        montar_tabela(f'{round(item["vms"]/round(soma_vms/1024/1024,2)/100,2)} %',400,155+soma_indices*20)
        montar_tabela(f'{round(item["rss"]/round(soma_rss/1024/1024,2)/100,2)} %',500,155+soma_indices*20)
        soma_indices = soma_indices + 1
    montar_tabela(f'Total de uso do sistema: {round(soma_percent/100,2)}  %',200,(200)+50)
    montar_tabela(f'Total de uso do vms: {round(soma_vms/1024/1024,2)}  MB',200,(200)+30)
    montar_tabela(f'Total de uso do rss: {round(soma_rss/1024/1024,2)}  MB',200,(200)+10)"""
    
def conteudo_aba0():
    posx = 10
    soma_indices = 0  
    montar_tabela("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------",0,130)
    montar_tabela("Tamanho",10,190)
    montar_tabela("Criação",posx+90,190)
    montar_tabela("Modificação",posx+290,190)
    montar_tabela("Nome do arquivo",posx+470,190)
    
    lista = os.listdir()
    
    soma_tamanho = 0
    for i in dic:
        soma_tamanho = soma_tamanho + dic[i][0]
    for i in lista: # Varia na lista dos arquivos e diretórios
        if os.path.isfile(i): # checa se é um arquivo
            kb = (dic[i][0]/1024)
            tamanho = '{:10}'.format(str('{:.2f}'.format(kb)+' KB'))
            montar_tabela(f'{tamanho}', posx, 220+soma_indices*20) # Tamanho
            montar_tabela(f'{dic[i][1]}', posx+90, 220+soma_indices*20) # Tempo de criação
            montar_tabela(f'{dic[i][2]}', posx+290, 220+soma_indices*20) # Tempo de modificação
            montar_tabela(f'{i}',posx+470,220+soma_indices*20)
            soma_indices = soma_indices + 1
    montar_tabela(f'Tamanho total dos arquivos: {round((soma_tamanho/1024),2)} KB',posx,(220+soma_indices*20))
    montar_tabela(f'Média de tamanho  dos arquivos: {round((soma_tamanho/len(tamanho)/1024),2)} KB',posx,(240+soma_indices*20))  
    
def conteudo_aba2():
    soma_indices = 0
    interfaces = psutil.net_if_addrs()
    #print(interfaces)
    #print(interfaces)
   #nomes = []
    """for nome_da_rede in interfaces:
        nomes.append(str(nome_da_rede))
    print(nomes)"""
    identifica_ip_router = netifaces.gateways()
    #print(identifica_ip_router)
    for i, j in identifica_ip_router.items():
        try:
            gat = j[2][0]
        except:
            pass
    montar_tabela("Nome da Rede", 5,200)
    montar_tabela("Endereço Ip da Rede", 200,200)
    montar_tabela("Mascara de Rede", 350,200)
    montar_tabela("Gateway: ", 5,160)
    montar_tabela(gat, 85,160)
    for nome_rede, info_rede in interfaces.items():
        montar_tabela(f'{nome_rede}',5,220+soma_indices*20)
        #Endereço_IP
        montar_tabela(f'{info_rede[1][1]}',200,220+soma_indices*20)
        #mascara
        montar_tabela(f'{info_rede[1][2]}',350,220+soma_indices*20)
        #for j in interfaces[i]:
            #montar_tabela("\t"+str(j),5,300+soma_indices*20)
        soma_indices = soma_indices + 1
            
def conteudo_aba3():
    desenha_grafico_vms()
    
clock = pygame.time.Clock()

tela.fill(branco)
aba0,aba1,aba2,aba3 =  cria_abas()
aba_setada = "aba_setada_3"
conteudo_aba3()

while True:   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminou = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
            pos = pygame.mouse.get_pos()
            if aba0.area.collidepoint(pos):
                tela.fill(branco)
                aba0, aba1, aba2, aba3 = cria_abas()
                aba_setada = "aba_setada_0"
                    
            if aba1.area.collidepoint(pos):
                tela.fill(branco)
                aba0, aba1, aba2, aba3 = cria_abas()
                aba_setada = "aba_setada_1"

            if aba2.area.collidepoint(pos):
                tela.fill(branco)
                aba0, aba1, aba2, aba3 = cria_abas()
                aba_setada = "aba_setada_2"
                
            if aba3.area.collidepoint(pos):
                tela.fill(branco)
                aba0, aba1, aba2, aba3 = cria_abas()
                aba_setada = "aba_setada_3"
       
    conta_clocks +=1
    
    if conta_clocks == 50:
        if conta_segundos>=0:
            conta_segundos+=1
        conta_clocks = 0
        tela.fill(branco)
        aba0, aba1, aba2, aba3 = cria_abas()  
        if aba_setada == "aba_setada_0":
            mostra_segundos()
            conteudo_aba0()  
        if aba_setada == "aba_setada_1":
            mostra_segundos()
            conteudo_aba1()
        if aba_setada == "aba_setada_2":
            mostra_segundos()
            conteudo_aba2()
        if aba_setada == "aba_setada_3":
            mostra_segundos()
            conteudo_aba3()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pygame.display.update()
    clock.tick(50)
    
pygame.display.quit()