# 🖥️ Interfaces do Sistema – BemStock

---

## 1. 📌 Visão Geral

Este documento descreve as interfaces do sistema **BemStock**, incluindo:

* Estrutura das telas
* Componentes visuais
* Fluxo de navegação
* Padrão visual (cores e tipografia)

O objetivo é garantir **consistência visual, usabilidade e padronização** da interface do sistema.

---

## 2. 🎨 Identidade Visual

A identidade visual do sistema foi construída com base nas cores da instituição **Lar Bem**, utilizando tons de roxo e lilás.

### 🎯 Características

* Interface clara (light mode)
* Layout baseado em cards
* Espaçamento equilibrado
* Tipografia legível
* Destaque para ações principais

---

## 3. 🎨 Paleta de Cores

### 🎯 Cores Principais

| Categoria  | Nome         | Cor | Código    |
| ---------- | ------------ | --- | --------- |
| Roxo       | Principal    | 🟪  | `#8B5CF6` |
| Roxo       | Hover        | 🟪  | `#7C3AED` |
| Roxo       | Claro        | 🟪  | `#A78BFA` |
| Fundo      | Rosa Fundo   | 🟫  | `#F3E8FF` |
| Fundo      | Rosa Claro   | 🟫  | `#FAF5FF` |
| Bordas     | Lilás        | 🟪  | `#E9D5FF` |
| Sucesso    | Verde        | 🟩  | `#10B981` |
| Erro       | Vermelho     | 🟥  | `#EF4444` |
| Alerta     | Laranja      | 🟧  | `#F59E0B` |
| Informação | Azul         | 🟦  | `#3B82F6` |
| Neutro     | Branco       | ⬜   | `#FFFFFF` |
| Neutro     | Cinza Claro  | ⬜   | `#F3F4F6` |
| Neutro     | Cinza Médio  | ⬛   | `#6B7280` |
| Neutro     | Cinza Escuro | ⬛   | `#1F2937` |

---

### 🧩 Aplicação das Cores

| Elemento                  | Cor Utilizada  | Código    |
| ------------------------- | -------------- | --------- |
| Fundo principal da janela | Rosa Fundo     | `#F3E8FF` |
| Cards / Frames            | Branco         | `#FFFFFF` |
| Botões principais         | Roxo Principal | `#8B5CF6` |
| Hover de botões           | Roxo Escuro    | `#7C3AED` |
| Textos principais         | Cinza Escuro   | `#1F2937` |
| Textos secundários        | Cinza Médio    | `#6B7280` |
| Inputs                    | Cinza Claro    | `#F3F4F6` |
| Bordas                    | Lilás          | `#E9D5FF` |

---

## 4. 🔤 Tipografia

### 🎯 Fonte Principal

* **Segoe UI**

### 🧩 Hierarquia Tipográfica

| Tipo          | Tamanho | Peso    | Uso                |
| ------------- | ------- | ------- | ------------------ |
| Título grande | 32px    | Negrito | Títulos principais |
| Título        | 24px    | Negrito | Seções             |
| Subtítulo     | 18px    | Negrito | Cabeçalhos         |
| Texto grande  | 16px    | Normal  | Destaques          |
| Texto padrão  | 14px    | Normal  | Conteúdo           |
| Texto pequeno | 12px    | Normal  | Legendas           |
| Botão         | 14px    | Negrito | Botões             |
| Label         | 13px    | Negrito | Formulários        |

---

## 5. 🧭 Estrutura de Navegação

### 📌 Fluxo Geral

```text
Login → Dashboard → Produtos
                  → Movimentações
                  → Usuários (admin)
```

### 📌 Regras de Navegação

* Sidebar fixa em todas as telas (exceto login)
* Navegação por menu lateral
* Retorno sempre disponível
* Acesso a usuários restrito ao perfil admin

---

## 6. 🖥️ Telas do Sistema

---

### 🔐 6.1 Login

**Objetivo:** Autenticar o usuário no sistema

**Elementos:**

* Campo e-mail
* Campo senha
* Checkbox “mostrar senha”
* Botão “entrar”

**Características:**

* Layout centralizado
* Interface simples e direta

---

### 📊 6.2 Dashboard

**Objetivo:** Exibir visão geral do sistema

**Elementos:**

* Cards informativos
* Botões de atalho
* Menu lateral

---

### 📦 6.3 Produtos

**Objetivo:** Gerenciar produtos do estoque

**Elementos:**

* Campo de busca
* Filtro por categoria
* Tabela de produtos
* Botão “novo produto”

---

### 📝 6.4 Cadastro de Produto

**Objetivo:** Criar ou editar produtos

**Elementos:**

* Campos de formulário
* Botões salvar/cancelar

---

### 🔄 6.5 Movimentações

**Objetivo:** Visualizar histórico de movimentações

**Elementos:**

* Filtros
* Tabela de movimentações

---

### ➕ 6.6 Cadastro de Movimentação

**Objetivo:** Registrar entrada e saída de produtos

**Elementos:**

* Produto
* Tipo
* Quantidade
* Data
* Observações

---

### 👥 6.7 Usuários

**Objetivo:** Gerenciar usuários do sistema

**Acesso:** Apenas administradores

---

### 🧾 6.8 Cadastro de Usuário

**Objetivo:** Criar e editar usuários

---

## 7. 🧩 Componentes de Interface

### Botões

* Primário (ação principal)
* Secundário (cancelar)
* Perigo (excluir)

### Inputs

* Campo de texto
* Combobox
* Checkbox

### Tabelas

* Cabeçalho fixo
* Scroll vertical e horizontal
* Colunas alinhadas

---

## 8. 🎯 Experiência do Usuário (UX)

O sistema foi projetado para:

* ✔ Facilidade de uso
* ✔ Navegação intuitiva
* ✔ Redução de erros
* ✔ Fluxo simples e direto

---

## 9. 📱 Responsividade

* Layout adaptável
* Scroll automático quando necessário
* Interface centralizada

---

## 10. ✅ Considerações Finais

* Interface padronizada
* Visual consistente
* Foco na usabilidade
* Adequado ao ambiente administrativo

---
