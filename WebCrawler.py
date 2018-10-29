from bs4 import BeautifulSoup
import requests
import mongo_connection

TIMEOUT = 1.5 # Define timeout para requests
'''
    TYPECONNECTION indica o tipo de conexão com o mongodb.

    1 = Conexão com cluster (na nuvem)
    2 = Conexão com bd local
'''
TYPECONNECTION = 1 

uses = input('Usuário MongoDB> ')
pwd = input('Senha MongoDB> ')

if TYPECONNECTION == 1:    
    mongo = mongo_connection.MongoConnection(f'mongodb+srv://{uses}:{pwd}@cluster0-cgmge.mongodb.net/test?retryWrites=true')
    db = mongo.get_client('webcrawler')

# Função para extrair o título da página, se existir.
def extract_title(content):
    soup = BeautifulSoup(content, 'lxml')
    tag = soup.find('title', text=True) # Tenta encontrar a primeira tag 'title' preenchida

    return tag.string.strip() if tag else None # retorna o valor dentro da tag

# Função para extrair todos os links da página
def extract_links(content):
    soup = BeautifulSoup(content, 'lxml')
    links = set() # Cria uma lista que não permite valores repetidos 

    for tag in soup.find_all('a', href=True): # Pega todas as tags 'a' que contenham o 'href' preenchido
        if tag['href'].startswith('http://') or tag['href'].startswith('https://'): # Se o 'href' começa com http então é link válido
            links.add(tag['href']) # Adiciona a tag na lista

    return links

def crawl(start_url):
    if db.indexed.find({'Url': start_url}).count() == 0:
        db.available_urls.update({}, {'Url': start_url}, upsert=True)

    while db.available_urls.count_documents({}) > 0:
        url = db.available_urls.find_one({}) # Pega uma url da lista de urls disponiveis         
        db.available_urls.delete_one({'_id':url['_id']}) # Retira a url da lista e insere na variável url   

        url = url['Url']
        try:
            content = requests.get(url, timeout=TIMEOUT).text # Pega o conteúdo em html da página
        except Exception: # Caso dê erro ao pegar o conteúdo, pula para a próxima url disponível
            continue

        title = extract_title(content) # Pega o título da página

        print('-' * 100)
        if title: # Se o titulo não for nulo, imprime
            print(f'{title}'.center(100))

        print(f'{url}'.center(100)) # Imprime a url da página
        print()
        print('-' * 100)                

        for link in extract_links(content): # Pega todos os links válidos da página            
            print(link)
            db.available_urls.update({'Url': link}, {'Url': link}, upsert=True)

        db.indexed.insert_one({'Title': title, 'Url': url}) # Insere o titulo e a Url no banco de dados
        db.seen_urls.insert_one({'Url': url}) # Adiciona a urls já vistas
                
    print()
    print('Nenhuma url disponível!!')
    print('Tente inserir outra Url Inicial')     

if __name__ == '__main__': # Inicia o crawler, CTRL + C para parar.
    try:
        crawl('https://www.python.org/')
    except KeyboardInterrupt:
       print('Terminado!!')
