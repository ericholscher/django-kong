from distutils.core import setup

setup(
    name = "django-kong",
    version = "0.9",
    packages = [
        "kong",
        "kong.management",
        "kong.management.commands",
        "kong.templatetags",
        "kong.tests",
    ],
    author = "Eric Holscher",
    author_email = "eric@ericholscher.com",
    description = "A server description and deployment testing tool for King Kong sized sites",
    url = "http://github.com/ericholscher/django-kong/tree/master",
    package_data = {
        'kong': [
            'templates/*.html',
            'templates/kong/*.html',
            'templates/kong/*.txt',
            'fixtures/*.json',

        ],
    },
)
