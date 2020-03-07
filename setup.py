from setuptools import setup
import mistletoe

setup(
    name="mistletoe",
    version=mistletoe.__version__,
    description="A fast, extensible Markdown parser in pure Python.",
    url="https://github.com/miyuchina/mistletoe",
    author="Mi Yu",
    author_email="hello@afteryu.me",
    license="MIT",
    packages=["mistletoe"],
    entry_points={"console_scripts": ["mistletoe = mistletoe.__main__:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    keywords="markdown lexer parser development",
    python_requires="~=3.5",
    extras_require={
        "code_style": ["flake8<3.8.0,>=3.7.0", "black==19.10b0", "pre-commit==1.17.0"],
        "testing": ["coverage", "pytest>=3.6,<4", "pytest-cov", "pytest-regressions"],
    },
    zip_safe=False,
)
