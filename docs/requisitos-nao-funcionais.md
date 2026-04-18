# ⚙️ Requisitos Não Funcionais — BemStock

## 1. Introdução

Os requisitos não funcionais descrevem as características de qualidade que o sistema **BemStock** deve possuir, garantindo que o sistema seja seguro, eficiente, fácil de usar e adequado ao ambiente da instituição Lar Bem.

Esses requisitos complementam os requisitos funcionais e asseguram a qualidade do sistema durante sua utilização.

---

## 2. Usabilidade

**RNF01.** O sistema deve possuir uma interface simples, intuitiva e de fácil aprendizado.

**RNF02.** O sistema deve apresentar telas organizadas, com navegação clara entre as funcionalidades.

**RNF03.** O sistema deve utilizar linguagem clara e acessível aos usuários.

**RNF04.** O sistema deve apresentar mensagens de erro e sucesso de forma clara e objetiva.

**RNF05.** O sistema deve permitir que usuários com baixo nível de conhecimento técnico utilizem suas funcionalidades.

**RNF06.** O sistema deve manter consistência visual entre as telas (cores, botões, layout).

**RNF07.** O sistema deve permitir interação fluida com os campos (ex.: dropdowns abrindo ao clicar em qualquer área do campo).

**RNF08.** O sistema deve exibir corretamente conteúdos longos nas tabelas, utilizando quebra de linha quando necessário.

---

## 3. Funcionamento Offline

**RNF09.** O sistema deve funcionar localmente no computador da instituição.

**RNF10.** O sistema deve operar sem necessidade de conexão com a internet.

**RNF11.** Os dados devem ser armazenados localmente em banco de dados SQLite.

---

## 4. Segurança

**RNF12.** O sistema deve exigir autenticação por e-mail e senha para acesso.

**RNF13.** O sistema deve permitir acesso apenas a usuários cadastrados.

**RNF14.** O sistema deve armazenar as senhas de forma segura utilizando hash (SHA-256).

**RNF15.** O sistema deve aplicar validações para impedir operações inválidas.

**RNF16.** O sistema deve restringir funcionalidades com base no perfil do usuário (`admin` ou `estoque`).

**RNF17.** O sistema deve implementar um fluxo de primeiro acesso obrigatório para o usuário administrador inicial.

**RNF18.** O sistema deve impedir o uso de credenciais padrão após o primeiro login.

---

## 5. Desempenho

**RNF19.** O sistema deve responder às operações principais sem atrasos perceptíveis ao usuário.

**RNF20.** O sistema deve carregar as telas rapidamente para uso cotidiano.

**RNF21.** O sistema deve permitir consultas de estoque e histórico de movimentações de forma eficiente.

**RNF22.** O sistema deve suportar paginação de dados para evitar sobrecarga na interface.

---

## 6. Manutenção e Organização do Código

**RNF23.** O sistema deve seguir arquitetura em camadas (views, controllers, models, database e utils).

**RNF24.** O sistema deve possuir estrutura de pastas organizada e padronizada.

**RNF25.** O código deve utilizar nomes claros e legíveis.

**RNF26.** O sistema deve possuir documentação no repositório (README e arquivos em /docs).

**RNF27.** O sistema deve utilizar tecnologias gratuitas e adequadas ao escopo acadêmico:

- Python  
- CustomTkinter  
- SQLite  

---

## 7. Confiabilidade

**RNF28.** O sistema deve garantir consistência dos dados após cada operação.

**RNF29.** O sistema deve registrar corretamente todas as movimentações realizadas.

**RNF30.** O sistema deve manter o estoque atualizado com base nas movimentações.

**RNF31.** O sistema não deve permitir inconsistências no estoque (ex.: valores negativos).

**RNF32.** O sistema deve garantir integridade referencial entre usuários, produtos e movimentações.

---

## 8. Implantação

**RNF33.** O sistema deve poder ser executado em computadores com sistema operacional Windows.

**RNF34.** O sistema deve ser empacotado para facilitar sua execução (ex.: uso de PyInstaller).

**RNF35.** O sistema deve permitir instalação simples no ambiente da instituição.

---

## 9. Conclusão

Os requisitos não funcionais garantem que o sistema BemStock seja confiável, seguro, fácil de utilizar e adequado ao ambiente de uso da instituição Lar Bem, contribuindo para o controle eficiente do estoque.