# E-commerce com Gateway de Pagamentos

## 1. Sobre o projeto

Este projeto consiste em um e-commerce simulado desenvolvido para demonstrar conceitos de backend presentes em sistemas reais de processamento de pagamentos.

O sistema permite que um cliente realize uma compra, crie um pedido e solicite um pagamento através de um Gateway de Pagamentos.

O resultado do pagamento não é tratado diretamente durante o checkout. O sistema aguarda a confirmação do Gateway através de um Webhook.

O projeto também implementa mecanismos para garantir:

* segurança na comunicação com o Gateway;
* idempotência no processamento de eventos;
* consistência dos dados;
* processamento assíncrono;
* rastreabilidade das operações;
* separação adequada de responsabilidades.

---

## 2. Objetivo

O principal objetivo é desenvolver uma API capaz de representar o fluxo de uma compra real, incluindo:

1. criação do pedido;
2. criação da cobrança;
3. comunicação com um Gateway de Pagamento;
4. recebimento de Webhooks;
5. validação da autenticidade dos eventos;
6. prevenção de processamento duplicado;
7. atualização do status do pagamento;
8. atualização do status do pedido;
9. processamento assíncrono de tarefas;
10. envio de confirmação ao cliente.

O projeto poderá utilizar inicialmente um Gateway de Pagamento simulado, permitindo que toda a arquitetura seja desenvolvida sem depender de uma plataforma financeira externa.

Posteriormente, o Gateway simulado poderá ser substituído por uma integração com um ambiente Sandbox de um provedor real.

---

# 3. Escopo

## Dentro do escopo

### Usuários

O sistema deverá possuir usuários capazes de realizar compras.

### Produtos

O sistema deverá permitir o cadastro e consulta de produtos disponíveis para compra.

### Pedidos

O sistema deverá permitir que um usuário crie um pedido contendo um ou mais produtos.

### Pagamentos

Cada pedido deverá possuir um pagamento associado.

O pagamento deverá possuir seu próprio ciclo de vida e status.

### Gateway

O sistema deverá se comunicar com um Gateway de Pagamentos.

Inicialmente, será utilizado um Gateway simulado.

### Webhooks

O sistema deverá disponibilizar um endpoint para receber eventos enviados pelo Gateway.

### Segurança

Os Webhooks deverão possuir mecanismo de validação de autenticidade através de assinatura ou token.

### Idempotência

O sistema deverá impedir que o mesmo evento de pagamento seja processado mais de uma vez.

### Processamento assíncrono

Tarefas que não precisam bloquear o processamento principal deverão ser executadas de maneira assíncrona.

Exemplo:

* envio de e-mail de confirmação.

### Logs

O sistema deverá registrar informações importantes relacionadas ao processamento dos pedidos e pagamentos.

---

# 4. Fora do escopo inicial

Para evitar que o projeto se torne excessivamente complexo, não fazem parte da primeira versão:

* pagamento real;
* armazenamento de dados de cartão;
* integração bancária;
* emissão de nota fiscal;
* cálculo de frete;
* sistema de cupons;
* marketplace;
* microsserviços;
* Kubernetes;
* infraestrutura em cloud;
* múltiplos gateways simultâneos;
* processamento financeiro real.

Esses recursos poderão ser adicionados futuramente.

---

# 5. Requisitos Funcionais

## RF01 — Cadastro de usuário

O sistema deverá permitir o cadastro de usuários.

---

## RF02 — Cadastro de produtos

O sistema deverá permitir o cadastro de produtos contendo informações básicas, como:

* nome;
* descrição;
* preço;
* estoque;
* status de disponibilidade.

---

## RF03 — Consulta de produtos

O sistema deverá permitir consultar os produtos disponíveis para compra.

---

## RF04 — Criação de pedido

O usuário deverá conseguir criar um pedido contendo um ou mais produtos.

O sistema deverá calcular o valor total da compra.

---

## RF05 — Criação do pagamento

Após a criação do pedido, o sistema deverá criar uma solicitação de pagamento através do Gateway.

O pagamento deverá possuir um identificador próprio e um identificador externo fornecido pelo Gateway.

---

## RF06 — Status do pedido

O pedido deverá possuir estados que representem seu ciclo de vida.

Estados iniciais:

* PENDING_PAYMENT
* PAID
* PAYMENT_FAILED
* CANCELED

---

## RF07 — Status do pagamento

O pagamento deverá possuir estados próprios.

Estados iniciais:

* PENDING
* APPROVED
* FAILED
* CANCELED

---

## RF08 — Recebimento de Webhook

O sistema deverá disponibilizar um endpoint específico para receber notificações do Gateway.

O Webhook deverá informar, no mínimo:

* identificador do evento;
* identificador do pagamento;
* tipo do evento;
* novo status do pagamento.

---

## RF09 — Validação do Webhook

O sistema deverá validar a autenticidade do Webhook antes de processar qualquer alteração relacionada ao pagamento.

Eventos inválidos deverão ser rejeitados.

---

## RF10 — Processamento do pagamento

Quando um Webhook válido informar que um pagamento foi aprovado, o sistema deverá atualizar:

**Pagamento**

PENDING → APPROVED

**Pedido**

PENDING_PAYMENT → PAID

---

## RF11 — Pagamento recusado

Quando o Gateway informar uma falha no pagamento, o sistema deverá atualizar:

**Pagamento**

PENDING → FAILED

**Pedido**

PENDING_PAYMENT → PAYMENT_FAILED

---

## RF12 — Idempotência

O sistema deverá identificar eventos já processados.

Caso um mesmo Webhook seja recebido novamente, o sistema não deverá executar novamente as operações relacionadas ao evento.

---

## RF13 — Processamento assíncrono

Após a confirmação do pagamento, o sistema deverá criar uma tarefa assíncrona para processos que não precisam ocorrer durante o processamento principal.

Exemplo:

* envio de confirmação por e-mail.

---

## RF14 — Consulta do pedido

O usuário deverá conseguir consultar seus pedidos e seus respectivos status.

---

## RF15 — Consulta do pagamento

O sistema deverá permitir consultar o status do pagamento associado ao pedido.

---

# 6. Requisitos Não Funcionais

## RNF01 — Segurança

Informações sensíveis não deverão ser armazenadas de maneira insegura.

O segredo utilizado para validar Webhooks deverá ser armazenado através de variáveis de ambiente.

---

## RNF02 — Consistência

Alterações relacionadas ao pagamento e ao pedido deverão preservar a consistência dos dados.

---

## RNF03 — Idempotência

O processamento de eventos deverá ser seguro contra requisições repetidas.

---

## RNF04 — Disponibilidade

O processamento do Webhook deverá ser rápido e não deverá depender de tarefas demoradas.

---

## RNF05 — Observabilidade

Operações importantes deverão possuir logs suficientes para permitir investigação de problemas.

---

## RNF06 — Manutenibilidade

O sistema deverá possuir separação clara entre:

* API;
* aplicação;
* domínio;
* infraestrutura.

---

## RNF07 — Testabilidade

As regras de negócio deverão poder ser testadas independentemente das implementações externas.

---

## RNF08 — Containerização

O ambiente de desenvolvimento deverá ser executável através de Docker.

---

# 7. Tecnologias previstas

### Backend

* Python
* FastAPI

### Banco de dados

* PostgreSQL
* SQLAlchemy
* Alembic

### Processamento assíncrono

* Redis
* Celery

### Infraestrutura

* Docker
* Docker Compose

### Testes

* Pytest

### Gateway

Primeira versão:

* Gateway simulado

Possível evolução:

* Stripe Sandbox
* Mercado Pago Sandbox
* outro provedor compatível

---

# 8. Principais entidades

## User

Representa o cliente do e-commerce.

## Product

Representa um produto disponível para compra.

## Order

Representa uma compra realizada pelo usuário.

## OrderItem

Representa os produtos pertencentes a um pedido.

## Payment

Representa o pagamento associado a um pedido.

## WebhookEvent

Representa um evento recebido do Gateway e permite controlar o processamento duplicado.

---

# 9. Estados principais

### Pedido

PENDING_PAYMENT

↓

PAID

ou

PAYMENT_FAILED

ou

CANCELED

### Pagamento

PENDING

↓

APPROVED

ou

FAILED

ou

CANCELED

---

# 10. Fluxo resumido

Cliente

↓

Checkout

↓

Criação do pedido

↓

Criação do pagamento

↓

Gateway de Pagamento

↓

Processamento externo

↓

Webhook

↓

Validação de segurança

↓

Verificação de idempotência

↓

Atualização do pagamento

↓

Atualização do pedido

↓

Criação de tarefa assíncrona

↓

Envio de confirmação

---

# 11. Critérios de conclusão

O projeto será considerado funcional quando for possível demonstrar o seguinte cenário:

1. Um usuário realiza uma compra.
2. O sistema cria o pedido.
3. O sistema cria o pagamento.
4. O Gateway recebe a solicitação.
5. O Gateway simula o processamento.
6. O Gateway envia um Webhook.
7. O sistema valida a autenticidade do evento.
8. O sistema verifica se o evento já foi processado.
9. O pagamento é atualizado.
10. O pedido é atualizado.
11. Uma tarefa assíncrona é criada.
12. O cliente recebe a confirmação.
13. Um Webhook duplicado não gera um novo processamento.
14. Um Webhook inválido é rejeitado.

---

# 12. Evoluções futuras

Após a primeira versão, o projeto poderá evoluir para:

* integração com Gateway real em Sandbox;
* múltiplos métodos de pagamento;
* múltiplos gateways;
* retry de tarefas;
* recuperação de tarefas que falharam;
* dashboard administrativo;
* métricas;
* tracing;
* notificações;
* histórico de eventos;
* controle de estoque mais avançado;
* aplicação frontend.

---

# 13. Principal objetivo técnico

Mais do que construir um e-commerce, este projeto busca demonstrar domínio sobre um fluxo de backend que envolve:

**integrações externas + processamento assíncrono + Webhooks + segurança + idempotência + transações + arquitetura limpa.**
