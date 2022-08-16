#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse

from core import InfoCombustible
from model import CCAA, Municipio, Provincia

if __name__ == '__main__':
    # import sys

    # sys.argv.extend(['-p', 'cadiz'])
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--carburantes', action='store_true', help='Listado de carburantes (Productos)')
    zona = parser.add_mutually_exclusive_group()
    zona.add_argument('-c', '--ccaa', help='Filtro por Comunidad Autónoma.')
    zona.add_argument('-p', '--provincia', help='Filtro por Provincia.')
    zona.add_argument('-m', '--municipio', help='Filtro por Municipio.')

    args = parser.parse_args()
    # print(vars(args))
    if args.carburantes:
        for p in InfoCombustible.get_productos():
            print(p.codigo, p.nombre, p.descripcion)
    elif args.ccaa:
        results = InfoCombustible.buscar_por_nombre(args.ccaa)
        for r in results:
            if isinstance(r, CCAA):
                print(InfoCombustible.get_estaciones_por_ccaa(r))
                break
    elif args.provincia:
        results = InfoCombustible.buscar_por_nombre(args.provincia)
        for r in results:
            if isinstance(r, Provincia):
                for r in InfoCombustible.get_estaciones_por_provincia(r):
                    print(r.precio, r.rotulo, r.localidad)
                break
    elif args.municipio:
        results = InfoCombustible.buscar_por_nombre(args.municipio)
        for r in results:
            if isinstance(r, Municipio):
                print(InfoCombustible.get_estaciones_por_municipio(r))
                break
