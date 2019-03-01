from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import requests
import json
import time

def getKey():
  file = open("key.json", "r")
  key = json.load(file)

  return key['key']

f = open('logs.txt', 'w')

def request1():
    start = time.time()
    response1 = requests.get("http://api.icndb.com/jokes/random")
    end = time.time()
    latenta = end - start
    response1 = response1.json()

    f.write("http://api.icndb.com/jokes/random" + "\t"+ str(json.dumps(response1))+ str(latenta) +  "\n")
    print("jokes" + "\t"+ str(json.dumps(response1))+ str(latenta) +  "\n")

    return response1


def request2(id):
    start = time.time()
    url2 = "http://numbersapi.com/" + str(id) + "/year?json"
    response2 = requests.get(url2)
    end = time.time()
    latenta = end - start
    response2 = response2.json()

    f.write(url2 + "\t"+ str(json.dumps(response2))+ str(latenta) +  "\n")
    print(url2 + "\t"+ str(json.dumps(response2))+ str(latenta) +  "\n")

    return response2


def request3(text1, text2):
    url3 = "https://pastebin.com/api/api_post.php"
    values = {'api_option': 'paste',
            'api_dev_key': getKey(),
            'api_paste_code': text1 + '\n' + text2,
    }
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')  # data should be bytes
    start = time.time()
    req = urllib.request.Request(url3, data)

    with urllib.request.urlopen(req) as response:
        response3 = response.read().decode()
    end = time.time()
    latenta = end - start

    x = '{ "link":"0"}'
    y = json.loads(x)
    y["link"] = response3
    x = json.dumps(y)

    f.write(url3 + "\t"+ str(json.dumps(response3))+ str(latenta) +  "\n")


    return x


"""
response1 = request1()
response2 = request2(response1['value']['id'])
response3 = request3(response1['value']['joke'], response2['text'])

print(response3)
"""
 
# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
    if self.path == '/':
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:4200')
        self.end_headers()
 
        # Send message back to client
        message = json.dumps(request1())
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
    elif self.path == '/trivia':
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:4200')
        self.end_headers()
 
        # Send message back to client
        message = json.dumps(request2(request1()['value']['id']))
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
    elif self.path == '/pastebin':
        # Send response status code
        self.send_response(200)
 
        # Send headers
        self.send_header('Content-type','text/html')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:4200')
        self.end_headers()
 
        # Send message back to client
        message = request3(request1()['value']['joke'], request2(request1()['value']['id'])['text'])
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        
 
def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('localhost', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
 
 
run()