# PixelCoffee - Desktop App I

Aplicação Desktop desenvolvida em Python demonstrando conceitos fundamentais de Programação Orientada a Objetos (POO).

## 📐 Modelagem UML

![Diagrama UML](./uml_diagram.png)

## 🔗 Relações POO Implementadas
- **Herança:** `Bebida` e `Alimento` herdam de `Produto`.
- **Polimorfismo:** Método `calcularPrecoFinal()` sobrescrito nas subclasses.
- **Composição:** `Pedido` gerencia o ciclo de vida de `ItemPedido`.
- **Agregação:** `Pedido` associa-se de forma independente com `Cliente`.
- **Associação Simples:** `ItemPedido` referencia `Produto`.
- **Dependência:** `Pedido` utiliza `ImpressoraCupom` no método `emitirRecibo()`.