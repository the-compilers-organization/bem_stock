# Entidades e Informações do Domínio — BemStock

## 1. Visão geral

Para desenvolver o sistema **BemStock**, foi necessário identificar os principais elementos que fazem parte do domínio do problema. Essas entidades representam os objetos centrais do sistema de gerenciamento de estoque da instituição **Lar Bem**.

O sistema será responsável pelo controle de **alimentos, produtos de higiene e produtos de limpeza**, registrando entradas, saídas, controle de validade e acompanhamento das quantidades disponíveis.

As principais entidades identificadas para o domínio do sistema são:

- Usuário
- Categoria
- Produto
- Movimentação

Essas entidades servirão de base para a modelagem do banco de dados e para a arquitetura do sistema.

---

# 2. Entidades principais do sistema

## 2.1 Usuário

A entidade **Usuário** representa a pessoa responsável por acessar o sistema e realizar operações como cadastro de produtos e registro de movimentações no estoque.

### Atributos

- **id_usuario** – identificador único do usuário
- **nome** – nome do usuário
- **login** – nome de usuário utilizado para acessar o sistema
- **senha** – senha de autenticação do usuário
- **perfil** – tipo de usuário (por exemplo: administrador ou funcionário)

---

## 2.2 Categoria

A entidade **Categoria** representa o grupo ao qual um produto pertence.

No escopo atual do projeto, as categorias principais são:

- alimentos
- produtos de higiene
- produtos de limpeza

### Atributos

- **id_categoria** – identificador único da categoria
- **nome_categoria** – nome da categoria
- **descricao** – descrição opcional da categoria

---

## 2.3 Produto

A entidade **Produto** representa cada item armazenado no estoque da instituição.

Essa entidade contém as informações principais dos itens controlados no sistema.

### Atributos

- **id_produto** – identificador único do produto
- **nome** – nome do produto
- **descricao** – descrição ou observação sobre o produto
- **quantidade_atual** – quantidade disponível no estoque
- **unidade_medida** – unidade de controle do produto (ex.: unidade, pacote, litro, caixa)
- **estoque_minimo** – quantidade mínima recomendada para o produto
- **data_validade** – data de validade do produto
- **id_categoria** – referência à categoria do produto

---

## 2.4 Movimentação

A entidade **Movimentação** representa cada operação de entrada ou saída de produtos no estoque.

Essa entidade permite registrar o histórico de alterações de quantidade dos produtos.

### Atributos

- **id_movimentacao** – identificador único da movimentação
- **tipo_movimentacao** – tipo da movimentação (entrada ou saída)
- **quantidade** – quantidade movimentada
- **data_movimentacao** – data em que a movimentação ocorreu
- **observacao** – observação opcional sobre a movimentação
- **id_produto** – referência ao produto movimentado
- **id_usuario** – referência ao usuário que realizou a movimentação

---

# 3. Relacionamentos entre as entidades

## Categoria e Produto

Uma **categoria** pode possuir vários produtos, enquanto cada **produto** pertence a apenas uma categoria.

Relacionamento:

Categoria **1 : N** Produto

---

## Produto e Movimentação

Um **produto** pode possuir várias movimentações registradas no sistema, enquanto cada **movimentação** está associada a um único produto.

Relacionamento:

Produto **1 : N** Movimentação

---

## Usuário e Movimentação

Um **usuário** pode registrar várias movimentações no sistema, enquanto cada movimentação é registrada por um único usuário.

Relacionamento:

Usuário **1 : N** Movimentação

---

# 4. Resumo das entidades

## Usuário

- id_usuario
- nome
- login
- senha
- perfil

## Categoria

- id_categoria
- nome_categoria
- descricao

## Produto

- id_produto
- nome
- descricao
- quantidade_atual
- unidade_medida
- estoque_minimo
- data_validade
- id_categoria

## Movimentação

- id_movimentacao
- tipo_movimentacao
- quantidade
- data_movimentacao
- observacao
- id_produto
- id_usuario

---

# 5. Validação das entidades em relação ao domínio

As entidades identificadas atendem às necessidades do sistema porque permitem representar:

- os itens controlados no estoque por meio da entidade **Produto**
- a organização dos itens por meio da entidade **Categoria**
- os responsáveis pelas operações por meio da entidade **Usuário**
- o registro das entradas e saídas por meio da entidade **Movimentação**

Essas entidades são suficientes para implementar as funcionalidades principais do sistema BemStock na primeira versão do projeto.

---

# 6. Conclusão

A identificação das entidades e suas informações define a base para a modelagem do banco de dados e para a arquitetura do sistema.

Com essa definição, a equipe poderá avançar para as próximas etapas do projeto, como:

- criação das histórias de usuário
- definição dos critérios de aceitação em BDD
- modelagem do banco de dados
- implementação do sistema.

---

# Critério de pronto

Esta etapa é considerada concluída quando:

- as entidades principais do sistema estão identificadas
- os atributos iniciais de cada entidade foram definidos
- os relacionamentos entre as entidades estão documentados
- a equipe confirma que as entidades representam corretamente o domínio do sistema
