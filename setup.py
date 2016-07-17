from setuptools import setup


setup(
    name='kron',
    version='0.0',
    author='Sean Gilleran',
    author_email='sgilleran@gmail.com',
    url='https://github.com/seangilleran/kron',
    # download_url,
    license='MIT',
    install_requires=[
        'click>=6.6',
        'Flask>=0.11.1',
        'Flask-Classy>=0.6.10',
        'Flask-Script>=2.0.5',
        'Flask-SQLAlchemy>=2.1',
        'hashids>=1.1.0',
        'itsdangerous>=0.24',
        'Jinja2>=2.8',
        'MarkupSafe>=0.23',
        'pytz>=2016.6.1',
        'SQLAlchemy>=1.0.14',
        'Werkzeug>=0.11.10'
    ]
    packages=['kron'],
    include_package_data=True,
    zip_safe=False
)
