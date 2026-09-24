# System Design

## 1. Visão geral

O sistema é estruturado como uma aplicação backend modular responsável por gerenciar usuários, produtos, pedidos e pagamentos.

O processamento financeiro é delegado a um Gateway de Pagamentos externo.

O sistema não considera o pagamento aprovado apenas porque a solicitação de cobrança foi criada.

A confirmação definitiva ocorre através de um Webhook enviado pelo Gateway.

---

# 2. Arquitetura de alto nível

```text
                         ┌─────────────────┐
                         │     Cliente     │
                         └────────┬────────┘
                                  │
                                  │ HTTPS
                                  ▼
                         ┌─────────────────┐
                         │    FastAPI      │
                         │      API        │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
               ┌────────┐   ┌──────────┐   ┌──────────┐
               │ Users  │   │ Products │   │ Orders   │
               └────────┘   └──────────┘   └────┬─────┘
                                                 │
                                                 ▼
                                           ┌──────────┐
                                           │ Payment  │
                                           └────┬─────┘
                                                │
                                                ▼
                                      ┌──────────────────┐
                                      │ Payment Gateway  │
                                      └────────┬─────────┘
                                               │
                                               │ Webhook
                                               ▼
                                      ┌──────────────────┐
                                      │ Webhook Handler  │
                                      └────────┬─────────┘
                                               │
                            ┌──────────────────┼─────────────────┐
                            │                  │                 │
                            ▼                  ▼                 ▼
                       Segurança         Idempotência       Processamento
                            │                  │             do pagamento
                            └──────────────────┼─────────────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │   PostgreSQL    │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ Redis / Celery  │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │  Email Service  │
                                      └─────────────────┘
```

---

# 3. Componentes

## Cliente

Responsável por iniciar a compra e consultar o resultado do pedido.

---

## API

Responsável por receber requisições e encaminhá-las para as regras de aplicação.

Não deve conter regras complexas de negócio.

---

## Application

Responsável por executar os casos de uso.

Principais casos:

* criar pedido;
* iniciar pagamento;
* processar Webhook;
* consultar pedido;
* consultar pagamento.

---

## Domain

Contém as regras de negócio independentes de tecnologia.

Principais conceitos:

* Order;
* Payment;
* Product;
* estados do pedido;
* estados do pagamento;
* regras de transição;
* contratos de repositórios;
* contrato do Gateway.

---

## PostgreSQL

Responsável pelo armazenamento persistente.

Armazena:

* usuários;
* produtos;
* pedidos;
* itens dos pedidos;
* pagamentos;
* eventos de Webhook.

---

## Payment Gateway

Sistema externo responsável pelo processamento do pagamento.

Na primeira versão será simulado.

Posteriormente poderá ser substituído por um Gateway real em ambiente Sandbox.

---

## Redis

Responsável por fornecer infraestrutura para processamento assíncrono.

---

## Celery

Responsável por executar tarefas em segundo plano.

Exemplo:

**Enviar confirmação de pagamento.**

---

# 4. Fluxo de Checkout

```text
Cliente
   │
   │ Inicia checkout
   ▼
API
   │
   ▼
Validação do pedido
   │
   ▼
Verificação dos produtos
   │
   ▼
Cálculo do valor
   │
   ▼
Criação do Order
   │
   ▼
Criação do Payment
   │
   ▼
Solicitação ao Gateway
   │
   ▼
Gateway retorna identificador
   │
   ▼
Pagamento = PENDING
   │
   ▼
Pedido = PENDING_PAYMENT
```

Neste momento o checkout foi criado, mas o pagamento ainda não foi confirmado.

---

# 5. Fluxo do Gateway

```text
                   Payment PENDING
                          │
                          ▼
                  Payment Gateway
                          │
                     Processamento
                          │
                ┌─────────┴─────────┐
                │                   │
                ▼                   ▼
             APPROVED             FAILED
                │                   │
                └─────────┬─────────┘
                          │
                          ▼
                       Webhook
```

---

# 6. Fluxo do Webhook

```text
Payment Gateway
      │
      │ Evento
      ▼
POST /webhooks/payment
      │
      ▼
Recebe evento
      │
      ▼
Valida assinatura
      │
      ├─────────────── inválida ──────────────► Rejeita
      │
      ▼
Evento válido
      │
      ▼
Verifica event_id
      │
      ├────────────── já processado ──────────► Ignora
      │
      ▼
Evento novo
      │
      ▼
Inicia processamento
      │
      ▼
Atualiza Payment
      │
      ▼
Atualiza Order
      │
      ▼
Registra evento
      │
      ▼
Cria tarefa assíncrona
      │
      ▼
Retorna sucesso
```

---

# 7. Fluxo de pagamento aprovado

```text
Webhook
   │
   ▼
Evento: payment.approved
   │
   ▼
Validação
   │
   ▼
Idempotência
   │
   ▼
Payment
PENDING → APPROVED
   │
   ▼
Order
PENDING_PAYMENT → PAID
   │
   ▼
Evento registrado
   │
   ▼
Tarefa de confirmação
   │
   ▼
Redis
   │
   ▼
Celery Worker
   │
   ▼
Email de confirmação
```

---

# 8. Fluxo de pagamento recusado

```text
Webhook
   │
   ▼
Evento: payment.failed
   │
   ▼
Validação
   │
   ▼
Idempotência
   │
   ▼
Payment
PENDING → FAILED
   │
   ▼
Order
PENDING_PAYMENT → PAYMENT_FAILED
```

---

# 9. Fluxo de Webhook duplicado

O Gateway pode enviar o mesmo evento mais de uma vez.

```text
Gateway
   │
   ├──── Evento 123 ────► Sistema
   │
   ├──── Evento 123 ────► Sistema
   │
   └──── Evento 123 ────► Sistema
```

O sistema consulta o histórico:

```text
event_id = 123
```

Se o evento já estiver registrado:

```text
Não processar novamente
```

Resultado:

```text
Payment continua APPROVED
Order continua PAID
Nenhum processamento duplicado
```

---

# 10. Fluxo de segurança

```text
Gateway
   │
   │ Payload
   │ Signature
   ▼
Webhook
   │
   ▼
Validação da assinatura
   │
   ├── Inválida → Rejeitar
   │
   └── Válida
          │
          ▼
      Processar evento
```

O segredo utilizado na validação não deve fazer parte do código ou do banco de dados como informação exposta.

---

# 11. Consistência do pagamento

A atualização do pagamento e do pedido deve ser tratada de forma consistente.

Exemplo:

```text
Payment
PENDING
   │
   ▼
APPROVED
```

e:

```text
Order
PENDING_PAYMENT
   │
   ▼
PAID
```

As alterações relacionadas devem fazer parte da mesma operação transacional sempre que possível.

Se ocorrer uma falha durante a operação, o sistema deverá evitar ficar em um estado parcialmente atualizado.

---

# 12. Fluxo assíncrono

O processamento principal não deverá ficar esperando operações demoradas.

```text
Webhook
   │
   ▼
Atualiza banco
   │
   ▼
Cria tarefa
   │
   ▼
Retorna resposta
         │
         │
         ▼
      Redis
         │
         ▼
   Celery Worker
         │
         ▼
     Enviar email
```

A confirmação do pagamento não depende da conclusão do envio do e-mail.

---

# 13. Estados do sistema

## Order

```text
              ┌──────────────┐
              │   PENDING    │
              │   PAYMENT    │
              └──────┬───────┘
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
       PAID       FAILED     CANCELED
```

## Payment

```text
                 ┌─────────┐
                 │ PENDING │
                 └────┬────┘
                      │
              ┌───────┼───────┐
              │       │       │
              ▼       ▼       ▼
          APPROVED  FAILED  CANCELED
```

---

# 14. Banco de dados conceitual

```text
User
 │
 │ 1:N
 ▼
Order
 │
 ├───────────────┐
 │               │
 │ 1:N           │ 1:1
 ▼               ▼
OrderItem       Payment
 │
 │ N:1
 ▼
Product


WebhookEvent
     │
     └── registra eventos recebidos
```

---

# 15. Responsabilidades

| Componente      | Responsabilidade                    |
| --------------- | ----------------------------------- |
| API             | Receber requisições                 |
| Use Cases       | Executar casos de uso               |
| Domain          | Regras de negócio                   |
| Repository      | Persistência                        |
| PostgreSQL      | Armazenamento                       |
| Payment Gateway | Processamento externo               |
| Webhook         | Receber eventos                     |
| Redis           | Suporte ao processamento assíncrono |
| Celery          | Executar tarefas                    |
| Email Service   | Enviar notificações                 |

---

# 16. Princípios arquiteturais

O projeto deverá seguir os seguintes princípios:

### Separação de responsabilidades

Cada componente deve possuir uma responsabilidade clara.

### Dependency Inversion

As regras de negócio não devem depender diretamente de tecnologias externas.

### Idempotência

Eventos repetidos não devem gerar efeitos repetidos.

### Segurança

Informações recebidas de sistemas externos devem ser validadas antes de alterar o estado interno.

### Consistência

Atualizações relacionadas a um mesmo fluxo devem preservar a consistência dos dados.

### Assincronicidade

Operações demoradas ou que não precisam bloquear o fluxo principal devem ser processadas em segundo plano.

### Testabilidade

As regras principais devem poder ser testadas sem depender obrigatoriamente de serviços externos.

---

# 17. Fluxo completo do sistema

```text
┌──────────────┐
│    CLIENTE   │
└──────┬───────┘
       │
       │ Compra
       ▼
┌──────────────┐
│     API      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    ORDER     │
│   PENDING    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   PAYMENT    │
│   PENDING    │
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│  PAYMENT GATEWAY    │
└──────────┬──────────┘
           │
           │ Processamento
           ▼
     ┌─────────────┐
     │   WEBHOOK   │
     └──────┬──────┘
            │
            ▼
     ┌─────────────┐
     │  SEGURANÇA  │
     └──────┬──────┘
            │
            ▼
     ┌─────────────┐
     │ IDEMPOTÊNCIA│
     └──────┬──────┘
            │
            ▼
     ┌─────────────┐
     │  DATABASE   │
     │             │
     │ Payment     │
     │ Order       │
     └──────┬──────┘
            │
            ▼
       ┌─────────┐
       │  REDIS  │
       └────┬────┘
            │
            ▼
      ┌───────────┐
      │  CELERY   │
      └─────┬─────┘
            │
            ▼
       ┌─────────┐
       │  EMAIL  │
       └─────────┘
```

---

# 18. Resultado esperado

Ao final do fluxo, o sistema deverá conseguir responder à seguinte pergunta:

> "O cliente realizou uma compra. O pagamento foi realmente confirmado pelo Gateway e o pedido está consistente?"

O sistema deverá conseguir demonstrar isso através do estado persistido do pedido e do pagamento, do registro do evento recebido e dos logs do processamento.

O projeto, portanto, não tem como objetivo apenas "fazer um pagamento".

Seu principal objetivo técnico é demonstrar um fluxo confiável de:

**Checkout → Pagamento → Webhook → Segurança → Idempotência → Persistência → Processamento Assíncrono → Confirmação**
