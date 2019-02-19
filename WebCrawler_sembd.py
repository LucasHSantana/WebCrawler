from bs4 import BeautifulSoup
import requests

TIMEOUT = 1.5 # Define timeout para requests

# Função para extrair o título da página, se existir.
def extract_title(content):
    soup = BeautifulSoup(content, 'html.parser')
    tag = soup.find('title', text=True) # Tenta encontrar a primeira tag 'title' preenchida

    return tag.string.strip() if tag else None # retorna o valor dentro da tag

# Função para extrair todos os links da página
def extract_links(content):
    soup = BeautifulSoup(content, 'html.parser')
    links = set() # Cria uma lista que não permite valores repetidos 

    for tag in soup.find_all('a', href=True): # Pega todas as tags 'a' que contenham o 'href' preenchido
        if tag['href'].startswith('http://') or tag['href'].startswith('https://'): # Se o 'href' começa com http então é link válido
            links.add(tag['href']) # Adiciona a tag na lista

    return links

def crawl(start_url):
    urls_vistas = set([start_url])
    urls_disponiveis = set([start_url])

    while urls_disponiveis:
        url = urls_disponiveis.pop() # Pega uma url da lista de urls disponiveis                 
        
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
            urls_disponiveis.add(link)

        urls_vistas.add(url)        

                
    print()
    print('Nenhuma url disponível!!')
    print('Tente inserir outra Url Inicial')     

if __name__ == '__main__': # Inicia o crawler, CTRL + C para parar.
    try:
        crawl('https://www.python.org/')
    except KeyboardInterrupt:
       print('Terminado!!')
