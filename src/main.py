#!/usr/bin/python
from os.path import exists as file_exists, dirname, join
from xml.etree.ElementTree import Element, SubElement, tostring, indent, parse

tags: list = []
tags_nao_repetidas: set

def le_modelo(nome_do_arquivo):
  diretorio_atual = dirname(__file__)
  caminho_do_modelo = join(diretorio_atual, nome_do_arquivo)
  
  if file_exists(caminho_do_modelo):
    arvore = parse(caminho_do_modelo)
    for filho in arvore.getroot():
      tags.append(filho.tag.split('}')[1])
    tags_nao_repetidas = set(tags)
    print(sorted(tags_nao_repetidas), len(tags_nao_repetidas))
  else:
    print('O modelo não foi encontrado')

modelo = 'aapl-20090926.xml'
# modelo = 'modelo.xbrl'
le_modelo(modelo)
'''

# faz as identações corretas e adiciona a declaração xml
def prettify(element: Element):
  indent(element)
  return tostring(element, 'utf-8',xml_declaration=True)

# cria o arquivo
def cria_arquivo(root):
  with open("./src/instance.xml", "wb") as file:
    file.write(prettify(root))

def adicionar_atributos(tag, atributos: dict[str, str]):
  for chave, valor in atributos.items():
    tag.set(chave, valor)

# cria o primeiro elemento
xbrl = Element('xbrli:xbrl')

adicionar_atributos(
  xbrl, 
  {
    'xmlns:xbrli':'http://www.xbrl.org/2003/instance',
    'xmlns:gl-bus':'http://www.xbrl.org/int/gl/bus/2015-03-25',
    'xmlns:gl-cor':'http://www.xbrl.org/int/gl/cor/2015-03-25',
    'xmlns:iso4217':'http://www.xbrl.org/2003/iso4217',
    'xmlns:link':'http://www.xbrl.org/2003/linkbase',
    'xmlns:xlink':'http://www.w3.org/1999/xlink',
    'xmlns:xsi':'http://www.w3.org/2001/XMLSchema-instance'
  }
)

link_schema_ref = SubElement(xbrl,'link:schemaRef')

adicionar_atributos(
  link_schema_ref,
  {
    'xlink:href':'SICONFI/cor/ext/gl/plt/case-c-b-m-u-t-s/gl-plt-all-2015-03-25.xsd',
    'xlink:type':'simple'
  }
)

cria_arquivo(xbrl)
'''
