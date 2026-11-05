def validar_transacao(transacao: dict) -> tuple[bool, str]:
    """
    Valida os dados de uma transação.
    """

    valor_bruto = transacao.get("valor_bruto")
    idade = transacao.get("idade")
    cpf = str(transacao.get("cpf", ""))

    if valor_bruto is None or valor_bruto <= 0:
        return False, "Valor bruto deve ser maior que zero."

    if idade is None or idade < 0 or idade > 120:
        return False, "Idade deve estar entre 0 e 120 anos."

    if len(cpf) != 11 or not cpf.isdigit():
        return False, "CPF deve conter exatamente 11 números."

    if idade < 18 and transacao.get("categoria") == "eletronicos":
        return False, "Menores de 18 anos não podem comprar eletrônicos."

    return True, "OK"


def calcular_desconto_e_final(
    valor_bruto: float,
    idade: int,
    categoria: str
) -> tuple[float, float]:
    """
    Calcula o desconto e o valor final da compra.
    """

    desconto = 0.0

    if idade >= 60:
        desconto += 0.15

    if categoria == "livros":
        desconto += 0.10

    if desconto > 0.25:
        desconto = 0.25

    valor_desconto = valor_bruto * desconto
    valor_final = valor_bruto - valor_desconto

    return valor_desconto, valor_final