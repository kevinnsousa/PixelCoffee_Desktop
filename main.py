from banco import BancoDados

db = BancoDados()

def menu():
    while True:
        print("\n===================================")
        print("     PIXELCOFFEE - DESK APP III    ")
        print("===================================")
        print("1. Listar Cardápio de Produtos")
        print("2. Cadastrar Novo Produto")
        print("3. Listar Clientes Cadastrados")
        print("4. Cadastrar Novo Cliente")
        print("5. Criar Novo Pedido")
        print("6. Listar/Imprimir Pedidos Realizados")
        print("0. Sair do Sistema")
        print("-----------------------------------")
        
        opcao = input("Opção escolhida: ")

        if opcao == "1":
            produtos = db.listar_produtos()
            print("\n--- CARDÁPIO DE PRODUTOS ---")
            if not produtos:
                print("Nenhum produto cadastrado.")
            for p in produtos:
                print(f"ID: {p[0]} | Nome: {p[1]} | Preço: R$ {p[2]:.2f}")

        elif opcao == "2":
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: "))
            db.inserir_produto(nome, preco)
            print("Produto cadastrado com sucesso no banco de dados!")

        elif opcao == "3":
            clientes = db.listar_clientes()
            print("\n--- CLIENTES CADASTRADOS ---")
            if not clientes:
                print("Nenhum cliente cadastrado.")
            for c in clientes:
                print(f"ID: {c[0]} | Nome: {c[1]}")

        elif opcao == "4":
            nome = input("Nome do cliente: ")
            db.inserir_cliente(nome)
            print("Cliente cadastrado com sucesso no banco de dados!")

        elif opcao == "5":
            cliente_nome = input("Nome do cliente para o pedido: ")
            itens = input("Itens do pedido: ")
            total = float(input("Valor total do pedido: R$ "))
            db.inserir_pedido(cliente_nome, itens, total)
            print("Pedido gravado no banco de dados com sucesso!")

        elif opcao == "6":
            pedidos = db.listar_pedidos()
            print("\n--- HISTÓRICO DE PEDIDOS ---")
            if not pedidos:
                print("Nenhum pedido realizado.")
            for ped in pedidos:
                print(f"Pedido #{ped[0]} | Cliente: {ped[1]} | Itens: {ped[2]} | Total: R$ {ped[3]:.2f}")

        elif opcao == "0":
            print("A encerrar o sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()