# coding: utf-8

"""
    WebScraping.AI

    WebScraping.AI scraping API provides LLM-powered tools with Chromium JavaScript rendering, rotating proxies, and built-in HTML parsing.

    The version of the OpenAPI document: 3.2.0
    Contact: support@webscraping.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "webscraping-ai"
VERSION = "3.2.0"
PYTHON_REQUIRES = ">= 3.8"
REQUIRES = [
    "urllib3 >= 1.25.3, < 3.0.0",
    "python-dateutil >= 2.8.2",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="WebScraping.AI",
    author="WebScraping.AI Support",
    author_email="support@webscraping.ai",
    url="https://webscraping.ai",
    keywords=["OpenAPI", "OpenAPI-Generator", "WebScraping.AI"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description="""\
    WebScraping.AI scraping API provides LLM-powered tools with Chromium JavaScript rendering, rotating proxies, and built-in HTML parsing.
    """,  # noqa: E501
    package_data={"webscraping_ai": ["py.typed"]},
)