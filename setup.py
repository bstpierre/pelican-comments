from setuptools import setup

"""
Static comments plugin for Pelican.
"""

setup(
    name='pelican_comments',
    version='0.0.1',
    long_description=__doc__,
    py_modules=['pelican_comments'],
    author='Brian St. Pierre',
    author_email='brian@bstpierre.org',

    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Environment :: Plugins',
        'Topic :: Internet :: WWW/HTTP',
        ],
)
