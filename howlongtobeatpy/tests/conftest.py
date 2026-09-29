import random
import time
import pytest

@pytest.fixture(autouse=True)
def delay_between_tests():
    """
    This is a pytest logic to make the tests wait some seconds between one test and the next one
    Otherwise making them run too fast will return HTTP 429 Too Many Requests
    Tests will take more, but there is no rush for them
    """
    yield
    time.sleep(random.uniform(3, 6))
