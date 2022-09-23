#!/usr/bin/python
from os.path import exists as file_exists, dirname, join
from xml.etree.ElementTree import Element, tostring, indent, parse, iterparse, register_namespace

tags: list = []
tags_nao_repetidas: set

# faz as identações corretas e adiciona a declaração xml


def prettify(element: Element):
    """ documenta cao"""
    indent(element)
    return tostring(element, 'utf-8', xml_declaration=True)

# cria o arquivo


def cria_arquivo(root):
    with open("./src/instance.xml", "wb") as file:
        file.write(prettify(root))


def adicionar_atributos(tag, atributos: dict[str, str]):
    for chave, valor in atributos.items():
        tag.set(chave, valor)


def register_all_namespaces(filename):
    namespaces = dict(
        [node for _, node in iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        register_namespace(ns, namespaces[ns])


def le_modelo(nome_do_arquivo):
    diretorio_atual = dirname(__file__)
    caminho_do_modelo = join(diretorio_atual, nome_do_arquivo)

    if file_exists(caminho_do_modelo):
        register_all_namespaces(caminho_do_modelo)
        arvore = parse(caminho_do_modelo)

        novo_xbrl = arvore.getroot()
        print(novo_xbrl[0])
        # cria_arquivo(novo_xbrl)
        # le tags
        # for filho in arvore.getroot():
        #     tags.append(filho.tag.split('}')[1])
        #     tags_nao_repetidas = set(tags)
        #     print(sorted(tags_nao_repetidas), len(tags_nao_repetidas))

    else:
        print('O modelo não foi encontrado')


# modelo = 'aapl-20090926.xml'
modelo = 'modelo.xbrl'
le_modelo(modelo)


'''
1 - verificar se tem modelo ou é novo

2 - criar com base no modelo ou um novo 

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
