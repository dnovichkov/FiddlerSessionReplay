from main import get_url


def test_get_url():
    test_string = 'POST http://localhost:8000/auth/token/create HTTP/1.1\n' \
                  'Host: localhost:8000\n' \
                  'Connection: keep-alive\n' \
                  'Content-Length: 38\n' \
                  'Accept: application/json, text/plain, */*\n' \
                  'AdditionalParams:\n' \
                  'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36\n' \
                  'Content-Type: application/json;charset=UTF-8\n' \
                  'Origin: http://localhost:8000\n' \
                  'Sec-Fetch-Site: same-origin\n' \
                  'Sec-Fetch-Mode: cors\n' \
                  'Sec-Fetch-Dest: empty\n' \
                  'Referer: http://localhost:8000/auth/singin\n' \
                  'Accept-Encoding: gzip, deflate, br\n' \
                  'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7\n' \
                  'Cookie: OSESSIONID=OS15903837780896273042706759459425\n' \
                  '\n' \
                  '{"login":"editor","password":"editor"}'
    url = get_url(test_string)
    assert url == 'http://localhost:8000/auth/token/create'

    bad_string = 'POST URL'
    url = get_url(bad_string)
    assert url is None

    simple_string = 'POST URL VERSION'
    url = get_url(simple_string)
    assert url == 'URL'
