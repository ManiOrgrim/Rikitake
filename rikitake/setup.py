from setuptools import setup

setup(
    name = 'rikitake',
    version = '2.0.1',
    packages = ['rikitake',],
    install_requires=[ 'plumbum', ],
    entry_points = {
        'console_scripts': [
            'rikitake = rikitake.__main__:Rikitake',
            
        ]
    })
