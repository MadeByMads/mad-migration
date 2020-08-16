from setuptools import setup,find_packages

setup(
    name='MadMIgration',
    packages=["src","utils","config","scripts","db_init"],
    entry_points="""
        [console_scripts]
        madmigrate=scripts.start:cli
    """,
    classifiers=[
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3 :: Only",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
])











