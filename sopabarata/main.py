#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse

from core import InfoCombustible
from model import CCAA, Provincia


def main(args):
    # print(vars(args))
    # enmendar(args.provincia)
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
                    print(r.precio_gasolina_95, r.rotulo, r.localidad)
                break
    elif args.municipio:
        results = InfoCombustible.buscar_por_nombre(args.municipio)
        if type(results).__name__ == 'Municipio':
            for est in InfoCombustible.get_estaciones_por_municipio(results):
                print(est.precio_gasolina_95, est.rotulo, est.localidad)
        elif isinstance(results, list):
            for r in results:
                if type(r).__name__ == 'Municipio':
                    print(InfoCombustible.get_estaciones_por_municipio(r))


def run():
    # import sys
    # sys.argv.extend(['-m', 'Puerto Del Rosario'])
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--carburantes', action='store_true', help='Listado de carburantes (Productos)')
    zona = parser.add_mutually_exclusive_group()
    zona.add_argument('-c', '--ccaa', help='Filtro por Comunidad Autónoma.')
    zona.add_argument('-p', '--provincia', help='Filtro por Provincia.')
    zona.add_argument('-m', '--municipio', help='Filtro por Municipio.')

    main(parser.parse_args())


if __name__ == '__main__':
    run()
sa
sa
