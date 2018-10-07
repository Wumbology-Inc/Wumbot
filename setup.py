from setuptools import setup, find_packages

readme = ''
with open('README.md') as f:
    readme = f.read()

extras_require = {
    'docs': [
        'sphinx>=1.8.0',
        'sphinxcontrib-asyncio',
        'sphinxcontrib-websupport',
    ]
}

setup(name='wumbot',
      author='sco1',
      url='https://github.com/Wumbology-Inc/Wumbot',
      version='v0.10.0',
      description='A Python Discord bot for Wumbology, Inc.',
      long_description=readme,
      extras_require=extras_require,
      python_requires='>=3.6.0',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications :: Chat',
        'Topic :: Internet'
      ]
)