
calculadora de descontos de produtos
-------------------------------------

from collections import namedtuple

produto = namedtuple("produto", ["nome", "valor", "desconto_percentual"])


def calcular_valor_desconto(item):
    """calcula o valor (em reais) do desconto aplicado a um produto."""
    return item.valor * (item.desconto_percentual / 100)


def calcular_valor_final(item):
    """calcula o valor final do produto apos aplicacao do desconto."""
    return item.valor - calcular_valor_desconto(item)


def resumo_produto(item):
    """retorna um dicionario com todos os valores calculados de um produto."""
    valor_desconto = calcular_valor_desconto(item)
    valor_final = calcular_valor_final(item)
    return {
    "nome": item.nome,
      "valor_original": item.valor,
      "desconto_percentual": item.desconto_percentual,
      "valor_desconto": valor_desconto,
      "valor_final": valor_final,
}


def gerar_resumos(produtos):
    """aplica resumo_produto a uma lista de produtos."""
    return [resumo_produto(p) for p in produtos]


def somar_valores(resumos):
    """soma os valores totais de uma lista de resumos de produtos."""
    total_sem_desconto = sum(r["valor_original"] for r in resumos)
    total_com_desconto = sum(r["valor_final"] for r in resumos)
    total_descontos = sum(r["valor_desconto"] for r in resumos)
    return {
    "total_sem_desconto": total_sem_desconto,
    "total_com_desconto": total_com_desconto,
    "total_descontos": total_descontos,
}


def verificar_teto_gastos(totais, teto):
    
    verifica se os totais excedem o teto de gastos definido.

    regras:
    - se o total com desconto ainda ultrapassa o teto -> alerta critico.
    - se apenas o total sem desconto ultrapassa o teto -> alerta informativo
      (o desconto resolveu o problema).
    - caso contrario -> dentro do orcamento.
    
    sem_desconto = totais["total_sem_desconto"]
    com_desconto = totais["total_com_desconto"]

    if com_desconto > teto:
  return (
            f"atencao! valor excedido mesmo com aplicacao dos descontos!\n"
            f"   total com desconto: {com_desconto:.2f} reais | teto: {teto:.2f} reais"
        )
  elif sem_desconto > teto:
  return (
            f"valor acima do teto de gastos (sem desconto).\n"
            f"   apos os descontos, o valor ficou dentro do limite.\n"
            f"   total sem desconto: {sem_desconto:.2f} reais | teto: {teto:.2f} reais"
        )
  else:
    return (
            f"dentro do orcamento.\n"
            f"   total com desconto: {com_desconto:.2f} reais | teto: {teto:.2f} reais"
)


def verificar_teto_parcial(totais, teto):
    """
    verifica o total parcial (enquanto o usuario ainda esta adicionando produtos).
    retorna uma mensagem de alerta se o teto ja foi ultrapassado, ou none
    se ainda esta dentro do limite.
    """
    com_desconto = totais["total_com_desconto"]
    if com_desconto > teto:
        return (
            f"\nalerta: o total parcial (com desconto) ja passou do teto de gastos!\n"
            f"   total parcial: {com_desconto:.2f} reais | teto: {teto:.2f} reais\n"
            f"   voce pode continuar adicionando produtos ou finalizar a compra.\n"
  )
  return None

def formatar_relatorio(resumos, totais, teto):
    """monta uma string formatada com o relatorio completo."""
    linhas = ["=" * 50, "relatorio de descontos", "=" * 50]
    for r in resumos:
        linhas.append(
 f"\nproduto: {r['nome']}\n"
 f"  valor original : {r['valor_original']:.2f} reais\n"
 f"  desconto (%)   : {r['desconto_percentual']:.1f}%\n"
 f"  valor desconto : {r['valor_desconto']:.2f} reais\n"
 f"  valor final    : {r['valor_final']:.2f} reais"
        )
    linhas.append("\n" + "-" * 50)
    linhas.append(f"total sem desconto : {totais['total_sem_desconto']:.2f} reais")
    linhas.append(f"total de descontos : {totais['total_descontos']:.2f} reais")
    linhas.append(f"total com desconto : {totais['total_com_desconto']:.2f} reais")
    linhas.append("-" * 50)
    linhas.append(f"\n{verificar_teto_gastos(totais, teto)}")
    return "\n".join(linhas)

def ler_teto_gastos():
    """le o teto de gastos definido pelo usuario (chamado antes de tudo)."""
    valor = input("defina o teto de gastos (em reais): ").replace(",", ".")
    return float(valor)


def ler_produtos_do_usuario(teto):
    """
    le os dados dos produtos digitados pelo usuario via terminal.
    a cada produto adicionado, verifica se o total parcial ja passou
    do teto de gastos e alerta o usuario (sem interromper o programa).
    """
    produtos = []
    print("\ndigite os produtos (deixe o nome vazio para finalizar):\n")

    while True:
        nome = input("nome do produto: ").strip()
        if nome == "":
            break

        valor = float(input("valor do produto (em reais): ").replace(",", "."))
        desconto = float(input("desconto (%): ").replace(",", "."))
        produtos.append(produto(nome, valor, desconto))

        resumos_parciais = gerar_resumos(produtos)
        totais_parciais = somar_valores(resumos_parciais)
        alerta = verificar_teto_parcial(totais_parciais, teto)
        if alerta:
            print(alerta)

        print()
      
    return produtos
def main():
    """funcao principal que orquestra a execucao do programa."""
    teto = ler_teto_gastos()
    produtos = ler_produtos_do_usuario(teto)

    if not produtos:
        print("nenhum produto informado. encerrando.")
        return

    resumos = gerar_resumos(produtos)
    totais = somar_valores(resumos)
    relatorio = formatar_relatorio(resumos, totais, teto)
    print("\n" + relatorio)

if __name__ == "__main__":
    main()
