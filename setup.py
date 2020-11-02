from glob import glob
from os import path
from os.path import basename, splitext

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    setup(
        name='varsubst',
        version='1.0.0',
        url='https://github.com/tiboun/varsubst',
        author='Bounkong Khamphousone',
        author_email='bounkong@gmail.com',
        py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
        packages=find_packages('src'),
        package_dir={'': 'src'},
        include_package_data=True,
        zip_safe=False,
        description=("Substitute variables in a string with a given resolver."
                     " Act as a render template."),
        license="MIT",
        long_description=long_description,
        long_description_content_type='text/markdown',
        extras_require={
            'jinja2':  ["jinja2"]
        }
    )
