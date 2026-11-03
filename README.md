# PixelCoffee - Desktop App I

Aplicação Desktop desenvolvida em Python demonstrando conceitos fundamentais de Programação Orientada a Objetos (POO).

## 📐 Modelagem UML

```mermaid
classDiagram
    class Produto {
        <<abstract>>
        +int id_prod
        +string nome
        +float preco_base
        +calcularPrecoFinal()* float
        +getInfo() string
    }

    class Bebida {
        +int volume_ml
        +bool gelada
        +calcularPrecoFinal() float
        +getInfo() string
    }

    class Alimento {
        +bool contem_gluten
        +calcularPrecoFinal() float
        +getInfo() string
    }

    class Cliente {
        +string cpf
        +string nome
        +float desconto_fidelidade
        +getIdentificacao() string
    }

    class ItemPedido {
        +int quantidade
        +calcularSubtotal() float
        +getDetalhes() string
    }

    class Pedido {
        +int numero
        +adicionarItem(produto, quantidade)
        +calcularTotal() float
        +visualizarResumo() string
        +emitirRecibo(impressora)
    }

    class ImpressoraCupom {
        +imprimir(conteudo)
    }

    Produto <|-- Bebida : Herança
    Produto <|-- Alimento : Herança
    Pedido "1" *-- "0..*" ItemPedido : Composição
    Pedido "0..*" o-- "0..1" Cliente : Agregação
    ItemPedido "0..*" --> "1" Produto : Associação
    Pedido ..> ImpressoraCupom : Dependência
