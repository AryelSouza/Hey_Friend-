# Conjunto de ferramentas ajeis para para manipulaçao de bancos de dados
# com um ORM simples feito com o modulo sqlite3 padrao do python
# tambem conta com ferramentas de criaçao de pdf feito em python puro

import sqlite3
import socket


################################################################################
#                                  DATABASE                                    #
################################################################################
class Orm:
    """Classe para o ORM ou CRUD completo
    ###############
    #   CREATE    #
    ###############
        create_table() -> Cria uma tabela com uma query SQL.

    ###############
    #   SELECT    #
    ###############
        select_all() -> Retorna todos os elementos de uma tabela.
        select_action_column() -> Retorna todos os elementos de uma coluna.

    ###############
    #   INSERT    #
    ###############
        insert_into() ->

    ###############
    #   DELETER   #
    ###############
        delete_one_elemet() ->

    ###############
    #   UPDATE    #
    ###############
        ??????????????????
        ??????????????????
 
    ###############
    #   UPDATE    #
    ###############
        exists_element_in_table() ->
    """

    def __init__(self,PATHDATABASE: str) -> None:
        """
        no self.pathdatabase voce deve especificar o caminho para
        o banco de dados.
        """
        self.pathdatabase = PATHDATABASE
        self.con = sqlite3.connect(self.pathdatabase)
        self.cur = self.con.cursor()

    def __del__(self) -> None:
        self.con.commit()
        self.con.close()

    def query_sql(self, query_sql: str) -> None:
        """Cria uma table com o nome desejado."""
        self.cur.execute(query_sql)

    def select_all(self,name_table: str) -> [(str)]:
        """Retorna todos os elementos de uma tabela expecifica."""
        all_itens = self.cur.execute(f'SELECT * FROM {name_table};')
        return all_itens.fetchall()

    def select_action_column(self,
            name_table: str,
            name_column: str,
            action: str
        ) -> float:
        """
        Retorna um valor com uma funçao de calculo no sql recebe 3
        agumentos nome da tabela, coluna e a açao desejada na coluna.
        """
        column_calcu = self.cur.execute(f'''
            SELECT {action}({name_column})
            FROM {name_table};
        ''')
        return round(float(column_calcu.fetchone()[0]),2)

    def select_today_records(self, name_table: str, data_column: str) -> list[tuple]:
        # Historico de produtos vendidos hoje
        data_de_hoje = datetime.today().date()
        data_de_hoje_formatada = data_de_hoje.strftime('%Y-%m-%d')
        self.cur.execute(f'''
            SELECT * FROM  {name_table} 
            WHERE {data_column} = '{data_de_hoje_formatada}'
            ORDER BY {data_column} DESC;
        ''')
        return self.cur.fetchall()

    def select_seven_day_records(self, name_table: str, data_column: str) -> list[tuple]:
        # Retorna todos os registros de uma tabela em um intervaulo de sete dias
        data_de_hoje = datetime.today().date()
        data_de_sete_dias_atras = data_de_hoje - timedelta(days=7)
        data_de_hoje_formatada = data_de_hoje.strftime('%Y-%m-%d')
        data_de_sete_dias_atras_formatada = data_de_sete_dias_atras.strftime('%Y-%m-%d')
        self.cur.execute(f'''
            SELECT * FROM {name_table}
            where {data_column} <= '{data_de_hoje_formatada}'
            AND {data_column} >= '{data_de_sete_dias_atras_formatada}'
            ORDER BY {data_column} DESC;
        ''')
        return self.cur.fetchall()

    def select_thirty_day_records(self, name_table: str, data_column: str) -> list[tuple]:
        # Retorna todos os registros de uma tabela em um intervaulo de sete dias
        data_de_hoje = datetime.today().date()
        data_de_sete_dias_atras = data_de_hoje - timedelta(days=30)
        data_de_hoje_formatada = data_de_hoje.strftime('%Y-%m-%d')
        data_de_sete_dias_atras_formatada = data_de_sete_dias_atras.strftime('%Y-%m-%d')
        self.cur.execute(f'''
            SELECT * FROM {name_table}
            where {data_column} <= '{data_de_hoje_formatada}'
            AND {data_column} >= '{data_de_sete_dias_atras_formatada}'
            ORDER BY {data_column} DESC;
        ''')
        return self.cur.fetchall()

    def select_sum_today_records(
            self,
            name_table: str,
            data_column: str,
            sum_column: str
        ) -> int:
        # Retorna a soma  de produtos vendidos hoje
        data_de_hoje = datetime.today().date()
        data_de_hoje_formatada = data_de_hoje.strftime('%Y-%m-%d')
        self.cur.execute(f'''
            SELECT SUM({sum_column}) FROM  {name_table} 
            WHERE {data_column} = '{data_de_hoje_formatada}'
            ORDER BY {data_column} DESC;
        ''')
        return self.cur.fetchall()[0][0]

    def select_sum_seven_day_records(
            self,
            name_table: str,
            data_column: str,
            sum_column: str
        ) -> int:
        # Retorna a soma de todos os registros de uma tabela em um intervaulo de sete dias
        data_de_hoje = datetime.today().date()
        data_de_sete_dias_atras = data_de_hoje - timedelta(days=7)
        data_de_hoje_formatada = data_de_hoje.strftime('%Y-%m-%d')
        data_de_sete_dias_atras_formatada = data_de_sete_dias_atras.strftime('%Y-%m-%d')
        self.cur.execute(f'''
            SELECT SUM({sum_column}) FROM {name_table}
            where {data_column} <= '{data_de_hoje_formatada}'
            AND {data_column} >= '{data_de_sete_dias_atras_formatada}'
            ORDER BY {data_column} DESC;
        ''')
        return self.cur.fetchall()[0][0]

    def select_sum_thirty_day_records(
            self,
            name_table: str,
            data_column: str,
            sum_column: str
        ) -> int:
        # Retorna a soma de todos os registros de uma tabela em um intervaulo de sete dias
        data_de_hoje = datetime.today().date()
        data_de_sete_dias_atras = data_de_hoje - timedelta(days=30)
        data_de_hoje_formatada = data_de_hoje.strftime('%Y-%m-%d')
        data_de_sete_dias_atras_formatada = data_de_sete_dias_atras.strftime('%Y-%m-%d')
        self.cur.execute(f'''
            SELECT SUM({sum_column}) FROM {name_table}
            where {data_column} <= '{data_de_hoje_formatada}'
            AND {data_column} >= '{data_de_sete_dias_atras_formatada}'
            ORDER BY {data_column} DESC;
        ''')
        return self.cur.fetchall()[0][0]

    def insert_into(self, name_table: str, values: dict) -> None:
        """Isere N elementos em uma tabela,com args nome e o dict dados"""
        #(len(values.keys()) *'?,')[0:-1] - retorner N * '?,'
        #[0:-1] - retira aa vigula no final da sting
        #[tuple(values.values())] - retun lista com uma dupla de valores
        if 'typeform' in values.keys():
            del values['typeform']
        args: str = (len(values.keys()) *'?,')[0:-1]
        self.cur.executemany(f'''
            insert into {name_table}
            values({args});
        ''',[tuple(values.values())])

    def delete_one_elemet(self, name_table: str, name_column: str, velue: str) -> None:
        """Deleta um unico elemento da tabela"""
        self.cur.execute(f'''
            DELETE FROM {name_table}
            WHERE {name_column} == '{velue}';
        ''')

    def exists_element_in_table(
            self,
            name_table: str,
            name_column: str,
            value: str
        ) -> bool:
        """Verivica se um elemento existe na tabela,
        e retorna True ou False
        """
        self.cur.execute(f'''
            SELECT EXISTS (
                SELECT 1
                FROM {name_table}
                WHERE {name_column} = '{value}'
            ) AS valor_existe;
        ''')
        result = self.cur.fetchone()[0]
        if result == 0:
            return True
        return False 

    def get_counts_for_1_7_30_days_records(
            self,
            name_table: str,
            data_column: str
        ) -> list[tuple]:
        # retorna um dict das soma de cada periodo de um , sete e trinta dias
        return {
            'oneday': len(self.select_today_records(name_table, data_column)),
            'sevenday': len(self.select_seven_day_records(name_table, data_column)),
            'thirtyday': len(self.select_thirty_day_records(name_table, data_column)),
        }

    def get_sum_for_1_7_30_days_records(
            self,
            name_table: str,
            data_column: str,
            sum_column: str
        ) -> list[tuple]:
        return {
            'sumoneday': self.select_sum_today_records(name_table, data_column, sum_column),
            'sumsevenday': self.select_sum_seven_day_records(name_table, data_column, sum_column),
            'sumthirtyday': self.select_sum_thirty_day_records(name_table, data_column, sum_column),
        }

################################################################################
#                               SOCKET-TOOLS                                   #
################################################################################
class ToolsSocket:
    def image_server(HOST: str, PORT: str, PATHIMAGE: str) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Esse method setsockopt seve para fehcar a connecao e permitir
        # com quer N clientes se conectem ao socter na rede
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                request = conn.recv(1024).decode('utf-8')
                method = request.split()[1][0:7]
                image = request.split()[1][8:]
                if method == '/images':
                    with open(f'{PATHIMAGE}/{image}', 'rb') as img:
                        image_data = img.read()
                        response = (
                            'HTTP/1.1 200 OK\r\n'
                            'Content-Type: image/png\r\n'
                            'Content-Length: {}\r\n'.format(len(image_data)) +
                            '\r\n'
                        ).encode() + image_data
                    conn.sendall(response)

    def file_server(HOST: str, PORT: str, PATHFILE: str) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    request = conn.recv(1024).decode('utf-8')
                    method = request.split()[1][0:15]
                    filename = request.split()[1][11:]
                    print(method)
                    print(request)
                    if method == '/downloads/pdf/':
                        with open(f'./{PATHFILE}/recibos/{filename}', 'rb') as img:
                            image_data = img.read()
                            response = (
                                'HTTP/1.1 200 OK\r\n'
                                'Content-Type: application/pdf\r\n'
                                'Content-Length: {}\r\n'.format(len(image_data)) +
                                'Connection: close\r\n'  # Fecha a conexão após a resposta
                                '\r\n'
                            ).encode() + image_data
                        conn.sendall(response)

                    if method == '/downloads/csv/':
                        with open(f'./{PATHFILE}/csv/{filename}', 'rb') as img:
                            image_data = img.read()
                            response = (
                                'HTTP/1.1 200 OK\r\n'
                                'Content-Type: application/csv\r\n'
                                'Content-Length: {}\r\n'.format(len(image_data)) +
                                'Connection: close\r\n'  # Fecha a conexão após a resposta
                                '\r\n'
                            ).encode() + image_data
                        conn.sendall(response)

    def to_dict(request: str) -> str:
        # pega o cabecalho http e extrai somente os dados do post
        # logo em seguida transforma os dados em um dicionario
        # retorna um dict com os dados do post
        entrada = request.split()[-1]
        pares = entrada.split('&')
        resultado = {}
        for par in pares:
            chave, valor = par.split('=')
            resultado[chave] = valor
        return resultado

    def get_method(request: str) -> str:
        # retorna uma string com o emthod desejado
        return request.split()[1]
                    
    def cacel_client(conn):
        # evitar erro de falha na conexao do client, erro request vazio
        # dois argumentos coonn o objeto novo de conexao, e o nome do 
        # file para renderizar a home inicial mesmo no erro da reposta
        content='tttttttttttttttttttttt'
        response = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: text/html\r\n'
            'Content-Length: {}\r\n'.format(len(content)) +
            '\r\n'
        ).encode() + content.encode('utf-8')
        conn.sendall(response)
        conn.close()
         


################################################################################
#                                  DATABASE                                    #
################################################################################
class RegexHtml:pass



################################################################################
#                                  DATABASE                                    #
################################################################################
class LoginRequest:pass










































































