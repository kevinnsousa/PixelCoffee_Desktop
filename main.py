from abc import ABC, abstractmethod


class Produto(ABC):
    def __init__(self, id_prod: int, nome: str, preco_base: float):
        self.id_prod = id_prod
        self.nome = nome
        self.preco_base = preco_base

    @abstractmethod
    def calcularPrecoFinal(self) -> float:
        pass

    def getInfo(self) -> str:
        return f"[{self.id_prod}] {self.nome} - R$ {self.calcularPrecoFinal():.2f}"


class Bebida(Produto):
    def __init__(self, id_prod: int, nome: str, preco_base: float, volume_ml: int, gelada: bool = False):
        super().__init__(id_prod, nome, preco_base)
        self.volume_ml = volume_ml
        self.gelada = gelada

    def calcularPrecoFinal(self) -> float:
        adicional = 0.50 if self.gelada else 0.0
        return self.preco_base + adicional

    def getInfo(self) -> str:
        temperatura = "Gelada" if self.gelada else "Quente"
        return f"[Bebida] {self.nome} ({self.volume_ml}ml, {temperatura}) - R$ {self.calcularPrecoFinal():.2f}"


class Alimento(Produto):
    def __init__(self, id_prod: int, nome: str, preco_base: float, contem_gluten: bool = False):
        super().__init__(id_prod, nome, preco_base)
        self.contem_gluten = contem_gluten

    def calcularPrecoFinal(self) -> float:
        return self.preco_base if self.contem_gluten else self.preco_base * 1.10

    def getInfo(self) -> str:
        tag_gluten = "Com Glúten" if self.contem_gluten else "Sem Glúten"
        return f"[Alimento] {self.nome} ({tag_gluten}) - R$ {self.calcularPrecoFinal():.2f}"


class Cliente:
    def __init__(self, cpf: str, nome: str, desconto_fidelidade: float = 0.05):
        self.cpf = cpf
        self.nome = nome
        self.desconto_fidelidade = desconto_fidelidade

    def getIdentificacao(self) -> str:
        return f"{self.nome} (CPF: {self.cpf})"


class ItemPedido:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade

    def calcularSubtotal(self) -> float:
        return self.produto.calcularPrecoFinal() * self.quantidade

    def getDetalhes(self) -> str:
        return f"- {self.produto.nome} (x{self.quantidade}) = R$ {self.calcularSubtotal():.2f}"


class ImpressoraCupom:
    def imprimir(self, conteudo: str):
        print("\n" + "=" * 45)
        print("          PIXELCOFFEE - RECIBO FISCAL         ")
        print("=" * 45)
        print(conteudo)
        print("=" * 45 + "\n")


class Pedido:
    def __init__(self, numero: int, cliente: Cliente = None):
        self.numero = numero
        self.cliente = cliente
        self.itens: list[ItemPedido] = []

    def adicionarItem(self, produto: Produto, quantidade: int):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        item = ItemPedido(produto, quantidade)
        self.itens.append(item)

    def calcularTotal(self) -> float:
        soma = sum(item.calcularSubtotal() for item in self.itens)
        if self.cliente:
            soma -= soma * self.cliente.desconto_fidelidade
        return soma

    def visualizarResumo(self) -> str:
        nome_cliente = self.cliente.getIdentificacao() if self.cliente else "Consumidor Não Identificado"
        linhas = [f"Pedido Nº {self.numero} | {nome_cliente}"]
        for item in self.itens:
            linhas.append(item.getDetalhes())
        linhas.append(f"TOTAL: R$ {self.calcularTotal():.2f}")
        return "\n".join(linhas)

    def emitirRecibo(self, impressora: ImpressoraCupom):
        corpo = self.visualizarResumo()
        impressora.imprimir(corpo)


def executar_testes():
    cafe = Bebida(1, "Café Expresso", 6.00, volume_ml=100, gelada=False)
    iced_latte = Bebida(2, "Iced Latte", 12.00, volume_ml=350, gelada=True)
    croissant = Alimento(3, "Croissant", 10.00, contem_gluten=True)
    brownie_fit = Alimento(4, "Brownie Especial", 10.00, contem_gluten=False)

    print(cafe.getInfo())
    print(iced_latte.getInfo())
    print(croissant.getInfo())
    print(brownie_fit.getInfo())

    cliente_kevin = Cliente("111.222.333-44", "Kevin Ferreira", desconto_fidelidade=0.10)
    cliente_joao = Cliente("222.333.444-55", "João Silva", desconto_fidelidade=0.05)
    cliente_arthur = Cliente("333.444.555-66", "Arthur Sampaio", desconto_fidelidade=0.05)
    cliente_amanda = Cliente("444.555.666-77", "Amanda Sousa", desconto_fidelidade=0.15)
    cliente_liz = Cliente("555.666.777-88", "Liz Lacerda", desconto_fidelidade=0.00)

    clientes = [cliente_kevin, cliente_joao, cliente_arthur, cliente_amanda, cliente_liz]
    for c in clientes:
        print(c.getIdentificacao())

    pedido1 = Pedido(numero=101, cliente=cliente_kevin)
    pedido1.adicionarItem(cafe, 2)
    pedido1.adicionarItem(iced_latte, 1)
    pedido1.adicionarItem(brownie_fit, 2)

    pedido2 = Pedido(numero=102, cliente=cliente_liz)
    pedido2.adicionarItem(iced_latte, 2)
    pedido2.adicionarItem(croissant, 1)

    pedido3 = Pedido(numero=103, cliente=cliente_joao)
    pedido3.adicionarItem(cafe, 1)
    pedido3.adicionarItem(croissant, 2)

    driver_impressao = ImpressoraCupom()
    pedido1.emitirRecibo(driver_impressao)
    pedido2.emitirRecibo(driver_impressao)
    pedido3.emitirRecibo(driver_impressao)


if __name__ == "__main__":
    executar_testes()