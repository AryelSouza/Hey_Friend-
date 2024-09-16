import socket
import random
import threading
import json
from os import makedirs,path
from jinja2 import Template
from maintools import (
        Orm,
        ToolsSocket,
)

PATHDATABASE = './db/database.sqlite'


def server_post(HOST, PORT, BUFF): #method post que impede o reenvio de formulario 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("-------- SERVER POST UP --------")
        while True:
            conn, addr = s.accept()
            with conn:
                request = conn.recv(BUFF).decode('utf-8')
                if not request:
                    conn.sendall((
                    'HTTP/1.1 204 No Content\r\n'
                    'Content-Length: 0\r\n'
                    'Connection: close\r\n'
                    '\r\n').encode())
                else:
                    print(request)
                    print('----------- POST  ---------------')
                    data_dict = ToolsSocket.to_dict(request)

                    if data_dict['typeform'] == '0': # faz a publicaçao com imagem
                        custom_post = {
                            'postid': random.randint(100_000,999_999),
                            'linkimage': data_dict['namelink'],
                            'like': 0,
                            'deslike': 0,
                            'coment': data_dict['comment'].replace('+',' '),
                            'user': data_dict['user']
                        }
                        Orm(PATHDATABASE).insert_into('posts',custom_post)

                    elif data_dict['typeform'] == '1': # adiciona as açoes like e deslike
                        if data_dict['typeaction'] == 'like':
                            Orm(PATHDATABASE).query_sql(f"""
                                update posts
                                set like = '{int(data_dict['like']) + 1}'
                                where postid = '{data_dict['postid']}';
                            """) 
                        elif data_dict['typeaction'] == 'deslike':
                            Orm(PATHDATABASE).query_sql(f"""
                                update posts
                                set deslike = '{int(data_dict['deslike']) + 1}'
                                where postid = '{data_dict['postid']}';
                            """) 
                        elif data_dict['typeaction'] == 'comment':
                            del data_dict['typeaction']
                            del data_dict['typeform']
                            Orm(PATHDATABASE).insert_into('comentario',data_dict)

                    elif data_dict['typeform'] == '2': # adiciona as açoes like e deslike
                        del data_dict['typeform']
                        data_dict['name'] = data_dict['name'].replace('+',' ')
                        data_dict['email'] = data_dict['email'].replace('%40','@')
                        print('helo ----------------------')
                        print(data_dict)
                        with open('./login/online', 'r') as file:
                            newuser = json.load(file)
                            newuser['name'] = data_dict['name']
                            newuser['email'] = data_dict['email']
                            
                        with open('./login/online','w') as file:
                            formatado = json.dumps(newuser,indent=True)
                            file.write(formatado)

                       
                        Orm(PATHDATABASE).insert_into('user',data_dict)






                    conn.sendall((
                        'HTTP/1.1 303 See Other\r\n'
                        'Location: http://localhost:2001/\r\n'
                        'Connection: close\r\n'
                        '\r\n'
                    ).encode())
 
            
def server_get(HOST: str, PORT: str, BUFF: str) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)# seve para fehcar a connecao
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    request = conn.recv(BUFF).decode('utf-8')
    if not request:
        conn.sendall((
        'HTTP/1.1 204 No Content\r\n'
        'Content-Length: 0\r\n'
        'Connection: close\r\n'
        '\r\n').encode())
    else:
        method = ToolsSocket.get_method(request)
        if method == '/':
            with open('./gitcustomclone.html', 'r') as file:
                content = file.read()
            with open('./login/online', 'r') as file:
                dic_online = json.load(file)
            template = Template(content)
            content = template.render(
                    dados=Orm(PATHDATABASE).select_all("posts")[::-1],
                    dadoscomentar=Orm(PATHDATABASE).select_all("comentario"),
                    userstatus=dic_online,
            )
            response = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/html\r\n'
                'Content-Length: {}\r\n'.format(len(content)) +
                '\r\n'
            ).encode() + content.encode('utf-8')
            conn.sendall(response)
            conn.close()








################################################################################
#                                    CONFIG                                    #
################################################################################
if __name__ == '__main__':

    # Cria os diretorios caso nao exista
    makedirs('./db', exist_ok=True)
    makedirs('./login', exist_ok=True)

    # Cria o aquivo de user que vai estar logado na aplicaçao
    if not path.isfile('./login/online'):
        with open('./login/online','w') as file:
            user_default = {
                'name': 'Anoinymous',
                'email': '...'
            }
            formatado = json.dumps(user_default,indent=True)
            file.write(formatado)

    # Inicia as threading par o fucionamento de imagem e downloads de
    # arquivos as portas desejadas
    threading.Thread(target=server_post,args=('localhost', 2000, 4096)).start()

    # Cria as tabelas no bancos de dados
    Orm(PATHDATABASE).query_sql("""
        CREATE TABLE IF NOT EXISTS posts (
            postid INT AUTO_INCREMENT PRIMARY KEY,
            linkimage TEXT,
            like TEXT,
            deslike TEXT,
            coment TEXT,
            user TEXT
        );
    """)
    Orm(PATHDATABASE).query_sql("""
        CREATE TABLE IF NOT EXISTS comentario (
            postid TEXT,
            comment TEXT,
            user TEXT
        );
    """)
    Orm(PATHDATABASE).query_sql("""
        CREATE TABLE IF NOT EXISTS user (
            name TEXT,
            email TEXT,
            senha TEXT
        );
    """)
 
    while True:
        server_get('localhost', 2001, 1024)





