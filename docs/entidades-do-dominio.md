# 📦 Entidades e Informações do Domínio — BemStock

## 1. Visão geral

Para desenvolver o sistema **BemStock**, foi necessário identificar os principais elementos que fazem parte do domínio do problema. Essas entidades representam os objetos centrais do sistema de gerenciamento de estoque da instituição **Lar Bem**.

O sistema é responsável pelo controle de **alimentos, produtos de higiene e produtos de limpeza**, registrando entradas, saídas, controle de validade e acompanhamento das movimentações realizadas no estoque.

As principais entidades identificadas são:

- Usuário  
- Produto  
- Movimentação  

Essas entidades servem de base para a modelagem do banco de dados e para a arquitetura do sistema.

---

# 2. Entidades principais do sistema

## 2.1 Usuário

A entidade **Usuário** representa a pessoa responsável por acessar o sistema e realizar operações como cadastro de produtos, registro de movimentações e administração do sistema.

### Atributos

- **id_usuario** – identificador único do usuário  
- **nome** – nome do usuário  
- **email** – e-mail utilizado para autenticação (único)  
- **senha** – senha criptografada do usuário  
- **perfil** – tipo de usuário (valores possíveis: `admin` ou `estoque`)  
- **primeiro_acesso** – indica se o usuário ainda precisa realizar a configuração inicial:
  - `1` → usuário em primeiro acesso (obrigatório alterar e-mail e senha)  
  - `0` → usuário já configurado  

### Observações importantes

- O sistema cria automaticamente um **usuário administrador temporário** no primeiro uso:
  - e-mail: `teste@bemstock.com`
  - senha: `123456`
  - perfil: `admin`
- Esse usuário **não pode utilizar o sistema normalmente** até atualizar suas credenciais.
- O campo `primeiro_acesso` é responsável por controlar esse comportamento.

---

## 2.2 Produto

A entidade **Produto** representa cada item armazenado no estoque da instituição.

O sistema **não armazena a quantidade diretamente no produto**, pois o controle é realizado por meio das movimentações.

### Atributos

- **id_produto** – identificador único do produto  
- **nome** – nome do produto  
- **categoria** – categoria predefinida:
  - Alimentos  
  - Limpeza  
  - Higiene Pessoal  
- **unidade_medida** – unidade de controle:
  - unidade  
  - pacote  
  - caixa  
  - litros  
  - ml  
  - kg  
  - grama  
- **estoque_minimo** – quantidade mínima recomendada  
- **descricao** – descrição opcional  

### Observações importantes

- O estoque atual é **calculado dinamicamente** com base nas movimentações.
- O sistema utiliza o `estoque_minimo` para identificar produtos com baixo estoque.

---

## 2.3 Movimentação

A entidade **Movimentação** representa cada operação de entrada ou saída de produtos no estoque.

Essa entidade é **responsável pelo controle completo do estoque**, registrando todo o histórico.

### Atributos

- **id_movimentacao** – identificador único da movimentação  

- **tipo_movimentacao** – tipo da operação:
  - entrada  
  - saída  

- **id_produto** – referência ao produto movimentado  

- **categoria** – categoria do produto no momento da movimentação  

- **quantidade** – quantidade movimentada  

- **fornecedor** – fornecedor do produto (opcional, usado em entradas)  

- **data_validade** – data de validade do lote (opcional)  

- **numero_lote** – identificação do lote (opcional)  

- **destino** – local de destino (usado em saídas):
  - cozinha  
  - banheiros  
  - area de servico  
  - lavanderia  
  - refeitório  
  - outros  

- **observacoes** – observações adicionais  

- **data_movimentacao** – data em que a movimentação ocorreu  

- **id_usuario** – usuário responsável pela movimentação  

### Observações importantes

- Cada movimentação registra **quem realizou a ação**, garantindo rastreabilidade.
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

- O sistema **não permite acessar o dashboard no primeiro login** do usuário administrador temporário.
- O usuário deve obrigatoriamente:
  - alterar o e-mail
  - alterar a senha
- Após essa alteração, o campo `primeiro_acesso` é atualizado para `0`.

- Produtos não podem ser removidos se possuírem histórico de movimentações.
- A categoria da movimentação deve corresponder à categoria do produto.
- Quantidades devem ser sempre valores inteiros positivos (ou zero para estoque mínimo).

---

# 5. Resumo das entidades

## Usuário

- id_usuario  
- nome  
- email  
- senha  
- perfil  
- primeiro_acesso  

---

## Produto

- id_produto  
- nome  
- categoria  
- unidade_medida  
- estoque_minimo  
- descricao  

---

## Movimentação

- id_movimentacao  
- tipo_movimentacao  
- id_produto  
- categoria  
- quantidade  
- fornecedor  
- data_validade  
- numero_lote  
- destino  
- observacoes  
- data_movimentacao  
- id_usuario  

---

# 6. Validação das entidades em relação ao domínio

As entidades identificadas atendem às necessidades do sistema porque permitem representar:

- os itens controlados no estoque por meio da entidade **Produto**  
- os responsáveis pelas operações por meio da entidade **Usuário**  
- o controle completo de entradas e saídas por meio da entidade **Movimentação**  

A decisão de **não armazenar a quantidade diretamente no produto** permite maior controle e rastreabilidade, já que o estoque pode ser calculado com base no histórico de movimentações.

O uso do campo `primeiro_acesso` garante maior segurança no sistema, evitando o uso de credenciais padrão.

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
- os relacionamentos estão definidos  
- as regras de negócio estão documentadas  
- a equipe valida que o modelo representa corretamente o domínio do sistema  