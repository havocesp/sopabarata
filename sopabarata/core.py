# -*- coding:utf-8 -*-
import sys
from typing import Dict, List, Optional as Opt, Union as U

import requests

import static as st
from model import CCAA, EESS, Municipio, Producto, Provincia
from utils import normalizar, to_num

Municipios = List[Municipio]
Productos = List[Producto]
Estaciones = List[EESS]
Autonomias = List[CCAA]
Provincias = List[Provincia]


# noinspection PyUnresolvedReferences
class InfoCombustible:
    _municipios: Opt[Municipios] = None
    _productos: Opt[Productos] = None

    @classmethod
    def _consulta(cls, url) -> U[List, Dict]:
        datos = None
        try:
            respuesta = requests.get(url)
            datos = respuesta.json()
        except Exception as err:
            print(f' - [ERROR] {err}', file=sys.stderr)
        return to_num(datos)

    @classmethod
    def gestion_resultados_estaciones(cls, datos, zone_type) -> List:
        datos = [EESS(**d) for d in datos.get('ListaEESSPrecio')]
        for d in list(datos):
            resultados = cls.buscar_por_nombre(getattr(d, zone_type.__name__.lower()))
            for r in resultados:
                if isinstance(r, zone_type):
                    setattr(d, zone_type.__name__.lower(), r)
                    break
        return sorted(datos, key=lambda s: s.precio)

    @classmethod
    def get_estaciones_por_producto(cls, producto) -> Estaciones:
        """Listado de todas las estaciones que tienen el codigo de producto solicitado.

        :param producto: codigo del producto usado como filtro de resultados..
        :return: todas las estaciones que tienen el producto solicitado.
        """
        producto = producto.codigo if isinstance(producto, Producto) else int(producto)
        data = cls._consulta(f'{st.REST_ESTACION}Producto/{producto:02d}')
        return data

    @classmethod
    def get_estaciones_por_ccaa(cls, ccaa) -> Estaciones:
        ccaa = ccaa.codigo if isinstance(ccaa, CCAA) else int(ccaa)
        data = cls._consulta(f'{st.REST_ESTACION}CCAA/{ccaa:02d}')
        return cls.gestion_resultados_estaciones(data, CCAA)

    @classmethod
    def get_estaciones_por_provincia(cls, provincia) -> Estaciones:
        provincia = provincia.codigo if isinstance(provincia, Provincia) else int(provincia)
        data = cls._consulta(f'{st.REST_ESTACION}Provincia/{provincia:02d}')
        return cls.gestion_resultados_estaciones(data, Provincia)

    @classmethod
    def get_estaciones_por_municipio(cls, municipio) -> Estaciones:
        municipio = municipio.codigo if isinstance(municipio, Provincia) else int(municipio)
        data = cls._consulta(f'{st.REST_ESTACION}Municipio/{municipio:04d}')
        return cls.gestion_resultados_estaciones(data, Municipio)

    @classmethod
    def get_estaciones_por_ccaa_y_producto(cls, ccaa, producto) -> Estaciones:
        producto = producto.codigo if isinstance(producto, Producto) else int(producto)
        ccaa = ccaa.codigo if isinstance(ccaa, CCAA) else int(ccaa)
        data = cls._consulta(f'{st.REST_ESTACION}CCAAProducto/{ccaa:02d}/{producto:02d}')
        return cls.gestion_resultados_estaciones(data, CCAA)

    @classmethod
    def get_estaciones_por_provincia_y_producto(cls, provincia, producto) -> Estaciones:
        producto = producto.codigo if isinstance(producto, Producto) else int(producto)
        provincia = provincia.codigo if isinstance(provincia, Provincia) else int(provincia)
        data = cls._consulta(f'{st.REST_ESTACION}ProvinciaProducto/{provincia:02d}/{producto:02d}')
        return cls.gestion_resultados_estaciones(data, Provincia)

    @classmethod
    def get_estaciones_por_municio_y_producto(cls, municipio, producto) -> Estaciones:
        municipio = municipio.codigo if isinstance(municipio, Provincia) else int(municipio)
        producto = producto.codigo if isinstance(producto, Producto) else int(producto)
        data = cls._consulta(f'{st.REST_ESTACION}MunicipioProducto/{municipio:04d}/{producto:02d}')
        return cls.gestion_resultados_estaciones(data, Municipio)

    @classmethod
    def get_productos(cls) -> Productos:
        """Obtiene datos sobre carburantes aceptados.

        >>> all(isinstance(p, Producto) for p in InfoCombustible().get_productos())
        True

        :return:
        """
        if cls._productos is None or len(cls._productos) == 0:
            cls._productos = cls._consulta(f'{st.REST_LISTADO}/ProductosPetroliferos/')
        return [Producto(**p) for p in cls._productos]

    @classmethod
    def get_comunidades_autonomas(cls) -> Autonomias:
        """Obtiene los datos replacionados con las comunidades autónomas.

        >>> all(isinstance(ccaa, CCAA) and len(ccaa) for ccaa in InfoCombustible().get_comunidades_autonomas())
        True

        :return:
        """
        return list({m.ccaa for m in cls.get_municipios()})
        # data = self._consulta(f'{st.REST_LISTADO}/ComunidadesAutonomas/')

    @classmethod
    def get_provincias(cls, ccaa=None) -> Provincias:
        # data = cls._consulta(f'{st.REST_LISTADO}/Provincias/')
        ccaa = ccaa.codigo if isinstance(ccaa, CCAA) else int(ccaa)
        return list({p.provincia for p in cls.get_municipios() if ccaa is None or p.ccaa == ccaa})

    @classmethod
    def get_municipios(cls) -> List[Municipio]:
        """Obtiene los datos de referencia de todos los municipios.

        >>> all(isinstance(m, Municipio) for m in InfoCombustible.get_municipios())
        True

        :return: datos de referencia de todos los municipios.
        """
        if cls._municipios is None or len(cls._municipios) == 0:
            cls._municipios = [Municipio(**i) for i in cls._consulta(f'{st.REST_LISTADO}/Municipios/')]
        return cls._municipios

    @classmethod
    def get_provincias_por_ccaa(cls, ccaa) -> Provincias:
        ccaa = ccaa.codigo if isinstance(ccaa, CCAA) else int(ccaa)
        return list({p.provincia for p in cls.get_municipios() if p.ccaa == ccaa})
        # return cls.gestion_resultados_estaciones(data)ls._consulta(f'{st.REST_LISTADO}/ProvinciasPorComunidad/{int(ccaa):02d}')

    @classmethod
    def get_municipios_por_provincia(cls, provincia) -> Municipios:
        provincia = provincia.codigo if isinstance(provincia, Provincia) else int(provincia)
        return list({p for p in cls.get_municipios() if p.provincia == provincia})
        # return cls.gestion_resultados_estaciones(data)ls._consulta(f'{st.REST_LISTADO}/MunicipiosPorProvincia/{int(provincia):02d}')

    @classmethod
    def buscar_por_nombre(cls, *args) -> U[List[U[Municipio, Provincia, CCAA]], U[Municipio, Provincia, CCAA]]:
        resultados = list()
        nombres = [normalizar(str(n).strip().lower()) for n in args if n]

        # if isinstance(nombre, str) and len(nombre) >= 0:
        for m in cls.get_municipios():
            if any(n in normalizar(m.lower()) for n in nombres):
                resultados.append(m)
            if any(n in normalizar(m.provincia.lower()) for n in nombres):
                resultados.append(m.provincia)
            if any(n in normalizar(m.ccaa.lower()) for n in nombres):
                resultados.append(m.ccaa)

        if len(resultados) == 1:
            return resultados[0]
        else:
            return sorted(set(resultados))

    @classmethod
    def buscar_por_codigo(cls, *args) -> U[List[U[Municipio, Provincia, CCAA]], U[Municipio, Provincia, CCAA]]:
        resultados = list()
        codigos = [int(c) for c in args if (isinstance(c or [], int) or str(c).isnumeric()) and int(c) > 0]
        for m in cls.get_municipios():
            if any(m.codigo == c for c in codigos):
                resultados.append(m)
            if any(m.provincia.codigo == c for c in codigos):
                resultados.append(m.provincia)
            if any(m.ccaa.codigo == c for c in codigos):
                resultados.append(m.ccaa)

        if len(resultados) == 1:
            return resultados[0]
        else:
            return sorted(set(resultados))

    @classmethod
    def buscar_producto(cls, *args) -> U[Productos, Producto]:
        resultados = list()
        productos = [str(n).strip().lower() for n in args if n]

        for m in cls.get_productos():
            if any(n in m.lower() or n in m.nombre.lower() for n in productos):
                resultados.append(m)

        if len(resultados) == 1:
            return resultados[0]
        else:
            return sorted(set(resultados))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    # print(InfoCombustible.buscar_por_nombre('albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete', 'albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete', 'albacete', 'albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete', 'albacete', 'albacete', 'albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete', 'albacete'))
    # print(InfoCombustible.buscar_por_nombre('albacete', 'albacete', 'albacete', 'albacete', 'albacete
    # municipio = InfoCombustible.buscar_por_nombre('Los Barrios')
    # print(municipio[0])
    # d = InfoCombustible.get_estaciones_por_municio_y_producto(municipio[0].codigo, 15)
    # pprint(d)
    # data = InfoCombustible.get_comunidades_autonomas()
    # data = InfoCombustible.buscar_ccaa_por_nombre('Canarias')
    # data = InfoCombustible.buscar_por_codigo(5, 67, 4005)
    # data = InfoCombustible.buscar_por_nombre('Puerto Del Rosario')
    # data = InfoCombustible.get_productos()
    # productos = InfoCombustible.buscar_producto('GPR')
    # for d in data:
    #     print(d.codigo, d, d.descripcion)
    # data = InfoCombustible.get_estaciones_por_producto(1)

    # # data = InfoCombustible.get_provincias(5)
    # if isinstance(data, list):
    #     pprint(list(map(str, data)))
    # else:
    #     print(data)
    # productos = infogas.get_productos()
