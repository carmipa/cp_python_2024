import os
from colorama import Fore, Style, init
import oracledb
import logging
from datetime import datetime

# Inicializa o colorama para uso das cores
init(autoreset=True)

# Configuração de logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def conectar_BD():
    """
    Estabelece conexão com o banco de dados Oracle.
    Retorna a conexão e o cursor.
    """
    try:
        dsn = oracledb.makedsn("localhost", 1521, service_name="XEPDB1")
        conexao = oracledb.connect(user="paulo", password="12345", dsn=dsn)
        inst_SQL = conexao.cursor()
        print(
            Fore.GREEN + "**************************************** CONEXÃO BEM-SUCEDIDA ****************************************" + Style.RESET_ALL)
        logging.info("Conexão ao banco de dados estabelecida com sucesso.")
        return conexao, inst_SQL
    except oracledb.DatabaseError as e:
        error, = e.args
        print(
            Fore.RED + "**************************************** ERRO NA CONEXÃO ****************************************" + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao conectar ao banco de dados: {error.message}")
        return None, None


def exibir_menu_principal():
    """
    Exibe o menu principal do sistema.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(
        Fore.BLUE + "**************************************** MENU PRINCIPAL ****************************************" + Style.RESET_ALL)
    print(Fore.BLUE + "* " + Style.RESET_ALL + "1 - Cadastro de Cargos")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "2 - Cadastro de Funcionários")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "3 - Relatório de Funcionários por Cargo")
    print(
        Fore.BLUE + "* " + Style.RESET_ALL + "4 - Relatório de Desenvolvedores Front-End com Salário entre 8000 e 12000")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "5 - Relatório de Funcionários de TI com mais de 21 anos")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "6 - Sair do Sistema")
    print(
        Fore.BLUE + "**************************************************************************************" + Style.RESET_ALL)


def print_cargo(cargo):
    """
    Imprime os detalhes de um cargo com formatação.
    """
    print(
        Fore.YELLOW + "----------------------------------------------------------------------------------------------------" + Style.RESET_ALL)
    print(Fore.CYAN + f"ID do Cargo...........: " + Style.RESET_ALL + f"{cargo[0]}")
    print(Fore.CYAN + f"Descrição do Cargo....: " + Style.RESET_ALL + f"{cargo[1]}")
    print(Fore.CYAN + f"Departamento..........: " + Style.RESET_ALL + f"{cargo[2]}")
    print(
        Fore.YELLOW + "----------------------------------------------------------------------------------------------------" + Style.RESET_ALL)


def print_funcionario(funcionario):
    """
    Imprime os detalhes de um funcionário com formatação.
    """
    print(
        Fore.YELLOW + "----------------------------------------------------------------------------------------------------" + Style.RESET_ALL)
    print(Fore.CYAN + "ID do Funcionário.......: " + Style.RESET_ALL + f"{funcionario[0]}")
    print(Fore.CYAN + "CPF....................: " + Style.RESET_ALL + f"{funcionario[1]}")
    print(Fore.CYAN + "Nome...................: " + Style.RESET_ALL + f"{funcionario[2]}")
    print(Fore.CYAN + "Salário................: " + Style.RESET_ALL + f"{funcionario[3]}")
    print(Fore.CYAN + "Idade..................: " + Style.RESET_ALL + f"{funcionario[4]}")
    print(Fore.CYAN + "Cargo..................: " + Style.RESET_ALL + f"{funcionario[5]}")
    print(Fore.CYAN + "Departamento............: " + Style.RESET_ALL + f"{funcionario[6]}")
    print(
        Fore.YELLOW + "----------------------------------------------------------------------------------------------------" + Style.RESET_ALL)


def crud_cargos(conexao, inst_SQL):
    """
    Realiza operações CRUD na tabela 'cargos'.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.MAGENTA + "************ CRUD - CARGOS ************" + Style.RESET_ALL)
        print("1 - Inserir novo cargo")
        print("2 - Alterar um cargo")
        print("3 - Excluir um cargo")
        print("4 - Relatório de todos os cargos")
        print("5 - Voltar ao Menu Principal")
        try:
            opcao = int(input(Fore.BLUE + "Digite a opção desejada: " + Style.RESET_ALL))
            if opcao == 1:
                inserir_cargo(conexao, inst_SQL)
            elif opcao == 2:
                alterar_cargo(conexao, inst_SQL)
            elif opcao == 3:
                excluir_cargo(conexao, inst_SQL)
            elif opcao == 4:
                listar_cargos(inst_SQL)
            elif opcao == 5:
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Entrada inválida. Por favor, digite um número." + Style.RESET_ALL)
        input(Fore.CYAN + "Pressione Enter para continuar..." + Style.RESET_ALL)


def inserir_cargo(conexao, inst_SQL):
    """
    Insere um novo registro na tabela 'cargos'.
    """
    try:
        descricao = input("Digite a descrição do cargo: ").strip()
        departamento = input("Digite o departamento do cargo: ").strip()
        str_consulta = """
            INSERT INTO cargos (cargo_descricao, cargo_departamento)
            VALUES (:descricao, :departamento)
        """
        inst_SQL.execute(str_consulta, {'descricao': descricao, 'departamento': departamento})
        conexao.commit()
        print(Fore.GREEN + "Cargo inserido com sucesso!" + Style.RESET_ALL)
        logging.info(f"Novo cargo inserido: {descricao}, Departamento: {departamento}")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao inserir cargo." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao inserir cargo: {error.message}")


def alterar_cargo(conexao, inst_SQL):
    """
    Altera um registro existente na tabela 'cargos'.
    """
    try:
        listar_cargos(inst_SQL)
        cargo_id = int(input("Digite o ID do cargo que deseja alterar: "))
        nova_descricao = input("Digite a nova descrição do cargo: ").strip()
        novo_departamento = input("Digite o novo departamento do cargo: ").strip()
        str_consulta = """
            UPDATE cargos
            SET cargo_descricao = :descricao,
                cargo_departamento = :departamento
            WHERE cargo_id = :id
        """
        inst_SQL.execute(str_consulta, {'descricao': nova_descricao, 'departamento': novo_departamento, 'id': cargo_id})
        if inst_SQL.rowcount == 0:
            print(Fore.YELLOW + "Nenhum cargo encontrado com o ID fornecido." + Style.RESET_ALL)
        else:
            conexao.commit()
            print(Fore.GREEN + "Cargo atualizado com sucesso!" + Style.RESET_ALL)
            logging.info(
                f"Cargo atualizado: ID {cargo_id}, Nova Descrição: {nova_descricao}, Novo Departamento: {novo_departamento}")
    except ValueError:
        print(Fore.RED + "Entrada inválida. ID deve ser um número." + Style.RESET_ALL)
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao atualizar cargo." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao atualizar cargo: {error.message}")


def excluir_cargo(conexao, inst_SQL):
    """
    Exclui um registro da tabela 'cargos'.
    """
    try:
        listar_cargos(inst_SQL)
        cargo_id = int(input("Digite o ID do cargo que deseja excluir: "))
        confirmacao = input(f"Tem certeza que deseja excluir o cargo ID {cargo_id}? (s/n): ").strip().lower()
        if confirmacao != 's':
            print("Operação cancelada.")
            return
        str_consulta = """
            DELETE FROM cargos
            WHERE cargo_id = :id
        """
        inst_SQL.execute(str_consulta, {'id': cargo_id})
        if inst_SQL.rowcount == 0:
            print(Fore.YELLOW + "Nenhum cargo encontrado com o ID fornecido." + Style.RESET_ALL)
        else:
            conexao.commit()
            print(Fore.GREEN + "Cargo excluído com sucesso!" + Style.RESET_ALL)
            logging.info(f"Cargo excluído: ID {cargo_id}")
    except ValueError:
        print(Fore.RED + "Entrada inválida. ID deve ser um número." + Style.RESET_ALL)
    except oracledb.IntegrityError:
        print(Fore.RED + "Não é possível excluir este cargo pois ele está associado a funcionários." + Style.RESET_ALL)
        logging.error(f"Tentativa de excluir cargo ID {cargo_id} que está associado a funcionários.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao excluir cargo." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao excluir cargo: {error.message}")


def listar_cargos(inst_SQL):
    """
    Lista todos os registros da tabela 'cargos'.
    """
    try:
        str_consulta = """
            SELECT cargo_id, cargo_descricao, cargo_departamento
            FROM cargos
            ORDER BY cargo_id
        """
        inst_SQL.execute(str_consulta)
        cargos = inst_SQL.fetchall()
        if not cargos:
            print(Fore.YELLOW + "Nenhum cargo encontrado." + Style.RESET_ALL)
            return
        print(
            Fore.YELLOW + "**************************************** LISTA DE CARGOS ****************************************" + Style.RESET_ALL)
        for cargo in cargos:
            print_cargo(cargo)
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao listar cargos." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao listar cargos: {error.message}")


def crud_funcionarios(conexao, inst_SQL):
    """
    Realiza operações CRUD na tabela 'funcionarios'.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.MAGENTA + "************ CRUD - FUNCIONÁRIOS ************" + Style.RESET_ALL)
        print("1 - Inserir novo funcionário")
        print("2 - Alterar um funcionário")
        print("3 - Excluir um funcionário")
        print("4 - Relatório de todos os funcionários")
        print("5 - Voltar ao Menu Principal")
        try:
            opcao = int(input(Fore.BLUE + "Digite a opção desejada: " + Style.RESET_ALL))
            if opcao == 1:
                inserir_funcionario(conexao, inst_SQL)
            elif opcao == 2:
                alterar_funcionario(conexao, inst_SQL)
            elif opcao == 3:
                excluir_funcionario(conexao, inst_SQL)
            elif opcao == 4:
                listar_funcionarios(inst_SQL)
            elif opcao == 5:
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Entrada inválida. Por favor, digite um número." + Style.RESET_ALL)
        input(Fore.CYAN + "Pressione Enter para continuar..." + Style.RESET_ALL)


def inserir_funcionario(conexao, inst_SQL):
    """
    Insere um novo registro na tabela 'funcionarios'.
    """
    try:
        cpf = input("Digite o CPF do funcionário (apenas números): ").strip()
        if not cpf.isdigit():
            print(Fore.RED + "CPF inválido. Deve conter apenas números." + Style.RESET_ALL)
            return
        nome = input("Digite o nome do funcionário: ").strip()
        salario = float(input("Digite o salário do funcionário: "))
        idade = int(input("Digite a idade do funcionário: "))
        listar_cargos(inst_SQL)
        cargo_id = int(input("Digite o ID do cargo do funcionário: "))

        # Verifica se o cargo_id existe
        str_verifica_cargo = "SELECT COUNT(*) FROM cargos WHERE cargo_id = :id"
        inst_SQL.execute(str_verifica_cargo, {'id': cargo_id})
        count = inst_SQL.fetchone()[0]
        if count == 0:
            print(Fore.RED + "Cargo ID não encontrado. Operação cancelada." + Style.RESET_ALL)
            return

        # Insere o funcionário
        str_insert_funcionario = """
            INSERT INTO funcionarios (funcionario_cpf, funcionario_nome, funcionario_salario, funcionario_integer)
            VALUES (:cpf, :nome, :salario, :idade)
            RETURNING funcionario_id INTO :id
        """
        funcionario_id = conexao.cursor().var(oracledb.NUMBER)
        inst_SQL.execute(str_insert_funcionario,
                         {'cpf': cpf, 'nome': nome, 'salario': salario, 'idade': idade, 'id': funcionario_id})
        novo_id = funcionario_id.getvalue()[0]
        # Insere na tabela d_f
        str_insert_df = """
            INSERT INTO d_f (cargos_cargo_id, funcionarios_funcionario_id)
            VALUES (:cargo_id, :func_id)
        """
        inst_SQL.execute(str_insert_df, {'cargo_id': cargo_id, 'func_id': novo_id})
        conexao.commit()
        print(Fore.GREEN + f"Funcionário inserido com sucesso! ID: {novo_id}" + Style.RESET_ALL)
        logging.info(
            f"Novo funcionário inserido: ID {novo_id}, CPF {cpf}, Nome {nome}, Salário {salario}, Idade {idade}, Cargo ID {cargo_id}")
    except ValueError:
        print(
            Fore.RED + "Entrada inválida. Certifique-se de que CPF é numérico, salário é um número e idade é um inteiro." + Style.RESET_ALL)
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao inserir funcionário." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao inserir funcionário: {error.message}")


def alterar_funcionario(conexao, inst_SQL):
    """
    Altera um registro existente na tabela 'funcionarios'.
    """
    try:
        listar_funcionarios(inst_SQL)
        funcionario_id = int(input("Digite o ID do funcionário que deseja alterar: "))

        # Verifica se o funcionário existe
        str_verifica_func = "SELECT COUNT(*) FROM funcionarios WHERE funcionario_id = :id"
        inst_SQL.execute(str_verifica_func, {'id': funcionario_id})
        count = inst_SQL.fetchone()[0]
        if count == 0:
            print(Fore.YELLOW + "Nenhum funcionário encontrado com o ID fornecido." + Style.RESET_ALL)
            return

        cpf = input("Digite o novo CPF do funcionário (apenas números): ").strip()
        if not cpf.isdigit():
            print(Fore.RED + "CPF inválido. Deve conter apenas números." + Style.RESET_ALL)
            return
        nome = input("Digite o novo nome do funcionário: ").strip()
        salario = float(input("Digite o novo salário do funcionário: "))
        idade = int(input("Digite a nova idade do funcionário: "))
        listar_cargos(inst_SQL)
        cargo_id = int(input("Digite o novo ID do cargo do funcionário: "))

        # Verifica se o cargo_id existe
        str_verifica_cargo = "SELECT COUNT(*) FROM cargos WHERE cargo_id = :id"
        inst_SQL.execute(str_verifica_cargo, {'id': cargo_id})
        count_cargo = inst_SQL.fetchone()[0]
        if count_cargo == 0:
            print(Fore.RED + "Cargo ID não encontrado. Operação cancelada." + Style.RESET_ALL)
            return

        # Atualiza o funcionário
        str_update_funcionario = """
            UPDATE funcionarios
            SET funcionario_cpf = :cpf,
                funcionario_nome = :nome,
                funcionario_salario = :salario,
                funcionario_integer = :idade
            WHERE funcionario_id = :id
        """
        inst_SQL.execute(str_update_funcionario,
                         {'cpf': cpf, 'nome': nome, 'salario': salario, 'idade': idade, 'id': funcionario_id})

        # Atualiza a tabela d_f
        str_update_df = """
            UPDATE d_f
            SET cargos_cargo_id = :cargo_id
            WHERE funcionarios_funcionario_id = :func_id
        """
        inst_SQL.execute(str_update_df, {'cargo_id': cargo_id, 'func_id': funcionario_id})

        conexao.commit()
        print(Fore.GREEN + "Funcionário atualizado com sucesso!" + Style.RESET_ALL)
        logging.info(
            f"Funcionário atualizado: ID {funcionario_id}, CPF {cpf}, Nome {nome}, Salário {salario}, Idade {idade}, Cargo ID {cargo_id}")
    except ValueError:
        print(
            Fore.RED + "Entrada inválida. Certifique-se de que IDs são numéricos, salário é um número e idade é um inteiro." + Style.RESET_ALL)
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao atualizar funcionário." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao atualizar funcionário: {error.message}")


def excluir_funcionario(conexao, inst_SQL):
    """
    Exclui um registro da tabela 'funcionarios'.
    """
    try:
        listar_funcionarios(inst_SQL)
        funcionario_id = int(input("Digite o ID do funcionário que deseja excluir: "))
        confirmacao = input(
            f"Tem certeza que deseja excluir o funcionário ID {funcionario_id}? (s/n): ").strip().lower()
        if confirmacao != 's':
            print("Operação cancelada.")
            return

        # Exclui da tabela d_f primeiro devido à restrição de chave estrangeira
        str_delete_df = """
            DELETE FROM d_f
            WHERE funcionarios_funcionario_id = :id
        """
        inst_SQL.execute(str_delete_df, {'id': funcionario_id})

        # Exclui o funcionário
        str_delete_funcionario = """
            DELETE FROM funcionarios
            WHERE funcionario_id = :id
        """
        inst_SQL.execute(str_delete_funcionario, {'id': funcionario_id})
        if inst_SQL.rowcount == 0:
            print(Fore.YELLOW + "Nenhum funcionário encontrado com o ID fornecido." + Style.RESET_ALL)
        else:
            conexao.commit()
            print(Fore.GREEN + "Funcionário excluído com sucesso!" + Style.RESET_ALL)
            logging.info(f"Funcionário excluído: ID {funcionario_id}")
    except ValueError:
        print(Fore.RED + "Entrada inválida. ID deve ser um número." + Style.RESET_ALL)
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao excluir funcionário." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao excluir funcionário: {error.message}")


def listar_funcionarios(inst_SQL):
    """
    Lista todos os registros da tabela 'funcionarios' com seus respectivos cargos.
    """
    try:
        str_consulta = """
            SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_integer, c.cargo_descricao, c.cargo_departamento
            FROM funcionarios f
            JOIN d_f df ON f.funcionario_id = df.funcionarios_funcionario_id
            JOIN cargos c ON df.cargos_cargo_id = c.cargo_id
            ORDER BY f.funcionario_id
        """
        inst_SQL.execute(str_consulta)
        funcionarios = inst_SQL.fetchall()
        if not funcionarios:
            print(Fore.YELLOW + "Nenhum funcionário encontrado." + Style.RESET_ALL)
            return
        print(
            Fore.YELLOW + "************************************** LISTA DE FUNCIONÁRIOS **************************************" + Style.RESET_ALL)
        for func in funcionarios:
            print_funcionario(func)
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao listar funcionários." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao listar funcionários: {error.message}")


def relatorio_funcionarios_por_cargo(inst_SQL):
    """
    Gera o relatório de funcionários por cargo escolhido pelo usuário.
    """
    try:
        cargo = input("Digite o nome do cargo: ").strip()
        print(
            Fore.BLUE + f"**************************************** RELATÓRIO DE FUNCIONÁRIOS POR CARGO: {cargo.upper()} ****************************************" + Style.RESET_ALL)
        str_consulta = """
            SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_integer, c.cargo_descricao, c.cargo_departamento
            FROM funcionarios f
            JOIN d_f df ON f.funcionario_id = df.funcionarios_funcionario_id
            JOIN cargos c ON df.cargos_cargo_id = c.cargo_id
            WHERE c.cargo_descricao = :cargo
            ORDER BY f.funcionario_id
        """
        inst_SQL.execute(str_consulta, {'cargo': cargo})
        funcionarios = inst_SQL.fetchall()
        if not funcionarios:
            print(Fore.YELLOW + "Nenhum funcionário encontrado para o cargo especificado." + Style.RESET_ALL)
            return
        for func in funcionarios:
            print_funcionario(func)
        logging.info(f"Relatório de funcionários por cargo '{cargo}' gerado com sucesso.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(
            Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao gerar relatório de funcionários por cargo: {error.message}")


def relatorio_funcionarios_frontend_salario(inst_SQL):
    """
    Gera o relatório de desenvolvedores Front-End com salário entre 8000 e 12000.
    """
    try:
        print(
            Fore.BLUE + "**************************************** RELATÓRIO DE DESENVOLVEDORES FRONT-END COM SALÁRIO ENTRE 8000 E 12000 ****************************************" + Style.RESET_ALL)
        str_consulta = """
            SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_integer, c.cargo_descricao, c.cargo_departamento
            FROM funcionarios f
            JOIN d_f df ON f.funcionario_id = df.funcionarios_funcionario_id
            JOIN cargos c ON df.cargos_cargo_id = c.cargo_id
            WHERE c.cargo_descricao = 'Desenvolvedor Front End' 
            AND f.funcionario_salario BETWEEN 8000 AND 12000
            ORDER BY f.funcionario_id
        """
        inst_SQL.execute(str_consulta)
        funcionarios = inst_SQL.fetchall()
        if not funcionarios:
            print(
                Fore.YELLOW + "Nenhum desenvolvedor Front-End encontrado com o salário especificado." + Style.RESET_ALL)
            return
        for func in funcionarios:
            print_funcionario(func)
        logging.info("Relatório de desenvolvedores front-end com salário entre 8000 e 12000 gerado com sucesso.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(
            Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(
            f"Erro ao gerar relatório de desenvolvedores front-end com salário entre 8000 e 12000: {error.message}")


def relatorio_funcionarios_ti_maior_21(inst_SQL):
    """
    Gera o relatório de funcionários do departamento de TI com mais de 21 anos.
    """
    try:
        print(
            Fore.BLUE + "**************************************** RELATÓRIO DE FUNCIONÁRIOS DE TI COM MAIS DE 21 ANOS ****************************************" + Style.RESET_ALL)
        str_consulta = """
            SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_integer, c.cargo_descricao, c.cargo_departamento
            FROM funcionarios f
            JOIN d_f df ON f.funcionario_id = df.funcionarios_funcionario_id
            JOIN cargos c ON df.cargos_cargo_id = c.cargo_id
            WHERE c.cargo_departamento = 'TI'
            AND f.funcionario_integer > 21
            ORDER BY f.funcionario_id
        """
        inst_SQL.execute(str_consulta)
        funcionarios = inst_SQL.fetchall()
        if not funcionarios:
            print(Fore.YELLOW + "Nenhum funcionário de TI com mais de 21 anos encontrado." + Style.RESET_ALL)
            return
        for func in funcionarios:
            print_funcionario(func)
        logging.info("Relatório de funcionários de TI com mais de 21 anos gerado com sucesso.")
    except oracledb.DatabaseError as e:
        error, = e.args
        print(
            Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao gerar relatório de funcionários de TI com mais de 21 anos: {error.message}")


def main():
    """
    Função principal que executa o programa.
    """
    conexao, inst_SQL = conectar_BD()
    if not conexao:
        return

    while True:
        exibir_menu_principal()
        try:
            opc_principal = int(input(Fore.BLUE + "DIGITE A OPÇÃO DESEJADA: " + Style.RESET_ALL))
            match opc_principal:
                case 1:
                    crud_cargos(conexao, inst_SQL)
                case 2:
                    crud_funcionarios(conexao, inst_SQL)
                case 3:
                    relatorio_funcionarios_por_cargo(inst_SQL)
                case 4:
                    relatorio_funcionarios_frontend_salario(inst_SQL)
                case 5:
                    relatorio_funcionarios_ti_maior_21(inst_SQL)
                case 6:
                    print(
                        Fore.RED + "**************************************** SAINDO DO SISTEMA ****************************************" + Style.RESET_ALL)
                    logging.info("Encerrando o sistema.")
                    inst_SQL.close()
                    conexao.close()
                    break
                case _:
                    print(
                        Fore.RED + "**************************************** OPÇÃO INCORRETA. DIGITE UMA OPÇÃO VÁLIDA! ****************************************" + Style.RESET_ALL)
                    logging.warning("Opção incorreta inserida no menu principal.")
        except ValueError:
            print(
                Fore.RED + "**************************************** ERRO: DIGITE UM NÚMERO VÁLIDO! ****************************************" + Style.RESET_ALL)
            logging.warning("Erro ao converter a entrada para número no menu principal.")
        except Exception as e:
            print(
                Fore.RED + "**************************************** OCORREU UM ERRO DESCONHECIDO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + str(e) + Style.RESET_ALL)
            logging.error(f"Erro desconhecido no menu principal: {str(e)}")
        input(Fore.CYAN + "Pressione Enter para continuar..." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
