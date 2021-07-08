from setuptools import setup

setup(
    name='myflask',
    version='1.0',
    long_description=__doc__,
    packages=['server'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=2.0.1',
        # 'flask-cors',
        'flask-restx',
    ]
)