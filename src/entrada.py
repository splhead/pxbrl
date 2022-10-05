from validacoes.validador import Validador


class Entrada:
    nome: str
    mensagem: str
    resposta: str
    validador: Validador

    def __init__(self, nome, mensagem, validador):
        self.nome = nome
        self.mensagem = mensagem
        self.validador = validador

    def pergunta(self):
        self.resposta = input(self.mensagem)
        if (not self.validador.valida(self.resposta)):
            print('resposta inválida')
            self.pergunta()
        return self.resposta
