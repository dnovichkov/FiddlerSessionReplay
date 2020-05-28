from main import get_headers


def test_get_headers():
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
    headers = get_headers(test_string)
    assert headers.get('Cookie') == 'OSESSIONID=OS15903837780896273042706759459425'
    assert headers.get('Referer') == 'http://localhost:8000/auth/singin'
    assert headers.get('Unknown') is None
    assert len(headers) == 10
