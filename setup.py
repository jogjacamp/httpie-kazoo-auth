from setuptools import setup


repo_url = 'https://github.com/jogjacamp/httpie-kazoo-auth'
author = 'Sayid Munawar'
author_email = 'sayid.munawar@gmail.com'


with open('README.rst') as fh:
    long_description = fh.read()

setup(
    name='httpie-kazoo-auth',
    version='0.0.1',
    description='kzaoo auth plugin for HTTPie.',
    long_description=long_description,

    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,

    url=repo_url,
    download_url=repo_url,

    py_modules=['httpie_kazoo_auth'],

    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_kazoo_auth = httpie_kazoo_auth:KazooAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.9.0'
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
