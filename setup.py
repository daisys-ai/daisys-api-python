from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="daisys",
    version="1.0.1",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        'pydantic>=2',
        'httpx>=0.28.1',
    ],
    extras_require={
        'ws': ['httpx-ws>=0.7.1'],
    },
    author="daisys.ai",
    author_email="api@daisys.ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daisys-ai/daisys-api-python",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
