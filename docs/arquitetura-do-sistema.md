# Arquitetura do Sistema — BemStock

## 1. Introdução

Este documento descreve a arquitetura do sistema **BemStock**, desenvolvido para auxiliar no gerenciamento de estoque de alimentos, produtos de higiene e produtos de limpeza da instituição **Lar Bem**.

A arquitetura foi definida para organizar o desenvolvimento do sistema, separando responsabilidades entre módulos e facilitando a manutenção e evolução do projeto.

---

# 2. Visão geral da arquitetura

O sistema BemStock será uma aplicação **desktop**, executada localmente no computador da administração da instituição.

A arquitetura foi planejada utilizando uma estrutura em camadas, permitindo separar:

- interface com o usuário
- controle das operações
- regras de negócio
- acesso ao banco de dados

Essa organização facilita o desenvolvimento em equipe e torna o código mais organizado e compreensível.

---

# 3. Tecnologias utilizadas

## Linguagem principal

**Python**

Python foi escolhido por ser uma linguagem gratuita, de fácil aprendizado e adequada para desenvolvimento de aplicações desktop e integração com banco de dados.

---

## Interface gráfica

**CustomTkinter**

A biblioteca CustomTkinter será utilizada para desenvolver a interface gráfica do sistema.

Ela foi escolhida porque:

- é gratuita
- possui visual moderno
- é baseada no Tkinter
- é simples de usar em projetos acadêmicos
- permite criar interfaces amigáveis para o usuário

---

## Banco de dados

**SQLite**

O SQLite será utilizado como banco de dados do sistema.

Motivos da escolha:

- é gratuito
- funciona localmente
- não exige instalação de servidor
- é simples de configurar
- é ideal para aplicações desktop

---

## Acesso ao banco de dados

O acesso ao banco poderá ser feito utilizando:

- **sqlite3** (biblioteca nativa do Python)

ou

- **SQLAlchemy** (ORM opcional para organização do código)

Para simplificar o desenvolvimento inicial do projeto, pode ser utilizado o **sqlite3**.

---

# 4. Organização em camadas

A arquitetura do sistema será dividida nas seguintes camadas:

- View
- Controller
- Model
- Database
- Utils

Essa organização segue uma adaptação do padrão **MVC (Model-View-Controller)** para aplicações desktop.

---

# 5. Responsabilidade de cada camada

## 5.1 View

A camada **View** é responsável pela interface gráfica do sistema.

Funções principais:

- exibir telas
- coletar dados do usuário
- mostrar mensagens de erro ou sucesso
- apresentar informações do sistema

Exemplos de telas:

- tela de login
- tela principal (dashboard)
- cadastro de categorias
- cadastro de produtos
- registro de entrada de produtos
- registro de saída de produtos
- consulta de estoque
- histórico de movimentações

A View não deve conter regras de negócio complexas.

---

## 5.2 Controller

A camada **Controller** funciona como intermediária entre a interface e as regras do sistema.

Funções principais:

- receber ações da interface
- validar dados recebidos
- chamar funções da camada Model
- retornar respostas para a interface

Exemplos de operações:

- cadastrar produto
- registrar entrada de produto
- registrar saída de produto
- buscar produtos
- listar movimentações

---

## 5.3 Model

A camada **Model** representa as entidades do sistema e as regras de negócio.

Funções principais:

- representar os dados do sistema
- aplicar regras relacionadas ao estoque
- organizar dados antes de salvar ou consultar no banco

Principais entidades do sistema:

- Usuário
- Categoria
- Produto
- Movimentação

Exemplos de regras de negócio:

- impedir saída maior que o estoque disponível
- identificar produtos abaixo do estoque mínimo
- verificar produtos próximos da validade

---

## 5.4 Database

A camada **Database** é responsável pela comunicação com o banco de dados.

Funções principais:

- criar conexão com o banco SQLite
- criar tabelas
- inserir dados
- atualizar dados
- consultar dados
- excluir registros

Essa camada centraliza o acesso ao banco para manter o sistema organizado.

---

## 5.5 Utils

A camada **Utils** contém funções auxiliares reutilizáveis no sistema.

Exemplos:

- validações de dados
- formatação de datas
- mensagens padrão
- funções de apoio

Essa camada evita repetição de código.

---

# 6. Fluxo da aplicação

O funcionamento básico do sistema seguirá o fluxo abaixo:

1. O usuário interage com a interface (View)
2. A View envia a ação para o Controller
3. O Controller valida os dados e chama o Model
4. O Model executa as regras de negócio
5. O Model acessa a camada Database
6. O Database realiza operações no SQLite
7. O resultado retorna para o Controller
8. O Controller retorna a resposta para a View
9. A View exibe o resultado ao usuário

---

# 7. Estrutura inicial de pastas

A estrutura inicial sugerida para o projeto é:

```text
bemstock/
│
├── docs/
│ ├── dominio-do-projeto.md
│ ├── entidades-do-dominio.md
│ ├── requisitos-funcionais.md
│ ├── requisitos-nao-funcionais.md
│ └── arquitetura-do-sistema.md
│
├── src/
│ ├── main.py
│
│ ├── views/
│ │ ├── login_view.py
│ │ ├── dashboard_view.py
│ │ ├── categoria_view.py
│ │ ├── produto_view.py
│ │ └── movimentacao_view.py
│
│ ├── controllers/
│ │ ├── login_controller.py
│ │ ├── categoria_controller.py
│ │ ├── produto_controller.py
│ │ └── movimentacao_controller.py
│
│ ├── models/
│ │ ├── usuario.py
│ │ ├── categoria.py
│ │ ├── produto.py
│ │ └── movimentacao.py
│
│ ├── database/
│ │ ├── connection.py
│ │ └── schema.py
│
│ └── utils/
│ ├── validacoes.py
│ └── formatadores.py
│
├── assets/
│ └── logo.png
│
├── requirements.txt
└── README.md
```

---

# 8. Representação da arquitetura

Arquitetura simplificada:

```text
Usuário
  ↓
Interface (View)
  ↓
Controller
  ↓
Model
  ↓
Database
  ↓
SQLite
```


Fluxo detalhado:

```text
[Usuário]
    ↓
[Telas em CustomTkinter]
    ↓
[Controllers]
    ↓
[Models / Regras de negócio]
    ↓
[Camada de banco de dados]
    ↓
[SQLite]
```

---

# 9. Viabilidade da arquitetura

A arquitetura escolhida é adequada ao projeto porque:

- utiliza tecnologias gratuitas
- é simples de implementar
- organiza bem o código
- facilita manutenção futura
- permite divisão de tarefas entre os membros da equipe

Ela atende ao escopo do sistema BemStock, que inclui:

- cadastro de categorias
- cadastro de produtos
- entrada e saída de itens
- controle de estoque mínimo
- controle de validade
- histórico de movimentações

---

# 10. Conclusão

A arquitetura do sistema BemStock foi definida para garantir organização, clareza e viabilidade no desenvolvimento do projeto.

A solução utiliza:

- Python como linguagem principal
- CustomTkinter para interface gráfica
- SQLite como banco de dados local
- arquitetura em camadas para separar responsabilidades

Essa estrutura fornece uma base sólida para o desenvolvimento do sistema de gerenciamento de estoque da instituição Lar Bem.

---

# Critério de pronto

Esta etapa é considerada concluída quando:

- a linguagem principal do projeto está definida
- a biblioteca da interface gráfica está definida
- o banco de dados está definido
- a arquitetura em camadas está documentada
- as responsabilidades de cada camada estão descritas
- a arquitetura inicial está desenhada
- o grupo confirma que a arquitetura é viável para o desenvolvimento do projeto




