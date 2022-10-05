from typing import Protocol


class Validador(Protocol):
    def valida(self) -> bool:
        ...


Validador.valida = staticmethod(Validador.valida)
