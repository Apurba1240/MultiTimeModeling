from setuptools import setup, find_packages

setup(
    name='Sibyl',
    version='0.3',
    packages=find_packages(),
    install_requires=['cython', 'numpy', 'quandl', 'matplotlib', 'tensorflow', 'pandas', 'pycausalimpact', 'preprocessing', 'sklearn']
)