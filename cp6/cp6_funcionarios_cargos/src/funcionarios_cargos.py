import os
import colorama
import oracledb
import oracledb as orcl
import pandas as pd

# Inicializa o colorama para uso das cores
colorama.init()


def conectar_BD():
    # Função de conexão ao banco de dados
    try:
        dsn = oracledb.makedsn("localhost", "1521", service_name="XEPDB1")
        conexao = oracledb.connect(user="paulo", password="12345", dsn=dsn)
        inst_SQL = conexao.cursor()
        print(
            colorama.Fore.GREEN + "**************************************** CONEXÃO BEM-SUCEDIDA ****************************************" + colorama.Style.RESET_ALL)
        return conexao, inst_SQL, conexao
    except orcl.DatabaseError as e:
        print(
            colorama.Fore.RED + "**************************************** ERRO NA CONEXÃO ****************************************" + colorama.Style.RESET_ALL,
            e)
        return None, None, None


def main():
    conexao, inst_SQL, str_autentic = conectar_BD()

    while conexao:
        exibir_menu_principal()
        try:
            opc_principal = int(input(colorama.Fore.BLUE + "* DIGITE A OPÇÃO DESEJADA: " + colorama.Style.RESET_ALL))
            os.system('cls')
            match opc_principal:
                case 1:
                    crud_cargos(inst_SQL, str_autentic)
                case 2:
                    crud_funcionarios(inst_SQL, str_autentic)
                case 3:
                    relatorio_funcionarios_por_cargo(inst_SQL, str_autentic)
                case 4:
                    relatorio_funcionarios_por_faixa_salarial(inst_SQL, str_autentic)
                case 5:
                    relatorio_funcionarios_por_departamento(inst_SQL, str_autentic)
                case 6:
                    print(
                        colorama.Fore.RED + "**************************************** SAINDO DO SISTEMA ****************************************" + colorama.Style.RESET_ALL)
                    break
                case _:
                    print(
                        colorama.Fore.RED + "**************************************** OPÇÃO INCORRETA. DIGITE UMA OPÇÃO VÁLIDA! ****************************************" + colorama.Style.RESET_ALL)
        except ValueError:
            print(
                colorama.Fore.RED + "**************************************** ERRO: DIGITE UM NÚMERO VÁLIDO! ****************************************" + colorama.Style.RESET_ALL)


def exibir_menu_principal():
    print(
        colorama.Fore.BLUE + "**************************************** MENU PRINCIPAL ****************************************" + colorama.Style.RESET_ALL)
    print(colorama.Fore.BLUE + "* " + colorama.Style.RESET_ALL + "1 - Cadastro de Cargos")
    print(colorama.Fore.BLUE + "* " + colorama.Style.RESET_ALL + "2 - Cadastro de Funcionários")
    print(colorama.Fore.BLUE + "* " + colorama.Style.RESET_ALL + "3 - Relatório de Funcionários por Cargo")
    print(colorama.Fore.BLUE + "* " + colorama.Style.RESET_ALL + "4 - Relatório de Funcionários por Faixa Salarial")
    print(colorama.Fore.BLUE + "* " + colorama.Style.RESET_ALL + "5 - Relatório de Funcionários por Departamento")
    print(colorama.Fore.BLUE + "* " + colorama.Style.RESET_ALL + "6 - Sair do Sistema")
    print(
        colorama.Fore.BLUE + "**************************************************************************************" + colorama.Style.RESET_ALL)


def crud_cargos(inst_SQL, str_autentic):
    while True:
        print(
            colorama.Fore.BLUE + "**************************************** CADASTRO DE CARGOS ****************************************" + colorama.Style.RESET_ALL)
        print("1 - Inserção de Cargo")
        print("2 - Alteração de Cargo")
        print("3 - Exclusão de Cargo")
        print("4 - Relatório de todos os Cargos")
        print("5 - Voltar para o Menu Principal")
        opc_cargo = input("DIGITE A OPÇÃO DESEJADA: ")

        match opc_cargo:
            case "1":
                try:
                    descricao = input("Digite a descrição do cargo: ")
                    departamento = input("Digite o departamento do cargo: ")
                    str_insert = f"INSERT INTO cargos (cargo_descricao, cargo_departamento) VALUES ('{descricao}', '{departamento}')"
                    insert_tabela(inst_SQL, str_autentic, str_insert)
                    print(
                        colorama.Fore.YELLOW + "**************************************** CARGO INSERIDO COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
                except ValueError:
                    print(
                        colorama.Fore.RED + "**************************************** ERRO AO INSERIR CARGO ****************************************" + colorama.Style.RESET_ALL)
            case "2":
                try:
                    cargo_id = int(input("Digite o ID do cargo a ser alterado: "))
                    descricao = input("Digite a nova descrição do cargo: ")
                    departamento = input("Digite o novo departamento do cargo: ")
                    str_update = f"UPDATE cargos SET cargo_descricao='{descricao}', cargo_departamento='{departamento}' WHERE cargo_id={cargo_id}"
                    update_tabela(inst_SQL, str_autentic, str_update)
                    print(
                        colorama.Fore.YELLOW + "**************************************** CARGO ALTERADO COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
                except ValueError:
                    print(
                        colorama.Fore.RED + "**************************************** ERRO AO ALTERAR CARGO ****************************************" + colorama.Style.RESET_ALL)
            case "3":
                try:
                    cargo_id = int(input("Digite o ID do cargo a ser excluído: "))
                    str_delete = f"DELETE FROM cargos WHERE cargo_id={cargo_id}"
                    delete_tabela(inst_SQL, str_autentic, str_delete)
                    print(
                        colorama.Fore.YELLOW + "**************************************** CARGO EXCLUÍDO COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
                except ValueError:
                    print(
                        colorama.Fore.RED + "**************************************** ERRO AO EXCLUIR CARGO ****************************************" + colorama.Style.RESET_ALL)
            case "4":
                str_consulta = "SELECT cargo_id, cargo_descricao, cargo_departamento FROM cargos"
                colunas = ['ID', 'Descrição', 'Departamento']
                consulta_tabela(inst_SQL, str_autentic, str_consulta, colunas)
            case "5":
                os.system('cls')
                break
            case _:
                print(
                    colorama.Fore.RED + "**************************************** OPÇÃO INCORRETA. DIGITE UMA OPÇÃO VÁLIDA! ****************************************" + colorama.Style.RESET_ALL)


def crud_funcionarios(inst_SQL, str_autentic):
    while True:
        print(
            colorama.Fore.BLUE + "**************************************** CADASTRO DE FUNCIONÁRIOS ****************************************" + colorama.Style.RESET_ALL)
        print("1 - Inserção de Funcionário")
        print("2 - Alteração de Funcionário")
        print("3 - Exclusão de Funcionário")
        print("4 - Relatório de todos os Funcionários")
        print("5 - Voltar para o Menu Principal")
        opc_funcionario = input("DIGITE A OPÇÃO DESEJADA: ")

        match opc_funcionario:
            case "1":
                try:
                    nome = input("Digite o nome do funcionário: ")
                    cpf = input("Digite o CPF do funcionário: ")
                    salario = float(input("Digite o salário do funcionário: "))
                    cargo_id = int(input("Digite o ID do cargo do funcionário: "))
                    str_insert = f"INSERT INTO funcionarios (funcionario_nome, funcionario_cpf, funcionario_salario, cargo_id) VALUES ('{nome}', '{cpf}', {salario}, {cargo_id})"
                    insert_tabela(inst_SQL, str_autentic, str_insert)
                    print(
                        colorama.Fore.YELLOW + "**************************************** FUNCIONÁRIO INSERIDO COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
                except ValueError:
                    print(
                        colorama.Fore.RED + "**************************************** ERRO AO INSERIR FUNCIONÁRIO ****************************************" + colorama.Style.RESET_ALL)
            case "2":
                try:
                    funcionario_id = int(input("Digite o ID do funcionário a ser alterado: "))
                    nome = input("Digite o novo nome do funcionário: ")
                    cpf = input("Digite o novo CPF do funcionário: ")
                    salario = float(input("Digite o novo salário do funcionário: "))
                    cargo_id = int(input("Digite o novo ID do cargo do funcionário: "))
                    str_update = f"UPDATE funcionarios SET funcionario_nome='{nome}', funcionario_cpf='{cpf}', funcionario_salario={salario}, cargo_id={cargo_id} WHERE funcionario_id={funcionario_id}"
                    update_tabela(inst_SQL, str_autentic, str_update)
                    print(
                        colorama.Fore.YELLOW + "**************************************** FUNCIONÁRIO ALTERADO COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
                except ValueError:
                    print(
                        colorama.Fore.RED + "**************************************** ERRO AO ALTERAR FUNCIONÁRIO ****************************************" + colorama.Style.RESET_ALL)
            case "3":
                try:
                    funcionario_id = int(input("Digite o ID do funcionário a ser excluído: "))
                    str_delete = f"DELETE FROM funcionarios WHERE funcionario_id={funcionario_id}"
                    delete_tabela(inst_SQL, str_autentic, str_delete)
                    print(
                        colorama.Fore.YELLOW + "**************************************** FUNCIONÁRIO EXCLUÍDO COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
                except ValueError:
                    print(
                        colorama.Fore.RED + "**************************************** ERRO AO EXCLUIR FUNCIONÁRIO ****************************************" + colorama.Style.RESET_ALL)
            case "4":
                str_consulta = "SELECT funcionario_id, funcionario_nome, funcionario_cpf, funcionario_salario FROM funcionarios"
                colunas = ['ID', 'Nome', 'CPF', 'Salário']
                consulta_tabela(inst_SQL, str_autentic, str_consulta, colunas)
            case "5":
                os.system('cls')
                break
            case _:
                print(
                    colorama.Fore.RED + "**************************************** OPÇÃO INCORRETA. DIGITE UMA OPÇÃO VÁLIDA! ****************************************" + colorama.Style.RESET_ALL)


def relatorio_funcionarios_por_cargo(inst_SQL, str_autentic):
    print(
        colorama.Fore.BLUE + "**************************************** RELATÓRIO DE FUNCIONÁRIOS POR CARGO ****************************************" + colorama.Style.RESET_ALL)
    str_consulta = """SELECT f.funcionario_id, f.funcionario_nome, c.cargo_descricao 
                      FROM funcionarios f JOIN cargos c ON f.cargo_id = c.cargo_id"""
    colunas = ['ID', 'Nome', 'Cargo']
    consulta_tabela(inst_SQL, str_autentic, str_consulta, colunas)


def relatorio_funcionarios_por_faixa_salarial(inst_SQL, str_autentic):
    print(
        colorama.Fore.BLUE + "**************************************** RELATÓRIO DE FUNCIONÁRIOS POR FAIXA SALARIAL ****************************************" + colorama.Style.RESET_ALL)
    salario_min = float(input("Digite o salário mínimo: "))
    salario_max = float(input("Digite o salário máximo: "))
    str_consulta = f"""SELECT funcionario_id, funcionario_nome, funcionario_salario 
                       FROM funcionarios WHERE funcionario_salario BETWEEN {salario_min} AND {salario_max}"""
    colunas = ['ID', 'Nome', 'Salário']
    consulta_tabela(inst_SQL, str_autentic, str_consulta, colunas)


def relatorio_funcionarios_por_departamento(inst_SQL, str_autentic):
    print(
        colorama.Fore.BLUE + "**************************************** RELATÓRIO DE FUNCIONÁRIOS POR DEPARTAMENTO ****************************************" + colorama.Style.RESET_ALL)
    departamento = input("Digite o departamento: ")
    str_consulta = f"""SELECT f.funcionario_id, f.funcionario_nome, c.cargo_departamento 
                       FROM funcionarios f JOIN cargos c ON f.cargo_id = c.cargo_id 
                       WHERE c.cargo_departamento = '{departamento}'"""
    colunas = ['ID', 'Nome', 'Departamento']
    consulta_tabela(inst_SQL, str_autentic, str_consulta, colunas)


def consulta_tabela(inst_SQL, str_autentic, str_consulta, colunas):
    try:
        inst_SQL.execute(str_consulta)
        resultados = inst_SQL.fetchall()
        df = pd.DataFrame(resultados, columns=colunas)
        print(df.to_string(index=False))
    except orcl.DatabaseError as e:
        print(
            colorama.Fore.RED + "**************************************** ERRO AO REALIZAR A CONSULTA ****************************************" + colorama.Style.RESET_ALL,
            e)


def insert_tabela(inst_SQL, str_autentic, str_insert):
    try:
        inst_SQL.execute(str_insert)
        str_autentic.commit()
        print(
            colorama.Fore.GREEN + "**************************************** INSERÇÃO REALIZADA COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
    except orcl.DatabaseError as e:
        print(
            colorama.Fore.RED + "**************************************** ERRO AO INSERIR DADOS ****************************************" + colorama.Style.RESET_ALL,
            e)


def update_tabela(inst_SQL, str_autentic, str_update):
    try:
        inst_SQL.execute(str_update)
        str_autentic.commit()
        print(
            colorama.Fore.GREEN + "**************************************** ATUALIZAÇÃO REALIZADA COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
    except orcl.DatabaseError as e:
        print(
            colorama.Fore.RED + "**************************************** ERRO AO ATUALIZAR DADOS ****************************************" + colorama.Style.RESET_ALL,
            e)


def delete_tabela(inst_SQL, str_autentic, str_delete):
    try:
        inst_SQL.execute(str_delete)
        str_autentic.commit()
        print(
            colorama.Fore.GREEN + "**************************************** EXCLUSÃO REALIZADA COM SUCESSO ****************************************" + colorama.Style.RESET_ALL)
    except orcl.DatabaseError as e:
        print(
            colorama.Fore.RED + "**************************************** ERRO AO EXCLUIR DADOS ****************************************" + colorama.Style.RESET_ALL,
            e)


if __name__ == "__main__":
    main()
