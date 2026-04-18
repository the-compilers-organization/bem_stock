<h1 align="center">📦 BemStock</h1>

<p align="center">
  <img src="http://img.shields.io/static/v1?label=Python&message=3.x&color=3776AB&style=for-the-badge&logo=python"/>
  <img src="http://img.shields.io/static/v1?label=CustomTkinter&message=GUI&color=1E90FF&style=for-the-badge"/>
  <img src="http://img.shields.io/static/v1?label=SQLite&message=Database&color=003B57&style=for-the-badge&logo=sqlite"/>
  <img src="http://img.shields.io/static/v1?label=Git&message=2.x&color=f05032&style=for-the-badge&logo=git"/>
  <img src="http://img.shields.io/static/v1?label=GitHub&message=2026&color=181717&style=for-the-badge&logo=github"/>
  <img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=yellow&style=for-the-badge"/>
  <img src="http://img.shields.io/static/v1?label=License&message=MIT&color=green&style=for-the-badge"/>
</p>

---

# 📌 Contexto

O projeto **BemStock** é um sistema de gerenciamento de estoque desenvolvido para auxiliar a instituição **Lar Bem**, localizada no Recife, no controle de alimentos, produtos de higiene e produtos de limpeza utilizados no dia a dia.

O sistema é executado localmente e permite registrar movimentações, controlar estoque e acompanhar validade de produtos.

---

# ❗ Problema

O controle manual de estoque pode gerar:

- falta de organização  
- dificuldade na identificação de itens em falta  
- ausência de controle de validade  
- falta de rastreabilidade  

O BemStock resolve esse problema oferecendo um sistema simples, organizado e confiável.

---

# 👥 Público-Alvo

- Funcionários administrativos  
- Responsáveis pelo estoque  
- Coordenação da instituição  

---

# 🎯 Objetivo

Organizar e controlar o estoque da instituição por meio de:

- registro de entradas e saídas  
- cálculo automático de estoque  
- controle de validade  
- histórico de movimentações  

---

# 🚀 Funcionalidades

### Funcionalidades principais

- Login de usuário  
- Primeiro acesso obrigatório (configuração de segurança)  
- Cadastro de usuários (admin)  
- Cadastro de produtos  
- Edição e exclusão de produtos  
- Registro de entrada e saída  
- Controle de estoque mínimo  
- Controle de validade  
- Histórico de movimentações com filtros  
- Paginação de dados  

---

# 🔐 Primeiro Acesso

Ao iniciar o sistema pela primeira vez, será criado automaticamente um usuário administrador:

- **E-mail:** `teste@bemstock.com`  
- **Senha:** `123456`  

### ⚠️ Regra obrigatória

No primeiro login:

- o sistema **não libera acesso ao dashboard**
- o usuário deve obrigatoriamente:
  - alterar o e-mail  
  - alterar a senha  

Somente após isso o sistema será liberado.

---

# 🎨 Protótipo

🔗 [Acessar protótipo no Figma](https://drawn-award-18708393.figma.site/)

---

# 🏗️ Arquitetura

O sistema utiliza arquitetura em camadas baseada em **MVC**:

- **View** → Interface gráfica  
- **Controller** → Regras de negócio  
- **Model** → Estrutura de dados  
- **Database** → Acesso ao banco  
- **Utils** → Funções auxiliares  

### Fluxo:

```text
Usuário
  ↓
Interface (CustomTkinter)
  ↓
Controller
  ↓
Database
  ↓
SQLite
```

---

# Estrutura do Projeto :file_folder:

```text 
bemstock/
│
├── docs/
│ ├── dominio-do-projeto.md
│ ├── entidades-do-dominio.md
│ ├── requisitos-funcionais.md
│ ├── requisitos-nao-funcionais.md
│ ├── arquitetura-do-sistema.md
│ └── atores-e-casos-de-uso.md
│
├── src/
│ ├── main.py
│ ├── models/
│ ├── views/
│ ├── controllers/
│ ├── database/
│ └── utils/
│
├── assets/
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Instalação :rocket:

### 1️⃣ Clonar o repositório

git clone https://github.com/SEU-REPOSITORIO/bemstock.git

---

### 2️⃣ Entrar na pasta do projeto

cd bemstock

---

### 3️⃣ Criar ambiente virtual

python -m venv venv

---


### 4️⃣ Ativar ambiente virtual

Windows:
### 3️⃣ Criar ambiente virtual


python -m venv venv


### 4️⃣ Ativar ambiente virtual

**Windows:**
venv\Scripts\activate


**Linux/Mac:**
source venv/bin/activate

---

### 5️⃣ Instalar dependências

pip install -r requirements.txt

---

# Tecnologias Utilizadas :wrench:

- **Python**
- **CustomTkinter**
- **SQLite**
- **Git**
- **GitHub**

---

# Documentação :book:

A documentação do projeto está disponível na pasta **docs** do repositório:

- [Domínio do Projeto](docs/dominio-do-projeto.md)
- [Entidades do Domínio](docs/entidades-do-dominio.md)
- [Requisitos Funcionais](docs/requisitos-funcionais.md)
- [Requisitos Não Funcionais](docs/requisitos-nao-funcionais.md)
- [Arquitetura do Sistema](docs/arquitetura-do-sistema.md)
- [Atores e Casos de Uso](docs/atores-e-casos-de-uso.png)

---

# Desenvolvedores/Contribuintes :octocat:

Time responsável pelo desenvolvimento do projeto

| [<img src="https://avatars.githubusercontent.com/u/222337719?v=4" width=115><br><sub>Allan Lucas</sub>](https://github.com/allagez) | [<img src="https://avatars.githubusercontent.com/u/229312657?v=4" width=115><br><sub>Breno Bezerra</sub>](https://github.com/brenobezerra2014-cyber) | [<img src="https://avatars.githubusercontent.com/u/130801505?v=4" width=115><br><sub>Francis Lauriano</sub>](https://github.com/FrancisLauriano) | [<img src="https://avatars.githubusercontent.com/u/234993270?v=4" width=115><br><sub>Jeanne Espíndola</sub>](https://github.com/Jeanne3229)
| :---: | :---: | :---: | :---:

---

# Licença

The [MIT License](LICENSE) (MIT)

Copyright :copyright: 2026 - BemStock
