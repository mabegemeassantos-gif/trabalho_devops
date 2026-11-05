# Processador de Transações - Projeto DevOps

## 1. Sobre o projeto

Este projeto consiste em uma aplicação CLI (Interface de Linha de Comando) desenvolvida em Python para processar transações de clientes a partir de um arquivo JSON.

O sistema realiza a validação dos dados, aplica regras de negócio, calcula descontos e armazena os resultados em um banco de dados SQLite.

O projeto também utiliza práticas de DevOps, incluindo testes automatizados, versionamento de banco de dados com Alembic, registros de logs e integração contínua com GitHub Actions.

## 2. Tecnologias utilizadas

- Python
- SQLite
- Alembic
- SQLAlchemy
- Pytest
- Git e GitHub
- GitHub Actions

## 3. Regras de negócio

O sistema realiza as seguintes validações:

- O valor bruto deve ser maior que zero.
- A idade deve estar entre 0 e 120 anos.
- O CPF deve conter exatamente 11 números.
- Menores de 18 anos não podem comprar produtos da categoria eletrônicos.

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
│   ├── versions/
│   │   ├── 56977921c4d0_criacao_inicial_da_tabela_transacoes.py
│   │   ├── 8ac7088a4eb1_expand_adiciona_primeiro_nome_e_.py
│   │   ├── 96fa79468ace_backfill_dos_nomes_dos_clientes.py
│   │   └── ba90bd6c0e41_contract_remove_campo_cliente.py
│   └── env.py
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
├── alembic.ini
└── README.md
```

## 5. Instalação e configuração

Clone o repositório:

```bash
git clone https://github.com/mabegemeassantos-gif/trabalho_devops.git
```

Entre na pasta do projeto:

```bash
cd trabalho_devops
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## 6. Migrações do banco de dados

O projeto utiliza Alembic para controlar a evolução da estrutura do banco de dados.

Foi aplicado o padrão **Expand-Contract**, dividido em três etapas:

- **Expand:** adiciona os campos `primeiro_nome` e `sobrenome`, mantendo temporariamente o campo antigo `cliente`.
- **Backfill:** transfere os nomes dos registros existentes para os novos campos.
- **Contract:** remove o campo antigo `cliente` após a migração dos dados.

Durante a etapa Expand, foi implementado o conceito de Dual Write, permitindo gravar as informações nos campos antigos e novos enquanto ambos coexistem.

Para executar todas as migrações:

```bash
python -m alembic upgrade head
```

## 7. Execução do sistema

Após instalar as dependências e executar as migrações, inicie o processamento:

```bash
python main.py
```

O sistema lê os registros de `dados_processamento.json`, realiza as validações, calcula os descontos e salva os resultados no banco SQLite.

Ao final, apresenta um resumo contendo:

- Total de registros processados.
- Quantidade de transações aprovadas.
- Quantidade de transações rejeitadas.
- Tempo total de execução.

## 8. Testes automatizados

O projeto utiliza Pytest para verificar o funcionamento das regras de negócio e das operações com o banco de dados.

Para executar os testes:

```bash
python -m pytest -v
```

Os testes verificam, entre outros casos:

- Validação de transações.
- CPF inválido.
- Valores negativos e iguais a zero.
- Limites de idade.
- Regras de desconto.
- Acúmulo de descontos.
- Operações de gravação e consulta no banco de dados.
- Dual Write durante a etapa Expand.

## 9. Logs e observabilidade

O sistema utiliza o módulo `logging` do Python para registrar os acontecimentos durante o processamento.

Os registros são armazenados no arquivo `app.log` e também exibidos no terminal.

São utilizados três níveis de log:

- **INFO:** informa o início, as aprovações e a conclusão do processamento.
- **WARNING:** registra transações rejeitadas.
- **ERROR:** registra falhas durante a execução, incluindo os detalhes da exceção.

O tempo de execução também é medido e apresentado no resumo final.

## 10. Integração contínua (CI/CD)

O projeto utiliza GitHub Actions para executar automaticamente o fluxo de integração contínua.

O workflow está configurado em:

`.github/workflows/ci.yml`

A automação executa as seguintes etapas:

1. Configura o ambiente Python.
2. Instala as dependências.
3. Executa os testes automatizados com Pytest.
4. Executa as migrações do banco de dados.
5. Executa o processamento das transações.

O workflow é acionado em eventos de Push e Pull Request para a branch principal (`main`).

## 11. Demonstração de Pull Request

Foi criada a branch `demonstracao-pr` para demonstrar o processo de revisão e integração de código utilizando Git e GitHub.

O Pull Request permite comparar as alterações realizadas com a branch `main` e verificar a execução automática dos testes pelo GitHub Actions antes da integração.

**Pull Request:** https://github.com/mabegemeassantos-gif/trabalho_devops/pull/1
