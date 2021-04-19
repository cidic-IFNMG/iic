import setuptools

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name='cidic_iic',
    install_requires=[
          'matplotlib',
          'numpy',
          'pandas'],
    packages=['cidic_iic'],	
    version='0.0.1',
    description='Códigos da disciplina Introdução à IC - Grupo {cidic}',
    long_description='Curso de Introdução à Inteligência Computacional - Grupo de Pesquisa em Ciência de Dados e Inteligência Computacional - {cidic}',
    long_description_content_type="text/markdown",
    author='Petronio Candido L. e Silva',
    author_email='petronio.candido@gmail.com',
    url='https://github.com/cidic-IFNMG/introducao-inteligencia-computacional/',
    download_url='https://github.com/cidic-IFNMG/introducao-inteligencia-computacional/archive/refs/tags/0.0.1.tar.gz',
    keywords=['computational intelligence', 'genetic algorithms', 'fuzzy logic'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',    
    ]
)
