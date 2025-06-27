def identificar_bandeira(numero_cartao: str) -> str:
    """
    Identifica a bandeira de um cartão de crédito a partir do seu número.

    A lógica de validação é baseada nos prefixos (BINs) e no comprimento
    do número do cartão. A função é robusta para limpar caracteres não
    numéricos e lida com as principais bandeiras do mercado.

    Args:
        numero_cartao (str): O número do cartão de crédito, que pode
                             conter espaços ou hífens.

    Returns:
        str: O nome da bandeira identificada (ex: "Visa", "MasterCard")
             ou uma mensagem de erro ("Número inválido") ou de não
             identificação ("Bandeira não identificada").
    """
    # 1. Limpa a entrada, removendo todos os caracteres que não são dígitos.
    numero = ''.join(filter(str.isdigit, numero_cartao))

    # 2. Valida se a entrada contém números após a limpeza.
    if not numero:
        return "Número inválido"

    # 3. Define as regras de identificação em uma lista de tuplas.
    #    Cada tupla contém (Nome da Bandeira, Função de Validação).
    #    A ordem das regras é importante em caso de prefixos sobrepostos.
    bandeiras = [
        # Visa: Começa com '4' e tem 13, 16 ou 19 dígitos.
        ("Visa", lambda n: n.startswith("4") and len(n) in [13, 16, 19]),
        
        # MasterCard: Começa com '51' a '55' e tem 16 dígitos.
        ("MasterCard", lambda n: 51 <= int(n[:2]) <= 55 and len(n) == 16),
        
        # American Express: Começa com '34' ou '37' e tem 15 dígitos.
        ("American Express", lambda n: n.startswith(("34", "37")) and len(n) == 15),
        
        # Discover: Vários prefixos e comprimentos.
        ("Discover", lambda n: n.startswith(("6011", "65")) or (len(n) >= 3 and 644 <= int(n[:3]) <= 649)),
        
        # Diners Club: Começa com '36' e tem 14 dígitos.
        ("Diners Club", lambda n: n.startswith("36") and len(n) == 14),
        
        # Hipercard: Começa com '38' e tem 14 dígitos. (Nota: Existem outros prefixos, como '60')
        ("Hipercard", lambda n: n.startswith("38") and len(n) == 14),
        
        # Elo: Múltiplos prefixos, um dos mais complexos.
        ("Elo", lambda n: any(n.startswith(p) for p in ["636368", "438935", "504175", "451416", "636297", "5067", "4576", "4011"])),
    ]

    # 4. Itera sobre as regras para encontrar uma correspondência.
    for nome, condicao in bandeiras:
        try:
            if condicao(numero):
                return nome
        except ValueError:
            # Captura erros de conversão (ex: int(n[:2])) para entradas curtas.
            continue
    
    # 5. Se nenhuma regra corresponder, a bandeira não foi identificada.
    return "Bandeira não identificada"

# Bloco de execução principal para testar a função.
if __name__ == "__main__":
    print("--- Identificador de Bandeira de Cartão de Crédito ---")
    print("Digite o número do cartão (ou pressione Enter para sair).")
    
    while True:
        numero = input("\nNúmero do cartão: ").strip()
        if not numero:
            break
            
        bandeira = identificar_bandeira(numero)
        print(f"Bandeira identificada: {bandeira}")