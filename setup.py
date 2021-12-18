"""The setup script."""
from setuptools import find_packages
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

test_requirements = ['pytest']

setup(
    author='Ammar Najjar',
    author_email='najjarammar@protonmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Automate my boring stuff.',
    entry_points={
        'console_scripts': [
            'pautomate=pautomate.main:main',
            'fetch=pautomate.main:fetch',
            'releases=pautomate.main:releases',
            'branches=pautomate.main:branches',
            'dnet=pautomate.main:dotnet',
        ],
    },
    license='MIT license',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pautomate',
    name='pautomate',
    packages=find_packages(include=['pautomate']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ammarnajjar/pautomate',
    version='0.1.1',
    zip_safe=False,
)
