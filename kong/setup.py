from setuptools import setup, find_packages

setup(
    name = "django-kong",
    version = "0.1",
    packages = find_packages(),
    author = "Eric Holscher",
    author_email = "eric@ericholscher.com",
    description = "A server description and deployment testing tool for King Kong sized sites",
    url = "http://github.com/ericholscher/django-kong/tree/master",
    include_package_data = True,
    )
