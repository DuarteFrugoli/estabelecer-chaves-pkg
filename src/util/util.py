def solicita_entrada(mensagem, tipo=int, validacao=None):
    """Solicita e valida a entrada do usuário."""
    while True:
        try:
            valor = tipo(input(mensagem))
            if validacao and not validacao(valor):
                raise ValueError("Entrada inválida.")
            return valor
        except ValueError as e:
            print(e)