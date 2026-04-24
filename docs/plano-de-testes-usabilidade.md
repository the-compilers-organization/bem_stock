# 📘 Plano de Testes de Usabilidade — BemStock

---

## 1. 🎯 Objetivo

Garantir que o sistema BemStock seja fácil de usar, compreensível e funcional para os usuários, permitindo que realizem todas as tarefas sem dificuldade.

---

## 2. 👥 Público-alvo

- Iniciantes em programação
- Alunos de graduação
- Usuários administrativos
- Usuários de estoque

---

## 3. 🛠️ Ambiente de Teste

Antes de iniciar os testes:

- Sistema em execução (`main.py`)
- Banco de dados criado (`bemstock.db`)
- Usuário administrador disponível:
  - Email: admin@bemstock.com
  - Senha: 123456

---

## 4. 🧠 Critérios de Usabilidade

Durante os testes, observar:

- Interface clara e organizada
- Botões visíveis e funcionais
- Mensagens de erro compreensíveis
- Navegação entre telas funcionando
- Tabelas alinhadas
- Facilidade de uso sem ajuda

---

# 🚀 5. Casos de Teste

---

# 🔐 5.1 Tela de Login

## CT001 — Acessar sistema

**Passos:**
1. Executar o sistema

**Resultado esperado:**
- Tela de login deve aparecer corretamente

---

## CT002 — Login válido

**Passos:**
1. Digitar email e senha corretos
2. Clicar em Entrar

**Resultado esperado:**
- Sistema deve abrir o Dashboard

---

## CT003 — Campos vazios

**Passos:**
1. Clicar em Entrar sem preencher os campos

**Resultado esperado:**
- Sistema deve mostrar mensagens de erro

---

## CT004 — Email inválido

**Passos:**
1. Digitar email inválido
2. Tentar login

**Resultado esperado:**
- Sistema deve informar erro

---

## CT005 — Mostrar senha

**Passos:**
1. Marcar e desmarcar checkbox

**Resultado esperado:**
- Senha deve aparecer e desaparecer

---

# 🏠 5.2 Dashboard

## CT006 — Visualizar dashboard

**Passos:**
1. Fazer login

**Resultado esperado:**
- Cards devem aparecer organizados

---

## CT007 — Navegação

**Passos:**
1. Clicar em Produtos
2. Clicar em Movimentações

**Resultado esperado:**
- Telas devem abrir corretamente

---

# 📦 5.3 Produtos

## CT008 — Listar produtos

**Passos:**
1. Acessar tela de produtos

**Resultado esperado:**
- Lista deve aparecer corretamente

---

## CT009 — Buscar produto

**Passos:**
1. Digitar nome no campo de busca

**Resultado esperado:**
- Lista deve filtrar

---

## CT010 — Criar produto

**Passos:**
1. Clicar em Novo Produto
2. Preencher dados
3. Salvar

**Resultado esperado:**
- Produto deve ser criado

---

## CT011 — Campos obrigatórios

**Passos:**
1. Tentar salvar sem preencher campos

**Resultado esperado:**
- Sistema deve mostrar erro

---

## CT012 — Editar produto

**Passos:**
1. Editar um produto
2. Salvar

**Resultado esperado:**
- Dados devem ser atualizados

---

## CT013 — Excluir produto

**Passos:**
1. Clicar em excluir

**Resultado esperado:**
- Sistema deve pedir confirmação

---

## CT014 — Verificar tabela

**Passos:**
1. Observar tabela

**Resultado esperado:**
- Colunas alinhadas
- Nenhum conteúdo cortado

---

# 🔄 5.4 Movimentações

## CT015 — Registrar entrada

**Passos:**
1. Criar movimentação tipo entrada

**Resultado esperado:**
- Estoque deve aumentar

---

## CT016 — Registrar saída

**Passos:**
1. Criar movimentação tipo saída

**Resultado esperado:**
- Estoque deve diminuir

---

## CT017 — Saída inválida

**Passos:**
1. Tentar saída maior que estoque

**Resultado esperado:**
- Sistema deve bloquear

---

## CT018 — Quantidade inválida

**Passos:**
1. Inserir valor inválido

**Resultado esperado:**
- Sistema deve mostrar erro

---

# 🔄 5.5.1 Edição de Movimentação

## CT019 — Editar movimentação

**Passos:**
1. Clicar em editar
2. Alterar dados
3. Salvar

**Resultado esperado:**
- Dados atualizados corretamente

---

## CT020 — Editar quantidade

**Passos:**
1. Alterar quantidade
2. Salvar

**Resultado esperado:**
- Estoque deve ser ajustado corretamente

---

## CT021 — Editar com erro

**Passos:**
1. Inserir valor inválido
2. Salvar

**Resultado esperado:**
- Sistema deve bloquear

---

## CT022 — Cancelar edição

**Passos:**
1. Editar movimentação
2. Cancelar

**Resultado esperado:**
- Nenhuma alteração deve ocorrer

---

# 🗑️ 5.5.2 Exclusão de Movimentação

## CT023 — Excluir movimentação

**Passos:**
1. Clicar em excluir
2. Confirmar

**Resultado esperado:**
- Movimentação deve ser removida

---

## CT024 — Verificar estoque

**Passos:**
1. Excluir movimentação
2. Verificar produto

**Resultado esperado:**
- Estoque deve ser corrigido

---

## CT025 — Cancelar exclusão

**Passos:**
1. Clicar em excluir
2. Cancelar

**Resultado esperado:**
- Movimentação não deve ser removida

---

# 📜 5.6 Histórico

## CT026 — Visualizar histórico

**Passos:**
1. Abrir histórico

**Resultado esperado:**
- Lista deve aparecer

---

## CT027 — Filtrar

**Passos:**
1. Aplicar filtros

**Resultado esperado:**
- Filtros devem funcionar

---

## CT028 — Limpar filtros

**Passos:**
1. Limpar filtros

**Resultado esperado:**
- Lista deve voltar ao normal

---

# 👤 5.7 Usuários

## CT029 — Criar usuário

**Passos:**
1. Cadastrar usuário

**Resultado esperado:**
- Usuário criado

---

## CT030 — Email duplicado

**Passos:**
1. Tentar cadastrar email repetido

**Resultado esperado:**
- Sistema deve bloquear

---

## CT031 — Editar usuário

**Passos:**
1. Editar usuário

**Resultado esperado:**
- Dados atualizados

---

## CT032 — Excluir usuário

**Passos:**
1. Excluir usuário

**Resultado esperado:**
- Usuário removido

---

# 🧭 5.8 Navegação

## CT033 — Alternar telas

**Passos:**
1. Navegar entre telas

**Resultado esperado:**
- Sistema não deve travar

---

## CT034 — Voltar ao dashboard

**Passos:**
1. Clicar em dashboard

**Resultado esperado:**
- Tela deve abrir corretamente

---

# 📱 5.9 Layout

## CT035 — Verificar alinhamento

**Passos:**
1. Observar interface

**Resultado esperado:**
- Elementos alinhados

---

## CT036 — Verificar textos

**Passos:**
1. Observar textos

**Resultado esperado:**
- Nenhum texto cortado

---

## CT037 — Verificar botões

**Passos:**
1. Observar botões

**Resultado esperado:**
- Botões claros e visíveis

---

# 🧪 6. Registro dos Testes

| Teste | Resultado | Observação |
|------|--------|-----------|
| CT001 | OK | |
| CT002 | OK | |
| CT003 | ERRO | |

---

# ✅ 7. Critérios de Aprovação

- Sistema fácil de usar
- Sem erros críticos
- Navegação funcionando
- Layout organizado

---

# ❌ 8. Critérios de Reprovação

- Sistema difícil de usar
- Erros frequentes
- Layout quebrado
- Falhas de navegação

---

# 🎯 9. Conclusão

Este plano permite validar completamente a usabilidade do sistema BemStock.