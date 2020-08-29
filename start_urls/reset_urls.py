import json

# reset urls el pais
with open('brasil_elpais.json') as json_file:
    data = json.load(json_file)
    data['internacional'] = 'https://brasil.elpais.com/seccion/internacional/'
    data['economia'] = 'https://brasil.elpais.com/seccion/economia/'
    data['cultura'] = 'https://brasil.elpais.com/seccion/cultura/'
    data['politica'] = 'https://brasil.elpais.com/seccion/politica/'
    data['opinion'] = 'https://brasil.elpais.com/seccion/opinion/'
    data['deportes'] = 'https://brasil.elpais.com/seccion/deportes/'
    data['ciencia'] = 'https://brasil.elpais.com/seccion/ciencia/'
    data['tecnologia'] = 'https://brasil.elpais.com/seccion/tecnologia/'
    data['estilo'] = 'https://brasil.elpais.com/seccion/estilo/'
    with open('brasil_elpais.json', 'w') as outfile:
        json.dump(data, outfile)

# reset urls carta capital
with open('carta_capital.json') as json_file:
    data = json.load(json_file)
    data['Politica'] = 'https://www.cartacapital.com.br/Politica/'
    data['Economia'] = 'https://www.cartacapital.com.br/Economia/'
    data['Sociedade'] = 'https://www.cartacapital.com.br/Sociedade/'
    data['Justica'] = 'https://www.cartacapital.com.br/Justica/'
    data['Mundo'] = 'https://www.cartacapital.com.br/Mundo/'
    data['Diversidade'] = 'https://www.cartacapital.com.br/Diversidade/'
    data['educacao'] = 'https://www.cartacapital.com.br/educacao'
    with open('carta_capital.json', 'w') as outfile:
        json.dump(data, outfile)

# reset urls estadao
with open('estadao.json') as json_file:
    data = json.load(json_file)
    data['ultimas'] = 'https://www.estadao.com.br/ultimas'
    with open('estadao.json', 'w') as outfile:
        json.dump(data, outfile)

# reset urls folha
with open('folha.json') as json_file:
    data = json.load(json_file)
    data['folha'] = 'http://search.folha.uol.com.br search?q=de&site%5B%5D=online%2Fopiniao&site%5B%5D=online%2Fpensata&site%5B%5D=online%2Fpaineldoleitor&site%5B%5D=online%2Fdinheiro&site%5B%5D=online%2Fcotidiano&site%5B%5D=online%2Fmundo&site%5B%5D=online%2Fesporte&site%5B%5D=online%2Fambiente&site%5B%5D=online%2Fciencia&site%5B%5D=online%2Fcomida&site%5B%5D=online%2Feducacao&site%5B%5D=online%2Fequilibrio&sd=01%2F01%2F2010&ed=31%2F12%2F2018&periodo=personalizado&sr=2476&results_count=588401&search_time=0%2C074&url=http%3A%2F%2Fsearch.folha.uol.com.br%2Fsearch%3Fq%3Dde%26site%255B%255D%3Donline%252Fopiniao%26site%255B%255D%3Donline%252Fpensata%26site%255B%255D%3Donline%252Fpaineldoleitor%26site%255B%255D%3Donline%252Fdinheiro%26site%255B%255D%3Donline%252Fcotidiano%26site%255B%255D%3Donline%252Fmundo%26site%255B%255D%3Donline%252Fesporte%26site%255B%255D%3Donline%252Fambiente%26site%255B%255D%3Donline%252Fciencia%26site%255B%255D%3Donline%252Fcomida%26site%255B%255D%3Donline%252Feducacao%26site%255B%255D%3Donline%252Fequilibrio%26sd%3D01%252F01%252F2010%26ed%3D31%252F12%252F2018%26periodo%3Dpersonalizado%26sr%3D2451'
    with open('folha.json', 'w') as outfile:
        json.dump(data, outfile)

# reset urls gazeta_do_povo
with open('gazeta_do_povo.json') as json_file:
    data = json.load(json_file)
    data['politica'] = 'https://www.gazetadopovo.com.br/politica/'
    data['economia'] = 'https://www.gazetadopovo.com.br/economia/'
    data['mundo'] = 'https://www.gazetadopovo.com.br/mundo/'
    data['justica'] = 'https://www.gazetadopovo.com.br/justica/'
    data['educacao'] = 'https://www.gazetadopovo.com.br/educacao/'
    data['esportes'] = 'https://www.gazetadopovo.com.br/esportes/'
    data['republica'] = 'https://www.gazetadopovo.com.br/republica/'
    data['agronegocio'] = 'https://www.gazetadopovo.com.br/agronegocio/'
    data['vida-e-cidadania'] = 'https://www.gazetadopovo.com.br/vida-e-cidadania/'
    with open('gazeta_do_povo.json', 'w') as outfile:
        json.dump(data, outfile)

# reset urls oantagonista
with open('oantagonista.json') as json_file:
    data = json.load(json_file)
    data['oantagonista'] = 'https://www.oantagonista.com/'
    with open('oantagonista.json', 'w') as outfile:
        json.dump(data, outfile)

# reset urls oglobo
with open('oglobo.json') as json_file:
    data = json.load(json_file)
    data['cultura'] = 'https://oglobo.globo.com/api/v1/vermais/cultura/conteudo.json?pagina=1&versao=v1'
    data['sociedade'] = 'https://oglobo.globo.com/api/v1/vermais/sociedade/conteudo.json?pagina=1&versao=v1'
    data['pais'] = 'https://oglobo.globo.com/api/v1/vermais/pais/conteudo.json?pagina=1&versao=v1'
    data['mundo'] = 'https://oglobo.globo.com/api/v1/vermais/mundo/conteudo.json?pagina=1&versao=v1'
    data['economia'] = 'https://oglobo.globo.com/api/v1/vermais/economia/conteudo.json?pagina=1&versao=v1'
    data['tecnologia'] = 'https://oglobo.globo.com/api/v1/vermais/tecnologia/conteudo.json?pagina=1&versao=v1'
    data['saude'] = 'https://oglobo.globo.com/api/v1/vermais/saude/conteudo.json?pagina=1&versao=v1'
    data['ciencia'] = 'https://oglobo.globo.com/api/v1/vermais/ciencia/conteudo.json?pagina=1&versao=v1'
    data['esportes'] = 'https://oglobo.globo.com/api/v1/vermais/esportes/conteudo.json?pagina=1&versao=v1'
    data['educacao'] = 'https://oglobo.globo.com/api/v1/vermais/educacao/conteudo.json?pagina=1&versao=v1'
    data['opiniao'] = 'https://oglobo.globo.com/api/v1/vermais/opiniao/conteudo.json?pagina=1&versao=v1'

# reset urls veja
with open('veja.json') as json_file:
    data = json.load(json_file)
    data['veja'] = 'https://veja.abril.com.br/?infinity=infinite_scroll&page=0&order=DESC'
    with open('veja.json', 'w') as outfile:
        json.dump(data, outfile)

# reset urls brasil247
with open('brasil247.json') as json_file:
    data = json.load(json_file)
    data['poder'] = 'https://www.brasil247.com/poder'
    data['brasil'] = 'https://www.brasil247.com/brasil'
    data['mundo'] = 'https://www.brasil247.com/mundo'
    data['economia'] = 'https://www.brasil247.com/economia'
    with open('brasil247.json', 'w') as outfile:
        json.dump(data, outfile)
