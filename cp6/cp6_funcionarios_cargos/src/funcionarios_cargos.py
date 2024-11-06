import os
import json
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
        dsn = oracledb.makedsn("oracle.fiap.com.br", 1521, service_name="ORCL")
        conexao = oracledb.connect(user="RM557881", password="121079", dsn=dsn)
        inst_SQL = conexao.cursor()
        print(Fore.GREEN + "**************************************** CONEXÃO BEM-SUCEDIDA ****************************************" + Style.RESET_ALL)
        logging.info("Conexão ao banco de dados estabelecida com sucesso.")
        return conexao, inst_SQL
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "**************************************** ERRO NA CONEXÃO ****************************************" + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao conectar ao banco de dados: {error.message}")
        return None, None

def exibir_menu_principal():
    """
    Exibe o menu principal do sistema.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.BLUE + "**************************************** MENU PRINCIPAL ****************************************" + Style.RESET_ALL)
    print(Fore.BLUE + "* " + Style.RESET_ALL + "1 - Cadastro de Cargos")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "2 - Cadastro de Funcionários")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "3 - Relatório de Funcionários por Cargo")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "4 - Relatório de Desenvolvedores Front-End com Salário entre 8000 e 12000")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "5 - Relatório de Funcionários de TI com mais de 21 anos")
    print(Fore.BLUE + "* " + Style.RESET_ALL + "6 - Sair do Sistema")
    print(Fore.BLUE + "**************************************************************************************" + Style.RESET_ALL)

def print_cargo(cargo):
    """
    Imprime os detalhes de um cargo com formatação.
    """
    print(Fore.YELLOW + "----------------------------------------------------------------------------------------------------" + Style.RESET_ALL)
    print(Fore.CYAN + f"ID do Cargo...........: " + Style.RESET_ALL + f"{cargo['cargo_id']}")
    print(Fore.CYAN + f"Descrição do Cargo....: " + Style.RESET_ALL + f"{cargo['cargo_descricao']}")
    print(Fore.CYAN + f"Departamento..........: " + Style.RESET_ALL + f"{cargo['cargo_departamento']}")
    print(Fore.YELLOW + "----------------------------------------------------------------------------------------------------" + Style.RESET_ALL)

def print_funcionario(funcionario):
    """
    Imprime os detalhes de um funcionário com formatação.
    """
    print(Fore.YELLOW + "----------------------------------------------------------------------------------------------------" + Style.RESET_ALL)
    print(Fore.CYAN + "ID do Funcionário.......: " + Style.RESET_ALL + f"{funcionario['funcionario_id']}")
    print(Fore.CYAN + "CPF.....................: " + Style.RESET_ALL + f"{funcionario['funcionario_cpf']}")
    print(Fore.CYAN + "Nome....................: " + Style.RESET_ALL + f"{funcionario['funcionario_nome']}")
    print(Fore.CYAN + "Salário.................: " + Style.RESET_ALL + f"{funcionario['funcionario_salario']}")
    print(Fore.CYAN + "Idade...................: " + Style.RESET_ALL + f"{funcionario['funcionario_idade']}")
    print(Fore.CYAN + "Cargo...................: " + Style.RESET_ALL + f"{funcionario['cargo_descricao']}")
    print(Fore.CYAN + "Departamento............: " + Style.RESET_ALL + f"{funcionario['cargo_departamento']}")
    print(Fore.YELLOW + "----------------------------------------------------------------------------------------------------" + Style.RESET_ALL)

def salvar_em_json(nome_arquivo, dados):
    """
    Salva os dados fornecidos em um arquivo JSON.
    """
    try:
        with open(f"{nome_arquivo}.json", "w", encoding="utf-8") as json_file:
            json.dump(dados, json_file, ensure_ascii=False, indent=4)
        print(Fore.GREEN + f"Relatório salvo como {nome_arquivo}.json" + Style.RESET_ALL)
        logging.info(f"Relatório salvo como {nome_arquivo}.json")
    except Exception as e:
        print(Fore.RED + f"Erro ao salvar o relatório em JSON: {e}" + Style.RESET_ALL)
        logging.error(f"Erro ao salvar o relatório em JSON: {e}")

def fetch_as_dict(inst_SQL):
    """
    Converte o resultado da consulta para uma lista de dicionários.
    """
    columns = [col[0].lower() for col in inst_SQL.description]
    return [dict(zip(columns, row)) for row in inst_SQL.fetchall()]

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
            opcao_input = input(Fore.BLUE + "Digite a opção desejada: " + Style.RESET_ALL).strip()
            if not opcao_input.isdigit():
                raise ValueError("A opção deve ser um número.")
            opcao = int(opcao_input)
            if opcao == 1:
                inserir_cargo(conexao, inst_SQL)
            elif opcao == 2:
                alterar_cargo(conexao, inst_SQL)
            elif opcao == 3:
                excluir_cargo(conexao, inst_SQL)
            elif opcao == 4:
                listar_cargos(inst_SQL)
                # Opcional: Exportar relatório em JSON
                exportar = input("Deseja exportar o relatório em JSON? (s/n): ").strip().lower()
                if exportar == 's':
                    str_consulta = """
                        SELECT cargo_id, cargo_descricao, cargo_departamento
                        FROM cargos
                        ORDER BY cargo_id
                    """
                    inst_SQL.execute(str_consulta)
                    cargos = fetch_as_dict(inst_SQL)
                    cargos_list = []
                    for cargo in cargos:
                        cargos_list.append({
                            'cargo_id': int(cargo['cargo_id']),
                            'cargo_descricao': cargo['cargo_descricao'],
                            'cargo_departamento': cargo['cargo_departamento']
                        })
                    salvar_em_json("relatorio_todos_cargos", cargos_list)
            elif opcao == 5:
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente." + Style.RESET_ALL)
                logging.warning("Opção inválida inserida no CRUD de cargos.")
        except ValueError as ve:
            print(Fore.RED + f"**************************************** ERRO: {ve} ****************************************" + Style.RESET_ALL)
            logging.warning(f"Entrada inválida no CRUD de cargos: {ve}")
        except Exception as e:
            print(Fore.RED + "**************************************** OCORREU UM ERRO DESCONHECIDO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + str(e) + Style.RESET_ALL)
            logging.error(f"Erro desconhecido no CRUD de cargos: {str(e)}")
        input(Fore.CYAN + "Pressione Enter para continuar..." + Style.RESET_ALL)

def inserir_cargo(conexao, inst_SQL):
    """
    Insere um novo registro na tabela 'cargos'.
    """
    while True:
        try:
            descricao = input("Digite a descrição do cargo: ").strip()
            if not descricao:
                raise ValueError("Descrição não pode estar vazia.")
            departamento = input("Digite o departamento do cargo: ").strip()
            if not departamento:
                raise ValueError("Departamento não pode estar vazio.")
            str_consulta = """
                INSERT INTO cargos (cargo_descricao, cargo_departamento)
                VALUES (:descricao, :departamento)
                RETURNING cargo_id INTO :id
            """
            cargo_id_var = conexao.cursor().var(oracledb.NUMBER)
            inst_SQL.execute(str_consulta, {'descricao': descricao, 'departamento': departamento, 'id': cargo_id_var})
            novo_id = int(cargo_id_var.getvalue()[0])
            conexao.commit()
            print(Fore.GREEN + f"Cargo inserido com sucesso! ID: {novo_id}" + Style.RESET_ALL)
            logging.info(f"Novo cargo inserido: ID {novo_id}, Descrição: {descricao}, Departamento: {departamento}")
            break  # Sai do loop após inserção bem-sucedida
        except ValueError as ve:
            print(Fore.RED + f"Erro: {ve}" + Style.RESET_ALL)
            logging.warning(f"Tentativa de inserir cargo com dados inválidos: {ve}")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "Erro ao inserir cargo." + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao inserir cargo: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def alterar_cargo(conexao, inst_SQL):
    """
    Altera um registro existente na tabela 'cargos'.
    """
    while True:
        try:
            listar_cargos(inst_SQL)
            cargo_id_input = input("Digite o ID do cargo que deseja alterar: ").strip()
            if not cargo_id_input.isdigit():
                raise ValueError("ID deve ser um número.")
            cargo_id = int(cargo_id_input)
            nova_descricao = input("Digite a nova descrição do cargo: ").strip()
            if not nova_descricao:
                raise ValueError("Descrição não pode estar vazia.")
            novo_departamento = input("Digite o novo departamento do cargo: ").strip()
            if not novo_departamento:
                raise ValueError("Departamento não pode estar vazio.")
            str_consulta = """
                UPDATE cargos
                SET cargo_descricao = :descricao,
                    cargo_departamento = :departamento
                WHERE cargo_id = :id
            """
            inst_SQL.execute(str_consulta, {'descricao': nova_descricao, 'departamento': novo_departamento, 'id': cargo_id})
            if inst_SQL.rowcount == 0:
                print(Fore.YELLOW + "Nenhum cargo encontrado com o ID fornecido." + Style.RESET_ALL)
                logging.warning(f"Tentativa de alterar cargo inexistente: ID {cargo_id}")
            else:
                conexao.commit()
                print(Fore.GREEN + "Cargo atualizado com sucesso!" + Style.RESET_ALL)
                logging.info(f"Cargo atualizado: ID {cargo_id}, Nova Descrição: {nova_descricao}, Novo Departamento: {novo_departamento}")
            break  # Sai do loop após atualização
        except ValueError as ve:
            print(Fore.RED + f"Erro: {ve}" + Style.RESET_ALL)
            logging.warning(f"Tentativa de alterar cargo com dados inválidos: {ve}")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "Erro ao atualizar cargo." + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao atualizar cargo: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def excluir_cargo(conexao, inst_SQL):
    """
    Exclui um registro da tabela 'cargos'.
    """
    while True:
        try:
            listar_cargos(inst_SQL)
            cargo_id_input = input("Digite o ID do cargo que deseja excluir: ").strip()
            if not cargo_id_input.isdigit():
                raise ValueError("ID deve ser um número.")
            cargo_id = int(cargo_id_input)
            confirmacao = input(f"Tem certeza que deseja excluir o cargo ID {cargo_id}? (s/n): ").strip().lower()
            if confirmacao != 's':
                print("Operação cancelada.")
                break  # Sai do loop se o usuário cancelar
            str_consulta = """
                DELETE FROM cargos
                WHERE cargo_id = :id
            """
            inst_SQL.execute(str_consulta, {'id': cargo_id})
            if inst_SQL.rowcount == 0:
                print(Fore.YELLOW + "Nenhum cargo encontrado com o ID fornecido." + Style.RESET_ALL)
                logging.warning(f"Tentativa de excluir cargo inexistente: ID {cargo_id}")
            else:
                conexao.commit()
                print(Fore.GREEN + "Cargo excluído com sucesso!" + Style.RESET_ALL)
                logging.info(f"Cargo excluído: ID {cargo_id}")
            break  # Sai do loop após exclusão ou tentativa
        except ValueError as ve:
            print(Fore.RED + f"Erro: {ve}" + Style.RESET_ALL)
            logging.warning(f"Tentativa de excluir cargo com ID inválido: {ve}")
        except oracledb.DatabaseError as e:
            error, = e.args
            if isinstance(e, oracledb.IntegrityError):
                print(Fore.RED + "Não é possível excluir este cargo pois ele está associado a funcionários." + Style.RESET_ALL)
                logging.error(f"Tentativa de excluir cargo ID {cargo_id} que está associado a funcionários.")
            else:
                print(Fore.RED + "Erro ao excluir cargo." + Style.RESET_ALL)
                print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
                logging.error(f"Erro ao excluir cargo: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

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
        cargos = fetch_as_dict(inst_SQL)
        if not cargos:
            print(Fore.YELLOW + "Nenhum cargo encontrado." + Style.RESET_ALL)
            return
        print(Fore.YELLOW + "**************************************** LISTA DE CARGOS ****************************************" + Style.RESET_ALL)
        for cargo in cargos:
            cargo_dict = {
                'cargo_id': int(cargo['cargo_id']),
                'cargo_descricao': cargo['cargo_descricao'],
                'cargo_departamento': cargo['cargo_departamento']
            }
            print_cargo(cargo_dict)
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
            opcao_input = input(Fore.BLUE + "Digite a opção desejada: " + Style.RESET_ALL).strip()
            if not opcao_input.isdigit():
                raise ValueError("A opção deve ser um número.")
            opcao = int(opcao_input)
            if opcao == 1:
                inserir_funcionario(conexao, inst_SQL)
            elif opcao == 2:
                alterar_funcionario(conexao, inst_SQL)
            elif opcao == 3:
                excluir_funcionario(conexao, inst_SQL)
            elif opcao == 4:
                listar_funcionarios(inst_SQL)
                # Opcional: Exportar relatório em JSON
                exportar = input("Deseja exportar o relatório em JSON? (s/n): ").strip().lower()
                if exportar == 's':
                    str_consulta = """
                        SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                               c.cargo_descricao, c.cargo_departamento
                        FROM funcionarios f
                        JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
                        ORDER BY f.funcionario_id
                    """
                    inst_SQL.execute(str_consulta)
                    funcionarios = fetch_as_dict(inst_SQL)
                    funcionarios_list = []
                    for func in funcionarios:
                        funcionarios_list.append({
                            'funcionario_id': int(func['funcionario_id']),
                            'funcionario_cpf': func['funcionario_cpf'],
                            'funcionario_nome': func['funcionario_nome'],
                            'funcionario_salario': float(func['funcionario_salario']),
                            'funcionario_idade': int(func['funcionario_idade']),
                            'cargo_descricao': func['cargo_descricao'],
                            'cargo_departamento': func['cargo_departamento']
                        })
                    salvar_em_json("relatorio_todos_funcionarios", funcionarios_list)
            elif opcao == 5:
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente." + Style.RESET_ALL)
                logging.warning("Opção inválida inserida no CRUD de funcionários.")
        except ValueError as ve:
            print(Fore.RED + f"**************************************** ERRO: {ve} ****************************************" + Style.RESET_ALL)
            logging.warning(f"Entrada inválida no CRUD de funcionários: {ve}")
        except Exception as e:
            print(Fore.RED + "**************************************** OCORREU UM ERRO DESCONHECIDO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + str(e) + Style.RESET_ALL)
            logging.error(f"Erro desconhecido no CRUD de funcionários: {str(e)}")
        input(Fore.CYAN + "Pressione Enter para continuar..." + Style.RESET_ALL)

def inserir_funcionario(conexao, inst_SQL):
    """
    Insere um novo registro na tabela 'funcionarios'.
    """
    while True:
        try:
            cpf = input("Digite o CPF do funcionário (apenas números, 11 dígitos): ").strip()
            if not cpf.isdigit() or len(cpf) != 11:
                raise ValueError("CPF inválido. Deve conter exatamente 11 números.")
            nome = input("Digite o nome do funcionário: ").strip()
            if not nome:
                raise ValueError("Nome não pode estar vazio.")
            try:
                salario_input = input("Digite o salário do funcionário: ").strip()
                salario = float(salario_input)
                if salario < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Salário inválido. Deve ser um número positivo.")
            try:
                idade_input = input("Digite a idade do funcionário: ").strip()
                idade = int(idade_input)
                if idade <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Idade inválida. Deve ser um número inteiro positivo.")

            listar_cargos(inst_SQL)
            while True:
                cargo_id_input = input("Digite o ID do cargo do funcionário: ").strip()
                if not cargo_id_input.isdigit():
                    print(Fore.RED + "ID do cargo inválido. Deve ser um número inteiro." + Style.RESET_ALL)
                    logging.warning("Tentativa de inserir funcionário com ID de cargo inválido.")
                else:
                    cargo_id = int(cargo_id_input)
                    # Verifica se o cargo_id existe
                    str_verifica_cargo = "SELECT COUNT(*) AS count FROM cargos WHERE cargo_id = :id"
                    inst_SQL.execute(str_verifica_cargo, {'id': cargo_id})
                    result = inst_SQL.fetchone()
                    count = result['count'] if isinstance(result, dict) else result[0]
                    if count == 0:
                        print(Fore.RED + "Cargo ID não encontrado. Tente novamente." + Style.RESET_ALL)
                        logging.warning(f"Tentativa de inserir funcionário com cargo inexistente: ID {cargo_id}")
                    else:
                        break  # ID válido e existente

            # Insere o funcionário
            str_insert_funcionario = """
                INSERT INTO funcionarios (funcionario_cpf, funcionario_nome, funcionario_salario, funcionario_idade, cargos_cargo_id)
                VALUES (:cpf, :nome, :salario, :idade, :cargo_id)
                RETURNING funcionario_id INTO :id
            """
            funcionario_id_var = conexao.cursor().var(oracledb.NUMBER)
            inst_SQL.execute(str_insert_funcionario, {
                'cpf': cpf,
                'nome': nome,
                'salario': salario,
                'idade': idade,
                'cargo_id': cargo_id,
                'id': funcionario_id_var
            })
            novo_id = int(funcionario_id_var.getvalue()[0])

            conexao.commit()
            print(Fore.GREEN + f"Funcionário inserido com sucesso! ID: {novo_id}" + Style.RESET_ALL)
            logging.info(f"Novo funcionário inserido: ID {novo_id}, CPF {cpf}, Nome {nome}, Salário {salario}, Idade {idade}, Cargo ID {cargo_id}")
            break  # Sai do loop após inserção bem-sucedida
        except ValueError as ve:
            print(Fore.RED + f"Erro: {ve}" + Style.RESET_ALL)
            logging.warning(f"Tentativa de inserir funcionário com dados inválidos: {ve}")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "Erro ao inserir funcionário." + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao inserir funcionário: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def alterar_funcionario(conexao, inst_SQL):
    """
    Altera um registro existente na tabela 'funcionarios'.
    """
    while True:
        try:
            listar_funcionarios(inst_SQL)
            funcionario_id_input = input("Digite o ID do funcionário que deseja alterar: ").strip()
            if not funcionario_id_input.isdigit():
                raise ValueError("ID do funcionário inválido. Deve ser um número inteiro.")
            funcionario_id = int(funcionario_id_input)

            # Verifica se o funcionário existe
            str_verifica_func = "SELECT COUNT(*) AS count FROM funcionarios WHERE funcionario_id = :id"
            inst_SQL.execute(str_verifica_func, {'id': funcionario_id})
            result = inst_SQL.fetchone()
            count = result['count'] if isinstance(result, dict) else result[0]
            if count == 0:
                print(Fore.YELLOW + "Nenhum funcionário encontrado com o ID fornecido." + Style.RESET_ALL)
                logging.warning(f"Tentativa de alterar funcionário inexistente: ID {funcionario_id}")
                return  # Retorna ao menu de CRUD de funcionários

            cpf = input("Digite o novo CPF do funcionário (apenas números, 11 dígitos): ").strip()
            if not cpf.isdigit() or len(cpf) != 11:
                raise ValueError("CPF inválido. Deve conter exatamente 11 números.")
            nome = input("Digite o novo nome do funcionário: ").strip()
            if not nome:
                raise ValueError("Nome não pode estar vazio.")
            try:
                salario_input = input("Digite o novo salário do funcionário: ").strip()
                salario = float(salario_input)
                if salario < 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Salário inválido. Deve ser um número positivo.")
            try:
                idade_input = input("Digite a nova idade do funcionário: ").strip()
                idade = int(idade_input)
                if idade <= 0:
                    raise ValueError
            except ValueError:
                raise ValueError("Idade inválida. Deve ser um número inteiro positivo.")

            listar_cargos(inst_SQL)
            while True:
                cargo_id_input = input("Digite o novo ID do cargo do funcionário: ").strip()
                if not cargo_id_input.isdigit():
                    print(Fore.RED + "ID do cargo inválido. Deve ser um número inteiro." + Style.RESET_ALL)
                    logging.warning("Tentativa de alterar funcionário com ID de cargo inválido.")
                else:
                    cargo_id = int(cargo_id_input)
                    # Verifica se o cargo_id existe
                    str_verifica_cargo = "SELECT COUNT(*) AS count FROM cargos WHERE cargo_id = :id"
                    inst_SQL.execute(str_verifica_cargo, {'id': cargo_id})
                    result_cargo = inst_SQL.fetchone()
                    count_cargo = result_cargo['count'] if isinstance(result_cargo, dict) else result_cargo[0]
                    if count_cargo == 0:
                        print(Fore.RED + "Cargo ID não encontrado. Tente novamente." + Style.RESET_ALL)
                        logging.warning(f"Tentativa de alterar funcionário com cargo inexistente: ID {cargo_id}")
                    else:
                        break  # ID válido e existente

            # Atualiza o funcionário
            str_update_funcionario = """
                UPDATE funcionarios
                SET funcionario_cpf = :cpf,
                    funcionario_nome = :nome,
                    funcionario_salario = :salario,
                    funcionario_idade = :idade,
                    cargos_cargo_id = :cargo_id
                WHERE funcionario_id = :id
            """
            inst_SQL.execute(str_update_funcionario, {
                'cpf': cpf,
                'nome': nome,
                'salario': salario,
                'idade': idade,
                'cargo_id': cargo_id,
                'id': funcionario_id
            })

            conexao.commit()
            print(Fore.GREEN + "Funcionário atualizado com sucesso!" + Style.RESET_ALL)
            logging.info(f"Funcionário atualizado: ID {funcionario_id}, CPF {cpf}, Nome {nome}, Salário {salario}, Idade {idade}, Cargo ID {cargo_id}")
            break  # Sai do loop após atualização bem-sucedida
        except ValueError as ve:
            print(Fore.RED + f"Erro: {ve}" + Style.RESET_ALL)
            logging.warning(f"Tentativa de alterar funcionário com dados inválidos: {ve}")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "Erro ao atualizar funcionário." + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao atualizar funcionário: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def excluir_funcionario(conexao, inst_SQL):
    """
    Exclui um registro da tabela 'funcionarios'.
    """
    while True:
        try:
            listar_funcionarios(inst_SQL)
            funcionario_id_input = input("Digite o ID do funcionário que deseja excluir: ").strip()
            if not funcionario_id_input.isdigit():
                raise ValueError("ID do funcionário inválido. Deve ser um número inteiro.")
            funcionario_id = int(funcionario_id_input)
            confirmacao = input(f"Tem certeza que deseja excluir o funcionário ID {funcionario_id}? (s/n): ").strip().lower()
            if confirmacao != 's':
                print("Operação cancelada.")
                break  # Sai do loop se o usuário cancelar
            # Exclui o funcionário
            str_delete_funcionario = """
                DELETE FROM funcionarios
                WHERE funcionario_id = :id
            """
            inst_SQL.execute(str_delete_funcionario, {'id': funcionario_id})
            if inst_SQL.rowcount == 0:
                print(Fore.YELLOW + "Nenhum funcionário encontrado com o ID fornecido." + Style.RESET_ALL)
                logging.warning(f"Tentativa de excluir funcionário inexistente: ID {funcionario_id}")
            else:
                conexao.commit()
                print(Fore.GREEN + "Funcionário excluído com sucesso!" + Style.RESET_ALL)
                logging.info(f"Funcionário excluído: ID {funcionario_id}")
            break  # Sai do loop após exclusão ou tentativa
        except ValueError as ve:
            print(Fore.RED + f"Erro: {ve}" + Style.RESET_ALL)
            logging.warning(f"Tentativa de excluir funcionário com ID inválido: {ve}")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "Erro ao excluir funcionário." + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao excluir funcionário: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def listar_funcionarios(inst_SQL):
    """
    Lista todos os registros da tabela 'funcionarios' com seus respectivos cargos.
    """
    try:
        str_consulta = """
            SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                   c.cargo_descricao, c.cargo_departamento
            FROM funcionarios f
            JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
            ORDER BY f.funcionario_id
        """
        inst_SQL.execute(str_consulta)
        funcionarios = fetch_as_dict(inst_SQL)
        if not funcionarios:
            print(Fore.YELLOW + "Nenhum funcionário encontrado." + Style.RESET_ALL)
            return
        print(Fore.YELLOW + "************************************** LISTA DE FUNCIONÁRIOS **************************************" + Style.RESET_ALL)
        for func in funcionarios:
            funcionario_dict = {
                'funcionario_id': int(func['funcionario_id']),
                'funcionario_cpf': func['funcionario_cpf'],
                'funcionario_nome': func['funcionario_nome'],
                'funcionario_salario': float(func['funcionario_salario']),
                'funcionario_idade': int(func['funcionario_idade']),
                'cargo_descricao': func['cargo_descricao'],
                'cargo_departamento': func['cargo_departamento']
            }
            print_funcionario(funcionario_dict)
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao listar funcionários." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao listar funcionários: {error.message}")

def relatorio_funcionarios_por_cargo(inst_SQL):
    """
    Gera o relatório de funcionários por cargo escolhido pelo usuário e salva em JSON.
    """
    while True:
        try:
            cargo = input("Digite o nome do cargo: ").strip()
            if not cargo:
                raise ValueError("Nome do cargo não pode estar vazio.")
            print(Fore.BLUE + f"**************************************** RELATÓRIO DE FUNCIONÁRIOS POR CARGO: {cargo.upper()} ****************************************" + Style.RESET_ALL)
            str_consulta = """
                SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                       c.cargo_descricao, c.cargo_departamento
                FROM funcionarios f
                JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
                WHERE c.cargo_descricao = :cargo
                ORDER BY f.funcionario_id
            """
            inst_SQL.execute(str_consulta, {'cargo': cargo})
            funcionarios = fetch_as_dict(inst_SQL)
            if not funcionarios:
                print(Fore.YELLOW + "Nenhum funcionário encontrado para o cargo especificado." + Style.RESET_ALL)
                logging.info(f"Relatório por cargo '{cargo}' gerado sem resultados.")
                break  # Sai do loop se não houver resultados
            funcionarios_list = []
            for func in funcionarios:
                funcionario_dict = {
                    'funcionario_id': int(func['funcionario_id']),
                    'funcionario_cpf': func['funcionario_cpf'],
                    'funcionario_nome': func['funcionario_nome'],
                    'funcionario_salario': float(func['funcionario_salario']),
                    'funcionario_idade': int(func['funcionario_idade']),
                    'cargo_descricao': func['cargo_descricao'],
                    'cargo_departamento': func['cargo_departamento']
                }
                funcionarios_list.append(funcionario_dict)
                print_funcionario(funcionario_dict)
            # Salvar em JSON
            nome_arquivo = f"relatorio_funcionarios_por_cargo_{cargo.replace(' ', '_')}"
            salvar_em_json(nome_arquivo, funcionarios_list)
            logging.info(f"Relatório de funcionários por cargo '{cargo}' gerado com sucesso.")
            break  # Sai do loop após geração do relatório
        except ValueError as ve:
            print(Fore.RED + f"Erro: {ve}" + Style.RESET_ALL)
            logging.warning(f"Tentativa de gerar relatório com nome de cargo inválido: {ve}")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao gerar relatório de funcionários por cargo: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def relatorio_funcionarios_frontend_salario(inst_SQL):
    """
    Gera o relatório de desenvolvedores Front-End com salário entre 8000 e 12000 e salva em JSON.
    """
    while True:
        try:
            print(Fore.BLUE + "**************************************** RELATÓRIO DE DESENVOLVEDORES FRONT-END COM SALÁRIO ENTRE 8000 E 12000 ****************************************" + Style.RESET_ALL)
            str_consulta = """
                SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                       c.cargo_descricao, c.cargo_departamento
                FROM funcionarios f
                JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
                WHERE c.cargo_descricao = 'Desenvolvedor Front End' 
                AND f.funcionario_salario BETWEEN 8000 AND 12000
                ORDER BY f.funcionario_id
            """
            inst_SQL.execute(str_consulta)
            funcionarios = fetch_as_dict(inst_SQL)
            if not funcionarios:
                print(Fore.YELLOW + "Nenhum desenvolvedor Front-End encontrado com o salário especificado." + Style.RESET_ALL)
                logging.info("Relatório de desenvolvedores Front-End com salário entre 8000 e 12000 gerado sem resultados.")
                break  # Sai do loop se não houver resultados
            funcionarios_list = []
            for func in funcionarios:
                funcionario_dict = {
                    'funcionario_id': int(func['funcionario_id']),
                    'funcionario_cpf': func['funcionario_cpf'],
                    'funcionario_nome': func['funcionario_nome'],
                    'funcionario_salario': float(func['funcionario_salario']),
                    'funcionario_idade': int(func['funcionario_idade']),
                    'cargo_descricao': func['cargo_descricao'],
                    'cargo_departamento': func['cargo_departamento']
                }
                funcionarios_list.append(funcionario_dict)
                print_funcionario(funcionario_dict)
            # Salvar em JSON
            nome_arquivo = "relatorio_desenvolvedores_frontend_salario_8000_12000"
            salvar_em_json(nome_arquivo, funcionarios_list)
            logging.info("Relatório de desenvolvedores Front-End com salário entre 8000 e 12000 gerado com sucesso.")
            break  # Sai do loop após geração do relatório
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao gerar relatório de desenvolvedores Front-End com salário entre 8000 e 12000: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def relatorio_funcionarios_ti_maior_21(inst_SQL):
    """
    Gera o relatório de funcionários do departamento de TI com mais de 21 anos e salva em JSON.
    """
    while True:
        try:
            print(Fore.BLUE + "**************************************** RELATÓRIO DE FUNCIONÁRIOS DE TI COM MAIS DE 21 ANOS ****************************************" + Style.RESET_ALL)
            str_consulta = """
                SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                       c.cargo_descricao, c.cargo_departamento
                FROM funcionarios f
                JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
                WHERE c.cargo_departamento = 'TI'
                AND f.funcionario_idade > 21
                ORDER BY f.funcionario_id
            """
            inst_SQL.execute(str_consulta)
            funcionarios = fetch_as_dict(inst_SQL)
            if not funcionarios:
                print(Fore.YELLOW + "Nenhum funcionário de TI com mais de 21 anos encontrado." + Style.RESET_ALL)
                logging.info("Relatório de funcionários de TI com mais de 21 anos gerado sem resultados.")
                break  # Sai do loop se não houver resultados
            funcionarios_list = []
            for func in funcionarios:
                funcionario_dict = {
                    'funcionario_id': int(func['funcionario_id']),
                    'funcionario_cpf': func['funcionario_cpf'],
                    'funcionario_nome': func['funcionario_nome'],
                    'funcionario_salario': float(func['funcionario_salario']),
                    'funcionario_idade': int(func['funcionario_idade']),
                    'cargo_descricao': func['cargo_descricao'],
                    'cargo_departamento': func['cargo_departamento']
                }
                funcionarios_list.append(funcionario_dict)
                print_funcionario(funcionario_dict)
            # Salvar em JSON
            nome_arquivo = "relatorio_funcionarios_ti_maior_21"
            salvar_em_json(nome_arquivo, funcionarios_list)
            logging.info("Relatório de funcionários de TI com mais de 21 anos gerado com sucesso.")
            break  # Sai do loop após geração do relatório
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao gerar relatório de funcionários de TI com mais de 21 anos: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def listar_funcionarios(inst_SQL):
    """
    Lista todos os registros da tabela 'funcionarios' com seus respectivos cargos.
    """
    try:
        str_consulta = """
            SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                   c.cargo_descricao, c.cargo_departamento
            FROM funcionarios f
            JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
            ORDER BY f.funcionario_id
        """
        inst_SQL.execute(str_consulta)
        funcionarios = fetch_as_dict(inst_SQL)
        if not funcionarios:
            print(Fore.YELLOW + "Nenhum funcionário encontrado." + Style.RESET_ALL)
            return
        print(Fore.YELLOW + "************************************** LISTA DE FUNCIONÁRIOS **************************************" + Style.RESET_ALL)
        for func in funcionarios:
            funcionario_dict = {
                'funcionario_id': int(func['funcionario_id']),
                'funcionario_cpf': func['funcionario_cpf'],
                'funcionario_nome': func['funcionario_nome'],
                'funcionario_salario': float(func['funcionario_salario']),
                'funcionario_idade': int(func['funcionario_idade']),
                'cargo_descricao': func['cargo_descricao'],
                'cargo_departamento': func['cargo_departamento']
            }
            print_funcionario(funcionario_dict)
    except oracledb.DatabaseError as e:
        error, = e.args
        print(Fore.RED + "Erro ao listar funcionários." + Style.RESET_ALL)
        print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
        logging.error(f"Erro ao listar funcionários: {error.message}")

def relatorio_funcionarios_por_cargo(inst_SQL):
    """
    Gera o relatório de funcionários por cargo escolhido pelo usuário e salva em JSON.
    """
    while True:
        try:
            cargo = input("Digite o nome do cargo: ").strip()
            if not cargo:
                raise ValueError("Nome do cargo não pode estar vazio.")
            print(Fore.BLUE + f"**************************************** RELATÓRIO DE FUNCIONÁRIOS POR CARGO: {cargo.upper()} ****************************************" + Style.RESET_ALL)
            str_consulta = """
                SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                       c.cargo_descricao, c.cargo_departamento
                FROM funcionarios f
                JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
                WHERE c.cargo_descricao = :cargo
                ORDER BY f.funcionario_id
            """
            inst_SQL.execute(str_consulta, {'cargo': cargo})
            funcionarios = fetch_as_dict(inst_SQL)
            if not funcionarios:
                print(Fore.YELLOW + "Nenhum funcionário encontrado para o cargo especificado." + Style.RESET_ALL)
                logging.info(f"Relatório por cargo '{cargo}' gerado sem resultados.")
                break  # Sai do loop se não houver resultados
            funcionarios_list = []
            for func in funcionarios:
                funcionario_dict = {
                    'funcionario_id': int(func['funcionario_id']),
                    'funcionario_cpf': func['funcionario_cpf'],
                    'funcionario_nome': func['funcionario_nome'],
                    'funcionario_salario': float(func['funcionario_salario']),
                    'funcionario_idade': int(func['funcionario_idade']),
                    'cargo_descricao': func['cargo_descricao'],
                    'cargo_departamento': func['cargo_departamento']
                }
                funcionarios_list.append(funcionario_dict)
                print_funcionario(funcionario_dict)
            # Salvar em JSON
            nome_arquivo = f"relatorio_funcionarios_por_cargo_{cargo.replace(' ', '_')}"
            salvar_em_json(nome_arquivo, funcionarios_list)
            logging.info(f"Relatório de funcionários por cargo '{cargo}' gerado com sucesso.")
            break  # Sai do loop após geração do relatório
        except ValueError as ve:
            print(Fore.RED + f"Erro: {ve}" + Style.RESET_ALL)
            logging.warning(f"Tentativa de gerar relatório com nome de cargo inválido: {ve}")
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao gerar relatório de funcionários por cargo: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def relatorio_funcionarios_frontend_salario(inst_SQL):
    """
    Gera o relatório de desenvolvedores Front-End com salário entre 8000 e 12000 e salva em JSON.
    """
    while True:
        try:
            print(Fore.BLUE + "**************************************** RELATÓRIO DE DESENVOLVEDORES FRONT-END COM SALÁRIO ENTRE 8000 E 12000 ****************************************" + Style.RESET_ALL)
            str_consulta = """
                SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                       c.cargo_descricao, c.cargo_departamento
                FROM funcionarios f
                JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
                WHERE c.cargo_descricao = 'Desenvolvedor Front End' 
                AND f.funcionario_salario BETWEEN 8000 AND 12000
                ORDER BY f.funcionario_id
            """
            inst_SQL.execute(str_consulta)
            funcionarios = fetch_as_dict(inst_SQL)
            if not funcionarios:
                print(Fore.YELLOW + "Nenhum desenvolvedor Front-End encontrado com o salário especificado." + Style.RESET_ALL)
                logging.info("Relatório de desenvolvedores Front-End com salário entre 8000 e 12000 gerado sem resultados.")
                break  # Sai do loop se não houver resultados
            funcionarios_list = []
            for func in funcionarios:
                funcionario_dict = {
                    'funcionario_id': int(func['funcionario_id']),
                    'funcionario_cpf': func['funcionario_cpf'],
                    'funcionario_nome': func['funcionario_nome'],
                    'funcionario_salario': float(func['funcionario_salario']),
                    'funcionario_idade': int(func['funcionario_idade']),
                    'cargo_descricao': func['cargo_descricao'],
                    'cargo_departamento': func['cargo_departamento']
                }
                funcionarios_list.append(funcionario_dict)
                print_funcionario(funcionario_dict)
            # Salvar em JSON
            nome_arquivo = "relatorio_desenvolvedores_frontend_salario_8000_12000"
            salvar_em_json(nome_arquivo, funcionarios_list)
            logging.info("Relatório de desenvolvedores Front-End com salário entre 8000 e 12000 gerado com sucesso.")
            break  # Sai do loop após geração do relatório
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao gerar relatório de desenvolvedores Front-End com salário entre 8000 e 12000: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

def relatorio_funcionarios_ti_maior_21(inst_SQL):
    """
    Gera o relatório de funcionários do departamento de TI com mais de 21 anos e salva em JSON.
    """
    while True:
        try:
            print(Fore.BLUE + "**************************************** RELATÓRIO DE FUNCIONÁRIOS DE TI COM MAIS DE 21 ANOS ****************************************" + Style.RESET_ALL)
            str_consulta = """
                SELECT f.funcionario_id, f.funcionario_cpf, f.funcionario_nome, f.funcionario_salario, f.funcionario_idade, 
                       c.cargo_descricao, c.cargo_departamento
                FROM funcionarios f
                JOIN cargos c ON f.cargos_cargo_id = c.cargo_id
                WHERE c.cargo_departamento = 'TI'
                AND f.funcionario_idade > 21
                ORDER BY f.funcionario_id
            """
            inst_SQL.execute(str_consulta)
            funcionarios = fetch_as_dict(inst_SQL)
            if not funcionarios:
                print(Fore.YELLOW + "Nenhum funcionário de TI com mais de 21 anos encontrado." + Style.RESET_ALL)
                logging.info("Relatório de funcionários de TI com mais de 21 anos gerado sem resultados.")
                break  # Sai do loop se não houver resultados
            funcionarios_list = []
            for func in funcionarios:
                funcionario_dict = {
                    'funcionario_id': int(func['funcionario_id']),
                    'funcionario_cpf': func['funcionario_cpf'],
                    'funcionario_nome': func['funcionario_nome'],
                    'funcionario_salario': float(func['funcionario_salario']),
                    'funcionario_idade': int(func['funcionario_idade']),
                    'cargo_descricao': func['cargo_descricao'],
                    'cargo_departamento': func['cargo_departamento']
                }
                funcionarios_list.append(funcionario_dict)
                print_funcionario(funcionario_dict)
            # Salvar em JSON
            nome_arquivo = "relatorio_funcionarios_ti_maior_21"
            salvar_em_json(nome_arquivo, funcionarios_list)
            logging.info("Relatório de funcionários de TI com mais de 21 anos gerado com sucesso.")
            break  # Sai do loop após geração do relatório
        except oracledb.DatabaseError as e:
            error, = e.args
            print(Fore.RED + "**************************************** ERRO AO GERAR RELATÓRIO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + f"Erro: {error.message}" + Style.RESET_ALL)
            logging.error(f"Erro ao gerar relatório de funcionários de TI com mais de 21 anos: {error.message}")
            break  # Opcional: Sai do loop se ocorrer um erro de banco de dados

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
            opc_principal_input = input(Fore.BLUE + "DIGITE A OPÇÃO DESEJADA: " + Style.RESET_ALL).strip()
            if not opc_principal_input.isdigit():
                raise ValueError("A opção deve ser um número.")
            opc_principal = int(opc_principal_input)
            if opc_principal == 1:
                crud_cargos(conexao, inst_SQL)
            elif opc_principal == 2:
                crud_funcionarios(conexao, inst_SQL)
            elif opc_principal == 3:
                relatorio_funcionarios_por_cargo(inst_SQL)
            elif opc_principal == 4:
                relatorio_funcionarios_frontend_salario(inst_SQL)
            elif opc_principal == 5:
                relatorio_funcionarios_ti_maior_21(inst_SQL)
            elif opc_principal == 6:
                print(Fore.RED + "**************************************** SAINDO DO SISTEMA ****************************************" + Style.RESET_ALL)
                logging.info("Encerrando o sistema.")
                inst_SQL.close()
                conexao.close()
                break
            else:
                print(Fore.RED + "**************************************** OPÇÃO INCORRETA. DIGITE UMA OPÇÃO VÁLIDA! ****************************************" + Style.RESET_ALL)
                logging.warning("Opção incorreta inserida no menu principal.")
        except ValueError as ve:
            print(Fore.RED + f"**************************************** ERRO: {ve} ****************************************" + Style.RESET_ALL)
            logging.warning(f"Erro ao converter a entrada para número no menu principal: {ve}")
        except Exception as e:
            print(Fore.RED + "**************************************** OCORREU UM ERRO DESCONHECIDO ****************************************" + Style.RESET_ALL)
            print(Fore.RED + str(e) + Style.RESET_ALL)
            logging.error(f"Erro desconhecido no menu principal: {str(e)}")
        input(Fore.CYAN + "Pressione Enter para continuar..." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
