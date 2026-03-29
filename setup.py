import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qdkit",
    version="0.1.2",
    author="teleping",
    author_email="teleping@gmail.com",
    description="quant data toolkits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/qdkit/",
    project_urls={
        "Bug Tracker": "https://pypi.org/project/qdkit/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "sqlalchemy",
        "pangres",
        "pymysql",
        "logbook",
        "pyyaml",
        "requests",
    ],
    extras_require={
        "bloomberg": ["xbbg"],
        "wind": ["WindPy"],
    },
)
