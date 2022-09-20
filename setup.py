from setuptools import find_packages, setup

exclude_pkgs = [
    '.idea*',
    'build*',
    '*.vs',
    '*.code',
    '*.atom',
    'pipsearch.egg-info*',
    'dist*',
    'venv*'
]

setup(
    name='sopabarata',
    version='0.1.2',
    packages=find_packages(exclude=exclude_pkgs),
    package_dir={'': 'sopabarata'},
    url='https://github.com/havocesp/sopabarata',
    author_email='umpierrez@pm.me',
    license='UNLICENSE',
    author='Daniel J. Umpierrez',
    entry_points={
        'console_scripts': [
            'sopabarata = sopabarata.main:run'
        ]
    },
    description='Buscador de precios de carburantes',
    long_description='Buscador de precios de carburantes'
)
