import json

with open('brasil_elpais.json') as json_file:
    data = json.load(json_file)
    data['internacional'] = 'https://brasil.elpais.com/seccion/internacional/'
    data['economia'] = 'https://brasil.elpais.com/seccion/economia/'
    data['cultura'] = 'https://brasil.elpais.com/seccion/cultura/'
    data['politica'] = 'https://brasil.elpais.com/seccion/politica/'
    data['opinion'] = 'https://brasil.elpais.com/seccion/opinion/'
    data['deportes'] = 'https://brasil.elpais.com/seccion/deportes/'
    with open('brasil_elpais.json', 'w') as outfile:  
        json.dump(data, outfile)
            
