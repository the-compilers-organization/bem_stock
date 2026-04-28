# 📘 Plano de Testes de Usabilidade — BemStock

---

## 1. 🎯 Objetivo

Garantir que o sistema BemStock seja fácil de usar, compreensível, organizado e funcional, permitindo que usuários realizem as tarefas principais sem dificuldade.

---

## 2. 👥 Público-alvo

- Iniciantes em programação
- Alunos de graduação
- Usuários administrativos
- Usuários de estoque

---

## 3. 🛠️ Ambiente de Teste

Antes de iniciar os testes:

1. Abrir o projeto no VS Code.
2. Verificar se o arquivo `main.py` existe na pasta `src`.
3. Executar o sistema com o ambiente virtual ativado: execute o arqrivo `main.py`.
4. Confirmar que o banco `bemstock.db` foi criado.
5. Usar o usuário administrador padrão:

- Email: `admin@bemstock.com`
- Senha: `123456`

---

## 4. 🧠 O que observar durante os testes

Durante cada teste, verificar:

- A tela está clara?
- Os botões são fáceis de encontrar?
- As mensagens são compreensíveis?
- A navegação funciona corretamente?
- As tabelas estão alinhadas?
- Alguma informação está cortada?
- O sistema evita erros do usuário?
- O estoque permanece correto após movimentações?

---

# 🚀 5. Casos de Teste

---

# 🔐 5.1 Tela de Login

---

## CT001 — Abrir o sistema

**Passos:**
1. Abrir o projeto.
2. Executar o arquivo `main.py`.
3. Aguardar a tela inicial carregar.

**Resultado esperado:**
- A tela de login deve aparecer.
- Os campos de e-mail e senha devem estar visíveis.
- O botão “Entrar” deve estar visível.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Chegou ao resultado esperado, a tela é intuitiva e objetiva.
_________________________________________

---

## CT002 — Login com dados válidos

**Passos:**
1. Clicar no campo de e-mail.
2. Digitar `admin@bemstock.com`.
3. Clicar no campo de senha.
4. Digitar `123456`.
5. Clicar no botão “Entrar”.

**Resultado esperado:**
- O sistema deve abrir o Dashboard.

**Resultado obtido:**  
( ) OK   (X) ERRO  

**Observações:**  

O sistema retorna a mensagem "Usuário não encontrado".
_________________________________________

---

## CT003 — Login com campos vazios

**Passos:**
1. Abrir a tela de login.
2. Não preencher nenhum campo.
3. Clicar em “Entrar”.

**Resultado esperado:**
- O sistema deve exibir mensagem informando que os campos são obrigatórios.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retorna a mensagem "Por favor, digite seu e-mail", porém não especifica que os dois campos estão sem dígitos.
_________________________________________

---

## CT004 — Login com e-mail inválido

**Passos:**
1. Digitar `admin`.
2. Digitar uma senha qualquer.
3. Clicar em “Entrar”.

**Resultado esperado:**
- O sistema deve informar que o e-mail é inválido.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:** 

Chegou ao resultado, o sistema retornou a mensagem "E-mail inválido".
_________________________________________

---

## CT005 — Login com senha incorreta

**Passos:**
1. Digitar `admin@bemstock.com`.
2. Digitar `senhaerrada`.
3. Clicar em “Entrar”.

**Resultado esperado:**
- O sistema deve bloquear o acesso.
- Deve exibir mensagem clara de erro.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Assim como o resultado esperado, o sistema bloqueou o acesso e retornou o erro, porém retornou a mensagem "Usuário não encontrado, não especificando que o erro foi a senha ou o e-mail"
_________________________________________

---

## CT006 — Mostrar e ocultar senha

**Passos:**
1. Digitar uma senha no campo senha.
2. Marcar a opção “Mostrar senha”.
3. Desmarcar a opção “Mostrar senha”.

**Resultado esperado:**
- A senha deve aparecer quando marcada.
- A senha deve ficar oculta quando desmarcada.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema respondeu como esperado, facilitando o usuário a visualizar a senha que está sendo inserida.
_________________________________________

---

# 🏠 5.2 Dashboard

---

## CT007 — Visualizar Dashboard

**Passos:**
1. Fazer login com sucesso.
2. Observar a tela inicial do sistema.

**Resultado esperado:**
- O Dashboard deve aparecer.
- Os cards devem estar organizados.
- O menu lateral deve estar visível.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Opções estão visíveis e claras. 
_________________________________________

---

## CT008 — Acessar Produtos pelo Dashboard

**Passos:**
1. No Dashboard, localizar o botão ou menu “Produtos”.
2. Clicar em “Produtos”.

**Resultado esperado:**
- A tela de Lista de Produtos deve abrir.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Direcionado para a tela de lista de produtos com sucesso, no momento, sem nenhum produto registrado.
_________________________________________

---

## CT009 — Acessar Movimentações pelo Dashboard

**Passos:**
1. No Dashboard, localizar “Movimentações”.
2. Clicar na opção.

**Resultado esperado:**
- A tela de Histórico de Movimentações deve abrir.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Direcionado para a tela de histórico de movimentações com sucesso, no momento, sem nenhum registro.
_________________________________________

---

## CT010 — Verificar acesso ao menu Usuários como admin

**Passos:**
1. Entrar como administrador.
2. Observar o menu lateral.

**Resultado esperado:**
- A opção “Usuários” deve aparecer para o administrador.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

A opção disponível para admins está visível na lateral junto com as demais opções do estoque.
_________________________________________

---

## CT011 — Verificar restrição do menu Usuários para perfil estoque

**Passos:**
1. Entrar com usuário de perfil `estoque`.
2. Observar o menu lateral.

**Resultado esperado:**
- A opção “Usuários” não deve aparecer para o perfil estoque.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O usuário possui apenas três opções no menu lateral.
_________________________________________

---

# 📦 5.3 Lista de Produtos

---

## CT012 — Visualizar lista de produtos

**Passos:**
1. Acessar a tela “Produtos”.
2. Observar a lista exibida.

**Resultado esperado:**
- A lista deve aparecer organizada.
- Os cabeçalhos devem estar visíveis.
- Nenhuma coluna deve estar cortada.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Foi adicionado um produto na lista para poder visualizar as colunas e cabeçalhos.
_________________________________________

---

## CT013 — Verificar alinhamento da tabela de produtos

**Passos:**
1. Observar os títulos das colunas.
2. Comparar os títulos com os conteúdos das células.

**Resultado esperado:**
- Os cabeçalhos devem estar alinhados com os conteúdos.
- As colunas Status, Validade e Ações não devem estar desalinhadas.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:** 

As colunas e cabeçalhos estão alinhados, com os conteúdos relacionados corretos.
_________________________________________

---

## CT014 — Verificar coluna Ações

**Passos:**
1. Observar a coluna “Ações”.
2. Verificar os botões de editar e excluir.

**Resultado esperado:**
- Os ícones devem aparecer completos.
- Nenhum botão deve estar cortado.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:** 

Os botões estão intuitivos, porém a opção "Editar" parece pouco visível.
_________________________________________

---

## CT015 — Buscar produto existente

**Passos:**
1. Clicar no campo de busca.
2. Digitar o nome de um produto cadastrado.

**Resultado esperado:**
- A lista deve mostrar apenas produtos correspondentes à busca.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Produto usado como exemplo foi exibido.
_________________________________________

---

## CT016 — Buscar produto inexistente

**Passos:**
1. Clicar no campo de busca.
2. Digitar um nome que não existe.

**Resultado esperado:**
- A lista deve ficar vazia ou exibir uma mensagem clara.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Após clicar em "Filtrar" o sistema retorna a mensagem "Nenhum produto encontrado" na lista de produtos.
_________________________________________

---

## CT017 — Filtrar produto por categoria

**Passos:**
1. Abrir a tela de produtos.
2. Selecionar uma categoria no filtro.

**Resultado esperado:**
- Apenas produtos da categoria escolhida devem aparecer.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Chegou ao resultado esperado, exibindo os respectivos produtos de cada categoria e retornando a mensagem "Nenhum produto encontrado" nas categorias que não possuem produtos.
_________________________________________

---

## CT018 — Limpar filtros de produtos

**Passos:**
1. Aplicar uma busca ou filtro.
2. Clicar em limpar filtros ou apagar a busca.

**Resultado esperado:**
- Todos os produtos devem voltar a aparecer.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Os produtos cadastrados voltaram a aparecer com sucesso.
_________________________________________

---

## CT019 — Testar rolagem vertical da lista de produtos

**Passos:**
1. Cadastrar vários produtos.
2. Acessar a lista.
3. Usar a rolagem vertical.

**Resultado esperado:**
- A rolagem deve funcionar.
- O conteúdo não deve sobrepor outros elementos.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Exibição da lista continua correta, com células e conteúdos alinhados.
_________________________________________

---

## CT020 — Testar rolagem horizontal da lista de produtos

**Passos:**
1. Acessar a lista de produtos.
2. Usar a rolagem horizontal.

**Resultado esperado:**
- Cabeçalho e conteúdo devem rolar juntos.
- As colunas devem continuar alinhadas.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Exibição da lista continua correta, com células e conteúdos alinhados, porém a rolagem horizontal só pôde ser utilizada com a janela reduzida.
_________________________________________

---

# 📝 5.4 Cadastro e Edição de Produto

---

## CT021 — Abrir cadastro de produto

**Passos:**
1. Acessar a tela “Produtos”.
2. Clicar em “Novo Produto”.

**Resultado esperado:**
- O formulário de cadastro deve abrir.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:** 

Campos disponíveis na tela de criação de produtos são claras, indicando também quais dos campos são obrigatórios.
_________________________________________

---

## CT022 — Cadastrar produto válido

**Passos:**
1. Clicar em “Novo Produto”.
2. Preencher o nome.
3. Selecionar categoria.
4. Selecionar unidade de medida.
5. Informar estoque mínimo.
6. Preencher descrição, se necessário.
7. Clicar em “Salvar”.

**Resultado esperado:**
- Produto deve ser cadastrado.
- Sistema deve exibir mensagem de sucesso.
- Produto deve aparecer na lista.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O produto e todos os dados inseridos nos campos são exibidos na lista.
_________________________________________

---

## CT023 — Cadastrar produto sem nome

**Passos:**
1. Abrir cadastro de produto.
2. Deixar o nome vazio.
3. Preencher os demais campos.
4. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve informar que o nome é obrigatório.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retornou a mensagem "O nome é obrigatório" abaixo do campo "Nome", deixando claro onde foi o erro do usuário.
_________________________________________

---

## CT024 — Cadastrar produto sem categoria

**Passos:**
1. Abrir cadastro.
2. Preencher nome.
3. Não selecionar categoria.
4. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve informar que a categoria é obrigatória ou inválida.

**Resultado obtido:**  
( ) OK   (X) ERRO  

**Observações:**  

Não é possível cadastrar o produto sem categoria, visto que o sistema inicia como padrão a opção "Alimentos" no campo.
_________________________________________

---

## CT025 — Cadastrar produto com estoque mínimo negativo

**Passos:**
1. Abrir cadastro.
2. Preencher os campos.
3. Digitar `-5` no estoque mínimo.
4. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve impedir o cadastro.
- Deve informar que o estoque mínimo não pode ser negativo.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retorna a mensagem de erro "Informe um número maior ou igual a zero" abaixo do campo de "Estoque mínimo".
_________________________________________

---

## CT026 — Cadastrar produto com estoque mínimo em texto

**Passos:**
1. Abrir cadastro.
2. Digitar `abc` no estoque mínimo.
3. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve impedir.
- Deve informar que o campo deve ser numérico.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retorna a mensagem de erro "Informe um número inteiro válido" abaixo do campo de "Estoque Mínimo".
_________________________________________

---

## CT027 — Editar produto

**Passos:**
1. Acessar a lista de produtos.
2. Localizar um produto.
3. Clicar no botão editar.
4. Alterar algum campo.
5. Clicar em “Salvar”.

**Resultado esperado:**
- Produto deve ser atualizado.
- Alteração deve aparecer na lista.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Todas as alterações feitas foram realizadas com sucesso.
_________________________________________

---

## CT028 — Cancelar edição de produto

**Passos:**
1. Abrir edição de um produto.
2. Alterar algum campo.
3. Clicar em “Cancelar” ou “Voltar”.

**Resultado esperado:**
- Alterações não devem ser salvas.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Nenhuma das alterações foram registradas na lista.
_________________________________________

---

## CT029 — Excluir produto sem movimentação

**Passos:**
1. Localizar um produto sem histórico de movimentação.
2. Clicar em excluir.
3. Confirmar exclusão.

**Resultado esperado:**
- Produto deve ser removido da lista.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:** 

Foi exibida uma janela para confirmar a exclusão do produto. Ao confirmar, o produto foi excluído com sucesso.
_________________________________________

---

## CT030 — Tentar excluir produto com movimentação

**Passos:**
1. Localizar produto que possui entrada ou saída registrada.
2. Clicar em excluir.

**Resultado esperado:**
- Sistema deve bloquear a exclusão.
- Deve informar que o produto possui histórico de movimentação.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema não autorizou a exclusão após eu confirmar a opção, exibindo uma mensagem informando que o produto possui movimentação.
_________________________________________

---

# 🔄 5.5 Cadastro de Movimentação

---

## CT031 — Abrir cadastro de movimentação

**Passos:**
1. Acessar “Movimentações”.
2. Clicar em “Nova Movimentação”.

**Resultado esperado:**
- O formulário de movimentação deve abrir.
- Campos devem estar visíveis e organizados.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Todos os campos disponíveis estão claros e objetivos, sinalizando quais são obrigatórios e quais são opcionais.
_________________________________________

---

## CT032 — Registrar entrada válida

**Passos:**
1. Abrir nova movimentação.
2. Selecionar tipo “Entrada”.
3. Selecionar um produto.
4. Informar quantidade válida.
5. Informar fornecedor, se necessário.
6. Informar lote, se necessário.
7. Selecionar validade, se necessário.
8. Clicar em “Salvar”.

**Resultado esperado:**
- Movimentação deve ser registrada.
- Estoque do produto deve aumentar.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Todos os dados registrados nos campos foram exibidos logo após o salvamento.
_________________________________________

---

## CT033 — Registrar saída válida

**Passos:**
1. Abrir nova movimentação.
2. Selecionar tipo “Saída”.
3. Selecionar produto.
4. Informar quantidade válida.
5. Selecionar destino.
6. Clicar em “Salvar”.

**Resultado esperado:**
- Movimentação deve ser registrada.
- Estoque do produto deve diminuir.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Tanto a movimentação foi registrada como o estoque do produto diminuiu na lista de produtos.
_________________________________________

---

## CT034 — Registrar saída maior que estoque

**Passos:**
1. Selecionar tipo “Saída”.
2. Selecionar produto com pouco estoque.
3. Informar quantidade maior que o estoque disponível.
4. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve bloquear a saída.
- Deve informar estoque insuficiente.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema impediu a saída do produto.
_________________________________________

---

## CT035 — Movimentação sem produto

**Passos:**
1. Abrir nova movimentação.
2. Selecionar tipo.
3. Não selecionar produto.
4. Informar quantidade.
5. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve informar que o produto é obrigatório.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema exibiu uma mensagem "Selecione um produto válido" abaixo do campo "Produto".
_________________________________________

---

## CT036 — Movimentação sem tipo

**Passos:**
1. Abrir nova movimentação.
2. Não selecionar tipo.
3. Selecionar produto.
4. Informar quantidade.
5. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve informar que o tipo é obrigatório.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema exibe a imagem "Selecione o tipo de movimentação" abaixo do campo "Tipo de movimentação".
_________________________________________

---

## CT037 — Quantidade zero

**Passos:**
1. Abrir nova movimentação.
2. Preencher produto e tipo.
3. Digitar `0` na quantidade.
4. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve informar que a quantidade deve ser maior que zero.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retorna uma mensagem de erro abaixo do campo de "Quantidade", solicitando que o usuário insira um número inteiro maior que zero.
_________________________________________

---

## CT038 — Quantidade negativa

**Passos:**
1. Digitar `-3` no campo quantidade.
2. Tentar salvar.

**Resultado esperado:**
- Sistema deve bloquear.
- Deve exibir mensagem clara.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retorna uma mensagem de erro solicitando que o usuário insira um número inteiro maior que zero.
_________________________________________

---

## CT039 — Quantidade em texto

**Passos:**
1. Digitar `abc` no campo quantidade.
2. Tentar salvar.

**Resultado esperado:**
- Sistema deve informar que a quantidade deve ser numérica.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Abaixo do campo "Quantidade" o sistema retorna uma mensagem de erro solicitando que o usuário insira um número inteiro válido.
_________________________________________

---

## CT040 — Saída sem destino

**Passos:**
1. Selecionar tipo “Saída”.
2. Selecionar produto.
3. Informar quantidade.
4. Não selecionar destino.
5. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve informar que o destino é obrigatório para saída.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retorna uma mensagem próximo ao campo de "Destino" informando que o preenchimento é obrigatório.
_________________________________________

---

## CT041 — Selecionar data de validade

**Passos:**
1. Abrir nova movimentação de entrada.
2. Clicar no campo de validade.
3. Escolher uma data no calendário.

**Resultado esperado:**
- A data escolhida deve aparecer corretamente no campo.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

A data selecionada no calendário foi exibida corretamente no campo de validade.
_________________________________________

---

# ✏️ 5.6 Edição de Movimentação

---

## CT042 — Verificar botão editar movimentação

**Passos:**
1. Acessar o histórico de movimentações.
2. Observar a coluna “Ações”.

**Resultado esperado:**
- Deve existir botão de editar.
- O botão deve estar visível e alinhado.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Ambos os botões (Editar e Excluir) estão alinhados e visíveis.
_________________________________________

---

## CT043 — Abrir edição de movimentação

**Passos:**
1. Localizar uma movimentação.
2. Clicar no botão editar.

**Resultado esperado:**
- A tela de edição deve abrir.
- Os campos devem vir preenchidos com os dados da movimentação.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:** 

Todas as informações estão preenchidas em seus respectivos campos e disponíveis para edição.
_________________________________________

---

## CT044 — Editar quantidade de entrada

**Passos:**
1. Abrir edição de uma movimentação de entrada.
2. Alterar a quantidade.
3. Salvar.
4. Conferir o estoque do produto.

**Resultado esperado:**
- A movimentação deve ser atualizada.
- O estoque deve ser recalculado corretamente.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Resultado esperado foi obtido. O estoque foi atualizado e também considera as saídas feitas após a entrada.
_________________________________________

---

## CT045 — Editar quantidade de saída

**Passos:**
1. Abrir edição de uma movimentação de saída.
2. Alterar a quantidade.
3. Salvar.
4. Conferir o estoque.

**Resultado esperado:**
- A movimentação deve ser atualizada.
- O estoque deve ser ajustado corretamente.
- Se a quantidade for maior que o estoque disponível, o sistema deve bloquear.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

A movimentação foi atualizada e o estoque mudou respeitando a saída editada.
_________________________________________

---

## CT046 — Alterar tipo de Entrada para Saída

**Passos:**
1. Abrir edição de uma entrada.
2. Alterar tipo para “Saída”.
3. Salvar.

**Resultado esperado:**
- Sistema deve validar estoque.
- Caso não exista estoque suficiente, deve bloquear a edição.

**Resultado obtido:**  
( ) OK   (X) ERRO  

**Observações:**  

O sistema impede que o usuário modifique o tipo de movimentação.
_________________________________________

---

## CT047 — Alterar tipo de Saída para Entrada

**Passos:**
1. Abrir edição de uma saída.
2. Alterar tipo para “Entrada”.
3. Salvar.

**Resultado esperado:**
- O estoque deve ser recalculado corretamente.

**Resultado obtido:**  
( ) OK   (X) ERRO  

**Observações:**  

O sistema impede que o usuário modifique o tipo da movimentação.
_________________________________________

---

## CT048 — Alterar produto da movimentação

**Passos:**
1. Abrir edição de uma movimentação.
2. Alterar o produto.
3. Salvar.
4. Conferir estoque do produto antigo e do novo produto.

**Resultado esperado:**
- Estoque do produto antigo deve ser ajustado.
- Estoque do novo produto deve ser ajustado corretamente.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

As modificações foram exibidas corretamente na tela de Produtos e na tela de Movimentações, assim como o estoque de ambos os produtos.
_________________________________________

---

## CT049 — Editar movimentação com quantidade inválida

**Passos:**
1. Abrir edição.
2. Digitar quantidade zero, negativa ou texto.
3. Clicar em “Salvar”.

**Resultado esperado:**
- Sistema deve bloquear.
- Mensagem de erro deve ser clara.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retorna uma mensagem de erro abaixo do campo de "Quantidade" solicitando que o usuário insira um valor inteiro válido.
_________________________________________

---

## CT050 — Cancelar edição de movimentação

**Passos:**
1. Abrir edição.
2. Alterar algum campo.
3. Clicar em “Cancelar” ou “Voltar”.

**Resultado esperado:**
- Nenhuma alteração deve ser salva.
- Sistema deve retornar ao histórico.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:** 

Nenhuma movimentação foi modificada após clicar em "Voltar".
_________________________________________

---

# 🗑️ 5.7 Exclusão de Movimentação

---

## CT051 — Verificar botão excluir movimentação

**Passos:**
1. Acessar histórico de movimentações.
2. Observar coluna “Ações”.

**Resultado esperado:**
- Botão de excluir deve estar visível.
- O botão não deve estar cortado.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Botão visível ao scrollar horizontalmente.
_________________________________________

---

## CT052 — Cancelar exclusão de movimentação

**Passos:**
1. Clicar no botão excluir.
2. Quando aparecer a confirmação, clicar em cancelar.

**Resultado esperado:**
- A movimentação não deve ser removida.
- O estoque não deve ser alterado.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Não foi feita nenhuma exclusão ao recusar na janela de confirmação do sistema.
_________________________________________

---

## CT053 — Excluir movimentação de entrada

**Passos:**
1. Localizar uma movimentação de entrada.
2. Clicar em excluir.
3. Confirmar a exclusão.
4. Verificar o estoque do produto.

**Resultado esperado:**
- A movimentação deve ser removida.
- O estoque deve diminuir conforme a entrada excluída.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Movimentação excluída com sucesso e o respectivo estoque também foi modificado.
_________________________________________

---

## CT054 — Excluir movimentação de saída

**Passos:**
1. Localizar uma movimentação de saída.
2. Clicar em excluir.
3. Confirmar a exclusão.
4. Verificar o estoque do produto.

**Resultado esperado:**
- A movimentação deve ser removida.
- O estoque deve aumentar conforme a saída excluída.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

A movimentação de entrada foi excluída e seu respectivo estoque também foi modificado.
_________________________________________

---

## CT055 — Verificar histórico após exclusão

**Passos:**
1. Excluir uma movimentação.
2. Observar a lista de histórico.

**Resultado esperado:**
- A movimentação excluída não deve aparecer mais na lista.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

As movimentações foram excluídas e não são mais exibidas na tela de movimetações.
_________________________________________

---

# 📜 5.8 Histórico de Movimentações

---

## CT056 — Visualizar histórico

**Passos:**
1. Acessar a tela de movimentações.
2. Observar a lista.

**Resultado esperado:**
- As movimentações cadastradas devem aparecer.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Todas as movimentações estão exibidas corretamente e alinhadas.
_________________________________________

---

## CT057 — Filtrar por produto

**Passos:**
1. Selecionar um produto no filtro.
2. Aplicar o filtro.

**Resultado esperado:**
- Apenas movimentações daquele produto devem aparecer.

**Resultado obtido:**  
( ) OK   (X) ERRO  

**Observações:**  

O filtro Por Produto está solicitando ao usuário um ID.
_________________________________________

---

## CT058 — Filtrar por categoria

**Passos:**
1. Selecionar uma categoria.
2. Aplicar filtro.

**Resultado esperado:**
- Apenas movimentações da categoria selecionada devem aparecer.

(X) OK   ( ) ERRO  

**Observações:**  

Todas as categorias foram filtradas com sucesso.
_________________________________________

---

## CT059 — Filtrar por período válido

**Passos:**
1. Selecionar data inicial.
2. Selecionar data final.
3. Aplicar filtro.

**Resultado esperado:**
- Apenas movimentações dentro do período devem aparecer.

**Resultado obtido:**  
( ) OK   (X) ERRO  

**Observações:**  

Os registros de movimentações exibidos após a filtragem não respeitam as datas do intervalo.
_________________________________________

---

## CT060 — Filtrar com período inválido

**Passos:**
1. Selecionar data inicial maior que a data final.
2. Aplicar filtro.

**Resultado esperado:**
- Sistema deve informar que o período é inválido.

**Resultado obtido:**  
( ) OK   (X) ERRO  

**Observações:**  

O sistema exibe todos os registros já feitos, sem respeitar o intervalo além de não impedir a filtragem.
_________________________________________

---

## CT061 — Limpar filtros

**Passos:**
1. Aplicar filtros.
2. Clicar em “Limpar filtros”.

**Resultado esperado:**
- A lista deve voltar ao estado original.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Os campos de filtragem foram limpos e o histórico de movimentações está completo.
_________________________________________

---

# 👤 5.9 Usuários

---

## CT062 — Visualizar lista de usuários

**Passos:**
1. Entrar como administrador.
2. Acessar “Usuários”.

**Resultado esperado:**
- A lista de usuários deve aparecer.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Tanto usuários administradores e de estoque estão sendo exibidos na tela.
_________________________________________

---

## CT063 — Buscar usuário por nome

**Passos:**
1. Clicar no campo de busca.
2. Digitar nome de um usuário cadastrado.

**Resultado esperado:**
- A lista deve filtrar corretamente.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Usuários filtrados por nome apareceram corretamente, respeitando os campos de filtragem.
_________________________________________

---

## CT064 — Buscar usuário por e-mail

**Passos:**
1. Digitar parte do e-mail no campo de busca.

**Resultado esperado:**
- Usuários compatíveis devem aparecer.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Os usuários foram exibidos com os respectivos e-mails que foram inseridos no campo de filtros.
_________________________________________

---

## CT065 — Criar usuário válido

**Passos:**
1. Acessar “Usuários”.
2. Clicar em “Novo Usuário”.
3. Preencher nome.
4. Preencher e-mail válido.
5. Preencher senha.
6. Confirmar senha.
7. Selecionar perfil.
8. Clicar em “Salvar”.

**Resultado esperado:**
- Usuário deve ser cadastrado.
- Deve aparecer na lista.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Usuário criado com sucesso e sendo exibido na tela de usuários.
_________________________________________

---

## CT066 — Cadastrar usuário com e-mail inválido

**Passos:**
1. Abrir cadastro de usuário.
2. Digitar e-mail inválido.
3. Preencher os demais campos.
4. Salvar.

**Resultado esperado:**
- Sistema deve informar que o e-mail é inválido.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retornou uma mensagem de erro solicitando que o usuário insira o e-mail válido.
_________________________________________

---

## CT067 — Cadastrar usuário com e-mail duplicado

**Passos:**
1. Abrir cadastro de usuário.
2. Digitar e-mail já cadastrado.
3. Preencher os demais campos.
4. Salvar.

**Resultado esperado:**
- Sistema deve bloquear.
- Deve informar que já existe usuário com esse e-mail.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**

O sistema retorna uma janela com uma mensagem informando que já existe um usuário cadastrado com o e-mail.
_________________________________________

---

## CT068 — Cadastrar usuário com senhas diferentes

**Passos:**
1. Digitar uma senha.
2. Digitar confirmação diferente.
3. Clicar em salvar.

**Resultado esperado:**
- Sistema deve informar que as senhas não conferem.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O sistema retornou duas mensagens claras abaixo dos campos de senha identificando o erro do usuário.
_________________________________________

---

## CT069 — Editar usuário

**Passos:**
1. Localizar um usuário.
2. Clicar em editar.
3. Alterar nome ou perfil.
4. Salvar.

**Resultado esperado:**
- Dados devem ser atualizados.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

O novo nome do usuário foi exibido na lista, tanto os usuários administradores como estoque.
_________________________________________

---

## CT070 — Excluir usuário comum

**Passos:**
1. Localizar usuário comum.
2. Clicar em excluir.
3. Confirmar exclusão.

**Resultado esperado:**
- Usuário deve ser removido da lista.

**Resultado obtido:**  
(X) OK   ( ) ERRO  

**Observações:**  

Os usuários excluídos (tanto admin como estoque) não foram mais exibidos na lista.
_________________________________________

---

## CT071 — Tentar excluir administrador padrão

**Passos:**
1. Localizar o usuário `admin@bemstock.com`.
2. Clicar em excluir.

**Resultado esperado:**
- Sistema deve bloquear a exclusão do administrador padrão.

**Resultado obtido:**  
( ) OK   ( ) ERRO  

**Observações:**  
_________________________________________

---

# 🧭 5.10 Navegação Geral

---

## CT072 — Alternar entre telas

**Passos:**
1. Acessar Produtos.
2. Acessar Movimentações.
3. Acessar Usuários.
4. Voltar para Dashboard.

**Resultado esperado:**
- O sistema não deve travar.
- Todas as telas devem carregar corretamente.

**Resultado obtido:**  
( ) OK   ( ) ERRO  

**Observações:**  
_________________________________________

---

## CT073 — Usar botão Voltar ou Cancelar

**Passos:**
1. Abrir formulário de produto, usuário ou movimentação.
2. Clicar em “Voltar” ou “Cancelar”.

**Resultado esperado:**
- O sistema deve retornar para a tela anterior.
- Nenhuma informação deve ser salva sem confirmação.

**Resultado obtido:**  
( ) OK   ( ) ERRO  

**Observações:**  
_________________________________________

---

# 📱 5.11 Layout e Usabilidade Visual

---

## CT074 — Verificar textos cortados

**Passos:**
1. Observar todas as telas.
2. Verificar títulos, botões, colunas e cards.

**Resultado esperado:**
- Nenhum texto importante deve estar cortado.

**Resultado obtido:**  
( ) OK   ( ) ERRO  

**Observações:**  
_________________________________________

---

## CT075 — Verificar alinhamento das tabelas

**Passos:**
1. Observar tabela de produtos.
2. Observar tabela de movimentações.
3. Observar tabela de usuários.

**Resultado esperado:**
- Cabeçalhos devem estar alinhados com as células.

**Resultado obtido:**  
( ) OK   ( ) ERRO  

**Observações:**  
_________________________________________

---

## CT076 — Verificar clareza dos botões

**Passos:**
1. Observar botões principais.
2. Observar botões de editar e excluir.

**Resultado esperado:**
- O usuário deve entender a função de cada botão.

**Resultado obtido:**  
( ) OK   ( ) ERRO  

**Observações:**  
_________________________________________

---

## CT077 — Verificar mensagens de erro

**Passos:**
1. Gerar erros em formulários.
2. Ler as mensagens exibidas.

**Resultado esperado:**
- As mensagens devem ser simples e compreensíveis.

**Resultado obtido:**  
( ) OK   ( ) ERRO  

**Observações:**  
_________________________________________

---

## CT078 — Verificar mensagens de sucesso

**Passos:**
1. Cadastrar, editar ou excluir algum registro.
2. Observar a mensagem exibida.

**Resultado esperado:**
- O sistema deve informar claramente que a operação foi realizada.

**Resultado obtido:**  
( ) OK   ( ) ERRO  

**Observações:**  
_________________________________________

---

# ✅ 6. Critérios de Aprovação

O sistema será aprovado se:

- O usuário conseguir realizar as tarefas sem ajuda.
- As telas forem claras e organizadas.
- Os formulários validarem os campos corretamente.
- As tabelas estiverem alinhadas.
- As mensagens forem compreensíveis.
- O estoque permanecer correto após entradas, saídas, edições e exclusões.
- O sistema não travar durante a navegação.

---

# ❌ 7. Critérios de Reprovação

O sistema será reprovado se:

- O usuário não conseguir concluir tarefas básicas.
- As mensagens forem confusas.
- O layout estiver quebrado.
- As tabelas estiverem desalinhadas.
- O sistema permitir estoque inconsistente.
- O sistema travar durante o uso.
- Usuários sem permissão acessarem áreas restritas.

---

# 🎯 8. Conclusão

Este plano de testes cobre as principais situações de usabilidade do sistema BemStock, incluindo login, dashboard, produtos, movimentações, histórico, usuários, navegação, layout, edição, exclusão e consistência de estoque.