from distutils.core import setup

setup(
    name = "django-jiggety",
    version = "0.0.1",
    packages = [
        "jiggety",
        "jiggety.task_configs",
        "jiggety.task_results",
        "jiggety.tests",
    ],
    author = "Lukasz Dobrzanski",
    author_email = "lukasz.m.dobrzanski@gmail.com",
    description = "HTTP server response testing tool. FunFunFun",
    url = "http://github.com/ssspiochld/django-kong/tree/master",
    package_data = {
        'jiggety': [
            'templates/*',
            'utils/*',
        ],
    },
)
