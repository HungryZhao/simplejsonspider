from setuptools import setup, find_packages

setup(
    name='simplejsonspider',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    install_requires=[
        'requests',
        'PyYAML',
    ],
    python_requires='>=3.6',
)
