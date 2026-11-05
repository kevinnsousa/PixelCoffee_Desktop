"""
PROJETO PIXELCOFFEE - DESK APP II
Menu interativo totalmente funcional em console.
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------
# MODELOS (Herança, Polimorfismo, Composição, Agregação)
# ---------------------------------------------------------
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
        temp = "Gelada" if self.gelada else "Quente"
        return f"[Bebida] {self.nome} ({self.volume_ml}ml, {temp}) - R$ {self.calcularPrecoFinal():.2f}"


class Alimento(Produto):
    def __init__(self, id_prod: int, nome: str, preco_base: float, contem_gluten: bool = False):
        super().__init__(id_prod, nome, preco_base)
        self.contem_gluten = contem_gluten

    def calcularPrecoFinal(self) -> float:
        return self.preco_base if self.contem_gluten else self.preco_base * 1.10

    def getInfo(self) -> str:
        gluten = "Com Glúten" if self.contem_gluten else "Sem Glúten"
        return f"[Alimento] {self.nome} ({gluten}) - R$ {self.calcularPrecoFinal():.2f}"


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
        self.itens.append(ItemPedido(produto, quantidade))

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
        impressora.imprimir(self.visualizarResumo())


# ---------------------------------------------------------
# MENU INTERATIVO TOTALMENTE FUNCIONAL
# ---------------------------------------------------------
class PixelCoffeeApp:
    def __init__(self):
        # Base de dados em memória
        self.produtos: list[Produto] = [
            Bebida(1, "Café Expresso", 6.00, volume_ml=100, gelada=False),
            Bebida(2, "Iced Latte", 12.00, volume_ml=350, gelada=True),
            Alimento(3, "Croissant", 10.00, contem_gluten=True),
            Alimento(4, "Brownie Especial", 10.00, contem_gluten=False)
        ]
        self.clientes: list[Cliente] = [
            Cliente("111.222.333-44", "Kevin Ferreira", desconto_fidelidade=0.10)
        ]
        self.pedidos: list[Pedido] = []
        self.contador_pedidos = 100
        self.impressora = ImpressoraCupom()

    def exibir_menu_principal(self):
        print("\n======================================")
        print("         PIXELCOFFEE - DESK APP II    ")
        print("======================================")
        print("1. Listar Cardápio de Produtos")
        print("2. Cadastrar Novo Produto")
        print("3. Listar Clientes Cadastrados")
        print("4. Cadastrar Novo Cliente")
        print("5. Criar Novo Pedido")
        print("6. Listar/Imprimir Pedidos Realizados")
        print("0. Sair do Sistema")
        print("--------------------------------------")

    def listar_produtos(self):
        print("\n--- CARDÁPIO DE PRODUTOS ---")
        for p in self.produtos:
            print(p.getInfo())

    def cadastrar_produto(self):
        print("\n--- CADASTRO DE PRODUTO ---")
        tipo = input("Tipo (1 - Bebida / 2 - Alimento): ").strip()
        nome = input("Nome do produto: ").strip()
        preco = float(input("Preço base (R$): "))
        novo_id = len(self.produtos) + 1

        if tipo == "1":
            vol = int(input("Volume (ml): "))
            gelada = input("É gelada? (s/n): ").strip().lower() == 's'
            novo_prod = Bebida(novo_id, nome, preco, vol, gelada)
        else:
            gluten = input("Contém glúten? (s/n): ").strip().lower() == 's'
            novo_prod = Alimento(novo_id, nome, preco, gluten)

        self.produtos.append(novo_prod)
        print(f"✅ Produto '{nome}' cadastrado com sucesso!")

    def listar_clientes(self):
        print("\n--- CLIENTES CADASTRADOS ---")
        for c in self.clientes:
            print(c.getIdentificacao())

    def cadastrar_cliente(self):
        print("\n--- CADASTRO DE CLIENTE ---")
        cpf = input("CPF: ").strip()
        nome = input("Nome completo: ").strip()
        desc = float(input("Desconto de fidelidade (ex: 0.10 para 10%): "))
        novo_cliente = Cliente(cpf, nome, desc)
        self.clientes.append(novo_cliente)
        print(f"✅ Cliente '{nome}' cadastrado com sucesso!")

    def criar_pedido(self):
        print("\n--- NOVO PEDIDO ---")
        self.contador_pedidos += 1
        
        # Selecionar cliente
        print("Deseja vincular cliente?")
        for i, c in enumerate(self.clientes):
            print(f"[{i+1}] {c.getIdentificacao()}")
        print("[0] Sem cliente (Consumidor Não Identificado)")
        op_cliente = int(input("Opção: "))
        
        cliente_sel = self.clientes[op_cliente - 1] if op_cliente > 0 else None
        novo_pedido = Pedido(self.contador_pedidos, cliente_sel)

        # Adicionar itens
        while True:
            self.listar_produtos()
            id_p = int(input("\nDigite o ID do produto para adicionar (ou 0 para finalizar pedido): "))
            if id_p == 0:
                break
            prod_encontrado = next((p for p in self.produtos if p.id_prod == id_p), None)
            if prod_encontrado:
                qtd = int(input(f"Quantidade de '{prod_encontrado.nome}': "))
                novo_pedido.adicionarItem(prod_encontrado, qtd)
                print("Item adicionado!")
            else:
                print("Produto não encontrado.")

        if novo_pedido.itens:
            self.pedidos.append(novo_pedido)
            print("\n✅ Pedido finalizado com sucesso!")
            print(novo_pedido.visualizarResumo())
        else:
            print("Pedido cancelado por falta de itens.")

    def listar_pedidos(self):
        print("\n--- HISTÓRICO DE PEDIDOS ---")
        if not self.pedidos:
            print("Nenhum pedido realizado nesta sessão.")
            return

        for p in self.pedidos:
            print("\n" + p.visualizarResumo())
            imprimir = input("Deseja emitir o recibo impresso deste pedido? (s/n): ").strip().lower()
            if imprimir == 's':
                p.emitirRecibo(self.impressora)

    def executar(self):
        while True:
            self.exibir_menu_principal()
            opcao = input("Opção escolhida: ").strip()
            if opcao == "1":
                self.listar_produtos()
            elif opcao == "2":
                self.cadastrar_produto()
            elif opcao == "3":
                self.listar_clientes()
            elif opcao == "4":
                self.cadastrar_cliente()
            elif opcao == "5":
                self.criar_pedido()
            elif opcao == "6":
                self.listar_pedidos()
            elif opcao == "0":
                print("\nEncerrando o PixelCoffee. Até logo!")
                break
            else:
                print("Opção inválida!")


if __name__ == "__main__":
    app = PixelCoffeeApp()
    app.executar()