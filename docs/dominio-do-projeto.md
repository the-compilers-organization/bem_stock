# Domínio do Projeto — BemStock

## Problema

A instituição Lar Bem utiliza diariamente diversos itens essenciais para seu funcionamento, como alimentos, produtos de higiene e produtos de limpeza. O controle desses itens, quando realizado de forma manual, pode gerar dificuldades no acompanhamento das movimentações, na identificação de faltas e no controle de validade dos produtos.

Além disso, a ausência de registros organizados pode dificultar a rastreabilidade das entradas e saídas de itens.

---

## Contexto

O Lar Bem é uma instituição de acolhimento localizada no Recife, que atende meninas e adolescentes encaminhadas pela justiça devido a medidas protetivas.

Para garantir o funcionamento da instituição, é necessário manter um controle organizado dos recursos utilizados no dia a dia, assegurando que os itens estejam disponíveis quando necessário e que não haja desperdício.

---

## Objetivo do Sistema

O sistema BemStock tem como objetivo organizar e controlar o estoque de alimentos, produtos de higiene e produtos de limpeza da instituição.

O sistema permitirá:

- realizar login no sistema
- cadastrar produtos
- registrar entradas de itens
- registrar saídas de itens
- consultar o estoque disponível
- identificar produtos com estoque baixo
- controlar a validade dos produtos por meio de registros de entrada
- acompanhar o histórico de movimentações

---

## Usuários do Sistema

Os principais usuários do sistema serão:

- administradores do sistema (perfil `admin`)
- responsáveis pelo controle de estoque (perfil `estoque`)

Cada usuário terá permissões de acordo com seu perfil.

---

## Itens Controlados

O sistema controlará três categorias fixas predefinidas:

- Alimentos  
- Produtos de Higiene  
- Produtos de Limpeza  

Essas categorias não poderão ser alteradas pelo usuário, garantindo padronização dos dados.

---

## Operações do Sistema

O sistema BemStock permitirá realizar as seguintes operações:

### Login
- acessar o sistema por meio de autenticação com e-mail e senha

### Cadastro de produtos
- cadastrar itens do estoque com:
  - nome
  - categoria
  - unidade de medida
  - estoque mínimo
  - descrição

> Observação: a quantidade de produtos não é armazenada diretamente, sendo calculada a partir das movimentações.

---

### Consulta de estoque
- visualizar os produtos cadastrados
- verificar o estoque atual com base nas movimentações registradas
- identificar o status do estoque (normal, baixo, esgotado)

---

### Registro de entrada de produtos
- registrar a entrada de novos itens no estoque
- informar dados como:
  - quantidade
  - fornecedor (opcional)
  - data de validade (opcional)
  - número do lote (opcional)

---

### Registro de saída de produtos
- registrar a retirada de itens do estoque
- informar o destino do item (ex.: cozinha, refeitório, etc.)

---

### Controle de estoque mínimo
- identificar automaticamente produtos com quantidade abaixo do nível mínimo definido

---

### Controle de validade
- acompanhar a validade dos produtos com base nos registros de entrada
- identificar produtos próximos do vencimento ou vencidos

---

### Histórico de movimentações
- consultar todas as entradas e saídas realizadas
- aplicar filtros por:
  - produto
  - categoria
  - período
  - tipo de movimentação
  - fornecedor
  - lote

---

## Considerações sobre o domínio

O controle de estoque no sistema BemStock é baseado em **movimentações**, ou seja:

- o estoque não é armazenado diretamente no produto
- ele é calculado a partir das entradas e saídas registradas

Essa abordagem permite:

- maior controle e rastreabilidade
- histórico completo de operações
- melhor suporte para auditoria e análise

---

## Conclusão

O domínio do projeto BemStock está focado no controle eficiente de estoque de uma instituição social, garantindo organização, rastreabilidade e apoio à tomada de decisão.

A definição clara do domínio permite orientar o desenvolvimento do sistema e garantir que as funcionalidades atendam às necessidades reais da instituição.

---

## Critério de pronto

Esta etapa é considerada concluída quando:

- o problema está claramente definido  
- o contexto da instituição está descrito  
- os objetivos do sistema estão alinhados com a solução proposta  
- os usuários do sistema foram identificados  
- as operações do sistema estão documentadas  
- o domínio está consistente com a implementação do sistema  