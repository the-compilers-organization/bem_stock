# Requisitos Funcionais — BemStock

## 1. Introdução

Os requisitos funcionais descrevem as funcionalidades que o sistema **BemStock** deve oferecer para atender às necessidades da instituição Lar Bem no controle de estoque de alimentos, produtos de higiene e produtos de limpeza.

Esses requisitos foram definidos com base no domínio do sistema e nas necessidades dos usuários responsáveis pela administração do estoque.

---

# 2. Módulo de Autenticação

**RF01.** O sistema deve permitir que o usuário realize login informando usuário e senha.

**RF02.** O sistema deve permitir acesso apenas a usuários cadastrados.

**RF03.** O sistema deve identificar o usuário responsável pelas operações realizadas no sistema.

---

# 3. Módulo de Categorias

**RF04.** O sistema deve permitir cadastrar categorias de produtos.

**RF05.** O sistema deve permitir listar todas as categorias cadastradas.

**RF06.** O sistema deve permitir editar informações de uma categoria.

**RF07.** O sistema deve permitir excluir uma categoria que não esteja associada a produtos.

---

# 4. Módulo de Produtos

**RF08.** O sistema deve permitir cadastrar produtos no estoque.

**RF09.** O sistema deve permitir registrar no cadastro do produto as seguintes informações:
- nome do produto
- descrição
- categoria
- quantidade atual
- unidade de medida
- estoque mínimo
- data de validade

**RF10.** O sistema deve permitir listar todos os produtos cadastrados.

**RF11.** O sistema deve permitir buscar produtos por nome.

**RF12.** O sistema deve permitir filtrar produtos por categoria.

**RF13.** O sistema deve permitir editar informações de um produto.

**RF14.** O sistema deve permitir excluir um produto do sistema.

---

# 5. Módulo de Movimentação de Estoque

**RF15.** O sistema deve permitir registrar entrada de produtos no estoque.

**RF16.** O sistema deve permitir registrar saída de produtos do estoque.

**RF17.** O sistema deve atualizar automaticamente a quantidade disponível do produto após cada movimentação.

**RF18.** O sistema deve registrar a data da movimentação.

**RF19.** O sistema deve registrar o usuário responsável pela movimentação.

**RF20.** O sistema deve permitir registrar observações nas movimentações.

**RF21.** O sistema não deve permitir saída de quantidade maior do que a disponível em estoque.

---

# 6. Módulo de Controle de Estoque

**RF22.** O sistema deve permitir consultar a quantidade atual de cada produto.

**RF23.** O sistema deve identificar produtos com quantidade abaixo do estoque mínimo.

**RF24.** O sistema deve apresentar alertas para produtos com baixo estoque.

---

# 7. Módulo de Controle de Validade

**RF25.** O sistema deve permitir registrar a data de validade dos produtos.

**RF26.** O sistema deve identificar produtos próximos da data de vencimento.

**RF27.** O sistema deve permitir consultar produtos vencidos ou próximos do vencimento.

---

# 8. Módulo de Histórico

**RF28.** O sistema deve registrar todas as movimentações de entrada e saída de produtos.

**RF29.** O sistema deve permitir consultar o histórico de movimentações.

**RF30.** O sistema deve permitir filtrar movimentações por produto.

**RF31.** O sistema deve permitir filtrar movimentações por período.

**RF32.** O sistema deve permitir filtrar movimentações por tipo (entrada ou saída).

---

# 9. Módulo de Relatórios

**RF33.** O sistema deve permitir visualizar relatório de produtos em estoque.

**RF34.** O sistema deve permitir visualizar relatório de produtos com estoque baixo.

**RF35.** O sistema deve permitir visualizar relatório de produtos próximos da validade.

**RF36.** O sistema deve permitir visualizar relatório de movimentações realizadas.

---

# 10. Conclusão

Os requisitos funcionais definidos garantem que o sistema BemStock atenda às necessidades principais da instituição Lar Bem, permitindo o controle eficiente do estoque de alimentos, produtos de higiene e produtos de limpeza
