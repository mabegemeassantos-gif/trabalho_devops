import json
import logging
import time

from database import inicializar_banco, salvar_transacao
from regra_negocio import (
    validar_transacao,
    calcular_desconto_e_final
)


# Configuração dos registros de log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def processar_transacoes():
    inicio = time.perf_counter()

    logger.info("Iniciando processamento das transações.")

    # Inicializa o banco de dados
    inicializar_banco()

    # Lê os dados do arquivo JSON
    with open("dados_processamento.json", "r", encoding="utf-8") as arquivo:
        transacoes = json.load(arquivo)

    aprovadas = 0
    rejeitadas = 0

    for transacao in transacoes:

        valida, motivo = validar_transacao(transacao)

        if valida:
            desconto, valor_final = calcular_desconto_e_final(
                transacao["valor_bruto"],
                transacao["idade"],
                transacao["categoria"]
            )

            dados = {
                **transacao,
                "valor_final": valor_final,
                "status": "APROVADO",
                "motivo_rejeicao": None
            }

            aprovadas += 1

            logger.info(
                "Transação %s aprovada. Desconto: R$ %.2f",
                transacao["id_transacao"],
                desconto
            )

        else:
            dados = {
                **transacao,
                "valor_final": None,
                "status": "REJEITADO",
                "motivo_rejeicao": motivo
            }

            rejeitadas += 1

            logger.warning(
                "Transação %s rejeitada: %s",
                transacao["id_transacao"],
                motivo
            )

        salvar_transacao(dados)

    fim = time.perf_counter()
    tempo_total = (fim - inicio) * 1000

    total = aprovadas + rejeitadas

    print("\n===== RESUMO DO PROCESSAMENTO =====")
    print(f"Total processado: {total}")
    print(f"Transações aprovadas: {aprovadas}")
    print(f"Transações rejeitadas: {rejeitadas}")
    print(f"Tempo total: {tempo_total:.2f} ms")

    logger.info("Processamento finalizado.")


if __name__ == "__main__":
    processar_transacoes()