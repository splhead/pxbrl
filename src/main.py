#!/usr/bin/python
from os.path import exists as file_exists, dirname, join
from xml.etree.ElementTree import Element, SubElement, tostring, indent, parse, iterparse, register_namespace

namespaces: dict
raiz: Element


def prettify(element: Element):
    """faz as identações corretas e adiciona a declaração xml"""
    indent(element)
    return tostring(element, 'utf-8', xml_declaration=True)


def cria_arquivo(root):
    with open("./src/instance.xml", "wb") as file:
        file.write(prettify(root))


def adicionar_atributos(tag, atributos: dict[str, str]):
    for chave, valor in atributos.items():
        tag.set(chave, valor)


def registra_todos_namespaces(filename):
    '''corrige os prefixos dos namespaces'''
    def prefix_namespaces(temp_namespaces):
        namespaces_atualizados = {}
        for item in temp_namespaces.items():
            if item[0] != '':
                namespaces_atualizados.update({'xmlns:' + item[0]: item[1]})
        return namespaces_atualizados

    temp_namespaces = dict(
        [node for _, node in iterparse(filename, events=['start-ns'])])

    for ns in temp_namespaces:
        register_namespace(ns, temp_namespaces[ns])

    global namespaces
    namespaces = prefix_namespaces(temp_namespaces)


def local_do_arquivo(nome_do_arquivo):
    diretorio_atual = dirname(__file__)
    return join(diretorio_atual, nome_do_arquivo)


def existe_modelo(nome_do_arquivo):
    caminho_do_modelo = local_do_arquivo(nome_do_arquivo)
    arquivo_existe = file_exists(caminho_do_modelo)

    if arquivo_existe:
        return arquivo_existe
    else:
        print(f'O arquivo {nome_do_arquivo} não foi encontrado')


def carrega_modelo(nome_do_arquivo):
    caminho_do_modelo = local_do_arquivo(nome_do_arquivo)
    registra_todos_namespaces(caminho_do_modelo)
    arvore = parse(caminho_do_modelo)
    global raiz
    raiz = arvore.getroot()


def main():
    # tem um arquivo como modelo ou vai partir do padrão
    arquivo_de_entrada = 'aapl-20090926.xml'
    if existe_modelo(arquivo_de_entrada):
        carrega_modelo(arquivo_de_entrada)
    else:
        modelo_padrao = 'modelo.xbrl'
        carrega_modelo(modelo_padrao)

    # cria o primeiro elemento
    xbrl = Element(raiz.tag)
    adicionar_atributos(xbrl, namespaces)
    # # TODO: perguntar se quer editar ou adicionar namespaces

    schema_ref_do_modelo = raiz.find(
         '{http://www.xbrl.org/2003/linkbase}schemaRef')

    schema_ref = SubElement(xbrl, schema_ref_do_modelo.tag)
    adicionar_atributos(schema_ref, schema_ref_do_modelo.attrib)
    # # TODO: perguntar se quer editar ou adicionar atributos

    # # TODO: criar contextos e permitir sua edição

    cria_arquivo(xbrl)


main()
