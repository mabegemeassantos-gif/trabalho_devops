import pytest
from database import (
    inicializar_banco,
    salvar_transacao,
    buscar_transacao_por_id
)


def test_salvar_e_buscar_transacao(tmp_path):
    caminho_banco = str(tmp_path / "teste.db")

    inicializar_banco(caminho_banco)

    transacao = {
        "id_transacao": "TXTESTE01",
        "cliente": "Maria Silva",
        "cpf": "12345678901",
        "idade": 25,
        "valor_bruto": 100.0,
        "valor_final": 100.0,
        "status": "APROVADO",
        "motivo_rejeicao": None
    }

    salvar_transacao(transacao, caminho_banco)

    resultado = buscar_transacao_por_id(
        "TXTESTE01", caminho_banco
    )

    assert resultado is not None
    assert resultado["primeiro_nome"] == "Maria"
    assert resultado["sobrenome"] == "Silva"
    assert resultado["status"] == "APROVADO"
    assert "cliente" not in resultado


def test_buscar_transacao_inexistente(tmp_path):
    caminho_banco = str(tmp_path / "teste.db")

    inicializar_banco(caminho_banco)

    resultado = buscar_transacao_por_id(
        "NAOEXISTE", caminho_banco
    )

    assert resultado is None