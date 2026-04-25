# 📦 Entidades e Informações do Domínio — BemStock

## 1. Visão geral

Para desenvolver o sistema **BemStock**, foi necessário identificar os principais elementos que fazem parte do domínio do problema. Essas entidades representam os objetos centrais do sistema de gerenciamento de estoque da instituição **Lar Bem**.

O sistema é responsável pelo controle de **alimentos, produtos de higiene e produtos de limpeza**, registrando entradas, saídas, controle de validade e acompanhamento das movimentações realizadas no estoque.

As principais entidades identificadas são:

- Usuário
- Produto
- Movimentação

---

# 2. Entidades principais do sistema

## 2.1 Usuário

A entidade **Usuário** representa a pessoa responsável por acessar o sistema e realizar operações como cadastro de produtos, registro de movimentações e administração do sistema.

### Atributos

| Atributo | Tipo | Obrigatório? | Observação |
|---|---|---|---|
| `id_usuario` | INTEGER | Sim | Identificador único gerado automaticamente |
| `nome` | TEXT | Sim | Nome do usuário |
| `email` | TEXT | Sim | E-mail usado no login, deve ser único |
| `senha` | TEXT | Sim | Senha armazenada de forma criptografada/hash |
| `perfil` | TEXT | Sim | Deve ser `admin` ou `estoque` |
| `primeiro_acesso` | INTEGER | Sim | Valor padrão `1`; indica se o usuário precisa alterar credenciais |

### Observações importantes

- O sistema cria automaticamente um **usuário administrador temporário** no primeiro uso:
  - e-mail: `teste@bemstock.com`
  - senha: `123456`
  - perfil: `admin`
- O campo `primeiro_acesso` controla se o usuário ainda precisa atualizar suas credenciais.
- Quando `primeiro_acesso = 1`, o usuário ainda está em primeiro acesso.
- Quando `primeiro_acesso = 0`, o usuário já configurou suas credenciais.

---

## 2.2 Produto

A entidade **Produto** representa cada item armazenado no estoque da instituição.

O sistema **não armazena a quantidade diretamente no produto**, pois o controle é realizado por meio das movimentações.

### Atributos

| Atributo | Tipo | Obrigatório? | Observação |
|---|---|---|---|
| `id_produto` | INTEGER | Sim | Identificador único gerado automaticamente |
| `nome` | TEXT | Sim | Nome do produto |
| `categoria` | TEXT | Sim | Deve ser `Alimentos`, `Limpeza` ou `Higiene Pessoal` |
| `unidade_medida` | TEXT | Sim | Deve ser `unidade`, `pacote`, `caixa`, `litros`, `ml`, `kg` ou `grama` |
| `estoque_minimo` | INTEGER | Sim | Quantidade mínima recomendada em estoque |
| `descricao` | TEXT | Não | Descrição adicional do produto |

### Observações importantes

- O estoque atual é **calculado dinamicamente** com base nas movimentações.
- O sistema utiliza o `estoque_minimo` para identificar produtos com baixo estoque.
- A `descricao` é opcional.

---

## 2.3 Movimentação

A entidade **Movimentação** representa cada operação de entrada ou saída de produtos no estoque.

Essa entidade é responsável pelo controle completo do estoque, registrando todo o histórico de entradas e saídas.

### Atributos

| Atributo | Tipo | Obrigatório? | Observação |
|---|---|---|---|
| `id_movimentacao` | INTEGER | Sim | Identificador único gerado automaticamente |
| `tipo_movimentacao` | TEXT | Sim | Deve ser `entrada` ou `saida` |
| `id_produto` | INTEGER | Sim | Referência ao produto movimentado |
| `categoria` | TEXT | Sim | Categoria do produto no momento da movimentação |
| `quantidade` | INTEGER | Sim | Quantidade movimentada |
| `fornecedor` | TEXT | Condicional | Obrigatório apenas para movimentações do tipo `entrada` |
| `data_validade` | TEXT | Condicional | Obrigatória apenas para movimentações do tipo `entrada` |
| `numero_lote` | TEXT | Não | Identificação opcional do lote |
| `destino` | TEXT | Condicional | Obrigatório apenas para movimentações do tipo `saida` |
| `observacoes` | TEXT | Não | Observações adicionais |
| `data_movimentacao` | TEXT | Sim | Data e hora em que a movimentação foi registrada |
| `id_usuario` | INTEGER | Sim | Referência ao usuário responsável pela movimentação |

### Valores permitidos para `destino`

- `cozinha`
- `banheiros`
- `area de servico`
- `lavanderia`
- `refeitorio`
- `outros`

### Observações importantes

- Em movimentações de **entrada**, os campos `fornecedor` e `data_validade` são obrigatórios.
- Em movimentações de **saída**, o campo `destino` é obrigatório.
- A saída não recebe `data_validade`, pois a validade pertence ao lote registrado na entrada.
- Cada movimentação registra quem realizou a ação, garantindo rastreabilidade.
- O controle de validade é feito por lote, permitindo melhor gestão de alimentos e produtos perecíveis.

---

# 3. Relacionamentos entre as entidades

## Produto e Movimentação

Um **produto** pode possuir várias movimentações, enquanto cada movimentação pertence a um único produto.

**Relacionamento:**

Produto **1 : N** Movimentação

---

## Usuário e Movimentação

Um **usuário** pode registrar várias movimentações, enquanto cada movimentação é registrada por um único usuário.

**Relacionamento:**

Usuário **1 : N** Movimentação

---

# 4. Regras de negócio importantes

- O sistema não permite acessar o dashboard no primeiro login do usuário administrador temporário.
- O usuário deve obrigatoriamente alterar o e-mail e a senha no primeiro acesso.
- Após essa alteração, o campo `primeiro_acesso` é atualizado para `0`.
- Produtos não podem ser removidos se possuírem histórico de movimentações.
- A categoria da movimentação deve corresponder à categoria do produto.
- Quantidades de movimentação devem ser sempre valores inteiros positivos.
- O estoque mínimo pode ser zero ou um número inteiro positivo.
- Em entradas, `fornecedor` e `data_validade` são obrigatórios.
- Em saídas, `destino` é obrigatório.
- O campo `numero_lote` é opcional.
- O campo `observacoes` é opcional.

---

# 5. Resumo das entidades

## Usuário

| Atributo | Tipo | Obrigatório? |
|---|---|---|
| `id_usuario` | INTEGER | Sim |
| `nome` | TEXT | Sim |
| `email` | TEXT | Sim |
| `senha` | TEXT | Sim |
| `perfil` | TEXT | Sim |
| `primeiro_acesso` | INTEGER | Sim |

---

## Produto

| Atributo | Tipo | Obrigatório? |
|---|---|---|
| `id_produto` | INTEGER | Sim |
| `nome` | TEXT | Sim |
| `categoria` | TEXT | Sim |
| `unidade_medida` | TEXT | Sim |
| `estoque_minimo` | INTEGER | Sim |
| `descricao` | TEXT | Não |

---

## Movimentação

| Atributo | Tipo | Obrigatório? |
|---|---|---|
| `id_movimentacao` | INTEGER | Sim |
| `tipo_movimentacao` | TEXT | Sim |
| `id_produto` | INTEGER | Sim |
| `categoria` | TEXT | Sim |
| `quantidade` | INTEGER | Sim |
| `fornecedor` | TEXT | Condicional: obrigatório em entrada |
| `data_validade` | TEXT | Condicional: obrigatória em entrada |
| `numero_lote` | TEXT | Não |
| `destino` | TEXT | Condicional: obrigatório em saída |
| `observacoes` | TEXT | Não |
| `data_movimentacao` | TEXT | Sim |
| `id_usuario` | INTEGER | Sim |

---

# 6. Validação das entidades em relação ao domínio

As entidades identificadas atendem às necessidades do sistema porque permitem representar:

- os itens controlados no estoque por meio da entidade **Produto**
- os responsáveis pelas operações por meio da entidade **Usuário**
- o controle completo de entradas e saídas por meio da entidade **Movimentação**

A decisão de não armazenar a quantidade diretamente no produto permite maior controle e rastreabilidade, já que o estoque pode ser calculado com base no histórico de movimentações.

O uso do campo `primeiro_acesso` garante maior segurança no sistema, evitando o uso permanente de credenciais padrão.

---

# 7. Conclusão

A identificação das entidades e seus atributos estabelece uma base sólida para o desenvolvimento do sistema.

Com essa definição, é possível avançar para:

- modelagem do banco de dados
- criação das histórias de usuário
- definição de critérios de aceitação
- implementação do sistema

---

# Critério de pronto

Esta etapa é considerada concluída quando:

- as entidades principais estão identificadas
- os atributos estão alinhados com o banco de dados
- os tipos dos atributos estão documentados
- os campos obrigatórios e opcionais estão definidos
- os relacionamentos estão definidos
- as regras de negócio estão documentadas
- a equipe valida que o modelo representa corretamente o domínio do sistema