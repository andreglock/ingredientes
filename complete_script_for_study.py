import os
import json
import datetime
from bs4 import BeautifulSoup
import requests
import re

def save_range(start, end):
    print('step 1:', datetime.datetime.now())
    products = ''
    for i in range(start + 1, end + 1):
        try:
            title_ingredients = parse_pao_de_acucar_product('https://www.paodeacucar.com/produto/' + str(i))
            if title_ingredients: 
                products += add_product(title_ingredients[0], title_ingredients[1], title_ingredients[2])
                print('Found product',i)
        except:
            print('Failed for product:', i)

    filename = 'ingredients'+str(start)+'-'+str(end)+'.json'
    destination_path = os.path.join(cur_path, filename)

    with open(destination_path, 'w', encoding='utf-8') as new_file: 
        new_file.write(heading + products[:-2] + footer)
    print('File %s successfully generated on:' % filename, datetime.datetime.now())

cur_path = os.path.dirname(__file__)

heading = '{ "produtos": [\n'

footer = '\n]}'

def add_product(title, categories, ingredients):
    return '  {\n    "categorias": '+ categories +',\n'+'    "titulo": "'+ title +'",\n'+'    "ingredientes": "'+ ingredients +'"\n  },\n'

def parse_pao_de_acucar_product(link_to_product):
    request = requests.get(link_to_product)
    html = request.content
    
    indexed_page = BeautifulSoup(html, features="html.parser")

    title = indexed_page.find('title').get_text()
    product_title = title.split('|')[0][:-1]

    if (product_title == 'Pão de Açúcar'):
        return

    categoriesHTML = indexed_page.find_all("div", {"class":"jSDikk"})
    categories = "["
    for i in range(1, len(categoriesHTML)):
        categories = categories + '"{}", '.format(categoriesHTML[i].getText())
    categories = categories[:-2] + ']'

    table_rows = indexed_page.find_all("tr", {"class": "key-value-liststyles__Item-em9qim-1"}) 
    for table_row in table_rows:
        ingredients = re.search(r'Ingrediente.*?\.', table_row.get_text(), re.IGNORECASE)

        if ingredients != None:
            try:
                list_of_ingredients = table_row.get_text().split('Ingredientes')[1]
            except:
                list_of_ingredients = table_row.get_text().split('Ingrediente')[1]
               
            list_of_ingredients = remove_backslash_n_and_add_space(list_of_ingredients)
            return[product_title, categories, list_of_ingredients]

def parse_pao_de_acucar_product_with_or_without_ingredients(link_to_product):
    request = requests.get(link_to_product)
    html = request.content
    
    indexed_page = BeautifulSoup(html, features="html.parser")

    title = indexed_page.find('title').get_text()
    product_title = title.split('|')[0][:-1]

    if (product_title == 'Pão de Açúcar'):
        return

    categoriesHTML = indexed_page.find_all("div", {"class":"innwdk"})
    categories = "["
    for i in range(1, len(categoriesHTML)):
        categories = categories + '"{}", '.format(categoriesHTML[i].getText())
    categories = categories[:-2] + ']'

    table_rows = indexed_page.find_all("tr", {"class": "key-value-liststyles__Item-em9qim-1"}) 
    for table_row in table_rows:
        ingredients = re.search(r'Ingrediente.*?\.', table_row.get_text(), re.IGNORECASE)

        if ingredients != None:
            try:
                list_of_ingredients = table_row.get_text().split('Ingredientes')[1]
            except:
                list_of_ingredients = table_row.get_text().split('Ingrediente')[1]
               
            list_of_ingredients = remove_backslash_n_and_add_space(list_of_ingredients)
            return[product_title, categories, list_of_ingredients, link_to_product]
    return[product_title, categories, '', link_to_product]

def remove_backslash_n_and_add_space(string):
    return string.replace("\n", " ")

# usage: 
# save_range(1,1_800_000)