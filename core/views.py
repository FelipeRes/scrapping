from django.shortcuts import render
from django.http import HttpResponse
import html5lib
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import requests
import re
import time
from datetime import datetime, date
from .models import *
import xml.dom.minidom
from lxml import html
import os
import csv
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_links(url_base,url, pais_links):
    page = download(url)
    soup = BeautifulSoup(page, 'html5lib')
    lines = soup.find_all("tr")
    #===============
    link = []
    links = []
    for div_pais in lines:
        links = links + div_pais.find_all("a", href=True)
    for l in links:
        link.append(l['href'])
        print(l['href'])
    #===============
    #link = [pais.find("a", href=True)['href'] for pais in lines]
    pais_links = pais_links + link
    next_button = soup.find("div", id="pagination")
    next_and_previous = next_button.find_all("a", href=True)
    for n in next_and_previous:
        if "Next" in n.text:
            next_button_url = n["href"]
            return get_links(url_base,url_base+next_button_url,pais_links)
    return pais_links

def data(url):
    page = download(url)
    soup = BeautifulSoup(page, 'html5lib')

    area_div = soup.find("tr", id="places_area__row")
    area = area_div.find("td", class_="w2p_fw").text
    area = re.sub(r'[^\d]','',area)
    area = float(area)


    population_div = soup.find("tr", id="places_population__row")
    population = population_div.find("td", class_="w2p_fw").text
    population = population.replace(',','')
    population = float(population)

    densidade = 0
    if(area > 0):
        densidade = population/area

    name_div = soup.find("tr", id="places_country__row")
    name = name_div.find("td", class_="w2p_fw").text
    return {"name":name,"densidade":densidade}

def download(url, num_retries=10):
    print('Dowloading:', url)
    page = None

    try:
        response = requests.get(url)
        print(response.status_code)
        page = response.text
        if response.status_code >= 400:
            print('Download error:', response.text)
            time.sleep(30)
            print("Tenta de novo: " +str(num_retries))
            if num_retries != 0:
                return download(url, num_retries -1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e)
    return page


# Create your views here.

def index(request):
	return render(request, "index.html",{})

def atividade1(request):
	url = 'https://www.rottentomatoes.com/browse/tv-list-1'
	page = download(url)
	soup = BeautifulSoup(page, 'html5lib')
	filmes = soup.find_all("tr", class_="tv_show_tr")
	lista = []
	for filme in filmes:
	    nome = filme.find("td", class_="middle_col")
	    print('Serie :', nome.find("a").text)
	    n = nome.find("a").text
	    score = filme.find("td", class_="left_col")
	    s = score.find("span", class_="tMeterScore")
	    avaliacao = ""
	    if s == None:
	    	avaliacao = "Sem avaliação!"
	    else:
	    	avaliacao = s.text
	    valor = {"nome":n, "avaliacao":avaliacao}
	    lista.append(valor)
	data = {"lista":lista}
	print(data)
	return render(request, "atividade1.html", data)

def atividade2_process():
	url = 'http://www.imdb.com/chart/boxoffice'
	page = download(url)
	#print(page)

	soup = BeautifulSoup(page, 'html5lib')
	table = soup.find("tbody")
	filmes = table.find_all("tr")
	lista = []
	csv = []
	for filme in filmes:
	    nome = filme.find("td", class_="titleColumn").a.text
	    rating = filme.find("td", class_="ratingColumn").text
	    rating = re.sub(r'[^\d$.M]','',rating)
	    rating_number = re.sub(r'[^\d.]','',rating)
	    gross = filme.find_all("td", class_="ratingColumn")
	    gross_span = [span.find("span", class_="secondaryInfo" ) for span in gross]
	    gross_value = gross_span[1].text
	    weeks = filme.find("td", class_="weeksColumn").text
	    lista_csv = [nome,rating,gross_value,weeks]
	    csv.append(lista_csv)
	    valor = {"nome":nome,"rating":rating, "gross_value":gross_value, "weeks":weeks}
	    lista.append(valor)

	return {"lista":lista,"csv":csv}

def atividade2(request):
	lista = atividade2_process()["lista"]
	return render(request, "atividade2.html",{"lista":lista})

def atividade2_csv(request):
	lista = atividade2_process()['csv']
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="dados_da_copa.csv"'
	writer = csv.writer(response)

	for filme in lista:
		writer.writerow(filme)
	return response

def atividade3(request):
	url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/264/teresina-pi'
	page = download(url)
	soup = BeautifulSoup(page, 'html5lib')
	temperatura = soup.find("p",id="momento-temperatura").text
	sensacao = soup.find("li",id="momento-sensacao").text
	umidade = soup.find("li",id="momento-humidade").text
	pressao = soup.find("li",id="momento-pressao").text
	vento = soup.find("a",id="momento-vento").text
	vento = re.sub(r'[^\dkm/h]','',vento)
	atualizacao = soup.find("p",id="momento-atualizacao").text
	atualizacao = re.search(r'.\d\d:\d\d$',atualizacao).group(0)
	ultimas_atualizacoes = [atualizacao for atualizacao in ClimaTeresina.objects.all().reverse()]
	print(ultimas_atualizacoes)
	horario = ultimas_atualizacoes[0].horario
	horario = horario.replace(tzinfo=None)
	agora = datetime.now()
	agora = agora.replace(tzinfo=None)
	if ultimas_atualizacoes == [] or (ultimas_atualizacoes[0].atualizacao != atualizacao and horario.hour-agora.hour >= 1):
		clima = ClimaTeresina(atualizacao=atualizacao, 
			temperatura=temperatura, 
			sensacao=sensacao,
			umidade=umidade,
			pressao=pressao,
			vento=vento)
		clima.save()
	return render(request, 'atividade3.html', {"temperatura":temperatura, "sensacao":sensacao, "umidade":umidade,"pressao":pressao,"vento":vento, "atualizacao":atualizacao, "atualizacoes":ultimas_atualizacoes})

def atividade4(request):
	url_base = 'http://example.webscraping.com'
	links = get_links(url_base,url_base,[])
	all_data = []
	for l in links:
	    all_data.append(data(url_base+l))
	print(all_data)
	return render(request, "atividade4.html", {"all_data":all_data})

def atividade5_process():
	x = xml.dom.minidom.parse(os.path.join(PROJECT_ROOT, 'feed.xml'))
	valorTotal = x.getElementsByTagName("valorTotalPrevisto")
	values = []
	cidades = []
	dicionario = {}
	for v in valorTotal:
	    parent = v.parentNode
	    sede = parent.getElementsByTagName("cidadeSede")
	    descricao = sede[0].getElementsByTagName("descricao")
	    cidade = descricao[0].firstChild.nodeValue
	    cidades.append(cidade)
	    valor = float(v.firstChild.nodeValue)
	    values.append(valor)
	    if dicionario.get(cidade) == None:
	        dicionario[cidade] = []
	    dicionario[cidade].append(valor)
	for key in dicionario:
		dicionario[key].append(sum(dicionario[key]))
	return dicionario

def atividade5(request):
	dicionario = atividade5_process()
	return render(request,'atividade5.html',{"dicionario" : dicionario})

def atividade5_csv(replace):
	dicionario = atividade5_process()
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="dados_da_copa.csv"'
	writer = csv.writer(response)

	for sede in dicionario:
		lista = []
		lista.append(sede)
		lista = lista + dicionario[sede]
		print(lista)
		writer.writerow(lista)
	return response