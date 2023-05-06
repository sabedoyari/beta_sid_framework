import re

def dane_clean_address(address):
    d = {'Calle': 'CL',
         'Carrera': 'KR',
         'Diagonal': 'DG',
         'Autopista': 'AU',
         'Avenida': 'AV',
         'Av. Calle': 'AC',
         'Av. via': 'AK',
         'Camino': 'CM',
         'Carretera': 'CT',
         'Circular': 'CI',
         'Circunvalar': 'CV',
         'Paraje': 'PRJ',
         'Paseo': 'PAS',
         'Transversal': 'TV',
         'Troncal': 'TC',
         'Variante': 'VT'}
    
    regex = re.compile("(%s)" % "|".join(map(re.escape, d.keys())))
    
    address = regex.sub(lambda mo: d[mo.string[mo.start():mo.end()]], address) 

    # Dividir la dirección en sus componentes
    parts = address.split(' ')

    # Obtener el número de la vía
    via = parts[1]

    # Obtener el número del primer dígito después de la "#"
    num1_start = parts[2].find("#") + 1
    num1_final = parts[2].find("-", num1_start)
    num1 = parts[2][num1_start:num1_final]

    # Obtener el número del segundo dígito después de la "#"
    num2_start = num1_final + 1
    num2 = parts[2][num2_start:]

    # Unir los componentes en la dirección final
    clean_address = f"{parts[0]} {via} {num1} {num2}"

    return clean_address
