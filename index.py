import requests
from bs4 import BeautifulSoup
import pandas as pd

lista_completa = []

for i in range(0, 60):
    print("Requisição N°: ",i)
    lista_icones = []
    lista_descricao = []
    cidade_retorno = ""
    estado_retorno = ""
    telefone_retorno = ""
    email_retorno = ""
    site_retorno = ""
    cont = 0
    concatena = ""
    concatena_produtos = ""

    url = f"https://www.sindipecas.org.br/associados_e_produtos/detalhes.php?cod={i}"
    urlFormat = url.replace(" ", "")

    response = requests.get(urlFormat)
    content = response.content

    site = BeautifulSoup(content, 'html.parser')
    
    titulo = site.find('h3')
    razaoSocial = site.find('h4')
    dados = site.findAll('span', attrs={'class': 'associadosimp'})
    imagens = site.findAll('img', attrs={'class': 'seglist'})

    for icones in imagens:
        lista_icones.append(icones['title'])


    for info in dados:
        informacoes = info.text
        lista_descricao.append(informacoes.replace("\n", ""))


    qntd_descricoes = len(lista_descricao)

    while cont < qntd_descricoes:
        descricoes = lista_descricao[cont] 
        if concatena == "":
            concatena = descricoes
        else:
            concatena = concatena+ "^" +descricoes
        cont = cont + 1

    
    if titulo != None:
        split = concatena.split("^")
        print("")
        print("")
        print("split: ",split)
        print("")
        print("")
        contador = 0
        while contador < len(split):
            a = 0
            if contador==0: 
                cidade_retorno = split[contador]
            if contador==1: 
                estado_retorno = split[contador]
            if contador==2:
                verifica_telefone = "Telefone"
                if verifica_telefone not in split[contador]:
                    telefone_retorno = "-"
                    a = 1
                else:
                    telefone_retorno = split[contador]
            if contador==3:
                verifica_email = "@"
                if verifica_email not in split[contador-a]:
                    email_retorno = "-"
                    a = 1
                else:
                    email_retorno = split[contador-a]
            if contador==4:
                verifica_site = "www"
                if verifica_site not in split[contador-a]:
                    site_retorno = "-"
                    a = 1
                else:
                    site_retorno = split[contador-a]
            contador = contador + 1


        for conteudo in range(5, len(split)):
            concatena_produtos = concatena_produtos + split[conteudo]
         

        lista_completa.append([titulo, razaoSocial, cidade_retorno, estado_retorno, telefone_retorno, email_retorno, site_retorno, lista_icones, concatena_produtos])

excel = pd.DataFrame(lista_completa,columns=['Titulo', 'Razão Social', 'Cidade', 'Estado', 'Telefone', 'E-mail', 'Site', 'Descrições', 'Produtos'])
excel.to_excel('Fundamentus.xlsx', index=False)
print("Encerrado !")




