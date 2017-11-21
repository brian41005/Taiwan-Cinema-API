from setuptools import setup
setup(
    name='tw_movie_api',
    version='1.0',
    description='A useful module',
    license="MIT",
    long_description="go test it.",
    author='Brian Ma',
    author_email='brian41005@gmail.com',
    packages=['twmovieapi'],
    install_requires=['lxml', 'bs4', 'requests', 'Pillow']
)
