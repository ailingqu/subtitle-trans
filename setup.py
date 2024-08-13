import os

from setuptools import setup, find_packages

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_requirements(path):
    with open(path, encoding="utf-8") as requirements:
        return [requirement.strip() for requirement in requirements]


def get_long_description():
    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, encoding="utf-8") as readme_file:
        return readme_file.read()


def get_project_version():
    version_path = os.path.join(base_dir, "subtitle_trans", "version.py")
    version = {}
    with open(version_path, encoding="utf-8") as fp:
        exec(fp.read(), version)
    return version["__version__"]


install_requires = get_requirements(os.path.join(base_dir, "requirements.txt"))

setup(
    name='subtitle-trans',
    version=get_project_version(),
    license="MIT",
    packages=find_packages(),
    install_requires=install_requires,
    python_requires='==3.10',
    author='laihan',
    author_email='nclaihan@foxmail.com',
    description='A library that extracts subtitles from audio files and translates them into the target language',
    keywords="e",
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/ailingqu/subtitle-trans',  # 项目的主页
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
