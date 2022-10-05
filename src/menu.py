from xml.etree.ElementTree import Element


def mostrar_menu(opcoes: dict[str, tuple]):
    print(f'Escolha uma opção:')
    for chave in sorted(opcoes):
        print(f' {chave}) {opcoes[chave][0]}')


def ler_opcao(opcoes: dict[str, tuple]):
    while (opcao_escolhida := input('Opção: ')) not in opcoes:
        print('Opção incorreta, tente novamente.')
    return opcao_escolhida


def executa_opcao(opcao_escolhida: str, opcoes: dict[str, tuple]):
    if (len(opcoes[opcao_escolhida]) == 2):
        opcoes[opcao_escolhida][1]()
    else:
        opcoes[opcao_escolhida][1](*opcoes[opcao_escolhida][2])


def gerar_menu(opcoes: dict[str, tuple], opcao_de_saida: str):
    mostrar_menu(opcoes)
    opcao_escolhida = ler_opcao(opcoes)
    executa_opcao(opcao_escolhida, opcoes)
    if (opcao_escolhida != opcao_de_saida):
        gerar_menu(opcoes, opcao_de_saida)


def sair():
    print('\n')

# Exemplo de utilização

# def menu():
#     opcoes = {
#         '1': ('Listar atributos', listar),
#         '2': ('Sair', sair)
#     }

#     gerar_menu(opcoes, '2')


# if __name__ == '__main__':
#     menu()
