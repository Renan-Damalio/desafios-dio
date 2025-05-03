from abc import ABC, abstractmethod
from datetime import datetime, date
import textwrap

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar(self)

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar(self)

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar(self, transacao: Transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    def exibir(self, saldo: float):
        print("\n================ EXTRATO ================")
        if not self.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for t in self.transacoes:
                print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
        print(f"\nSaldo:\t\tR$ {saldo:.2f}")
        print("==========================================")

class Conta:
    def __init__(self, numero: int, cliente, agencia: str = "0001"):
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.saldo = 0.0
        self.historico = Historico()
        self.limite = 500.0
        self.limite_saques = 3
        self.numero_saques = 0

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            print("\n@@@ Valor inválido para saque. @@@")
        elif valor > self.saldo:
            print("\n@@@ Saldo insuficiente. @@@")
        elif valor > self.limite:
            print("\n@@@ Limite de saque excedido. @@@")
        elif self.numero_saques >= self.limite_saques:
            print("\n@@@ Número máximo de saques atingido. @@@")
        else:
            self.saldo -= valor
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
            return True
        return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self.saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Valor inválido para depósito. @@@")
            return False

class Cliente:
    def __init__(self, nome: str, cpf: str, data_nascimento: date, endereco: str):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        if conta in self.contas:
            transacao.registrar(conta)
        else:
            print("\n@@@ Conta não pertence ao cliente. @@@")

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

clientes = []
contas = []

def filtrar_cliente(cpf: str):
    return next((c for c in clientes if c.cpf == cpf), None)

def criar_cliente():
    cpf = input("CPF: ")
    if filtrar_cliente(cpf):
        print("\n@@@ CPF já cadastrado. @@@")
        return
    nome = input("Nome: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço: ")
    cliente = Cliente(nome, cpf, datetime.strptime(nascimento, "%d-%m-%Y").date(), endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta():
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf)
    if not cliente:
        print("\n@@@ Cliente não encontrado. @@@")
        return
    numero = len(contas) + 1
    conta = Conta.nova_conta(cliente, numero)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")

def listar_contas():
    for conta in contas:
        print("=" * 100)
        print(f"Agência:\t{conta.agencia}")
        print(f"C/C:\t\t{conta.numero}")
        print(f"Titular:\t{conta.cliente.nome}")

def main():
    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("CPF: ")
            cliente = filtrar_cliente(cpf)
            if not cliente:
                print("\n@@@ Cliente não encontrado. @@@")
                continue
            valor = float(input("Valor do depósito: "))
            cliente.realizar_transacao(cliente.contas[0], Deposito(valor))

        elif opcao == "s":
            cpf = input("CPF: ")
            cliente = filtrar_cliente(cpf)
            if not cliente:
                print("\n@@@ Cliente não encontrado. @@@")
                continue
            valor = float(input("Valor do saque: "))
            cliente.realizar_transacao(cliente.contas[0], Saque(valor))

        elif opcao == "e":
            cpf = input("CPF: ")
            cliente = filtrar_cliente(cpf)
            if not cliente:
                print("\n@@@ Cliente não encontrado. @@@")
                continue
            conta = cliente.contas[0]
            conta.historico.exibir(conta.saldo)

        elif opcao == "nu":
            criar_cliente()

        elif opcao == "nc":
            criar_conta()

        elif opcao == "lc":
            listar_contas()

        elif opcao == "q":
            break

        else:
            print("Operação inválida, selecione novamente.")

main()
