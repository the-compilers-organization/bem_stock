# Entidades e Informações do Domínio — BemStock

## 1. Visão geral

Para desenvolver o sistema **BemStock**, foi necessário identificar os principais elementos que fazem parte do domínio do problema. Essas entidades representam os objetos centrais do sistema de gerenciamento de estoque da instituição **Lar Bem**.

O sistema será responsável pelo controle de **alimentos, produtos de higiene e produtos de limpeza**, registrando entradas, saídas, controle de validade e acompanhamento das quantidades disponíveis.

As principais entidades identificadas para o domínio do sistema são:

- Usuário
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
- **email** – e-mail utilizado para autenticação no sistema (deve ser único)  
- **senha** – senha de autenticação do usuário  
- **perfil** – tipo de usuário (por exemplo: administrador ou funcionário)  

---

## 2.2 Produto

A entidade **Produto** representa cada item armazenado no estoque da instituição.

Essa entidade contém as informações principais dos itens controlados no sistema.

### Atributos

- **id_produto** – identificador único do produto  
- **nome** – nome do produto  
- **descricao** – descrição ou observação sobre o produto  
- **categoria** – categoria predefinida do produto (Alimentos, Produtos de Higiene ou Produtos de Limpeza)  
- **quantidade_atual** – quantidade disponível no estoque  
- **unidade_medida** – unidade de controle do produto (ex.: unidade, pacote, litro, caixa)  
- **estoque_minimo** – quantidade mínima recomendada para o produto  
- **data_validade** – data de validade do produto  

---

## 2.3 Movimentação

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
- email  
- senha  
- perfil  

---

## Produto

- id_produto  
- nome  
- descricao  
- categoria  
- quantidade_atual  
- unidade_medida  
- estoque_minimo  
- data_validade  

---

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
- os responsáveis pelas operações por meio da entidade **Usuário**  
- o registro das entradas e saídas por meio da entidade **Movimentação**  

A categoria do produto não foi modelada como entidade separada, pois o sistema utilizará categorias fixas predefinidas:

- Alimentos  
- Produtos de Higiene  
- Produtos de Limpeza  

Essas entidades são suficientes para implementar as funcionalidades principais do sistema BemStock na primeira versão do projeto.

---

# 6. Conclusão

A identificação das entidades e suas informações define a base para a modelagem do banco de dados e para a arquitetura do sistema.

Com essa definição, a equipe poderá avançar para as próximas etapas do projeto, como:

- criação das histórias de usuário  
- definição dos critérios de aceitação em BDD  
- modelagem do banco de dados  
- implementação do sistema  

---

# Critério de pronto

Esta etapa é considerada concluída quando:

- as entidades principais do sistema estão identificadas  
- os atributos iniciais de cada entidade foram definidos  
- os relacionamentos entre as entidades estão documentados  
- a equipe confirma que as entidades representam corretamente o domínio do sistema  
