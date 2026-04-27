import pytest

BASE_URL = "http://localhost:3000"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def page(page):
    """Override default page fixture to set a consistent viewport."""
    page.set_viewport_size({"width": 1280, "height": 800})
    return page
