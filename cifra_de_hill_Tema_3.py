import os  # biblioteca nativa usada apenas para salvar o relatório na mesma pasta do código
import random  # biblioteca nativa do Python usada apenas para sortear números inteiros no gerador automático de chaves


# TESTE CHAVE
def calcular_mdc(a, b):  # função para calcular o mdc, usada no teste de chave
  # transforma os valores em positivos caso algum seja negativo
  a = abs(a)
  b = abs(b)

  # repete a divisão pegando o resto até b chegar a zero (algoritmo de euclides)
  while b != 0:
    resto = a % b
    a = b
    b = resto
  return a


def inverso_modular(a, m):
  # garante que 'a' fique dentro do intervalo de 0 até m-1
  a = a % m

  # só existe inverso modular se a e m forem coprimos (mdc == 1)
  if calcular_mdc(a, m) != 1:
    return None

  # variáveis auxiliares do algoritmo de euclides estendido
  m_original = m
  x0, x1 = 0, 1

  while a > 1:
    quociente = a // m

    # atualiza 'm' e 'a' com o resto da divisão
    temp = m
    m = a % m
    a = temp

    # atualiza os coeficientes para encontrar o inverso
    temp = x0
    x0 = x1 - quociente * x0
    x1 = temp

  # se x1 terminar negativo, soma m_original para deixar positivo em Z_m
  if x1 < 0:
    x1 += m_original

  return x1


# OPERAÇÕES COM MATRIZES n x n
def obter_submatriz(matriz, linha_remover, coluna_remover):  # função auxiliar usada no determinante e na matriz adjunta para remover uma linha e uma coluna
  submatriz = []
  for i in range(len(matriz)):
    # pula a linha que precisa ser removida
    if i == linha_remover:
      continue

    nova_linha = []

    for j in range(len(matriz)):
      # adiciona apenas os elementos que não estão na coluna removida
      if j != coluna_remover:
        nova_linha.append(matriz[i][j])

    submatriz.append(nova_linha)

  return submatriz


def calcular_determinante(matriz):  # calcula o determinante de qualquer matriz n x n, usado no teste de chave e na inversa
  n = len(matriz)

  # caso base 1x1: o determinante é o próprio número
  if n == 1:
    return matriz[0][0]

  # caso base 2x2: diagonal principal menos diagonal secundária
  if n == 2:
    return (matriz[0][0] * matriz[1][1]) - (matriz[0][1] * matriz[1][0])

  # para 3x3 ou maior, usa a expansão de laplace pela primeira linha
  det = 0
  for j in range(n):
    # alterna o sinal (+ para coluna par, - para coluna ímpar)
    if j % 2 == 0:
      sinal = 1
    else:
      sinal = -1
    sub = obter_submatriz(matriz, 0, j)
    det += sinal * matriz[0][j] * calcular_determinante(sub)
  return det


def calcular_matriz_adjunta(matriz):  # calcula a matriz adjunta, usada na decifragem para achar K^-1
  n = len(matriz)

  # cria uma matriz n x n zerada para guardar a adjunta
  adjunta = []
  for i in range(n):
    adjunta.append([0] * n)

  # se a matriz for 1x1, a adjunta é [[1]]
  if n == 1:
    return [[1]]

  for i in range(n):
    for j in range(n):
      sub = obter_submatriz(matriz, i, j)
      # define o sinal do cofator: positivo se (i + j) for par, negativo se for ímpar
      if (i + j) % 2 == 0:
        sinal = 1
      else:
        sinal = -1

      # calcula o cofator multiplicando o sinal pelo determinante da submatriz
      cofator = sinal * calcular_determinante(sub)

      # salva o cofator já na posição transposta [j][i]
      adjunta[j][i] = cofator

  return adjunta


def multiplicar_matriz_vetor(matriz, vetor, m):  # multiplica a matriz pelo bloco de texto em módulo 'm' (serve para cifrar e decifrar)
  n = len(matriz)
  resultado = []

  for i in range(n):
    soma = 0

    # multiplica cada número da linha 'i' pelo número correspondente do vetor
    for j in range(n):
      soma += matriz[i][j] * vetor[j]

    # aplica o resto da divisão por 'm' para manter dentro do alfabeto (0 até m-1)
    resultado.append(soma % m)

  return resultado


# LEITURA, VALIDAÇÃO DA CHAVE E MATRIZ INVERSA MODULAR
def ler_matriz_chave(n, m):  # pede e lê a matriz-chave n x n digitada pelo usuário
  matriz = []
  print(
      f"\nDigite os valores da matriz-chave {n}x{n} (números de 0 até {m - 1}):"
  )
  print(
      f"Dica: digite os {n} números de cada linha SEPARADOS POR ESPAÇO e"
      " aperte Enter."
  )

  # lê uma linha de cada vez, de 0 até n - 1
  for i in range(n):
    while True:
      try:
        # lê a linha e separa os números pelos espaços
        entrada = input(f"  Linha {i + 1}: ").strip().split()

        # confere se o usuário digitou exatamente 'n' números nessa linha
        if len(entrada) != n:
          print(
              f"  [AVISO] Você digitou {len(entrada)} número(s), mas a matriz é"
              f" {n}x{n}. Tente essa linha de novo!"
          )
          continue

        # converte para inteiro e aplica (% m) para garantir que fique dentro de Z_m
        linha = [int(valor) % m for valor in entrada]
        matriz.append(linha)
        break

      except ValueError:
        # evita que o programa trave se o usuário digitar letra ou símbolo
        print(
            "  [AVISO] Digite apenas números inteiros separados por espaço!"
        )

  return matriz


def gerar_matriz_chave_valida(n, m):  # gera automaticamente uma matriz n x n válida para facilitar os testes
  print(f"\nSorteando uma matriz {n}x{n} invertível em módulo {m}...")

  # contador de tentativas até achar uma matriz válida
  tentativas = 0

  while True:
    tentativas += 1
    matriz_candidata = []

    # monta uma matriz n x n sorteando números entre 0 e m - 1
    for i in range(n):
      linha = []
      for j in range(n):
        linha.append(random.randint(0, m - 1))
      matriz_candidata.append(linha)

    # testa se a matriz sorteada é invertível em módulo m
    det = calcular_determinante(matriz_candidata)
    mdc = calcular_mdc(det, m)

    # se o determinante não for zero e o mdc com m for 1, a chave é válida
    if det != 0 and mdc == 1:
      print(f"[SUCESSO!] Matriz válida encontrada na {tentativas}ª tentativa!")
      return matriz_candidata


def validar_chave(matriz, m):  # valida se a matriz-chave pode ser usada na cifra de hill
  print("\n--- VALIDANDO A MATRIZ-CHAVE ---")

  # calcula o determinante da matriz
  det = calcular_determinante(matriz)
  print(f"1. Determinante calculado: det(K) = {det}")

  # verifica o mdc entre o determinante e o módulo m
  mdc = calcular_mdc(det, m)
  print(f"2. Verificando se são coprimos: MDC({det}, {m}) = {mdc}")

  # o determinante não pode ser zero e o mdc precisa ser igual a 1
  if det != 0 and mdc == 1:
    print(
        "[DEU CERTO!] A matriz é invertível em módulo"
        f" {m} (MDC == 1). Chave aprovada!"
    )
    return True, det
  else:
    # mostra o motivo caso a matriz não tenha inversa modular
    print("[ERRO! MATRIZ INVÁLIDA] Essa matriz NÃO possui inversa modular!")
    if det == 0:
      print(
          "Motivo: O determinante deu 0 (matriz singular, não tem como"
          " inverter)."
      )
    else:
      print(
          f"Motivo: O determinante ({det}) e o módulo ({m}) têm divisor comum"
          f" ({mdc} != 1)."
      )
    print(
        "Se cifrarmos uma mensagem com essa chave, será impossível decifrar"
        " depois.\n"
    )
    return False, det


# parâmetros opcionais det, inv_det e adjunta evitam recalcular Laplace (O(n!)) duas vezes
def calcular_inversa_modular(matriz, m, det=None, inv_det=None, adjunta=None):  # monta a matriz inversa K^-1 para usar na decifragem
  if det is None:
    det = calcular_determinante(matriz)

  # acha o inverso multiplicativo do determinante em módulo m (se ainda não tiver sido calculado)
  if inv_det is None:
    inv_det = inverso_modular(det, m)

  if inv_det is None:
    return None

  # calcula a matriz adjunta (cofatores transpostos) apenas se não tiver sido fornecida
  if adjunta is None:
    adjunta = calcular_matriz_adjunta(matriz)

  n = len(matriz)

  # aplica a fórmula K^-1 = (det(K)^-1 * adj(K)) mod m
  inversa = []
  for i in range(n):
    nova_linha = []
    for j in range(n):
      valor = (inv_det * adjunta[i][j]) % m
      nova_linha.append(valor)
    inversa.append(nova_linha)

  return inversa


# TEXTO, PADDING, CIFRAGEM, DECIFRAGEM E INTEGRIDADE
def texto_para_numeros(texto, m):  # converte a mensagem de texto em uma lista de números dentro de Z_m
  numeros = []
  # guarda o texto limpo que vai entrar na cifra para comparar na integridade depois
  texto_valido = ""

  if m == 26:
    # para m = 26, aceita apenas letras maiúsculas de A (0) até Z (25)
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    texto = texto.upper()

    for caractere in texto:
      if caractere in alfabeto:
        numeros.append(alfabeto.index(caractere))
        texto_valido += caractere
      else:
        # avisa se algum caractere fora de A-Z foi ignorado
        print(
            f"[AVISO] Caractere '{caractere}' ignorado (no modo m = 26 apenas"
            " letras A-Z são aceitas)."
        )

  elif m == 29:
    # para m = 29, usa o alfabeto com espaço, ponto e interrogação (0 até 28)
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .?"
    texto = texto.upper()

    for caractere in texto:
      if caractere in alfabeto:
        numeros.append(alfabeto.index(caractere))
        texto_valido += caractere
      else:
        print(
            f"  [AVISO] Caractere '{caractere}' ignorado (fora do alfabeto de"
            " 29 símbolos)."
        )

  else:
    # valida se o código do caractere está em [0, m - 1] em vez de aplicar (% m) silenciosamente,
    # evitando corrupção de caracteres fora do intervalo e falsos positivos na verificação de integridade
    for caractere in texto:
      codigo = ord(caractere)
      if 0 <= codigo < m:
        numeros.append(codigo)
        texto_valido += caractere
      else:
        print(
            f"[AVISO] Caractere '{caractere}' (código {codigo}) ignorado (fora"
            f" do intervalo 0 até {m - 1} para m = {m})."
        )

  return numeros, texto_valido


def numeros_para_texto(numeros, m):  # transforma os números de volta em texto
  texto = ""

  if m == 26:
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for num in numeros:
      texto += alfabeto[num % 26]

  elif m == 29:
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ .?"
    for num in numeros:
      texto += alfabeto[num % 29]

  else:
    # para tabela ascii (m = 256) ou geral, converte o código numérico de volta em caractere
    for num in numeros:
      texto += chr(num % m)
  return texto


def aplicar_padding(numeros, n, m):  # completa o último bloco com caracteres extras caso não feche o tamanho n
  numeros_com_pad = list(numeros)

  # verifica quantos números sobram na divisão do tamanho da mensagem por 'n'
  resto = len(numeros_com_pad) % n

  # se o resto for 0, a mensagem já fecha blocos exatos de tamanho 'n'
  if resto == 0:
    return numeros_com_pad, 0

  # calcula quantos caracteres faltam para completar o último bloco
  faltam = n - resto

  # usa o caractere 'X' como preenchimento padrão (posição 23 no alfabeto, ou 88 na tabela ascii)
  if m == 26 or m == 29:
    valor_pad = 23  # letra 'X'
  else:
    valor_pad = 88 % m  # caractere 'X' na tabela ascii (ou equivalente em Z_m)

  # adiciona o preenchimento no final até fechar o múltiplo de 'n'
  for _ in range(faltam):
    numeros_com_pad.append(valor_pad)

  return numeros_com_pad, faltam


def processar_blocos(numeros, matriz, m):  # fatia os números em blocos de tamanho 'n' e aplica a matriz (cifra ou decifra)
  n = len(matriz)
  resultado_final = []
  historico_blocos = (
      []
  )  # guarda cada passo (bloco entrada -> bloco saída) para exibir no relatório

  # percorre a lista pulando de 'n' em 'n' posições
  for i in range(0, len(numeros), n):
    # pega um bloco de 'n' números
    bloco_entrada = numeros[i : i + n]

    # multiplica a matriz pelo bloco em módulo 'm'
    bloco_saida = multiplicar_matriz_vetor(matriz, bloco_entrada, m)

    resultado_final.extend(bloco_saida)

    # registra a transformação no histórico
    historico_blocos.append((bloco_entrada, bloco_saida))

  return resultado_final, historico_blocos


def verificar_integridade(mensagem_original, mensagem_decifrada):
  # valida se a decifragem recuperou o texto exato
  print("\n--- VERIFICAÇÃO DE INTEGRIDADE ---")
  print(f"Mensagem Original  : '{mensagem_original}'")
  print(f"Mensagem Decifrada : '{mensagem_decifrada}'")

  # compara as duas strings para garantir que nada se perdeu
  if mensagem_original == mensagem_decifrada:
    print(
        "[SUCESSO TOTAL!] Integridade confirmada: a mensagem decodificada é"
        " IDÊNTICA à original!"
    )
    return True
  else:
    print(
        "[ERRO DE INTEGRIDADE!] A mensagem decodificada ficou diferente da"
        " original!"
    )
    return False


# GERAÇÃO DE RELATÓRIO COMPLETO
def formatar_matriz_texto(matriz):  # formata uma matriz em texto alinhado para o relatório
  linhas_formatadas = []
  for linha in matriz:
    # alinha cada número à direita com 4 espaços para as colunas ficarem retas
    elementos = " ".join(f"{num:>4}" for num in linha)
    linhas_formatadas.append(f"    [ {elementos} ]")
  return "\n".join(linhas_formatadas)


def gerar_relatorio(
    m,
    n,
    K,
    det,
    inv_det,
    adjunta,
    K_inv,
    mensagem_base,
    qtd_pad,
    numeros_com_pad,
    hist_cifragem,
    texto_cifrado,
    hist_decifragem,
    mensagem_decifrada,
    integridade_ok,
):  # gera o relatório técnico exigido no pdf do projeto
  # monta as linhas do relatório explicando cada etapa matemática e o fluxo dos blocos
  linhas = []
  linhas.append(
      "======================================================================"
  )
  linhas.append(
      "       RELATÓRIO TÉCNICO - CIFRA DE HILL GENERALIZADA (ANEL Z_m)      "
  )
  linhas.append(
      "======================================================================"
  )

  # parâmetros gerais configurados pelo usuário
  linhas.append("\n1. PARÂMETROS DA CRIPTOGRAFIA")
  linhas.append(
      f"   - Módulo do alfabeto/conjunto (m): {m} (valores de 0 a {m - 1})"
  )
  linhas.append(
      f"   - Ordem da matriz / tamanho do bloco (n): {n} (matriz {n}x{n})"
  )
  linhas.append("\n   Matriz-Chave (K) escolhida:")
  linhas.append(formatar_matriz_texto(K))

  # detalhamento do cálculo da matriz inversa modular (K^-1)
  linhas.append(
      "\n----------------------------------------------------------------------"
  )
  linhas.append("2. CÁLCULO DA MATRIZ INVERSA MODULAR (K^-1)")
  linhas.append(
      "----------------------------------------------------------------------"
  )
  linhas.append(
      "   Para que a cifra seja reversível em aritmética modular Z_m, aplicamos:"
  )
  linhas.append("   Fórmula: K^-1 = ( det(K)^-1 * adj(K) ) mod m\n")

  linhas.append("   Passo A - Determinante da matriz K:")
  linhas.append(f"             det(K) = {det}")
  linhas.append(
      f"             Teste de coprimalidade: MDC({det}, {m}) = 1 (Chave"
      " válida!)\n"
  )

  linhas.append("   Passo B - Inverso multiplicativo modular do determinante:")
  linhas.append(
      f"             Buscamos um inteiro x tal que ({det} * x) mod {m} = 1."
  )
  linhas.append(
      f"             Pelo Algoritmo de Euclides Estendido: det(K)^-1 = {inv_det}"
  )
  linhas.append(
      f"             Prova real: ({det} * {inv_det}) mod {m} ="
      f" {(det * inv_det) % m}\n"
  )

  linhas.append(
      "   Passo C - Matriz Adjunta adj(K) (Matriz dos Cofatores Transposta):"
  )
  linhas.append(formatar_matriz_texto(adjunta))

  linhas.append(
      f"\n   Passo D - Multiplicação escalar por {inv_det} e redução módulo"
      f" {m}:"
  )
  linhas.append("             Matriz Inversa Modular resultante (K^-1):")
  linhas.append(formatar_matriz_texto(K_inv))

  # fluxo de transformação dos blocos de texto
  linhas.append(
      "\n----------------------------------------------------------------------"
  )
  linhas.append("3. FLUXO DE TRANSFORMAÇÃO DOS BLOCOS DE TEXTO")
  linhas.append(
      "----------------------------------------------------------------------"
  )
  linhas.append(f"   - Mensagem original considerada : '{mensagem_base}'")
  linhas.append(
      f"   - Padding aplicado              : {qtd_pad} caractere(s) extra(s)"
      f" para fechar blocos de tamanho {n}"
  )
  linhas.append(f"   - Vetor numérico com padding    : {numeros_com_pad}\n")

  linhas.append("   Cifragem (C_i = K * P_i mod m):")
  for idx, (bloco_p, bloco_c) in enumerate(hist_cifragem, start=1):
    linhas.append(
        f"     Bloco {idx}: P_{idx} = {bloco_p}  -->  [K * P_{idx} mod {m}] "
        f" -->  C_{idx} = {bloco_c}"
    )

  # usa repr() fora de m = 26/29 para evitar que caracteres de controle (\n, \r, \x00, \x1b)
  # quebrem a formatação do terminal e do arquivo relatorio_cifra_hill.txt
  if m in (26, 29):
    linhas.append(f"     Texto Cifrado gerado: '{texto_cifrado}'\n")
  else:
    linhas.append(f"     Texto Cifrado gerado (repr): {repr(texto_cifrado)}\n")

  linhas.append("   Decifragem (P_i = K^-1 * C_i mod m):")
  for idx, (bloco_c, bloco_p_rec) in enumerate(hist_decifragem, start=1):
    linhas.append(
        f"     Bloco {idx}: C_{idx} = {bloco_c}  -->  [K^-1 * C_{idx} mod {m}]"
        f"  -->  P_{idx} = {bloco_p_rec}"
    )

  # conclusão da integridade
  linhas.append(
      "\n----------------------------------------------------------------------"
  )
  linhas.append("4. RESULTADO DA VERIFICAÇÃO DE INTEGRIDADE")
  linhas.append(
      "----------------------------------------------------------------------"
  )
  linhas.append(f"   - Texto Original  : '{mensagem_base}'")
  linhas.append(f"   - Texto Decifrado : '{mensagem_decifrada}'")
  status = "APROVADA (100% idêntico)" if integridade_ok else "FALHOU"
  linhas.append(f"   - Status Final    : {status}")
  linhas.append(
      "======================================================================"
  )

  # junta todas as linhas em um único texto
  relatorio_completo = "\n".join(linhas)

  # exibe o relatório na tela no final da execução
  print("\n" + relatorio_completo)

  pasta_atual_do_codigo = os.path.dirname(os.path.abspath(__file__))

  caminho_completo = os.path.join(
      pasta_atual_do_codigo, "relatorio_cifra_hill.txt"
  )

  # garante que o txt do relatório fique na mesma pasta que o código
  with open(caminho_completo, "w", encoding="utf-8") as arquivo:
    arquivo.write(relatorio_completo)

  print(
      "\n[RELATÓRIO SALVO!] Arquivo gravado na mesma pasta do código:\n "
      f" {caminho_completo}"
  )


# INTERAÇÃO COM O USUÁRIO
if __name__ == "__main__":
  while True:
    print("---- CIFRA DE HILL GENERALIZADA ----")
    # solicita o módulo m e a ordem n validando as entradas
    while True:
      try:
        m = int(
            input(
                "Digite o módulo m (ex: 26 para alfabeto ou 256 para tabela"
                " ASCII): "
            )
        )
        if m < 2:
          print("[AVISO] O módulo m precisa ser maior ou igual a 2!")
          continue
        break
      except ValueError:
        print("[AVISO] Digite um número inteiro válido para o módulo m!")

    while True:
      try:
        n = int(
            input(
                "Digite a ordem n da matriz-chave (ex: 2, 3 para 3x3, 4 para"
                " 4x4): "
            )
        )
        if n < 1:
          print("[AVISO] A ordem n da matriz precisa ser pelo menos 1!")
          continue
        # limite de segurança para evitar travamento por complexidade fatorial O(n!) da expansão de Laplace
        if n > 6:
          print(
              "[AVISO] Para evitar lentidão excessiva no cálculo manual de"
              " determinantes (complexidade fatorial), escolha n entre 1 e 6!"
          )
          continue
        break
      except ValueError:
        print("[AVISO] Digite um número inteiro válido para a ordem n!")

    # escolhe entre digitar ou gerar a matriz-chave
    print("\nComo você deseja definir a matriz-chave K?")
    print("  [1] Digitar a matriz manualmente")
    print("  [2] Gerar uma matriz-chave válida automaticamente")

    # garante que o usuário escolha apenas 1 ou 2
    while True:
      opcao_chave = input("Escolha uma opção (1 ou 2): ").strip()
      if opcao_chave in ("1", "2"):
        break
      print("[AVISO] Digite apenas 1 ou 2!")

    if opcao_chave == "1":
      # continua pedindo até o usuário digitar uma matriz válida (modo manual)
      while True:
        K = ler_matriz_chave(n, m)
        valida, det = validar_chave(K, m)
        if valida:
          break
        print(">>> Por favor, insira uma nova matriz-chave válida:")
    else:
      # sorteia até achar uma válida e chama validar_chave para mostrar os dados na tela (modo automático)
      K = gerar_matriz_chave_valida(n, m)
      valida, det = validar_chave(K, m)

    # calcula os componentes da inversa modular sem duplicar o cálculo de determinante e adjunta
    inv_det = inverso_modular(det, m)
    adjunta = calcular_matriz_adjunta(K)
    # reaproveita det, inv_det e adjunta já calculados acima
    K_inv = calcular_inversa_modular(
        K, m, det=det, inv_det=inv_det, adjunta=adjunta
    )

    print("\nMatriz Chave Original (K):")
    for linha in K:
      print(" ", linha)

    print("\nMatriz Inversa Modular (K^-1):")
    for linha in K_inv:
      print(" ", linha)

    print()
    # lê a mensagem, aplica padding, cifra e decifra
    print("---- PROCESSAMENTO DA MENSAGEM (CIFRAGEM E DECIFRAGEM) ----")
    while True:
      mensagem_usuario = input("\nDigite a mensagem de texto que deseja cifrar: ")
      numeros_originais, mensagem_base = texto_para_numeros(mensagem_usuario, m)
      if len(numeros_originais) > 0:
        break
      print(
          "[AVISO] A mensagem precisa ter pelo menos 1 caractere válido para o"
          f" módulo m = {m}!"
      )

    tamanho_original = len(numeros_originais)
    numeros_com_pad, qtd_pad = aplicar_padding(numeros_originais, n, m)

    # cifra com K e decifra com K^-1
    numeros_cifrados, hist_cifragem = processar_blocos(numeros_com_pad, K, m)
    texto_cifrado = numeros_para_texto(numeros_cifrados, m)

    numeros_decifrados_com_pad, hist_decifragem = processar_blocos(
        numeros_cifrados, K_inv, m
    )
    numeros_decifrados = numeros_decifrados_com_pad[:tamanho_original]
    mensagem_decifrada = numeros_para_texto(numeros_decifrados, m)

    # verificação de integridade
    integridade_ok = verificar_integridade(mensagem_base, mensagem_decifrada)

    # geração do relatório explicativo
    gerar_relatorio(
        m,
        n,
        K,
        det,
        inv_det,
        adjunta,
        K_inv,
        mensagem_base,
        qtd_pad,
        numeros_com_pad,
        hist_cifragem,
        texto_cifrado,
        hist_decifragem,
        mensagem_decifrada,
        integridade_ok,
    )

    # menu ao final para reiniciar (1) ou encerrar o programa (Enter vazio)
    while True:
      opcao_reiniciar = input(
          "\nDigite 1 para reiniciar com outros valores ou pressione Enter para sair: "
      ).strip()
      if opcao_reiniciar in ("", "1"):
        break
      print("[AVISO] Opção inválida! Digite 1 para reiniciar ou apenas Enter para sair.")

    if opcao_reiniciar == "":
      print("Encerrando o programa...")
      break
    print("\n" + "=" * 70 + "\n")