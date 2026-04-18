# Requisitos Funcionais — BemStock

## 1. Introdução

Os requisitos funcionais descrevem as funcionalidades que o sistema **BemStock** deve oferecer para atender às necessidades da instituição Lar Bem no controle de estoque de alimentos, produtos de higiene e produtos de limpeza.

Esses requisitos foram definidos com base no domínio do sistema, nas regras implementadas e nas necessidades dos usuários responsáveis pela administração do estoque.

---

## 2. Módulo de Autenticação

**RF01.** O sistema deve permitir que o usuário realize login informando e-mail e senha.

**RF02.** O sistema deve permitir acesso apenas a usuários cadastrados.

**RF03.** O sistema deve validar as credenciais do usuário antes de permitir o acesso.

**RF04.** O sistema deve identificar o usuário responsável pelas operações realizadas.

---

## 3. Módulo de Usuários

**RF05.** O sistema deve permitir que o administrador cadastre novos usuários.

**RF06.** O sistema deve permitir registrar no cadastro do usuário as seguintes informações:
- nome  
- e-mail  
- senha  
- perfil (`admin` ou `estoque`)

**RF07.** O sistema não deve permitir o cadastro de dois usuários com o mesmo e-mail.

**RF08.** O sistema deve permitir listar usuários cadastrados.

**RF09.** O sistema deve permitir buscar usuários por nome ou e-mail.

**RF10.** O sistema deve permitir editar os dados de um usuário.

**RF11.** O sistema deve permitir atualizar a senha de um usuário.

**RF12.** O sistema deve permitir excluir usuários.

**RF13.** O sistema não deve permitir excluir o usuário administrador padrão (`admin@bemstock.com`).

---

## 4. Módulo de Produtos

**RF14.** O sistema deve permitir cadastrar produtos no estoque.

**RF15.** O sistema deve permitir registrar no cadastro do produto as seguintes informações:
- nome do produto  
- categoria  
- unidade de medida  
- estoque mínimo  
- descrição  

**RF16.** O sistema deve permitir listar todos os produtos cadastrados.

**RF17.** O sistema deve permitir buscar produtos por nome.

**RF18.** O sistema deve permitir filtrar produtos por categoria.

**RF19.** O sistema deve permitir editar informações de um produto.

**RF20.** O sistema deve permitir excluir um produto.

**RF21.** O sistema não deve permitir excluir produtos que possuam movimentações registradas.

**RF22.** O sistema deve permitir utilizar apenas categorias predefinidas:
- Alimentos  
- Limpeza  
- Higiene Pessoal  

---

## 5. Módulo de Movimentação de Estoque

**RF23.** O sistema deve permitir registrar entrada de produtos no estoque.

**RF24.** O sistema deve permitir registrar saída de produtos do estoque.

**RF25.** O sistema deve registrar as seguintes informações na movimentação:
- tipo de movimentação (entrada ou saída)  
- produto  
- categoria  
- quantidade  
- data da movimentação  
- usuário responsável  

**RF26.** O sistema deve permitir registrar informações adicionais na movimentação:
- fornecedor (opcional)  
- data de validade (opcional)  
- número do lote (opcional)  
- destino (opcional, para saídas)  
- observações (opcional)  

**RF27.** O sistema deve validar se o produto e o usuário existem antes de registrar a movimentação.

**RF28.** O sistema deve garantir que a categoria da movimentação seja compatível com a categoria do produto.

**RF29.** O sistema deve registrar automaticamente a data e hora da movimentação.

---

## 6. Módulo de Controle de Estoque

**RF30.** O sistema deve calcular o estoque atual de cada produto com base nas movimentações de entrada e saída.

**RF31.** O sistema deve permitir consultar o estoque atual dos produtos.

**RF32.** O sistema deve identificar produtos com quantidade abaixo do estoque mínimo.

**RF33.** O sistema deve classificar o status do estoque (normal, baixo, esgotado).

---

## 7. Módulo de Controle de Validade

**RF34.** O sistema deve considerar a data de validade informada nas movimentações de entrada.

**RF35.** O sistema deve identificar produtos com validade próxima ou vencida.

**RF36.** O sistema deve permitir consultar produtos com problemas de validade.

---

## 8. Módulo de Histórico de Movimentações

**RF37.** O sistema deve registrar todas as movimentações de entrada e saída de produtos.

**RF38.** O sistema deve permitir consultar o histórico de movimentações.

**RF39.** O sistema deve permitir filtrar movimentações por:
- produto  
- categoria  
- período  
- tipo de movimentação  
- fornecedor  
- número de lote  

---

## 9. Conclusão

Os requisitos funcionais definidos garantem que o sistema BemStock atenda às necessidades principais da instituição Lar Bem, permitindo o controle eficiente do estoque por meio de movimentações, com rastreabilidade e organização das operações.