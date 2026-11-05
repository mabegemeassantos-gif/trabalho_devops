# Processador de Transações - Projeto DevOps

## 1. Sobre o projeto

Este projeto consiste em um sistema desenvolvido em Python para processar transações de clientes a partir de um arquivo JSON.

O sistema valida os dados, aplica regras de negócio, calcula descontos e armazena os resultados em um banco de dados SQLite.

O projeto também utiliza testes automatizados, migrações de banco de dados com Alembic, registros de logs e integração contínua com GitHub Actions.

## 2. Tecnologias utilizadas

- Python
- SQLite
- Alembic
- SQLAlchemy
- Pytest
- GitHub Actions

## 3. Regras de negócio

O sistema realiza as seguintes validações:

- O valor bruto deve ser maior que zero.
- A idade deve estar entre 0 e 120 anos.
- O CPF deve conter exatamente 11 números.
- Menores de 18 anos não podem comprar eletrônicos.

### Regras de desconto

- Pessoas com 60 anos ou mais recebem 15% de desconto.
- Compras da categoria livros recebem 10% de desconto.
- Os descontos podem ser acumulados, respeitando o limite máximo de 25%.

## 4. Estrutura do projeto

```text
trabalho_devops/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── test_regra_negocio.py
│   └── test_database.py
│
├── dados_processamento.json
├── database.py
├── main.py
├── regra_negocio.py
├── requirements.txt
├── README.md
└── app.log