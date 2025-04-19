

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("Usuário criado com sucesso!")

def excluir_usuario(usuarios, contas):
    cpf = input("Informe o CPF do usuário que deseja excluir: ")

    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado.")
        return

    contas_do_usuario = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]

    if contas_do_usuario:
        print("Usuário possui conta(s) ativa(s) e não pode ser excluído.")
        return

    usuarios.remove(usuario)
    print("Usuário excluído com sucesso!")



def gerar_numero_conta(contas):
    if not contas:
        return 1
    numeros_existentes = [conta["numero_conta"] for conta in contas]
    return max(numeros_existentes) + 1

def criar_conta(agencia, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado. Crie o usuário antes.")
        return

    numero_conta = gerar_numero_conta(contas)

    contas.append({
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
    })

    print(f"Conta criada com sucesso! Agência: {agencia}, Conta: {numero_conta}")

def encerrar_conta(contas):
    numero_conta = input("Informe o número da conta a ser encerrada: ")
    agencia = input("Informe a agência da conta: ")

    conta = next(
        (conta for conta in contas if conta["numero_conta"] == int(numero_conta) and conta["agencia"] == agencia),
        None
    )

    if not conta:
        print("Conta não encontrada.")
        return

    if conta["saldo"] > 0:
        print("Conta com saldo disponível. A conta não pode ser encerrada.")
        return

    contas.remove(conta)
    print("Conta encerrada com sucesso!")


def depositar(contas):
    numero_conta = int(input("Informe o número da conta para depósito: "))
    conta = localizar_conta(numero_conta, contas)

    if not conta:
        print("Conta não encontrada.")
        return

    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso.")
    else:
        print("Operação falhou! O valor informado é inválido.")

def sacar(contas, limite, limite_saques, saques_por_conta):
    numero_conta = int(input("Informe o número da conta para saque: "))
    conta = localizar_conta(numero_conta, contas)

    if not conta:
        print("Conta não encontrada.")
        return

    valor = float(input("Informe o valor do saque: "))
    numero_saques = saques_por_conta.get(numero_conta, 0)

    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        saques_por_conta[numero_conta] = numero_saques + 1
        print("Saque realizado com sucesso.")
    else:
        print("Operação falhou! O valor informado é inválido.")

def exibir_extrato(contas):
    numero_conta = int(input("Informe o número da conta para ver o extrato: "))
    conta = localizar_conta(numero_conta, contas)

    if not conta:
        print("Conta não encontrada.")
        return

    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("==========================================")

def localizar_conta(numero_conta, contas):
    return next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)



def menu():
    return input("""
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[ru] Remover Usuário
[rc] Encerrar Conta
[q] Sair

=> """)



def main():
    limite = 500
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    saques_por_conta = {}
    AGENCIA = "0001"

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(contas)

        elif opcao == "s":
            sacar(contas, limite, LIMITE_SAQUES, saques_por_conta)

        elif opcao == "e":
            exibir_extrato(contas)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            criar_conta(AGENCIA, usuarios, contas)

        elif opcao == "ru":
            excluir_usuario(usuarios, contas)

        elif opcao == "rc":
            encerrar_conta(contas)

        elif opcao == "q":
            print("Saindo... Até a próxima!")
            break

        else:
            print("Operação inválida. Tente novamente.")

# Executa o programa
main()
