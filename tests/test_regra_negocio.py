from regra_negocio import (
    validar_transacao,
    calcular_desconto_e_final
)


def test_transacao_valida():
    transacao = {
        "valor_bruto": 100,
        "idade": 25,
        "cpf": "12345678901",
        "categoria": "roupas"
    }

    resultado, mensagem = validar_transacao(transacao)

    assert resultado is True
    assert mensagem == "OK"


def test_valor_negativo():
    transacao = {
        "valor_bruto": -10,
        "idade": 25,
        "cpf": "12345678901",
        "categoria": "roupas"
    }

    resultado, mensagem = validar_transacao(transacao)

    assert resultado is False


def test_cpf_invalido():
    transacao = {
        "valor_bruto": 100,
        "idade": 25,
        "cpf": "12345",
        "categoria": "roupas"
    }

    resultado, mensagem = validar_transacao(transacao)

    assert resultado is False


def test_menor_comprando_eletronicos():
    transacao = {
        "valor_bruto": 100,
        "idade": 17,
        "cpf": "12345678901",
        "categoria": "eletronicos"
    }

    resultado, mensagem = validar_transacao(transacao)

    assert resultado is False


def test_desconto_idoso():
    desconto, valor_final = calcular_desconto_e_final(
        100, 60, "roupas"
    )

    assert desconto == 15
    assert valor_final == 85


def test_desconto_livros():
    desconto, valor_final = calcular_desconto_e_final(
        100, 30, "livros"
    )

    assert desconto == 10
    assert valor_final == 90


def test_descontos_acumulados():
    desconto, valor_final = calcular_desconto_e_final(
        100, 60, "livros"
    )

    assert desconto == 25
    assert valor_final == 75