# coding: utf-8

"""
    WebScraping.AI

    A client for https://webscraping.ai API. It provides a web scaping automation API with Chrome JS rendering, rotating proxies and builtin HTML parsing.  # noqa: E501

    The version of the OpenAPI document: 2.0.2
    Contact: support@webscraping.ai
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "webscraping-ai"
VERSION = "2.0.2"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

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
    long_description="""\
    A client for https://webscraping.ai API. It provides a web scaping automation API with Chrome JS rendering, rotating proxies and builtin HTML parsing.  # noqa: E501
    """
)
