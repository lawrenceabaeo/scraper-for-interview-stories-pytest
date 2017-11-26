import pytest


def pytest_addoption(parser):
    parser.addoption("--company", action="store", default="",
        help="The name of the company you want to search for")
    parser.addoption("--location", action="store", default="",
        help="Where the company is probably located")

@pytest.fixture
def company(request):
    return request.config.getoption("--company")

@pytest.fixture
def location(request):
    return request.config.getoption("--location")

    