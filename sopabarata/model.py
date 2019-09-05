# -*- coding:utf-8 -*-
from typing import Text

from utils import camel2snake, enmendar


class Base(Text):

    def __new__(cls, *args, **kwargs):
        args = list(map(enmendar, args))
        key = cls.__name__
        if cls.__name__ in 'Producto':
            key = 'NombreProductoAbreviatura'
        else:
            if cls.__name__ in 'EESS':
                key = 'Rótulo'
            kwargs = dict({k: enmendar(v) for k, v in kwargs.items()})

        init = args.pop() if len(args) else kwargs.get(key)
        # init = enmendar(init) if init else init
        if cls.__name__ in kwargs:
            kwargs[key] = init

        cls.kwargs = kwargs
        return Text.__new__(cls, init)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._datos = dict(**kwargs)
        self.codigo = kwargs.pop(f'ID{type(self).__name__}')

    def __repr__(self):
        data = [f'{k}="{v}"' if isinstance(v, str) else f'{k}={v}' for k, v in vars(self).items() if k[0].islower()]
        name = type(self).__name__
        self_str = f'"{self}'
        if len(data):
            self_str = f'{self_str}", '
        return f'{name}({self_str}{", ".join(data)})'.replace("{'", '{').replace("': ", ': ').replace(", '", ', ')

    @property
    def as_dict(self):
        return dict({k: v for k, v in vars(self).items()})

    @property
    def values(self):
        return list(vars(self).values())

    @property
    def nombre(self):
        return str(self)


class Producto(Base):
    """Clase modelo para producto."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.descripcion = kwargs.get('NombreProducto')


class Municipio(Base):
    """Clase modelo para Municipio."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.provincia = Provincia(**kwargs)
        self.ccaa = CCAA(**kwargs)


class Provincia(Base):
    """Clase modelo para Provincia."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.nombre = kwargs.pop('Provincia')
        self.ccaa = CCAA(**kwargs)


class CCAA(Base):
    """Clase modelo para las Comunidades Autonomas."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.codigo = kwargs.get('IDCCAA')


class EESS(Base):
    """Clase modelo para estacion."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.municipio = Municipio(**kwargs)
        self.provincia = Provincia(**kwargs)
        self.ccaa = kwargs.get('IDCCAA')
        self.codigo_postal = kwargs.get("C.P.")
        self.direccion = kwargs.get("Dirección")
        self.horario = kwargs.get("Horario")
        self.latitud = kwargs.get("Latitud")
        # wgs84
        self.longitud = kwargs.get("Longitud (WGS84)")
        self.localidad = kwargs.get("Localidad")
        self.margen = kwargs.get("Margen")
        self.precio = kwargs.get("PrecioProducto")
        self.remision = kwargs.get("Remisión")
        self.rotulo = kwargs.get("Rótulo")
        self.tipo_venta = kwargs.get("Tipo Venta")
        self.precio_biodiesel = kwargs.get("Precio Biodiesel")
        self.precio_bioetanol = kwargs.get("Precio Bioetanol")
        self.precio_gas_natural_comprimido = kwargs.get("Precio Gas Natural Comprimido")
        self.precio_gas_natural_licuado = kwargs.get("Precio Gas Natural Licuado")
        self.precio_gases_licuados_del_petroleo = kwargs.get("Precio Gases licuados del petróleo")
        self.precio_gasoleo_a = kwargs.get("Precio Gasoleo A")
        self.precio_gasoleo_b = kwargs.get("Precio Gasoleo B")
        self.precio_gasolina_95_proteccion = kwargs.get("Precio Gasolina 95 Protección")
        self.precio_gasolina_98 = kwargs.get("Precio Gasolina  98")
        self.precio_nuevo_gasoleo_a = kwargs.get("Precio Nuevo Gasoleo A")
        self.bio_etanol = kwargs.get("% BioEtanol")
        self.ester_metilico = kwargs.get("% Éster metílico")


if __name__ == '__main__':
    import pyperclip as clip
    import json

    copy, paste = clip.determine_clipboard()
    clip_content = paste().strip(' ,\n[]\r\t')
    if clip_content is None or not len(clip_content):
        clip_content = '{}'
    try:
        params = json.loads(clip_content.replace("'", '"'))
        params = list(params)
        class_name = 'Incidencia'
        ident = ' ' * 12

        code = f"""
    class {class_name}(Base):
        \"\"\"Clase modelo para {class_name.lower()}.\"\"\"

        def __init__(self):
            super().__init__(**locals())
"""

        if len(params):
            temp = list(params)
            new_params = list()
            for p in temp:
                parts = camel2snake(p).split('_')
                parts = '_'.join(s for s in parts if s != class_name.lower())
                if len(parts):
                    new_params.append(parts if parts != 'id' else 'codigo')
                    code = code.replace('self', f'self, **kwargs')
                    for new_param, param in zip(new_params, params):
                        code += f'{ident}self.{new_param.lower()} = kwargs.get("{param}")\n'

                    copy(code)
                    print(code)
    except json.JSONDecodeError as err:
        print(str(err))
        print(' - No se detecto datos en formato JSON en el portapeles.')
        exit(1)
