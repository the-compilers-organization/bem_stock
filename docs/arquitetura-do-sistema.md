# Arquitetura do Sistema — BemStock

## 1. Introdução

Este documento descreve a arquitetura do sistema **BemStock**, desenvolvido para auxiliar no gerenciamento de estoque de alimentos, produtos de higiene e produtos de limpeza da instituição **Lar Bem**.

A arquitetura foi definida com o objetivo de organizar o sistema em camadas, separando responsabilidades e facilitando a manutenção, evolução e entendimento do código.

---

## 2. Visão geral da arquitetura

O sistema BemStock é uma aplicação **desktop**, executada localmente no computador da instituição.

A arquitetura segue uma organização em camadas, permitindo separar:

- interface com o usuário  
- controle das operações  
- manipulação dos dados  
- acesso ao banco de dados  

Essa abordagem melhora a organização do sistema e facilita o desenvolvimento e manutenção.

---

## 3. Tecnologias utilizadas

### Linguagem principal

**Python**

Python foi escolhido por ser uma linguagem gratuita, de fácil aprendizado e adequada para desenvolvimento de aplicações desktop.

---

### Interface gráfica

**CustomTkinter**

A biblioteca CustomTkinter é utilizada para desenvolver a interface gráfica do sistema.

Motivos da escolha:

- gratuita  
- visual moderno  
- baseada no Tkinter  
- fácil integração com Python  
- adequada para projetos acadêmicos  

---

### Banco de dados

**SQLite**

O SQLite é utilizado como banco de dados do sistema.

Motivos da escolha:

- gratuito  
- funcionamento local  
- não necessita servidor  
- simples configuração  
- ideal para aplicações desktop  

---

### Acesso ao banco de dados

O acesso ao banco é realizado utilizando:

- **sqlite3** (biblioteca nativa do Python)

Essa abordagem simplifica o desenvolvimento e reduz a complexidade do projeto.

---

## 4. Organização em camadas

A arquitetura do sistema é dividida nas seguintes camadas:

- View  
- Controller  
- Model  
- Database  
- Utils  

Essa organização segue uma adaptação do padrão **MVC (Model-View-Controller)** para aplicações desktop.

---

## 5. Responsabilidade de cada camada

### 5.1 View

A camada **View** é responsável pela interface gráfica do sistema.

Funções principais:

- exibir telas  
- coletar dados do usuário  
- apresentar informações  
- exibir mensagens de erro e sucesso  
- controlar navegação entre telas  

Exemplos:

- login  
- dashboard  
- usuários  
- produtos  
- movimentações  

A View não contém regras de negócio, apenas interação com o usuário.

---

### 5.2 Controller

A camada **Controller** é responsável pela lógica de controle do sistema.

Funções principais:

- receber ações da View  
- validar dados  
- aplicar regras de negócio  
- interagir com o banco de dados  
- retornar resultados para a View  

Exemplos:

- autenticar usuário  
- cadastrar usuário  
- cadastrar produto  
- registrar movimentação  
- buscar e listar dados  

---

### 5.3 Model

A camada **Model** representa a estrutura dos dados do sistema.

Funções principais:

- organizar os dados em formato estruturado (dict)  
- preparar dados para inserção no banco  
- converter dados para tuplas compatíveis com SQL  

Principais entidades:

- Usuário  
- Produto  
- Movimentação  

> Observação: neste sistema, as regras de negócio estão concentradas nos Controllers.

---

### 5.4 Database

A camada **Database** é responsável pelo acesso ao banco de dados.

Funções principais:

- criar conexão com SQLite  
- definir e criar tabelas  
- executar comandos SQL  
- garantir persistência dos dados  

Arquivos principais:

- `connection.py`  
- `schema.py`  

---

### 5.5 Utils

A camada **Utils** contém funções auxiliares reutilizáveis.

Funções principais:

- validações de dados  
- formatação de datas  
- constantes do sistema  
- segurança (hash de senha)  

Exemplos:

- validação de e-mail  
- validação de quantidade  
- formatação de datas  
- hash de senha  

---

## 6. Fluxo da aplicação

O funcionamento do sistema segue o fluxo abaixo:

1. O usuário interage com a interface (View)  
2. A View envia a ação para o Controller  
3. O Controller valida os dados  
4. O Controller executa regras de negócio  
5. O Controller acessa o banco de dados  
6. O banco executa a operação  
7. O resultado retorna para o Controller  
8. O Controller retorna a resposta para a View  
9. A View exibe o resultado ao usuário  

---

## 7. Estrutura do projeto

A estrutura do projeto BemStock é organizada da seguinte forma:

```text
bemstock/
│
├── assets/
├── docs/
│   ├── dominio-do-projeto.md
│   ├── entidades-do-dominio.md
│   ├── requisitos-funcionais.md
│   ├── requisitos-nao-funcionais.md
│   └── arquitetura-do-sistema.md
│
├── src/
│   ├── main.py
│
│   ├── views/
│   │   ├── login_view.py
│   │   ├── dashboard_view.py
│   │   ├── usuario_view.py
│   │   ├── cadastro_usuario_view.py
│   │   ├── produto_view.py
│   │   ├── cadastro_produto_view.py
│   │   ├── movimentacao_view.py
│   │   └── cadastro_movimentacao_view.py
│
│   ├── controllers/
│   │   ├── login_controller.py
│   │   ├── usuario_controller.py
│   │   ├── produto_controller.py
│   │   └── movimentacao_controller.py
│
│   ├── models/
│   │   ├── usuario.py
│   │   ├── produto.py
│   │   └── movimentacao.py
│
│   ├── database/
│   │   ├── connection.py
│   │   └── schema.py
│
│   └── utils/
│       ├── constantes.py
│       ├── validacoes.py
│       ├── formatadores.py
│       └── seguranca.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
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
[Interface - CustomTkinter]
    ↓
[Controllers]
    ↓
[Database / SQLite]
    ↓
[Banco de dados]
```

---

# 9. Viabilidade da arquitetura

A arquitetura escolhida é adequada ao projeto porque:

- utiliza tecnologias gratuitas
- é simples de implementar
- organiza bem o código
- facilita a manutenção futura
- permite a divisão de tarefas entre os membros da equipe

Ela atende ao escopo do sistema BemStock, que inclui:

- cadastro de usuários
- cadastro de produtos
- entrada de produtos
- saída de produtos
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
- arquitetura em camadas para separação de responsabilidades

Essa estrutura fornece uma base sólida para o desenvolvimento do sistema de gerenciamento de estoque da instituição Lar Bem.

---

# Critério de pronto

Esta etapa é considerada concluída quando:

- a linguagem principal do projeto está definida
- a biblioteca da interface gráfica está definida
- o banco de dados está definido
- a arquitetura em camadas está documentada
- as responsabilidades de cada camada estão descritas
- a arquitetura inicial está representada
- o grupo confirma que a arquitetura é viável para o desenvolvimento do projeto


