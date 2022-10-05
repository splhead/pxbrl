#!/usr/bin/python
from os.path import exists as file_exists, dirname, join

from xml.etree.ElementTree import Element, SubElement, tostring, indent, parse, iterparse, register_namespace, dump

from menu import gerar_menu


namespaces: dict
raiz: Element


def prettify(element: Element):
    """faz as identações corretas e adiciona a declaração xml"""
    indent(element)
    return tostring(element, 'utf-8', xml_declaration=True,
                    default_namespace=None)


def salva_arquivo(root):
    with open("./src/instance.xml", "wb") as file:
        file.write(prettify(root))


# def obtem_uri_namespace(tag: str):
#     try:
#         return tag.split('}')[0][1:]
#     except IndexError:
#         return tag


def adiciona_atributos(elemento: Element, atributos: dict[str, str]):
    for chave, valor in atributos.items():
        elemento.set(remove_namespace(chave), valor)


def remove_atributos(elemento: Element,
                     atributos_para_remover: dict[str, str] = {},
                     remover_todos: bool = False):
    atributos_antigos = elemento.attrib
    elemento.clear()
    if (remover_todos):
        return elemento

    for atributo in atributos_para_remover:
        del atributos_antigos[atributo]
    adiciona_atributos(elemento, atributos_antigos)
    return elemento


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


def remove_namespace(tag: str):
    # {http://www.xbrl.org/2003/instance}xbrl esse é o padrão namespace + nome
    # remove o namespace da tag para não duplicar tag.split('}')[1]
    try:
        return tag.split('}')[1]
    # caso não encontre } a tag já está sem o namespace
    except IndexError:
        return tag


def cria_xbrl(tag: str):
    xbrl_elemento = Element(remove_namespace(tag))

    adiciona_atributos(xbrl_elemento, namespaces)

    def concluir():
        return

    # # TODO: perguntar se quer editar ou adicionar namespaces
    opcoes = {
        '1': ('Listar atributos', lista_atributos, [xbrl_elemento]),
        '2': ('Adicionar atributo', lista_atributos),
        '3': ('Remover atributo', lista_atributos),
        '4': ('Concluir', concluir)
    }

    gerar_menu(opcoes, '4')
    return xbrl_elemento


def main():
    # tem um arquivo como modelo ou vai partir do padrão
    arquivo_de_entrada = 'aapl-20090926.xml_'
    if existe_modelo(arquivo_de_entrada):
        carrega_modelo(arquivo_de_entrada)
    else:
        modelo_padrao = 'modelo.xbrl'
        carrega_modelo(modelo_padrao)

    # cria o primeiro elemento
    xbrl = cria_xbrl(raiz.tag)

    schema_ref_do_modelo = raiz.find(
        '{http://www.xbrl.org/2003/linkbase}schemaRef')

    schema_ref = SubElement(
        xbrl, remove_namespace(schema_ref_do_modelo.tag))
    adiciona_atributos(schema_ref, schema_ref_do_modelo.attrib)
    # # TODO: perguntar se quer editar ou adicionar atributos

    # # TODO: criar contextos e permitir sua edição

    salva_arquivo(xbrl)


def lista_atributos(elemento: Element):
    print(f'Abaixo são os atributos para a tag <{elemento.tag}>\n')
    for indice, atributo in enumerate(elemento.attrib, start=1):
        print(f'{indice} {atributo} => {elemento.attrib[atributo]}')
    print('\n')


if __name__ == "__main__":
    main()
