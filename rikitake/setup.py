from setuptools import setup

setup(
    name = 'rikitake',
    version = '2.0.0',
    packages = ['rikitake',],
    install_requires=[ 'plumbum', ],
    entry_points = {
        'console_scripts': [
            'rikitake = rikitake.__main__:Rikitake',
            
        ]
    })
