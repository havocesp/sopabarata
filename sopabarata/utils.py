# -*- coding:utf-8 -*-
import re


def normalizar(text: str) -> str:
    """Normaliza un texto quitando acentos y cambiandolos por la letra mas parecida.

    >>> normalizar('espáña')
    'espana'

    :param text: texto a normalizar.
    :return: texto normalizado.
    """
    return f'{text}'.translate(str.maketrans('áéíóúüñç', 'aeiouunc'))


def enmendar(nombre):
    articulos = ' (LA)', ' (La)', ' (El)', ' (Los)', ' (Las), ', ', (LOS)', ', (LAS)'
    if isinstance(nombre or 0, str):
        nombre = nombre.title()
        if any(a in nombre for a in articulos):
            for a in articulos:
                if nombre.endswith(a):
                    art = a.strip(' ()').title()
                    nombre = nombre.replace(a, '').title()
                    return f"{art} {nombre}"

    return nombre


def to_num(obj):
    if isinstance(obj, dict):
        return {k: to_num(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_num(v) for v in obj]
    else:
        try:
            return int(obj) if float(str(obj).replace(',', '.')).is_integer() else float(obj)
        except:
            return obj


def camel2snake(text):  # , class_name=None):
    """Convert text from camel case (helloWorld) to snake case (hello_world).

    >>> camel2snake('helloWorld' )
    'hello_world'

    :param str text:
    :return str:
    """
    if text == 'IDCCAA':
        text = 'id_ccaa'
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    str1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()
    return str1
