"""
PROJETO PIXELCOFFEE - MODELAGEM DESK APP I
Relações POO implementadas e documentadas:
1. Herança: Bebida e Alimento herdam de Produto.
2. Polimorfismo: Bebida e Alimento sobrescrevem o método abstrato 'calcularPrecoFinal'.
3. Composição: Pedido compõe ItemPedido (ItemPedido é instanciado e gerenciado por Pedido).
4. Agregação: Pedido agrega Cliente (Cliente existe com ciclo de vida independente).
5. Associação Simples: ItemPedido aponta para um Produto.
6. Dependência: Pedido recebe ImpressoraCupom via método temporário (não guarda como atributo).
"""

from abc import ABC, abstractmethod


# ==========================================================
# 1. HERANÇA E POLIMORFISMO (Classes Produto, Bebida e Alimento)
# ==========================================================
class Produto(ABC):
    def __init__(self, id_prod: int, nome: str, preco_base: float):
        self.id_prod = id_prod
        self.nome = nome
        self.preco_base = preco_base

    @abstractmethod
    def calcularPrecoFinal(self) -> float:
        """Método polimórfico implementado por subclasses."""
        pass

    def getInfo(self) -> str:
        return f"[{self.id_prod}] {self.nome} - R$ {self.calcularPrecoFinal():.2f}"


class Bebida(Produto):
    def __init__(self, id_prod: int, nome: str, preco_base: float, volume_ml: int, gelada: bool = False):
        super().__init__(id_prod, nome, preco_base)
        self.volume_ml = volume_ml
        self.gelada = gelada

    # [POLIMORFISMO] Bebida gelada tem taxa adicional de conservação de R$ 0,50
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

    # [POLIMORFISMO] Alimento sem glúten recebe acréscimo de insumo diferenciado de 10%
    def calcularPrecoFinal(self) -> float:
        return self.preco_base if self.contem_gluten else self.preco_base * 1.10

    def getInfo(self) -> str:
        tag_gluten = "Com Glúten" if self.contem_gluten else "Sem Glúten"
        return f"[Alimento] {self.nome} ({tag_gluten}) - R$ {self.calcularPrecoFinal():.2f}"


# ==========================================================
# 2. CLIENTE (Objeto para Agregação)
# ==========================================================
class Cliente:
    def __init__(self, cpf: str, nome: str, desconto_fidelidade: float = 0.05):
        self.cpf = cpf
        self.nome = nome
        self.desconto_fidelidade = desconto_fidelidade  # 5% padrão

    def getIdentificacao(self) -> str:
        return f"{self.nome} (CPF: {self.cpf})"


# ==========================================================
# 3. COMPOSIÇÃO E ASSOCIAÇÃO (ItemPedido e Pedido)
# ==========================================================
class ItemPedido:
    def __init__(self, produto: Produto, quantidade: int):
        # [ASSOCIAÇÃO]: ItemPedido referencia um Produto
        self.produto = produto
        self.quantidade = quantidade

    def calcularSubtotal(self) -> float:
        return self.produto.calcularPrecoFinal() * self.quantidade

    def getDetalhes(self) -> str:
        return f"- {self.produto.nome} (x{self.quantidade}) = R$ {self.calcularSubtotal():.2f}"


# ==========================================================
# 4. DEPENDÊNCIA (ImpressoraCupom)
# ==========================================================
class ImpressoraCupom:
    """Classe utilitária para registrar a dependência transitória."""
    def imprimir(self, conteudo: str):
        print("\n" + "=" * 45)
        print("          PIXELCOFFEE - RECIBO FISCAL         ")
        print("=" * 45)
        print(conteudo)
        print("=" * 45 + "\n")


class Pedido:
    def __init__(self, numero: int, cliente: Cliente = None):
        self.numero = numero
        # [AGREGAÇÃO]: Pedido agrega Cliente. O Cliente existe fora do Pedido.
        self.cliente = cliente
        # [COMPOSIÇÃO]: Itens pertencem e só existem dentro deste Pedido
        self.itens: list[ItemPedido] = []

    # Criação do ItemPedido encapsulada dentro da classe Pedido (Composição)
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

    # [DEPENDÊNCIA]: Recebe ImpressoraCupom apenas como parâmetro transitório
    def emitirRecibo(self, impressora: ImpressoraCupom):
        corpo = self.visualizarResumo()
        impressora.imprimir(corpo)


# ==========================================================
# 5. TESTES DE TODAS AS FUNCIONALIDADES
# ==========================================================
def executar_testes():
    print(">>> INICIANDO BATERIA DE TESTES DO PIXELCOFFEE <<<\n")

    # 1. Testando Herança e Polimorfismo
    cafe = Bebida(1, "Café Expresso", 6.00, volume_ml=100, gelada=False)
    iced_latte = Bebida(2, "Iced Latte", 12.00, volume_ml=350, gelada=True)
    croissant = Alimento(3, "Croissant", 10.00, contem_gluten=True)
    brownie_fit = Alimento(4, "Brownie Especial", 10.00, contem_gluten=False)

    print("--- [TESTE 1] Produtos e Preços Polimórficos ---")
    print(cafe.getInfo())          # R$ 6.00
    print(iced_latte.getInfo())    # R$ 12.50 (+0.50 por ser gelada)
    print(croissant.getInfo())     # R$ 10.00
    print(brownie_fit.getInfo())   # R$ 11.00 (+10% por ser sem glúten)

    # 2. Testando Agregação com Cliente
    cliente_vip = Cliente("111.222.333-44", "Kevin Ferreira", desconto_fidelidade=0.10)
    print(f"\n--- [TESTE 2] Cliente cadastrado: {cliente_vip.getIdentificacao()} ---")

    # 3. Testando Composição e Cálculo do Pedido
    pedido = Pedido(numero=101, cliente=cliente_vip)
    pedido.adicionarItem(cafe, 2)         # 2 * 6.00 = 12.00
    pedido.adicionarItem(iced_latte, 1)   # 1 * 12.50 = 12.50
    pedido.adicionarItem(brownie_fit, 2)  # 2 * 11.00 = 22.00
    # Subtotal bruto: 46.50 | Com 10% de fidelidade: 41.85

    print("\n--- [TESTE 3] Resumo do Pedido em Console ---")
    print(pedido.visualizarResumo())

    # 4. Testando Dependência
    print("\n--- [TESTE 4] Impressão via Dependência Externa ---")
    driver_impressao = ImpressoraCupom()
    pedido.emitirRecibo(driver_impressao)

    print(">>> TODOS OS TESTES FORAM EXECUTADOS COM SUCESSO! <<<")


if __name__ == "__main__":
    executar_testes()