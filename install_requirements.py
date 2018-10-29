'''
    Esse código utiliza o comando pip do python para instalar todas as dependências 
necessárias para executar o script principal.

É necessário que o arquivo requirements.txt esteja na mesma pasta desse script e que contenha
todas as dependências.
'''

import subprocess

subprocess.call('pip install -r requirements.txt', shell=True)