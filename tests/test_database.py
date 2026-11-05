
import sqlite3
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


def test_dual_write_durante_expand(tmp_path):
    caminho_banco = str(tmp_path / "teste_expand.db")

    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    # Simula a estrutura do banco após a migração Expand.
    cursor.execute("""
        CREATE TABLE transacoes (
            id_transacao TEXT PRIMARY KEY,
            cliente TEXT,
            primeiro_nome TEXT,
            sobrenome TEXT,
            cpf TEXT NOT NULL,
            idade INTEGER,
            valor_bruto REAL,
            valor_final REAL,
            status TEXT,
            motivo_rejeicao TEXT,
            data_processamento TIMESTAMP
        )
    """)

    conexao.commit()
    conexao.close()

    transacao = {
        "id_transacao": "TXEXPAND01",
        "cliente": "Carlos Eduardo Silva",
        "cpf": "12345678901",
        "idade": 25,
        "valor_bruto": 150.0,
        "valor_final": 150.0,
        "status": "APROVADO",
        "motivo_rejeicao": None
    }

    salvar_transacao(transacao, caminho_banco)

    resultado = buscar_transacao_por_id(
        "TXEXPAND01", caminho_banco
    )

    assert resultado is not None
    assert resultado["cliente"] == "Carlos Eduardo Silva"
    assert resultado["primeiro_nome"] == "Carlos"
    assert resultado["sobrenome"] == "Eduardo Silva"
