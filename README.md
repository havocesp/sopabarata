# SopaBarata

 - Author: Daniel J. Umpierrez
 - License: UNLICENSE
 - Version: 0.1.1

## Description

Buscador de precios de carburantes en España usando "Datos Abiertos".

## Instalacion

### Usando el comando `pip`

```sh
# `pip` command by supplying the github project repo URL.
$ pip install git+https://github.com/havocesp/sopabarata
```

## Uso

### Línea de comandos

```sh
# show accepted arguments
$ pcmc --help
# show 1H gainers filtered by exchanges HITBTC, BINANCE and CRYPTOPIA
$ pcmc --timeframe 1h --filter_by gainers hitbtc binance cryptopia
```

## Project dependencies.

- [requests](https://pypi.org/project/requests/)
- [python-dateutil](https://pypi.org/project/python-dateutil)

## Changelog

Project history changes.

### 0.1.1

- Cambiadas las dependencias, ahora solo son necesarias requests y dateutil.
- Actualizada version en setup.py
- Limpieza de código no necesario.
- Añadido gitignore.

### 0.1.0

- Version inicial.

## TODO

- [ ] Probar todas las funciones.
