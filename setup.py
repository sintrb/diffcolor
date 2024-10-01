from setuptools import setup
import os, io
from diffcolor import __version__

here = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(here, 'README.md'), encoding='UTF-8').read()
CHANGES = io.open(os.path.join(here, 'CHANGES.md'), encoding='UTF-8').read()
setup(name="diffcolor",
      version=__version__,
      keywords=('color', 'diff', 'comapre'),
      description="compare text and show the difference with color.",
      long_description=README + '\n\n\n' + CHANGES,
      long_description_content_type="text/markdown",
      url='https://github.com/sintrb/diffcolor/',
      author="trb",
      author_email="sintrb@gmail.com",
      packages=['diffcolor'],
      install_requires=[],
      zip_safe=False
      )
