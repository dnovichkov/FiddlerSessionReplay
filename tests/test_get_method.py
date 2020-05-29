from main import get_method


def test_get_method():
    method = get_method('GET url POST')
    assert method == 'GET'

    method = get_method('GET url ver')
    assert method == 'GET'

    method = get_method('POST smth else')
    assert method == 'POST'

    method = get_method('Some text without method')
    assert method is None
