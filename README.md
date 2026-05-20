<h1>BemStock</h1>

<p align="center">
  <img src="http://img.shields.io/static/v1?label=Python&message=3.x&color=3776AB&style=for-the-badge&logo=python"/>
  <img src="http://img.shields.io/static/v1?label=CustomTkinter&message=GUI&color=1E90FF&style=for-the-badge"/>
  <img src="http://img.shields.io/static/v1?label=SQLite&message=Database&color=003B57&style=for-the-badge&logo=sqlite"/>
  <img src="http://img.shields.io/static/v1?label=Git&message=2.x&color=f05032&style=for-the-badge&logo=git"/>
  <img src="http://img.shields.io/static/v1?label=GitHub&message=2026&color=181717&style=for-the-badge&logo=github"/>
  <img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=yellow&style=for-the-badge"/>
  <img src="http://img.shields.io/static/v1?label=License&message=MIT&color=green&style=for-the-badge"/>
</p>

> Status do Projeto: :heavy_check_mark: (concluído) | :warning: (em desenvolvimento) | :x: (não iniciada)

---

# Tópicos

:small_blue_diamond: [Contexto](#contexto-information_source) 

:small_blue_diamond: [Problema](#problema-writing_hand)  

:small_blue_diamond: [Público-Alvo](#público-alvo-busts_in_silhouette)  

:small_blue_diamond: [Objetivo](#objetivo-dart)  

:small_blue_diamond: [Funcionalidades](#funcionalidades-video_game)  

:small_blue_diamond: [Protótipo do Sistema](#protótipo-do-sistema-art) 

:small_blue_diamond: [Arquitetura](#arquitetura-computer)  

:small_blue_diamond: [Estrutura do Projeto](#estrutura-do-projeto-file_folder)  

:small_blue_diamond: [Pré-requisitos](#pré-requisitos-warning)

:small_blue_diamond: [Instalação](#instalação-rocket)  

:small_blue_diamond: [Como Rodar o Projeto](#como-rodar-o-projeto-computer)

:small_blue_diamond: [Primeiro Acesso](#primeiro-acesso-closed_lock_with_key) 

:small_blue_diamond: [Tecnologias Utilizadas](#tecnologias-utilizadas-wrench)  

:small_blue_diamond: [Documentação](#documentação-book)  

:small_blue_diamond: [Desenvolvedores](#desenvolvedorescontribuintes-octocat)  

:small_blue_diamond: [Licença](#licença)

---

# Contexto :information_source:

<p align="justify">
O projeto <strong>BemStock</strong> é um sistema de gerenciamento de estoque desenvolvido para auxiliar a instituição <strong>Lar Bem</strong>, localizada no Recife, no controle de alimentos, produtos de higiene e produtos de limpeza utilizados no dia a dia da instituição.
</p>

<p align="justify">
O sistema será executado em um computador da administração da instituição e permitirá registrar entradas e saídas de produtos, acompanhar a quantidade disponível em estoque e controlar a validade dos itens armazenados.
</p>

---

# Problema :writing_hand:

<p align="justify">
Instituições de acolhimento utilizam diversos itens essenciais para seu funcionamento diário, como alimentos, produtos de higiene e produtos de limpeza. Muitas vezes, o controle desses materiais é realizado de forma manual ou pouco estruturada, o que pode dificultar o acompanhamento do estoque e a identificação de itens em falta ou próximos do vencimento.
</p>

<p align="justify">
O BemStock busca resolver esse problema oferecendo uma ferramenta simples e organizada para registrar movimentações de estoque e acompanhar os recursos disponíveis na instituição.
</p>

---

# Público-Alvo :busts_in_silhouette:

- Funcionários administrativos da instituição
- Responsáveis pelo controle de estoque
- Coordenação da instituição Lar Bem

---

# Objetivo :dart:

<p align="justify">
O objetivo do sistema BemStock é organizar e controlar o estoque de alimentos, produtos de higiene e produtos de limpeza utilizados pela instituição Lar Bem.
</p>

<p align="justify">
O sistema permitirá registrar entradas e saídas de produtos, acompanhar quantidades disponíveis, controlar validade dos itens e manter histórico de movimentações, contribuindo para uma gestão mais eficiente dos recursos da instituição.
</p>

---

# Funcionalidades :video_game:

### Funcionalidades principais (MVP)

- Login de usuário  
- Primeiro acesso obrigatório (configuração de segurança)  
- Cadastro de usuários (admin)  
- Cadastro de produtos  
- Edição e exclusão de produtos  
- Registro de entrada de produtos  
- Registro de saída de produtos  
- Consulta de estoque (calculado por movimentações)  
- Controle de estoque mínimo  
- Controle de validade  
- Histórico de movimentações com filtros
- Paginação de dados  

---

# Protótipo do Sistema :art:

O design das telas do sistema BemStock foi desenvolvido com foco em **usabilidade, clareza e padronização visual**, baseado na identidade da instituição **Lar Bem**.

📄 A documentação completa da interface pode ser acessada em:

🔗 [Interfaces do Sistema](docs/interfaces-do-sistema.md)


🎨 O protótipo visual pode ser acessado no link abaixo:

🔗 [Acessar protótipo do BemStock no Figma](https://drawn-award-18708393.figma.site/)

---

# Arquitetura :computer:

O sistema BemStock utiliza uma arquitetura organizada em camadas inspirada no padrão **MVC**, composta por:

- **View** → Interface gráfica do sistema
- **Controller** → Controle das operações do sistema
- **Model** → Representação das entidades e regras de negócio
- **Database** → Comunicação com o banco de dados
- **Utils** → Funções auxiliares

Fluxo simplificado da aplicação:

```text
Usuário
  ↓
Interface (CustomTkinter)
  ↓
Controller
  ↓
Model
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

# Pré-requisitos :warning:

Antes de clonar o repositório e executar o projeto, é necessário ter instalado:

**1. Python 3.x:**
  - Caso não tenha python, instale: https://www.python.org/downloads/

**2. Git:**
  - Caso não tenha git, instale: http://git-scm.com/install/

**3. VS Code (ou outra IDE):**
  - Caso não tenha vscode, instale: https://code.visualstudio.com/download

---

# Instalação :rocket:

### 1️⃣ Clonar o repositório

git clone https://github.com/the-compilers-organization/bem_stock.git

---

### 2️⃣ Entrar na pasta do projeto

cd bem_stock

---

### 3️⃣ Criar ambiente virtual

python -m venv venv

---

### 4️⃣ Ativar ambiente virtual

**Windows:**
venv\Scripts\activate


**Linux/Mac:**
source venv/bin/activate

---

### 5️⃣ Instalar dependências

pip install -r requirements.txt

---


# Como Rodar o Projeto :computer:

Com o ambiente virtual ativado, execute:

python src/main.py

Após executar o comando, a interface gráfica do sistema será aberta automaticamente.

---

# Primeiro Acesso :closed_lock_with_key:

Ao iniciar o sistema pela primeira vez, será criado automaticamente um usuário administrador:

- **E-mail:** `teste@bemstock.com`  
- **Senha:** `123456`  

### Regra obrigatória ⚠️

No primeiro login:

- o sistema **não libera acesso ao dashboard**
- o usuário deve obrigatoriamente:
  - alterar o e-mail  
  - alterar a senha  

Somente após isso o sistema será liberado.

---

# Tecnologias Utilizadas :wrench:

- **Python**
- **CustomTkinter**
- **SQLite**
- **Pyinstaller**
- **Inno Setup Compiler**
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
- [Atores e Casos de Uso](docs/casos_de_uso_bem_stock.png)
- [Plano de Testes de Usabilidade](docs/plano-de-testes-usabilidade.md)
- [Interfaces do Sistema](docs/interfaces-do-sistema.md)

---

# Desenvolvedores/Contribuintes :octocat:

Time responsável pelo desenvolvimento do projeto

| [<img src="https://avatars.githubusercontent.com/u/222337719?v=4" width=115><br><sub>Allan Lucas</sub>](https://github.com/allagez) | [<img src="https://avatars.githubusercontent.com/u/229312657?v=4" width=115><br><sub>Breno Bezerra</sub>](https://github.com/brenobezerra2014-cyber) | [<img src="https://avatars.githubusercontent.com/u/130801505?v=4" width=115><br><sub>Francis Lauriano</sub>](https://github.com/FrancisLauriano) | [<img src="https://avatars.githubusercontent.com/u/234993270?v=4" width=115><br><sub>Jeanne Espíndola</sub>](https://github.com/Jeanne3229)
| :---: | :---: | :---: | :---:

---

# Licença

The [MIT License](LICENSE) (MIT)

Copyright :copyright: 2026 - BemStock