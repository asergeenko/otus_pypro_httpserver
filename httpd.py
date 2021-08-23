import asyncio
import argparse
import socket
import os
import mimetypes
from urllib.parse import unquote, urlparse
from datetime import datetime
import logging

from asyncio_pool import AioPool


PROTOCOL = 'HTTP/1.0'
SERVER_NAME = 'OTUServer'

METHODS = ('GET','HEAD')

TERMINATOR = '\r\n\r\n'

OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
NOT_ALLOWED = 405

STATUSES = {
    OK: 'OK',
    BAD_REQUEST: 'Bad Request',
    FORBIDDEN: 'Forbidden',
    NOT_FOUND: 'Not Found',
    NOT_ALLOWED: 'Method Not Allowed'
}

INDEX = 'index.html'
BUF_SIZE = 1024

class TinyHttpHandler:

    def __init__(self, doc_root):
        self.buffer = ''
        self.doc_root = doc_root

        self.filepath = ''
        self.method = METHODS[0]

        self.headers = {'Content-Type': 'text/html',
                        'Content-Length': '0',
                        'Server': SERVER_NAME,
                        'Connection': 'close',
                        'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'), }


    def parse(self,request_str):
        try:
            request = request_str.split('\r\n')
            method, qs, protocol = request[0].split()
            logging.info(request[0])

        except ValueError:
            return BAD_REQUEST
        if method not in METHODS:
            return NOT_ALLOWED

        self.method = method
        urlpath = unquote(urlparse(qs).path)

        path = self.doc_root + urlpath

        # Check if our top directory is DOCUMENT_ROOT (deny /../../../../../ cases)
        if not os.path.abspath(path).startswith(os.path.abspath(self.doc_root) + os.sep):
            return BAD_REQUEST

        # /directory/ - return DOC_ROOT/directory/index.html
        if path.endswith('/') and os.path.isfile(os.path.join(self.doc_root,path,INDEX)):
            self.filepath = os.path.join(self.doc_root,path,INDEX)
        # /../file.html - return DOC_ROOT/../file.html
        elif os.path.isfile(os.path.join(self.doc_root,path)):
            self.filepath = os.path.join(self.doc_root,path)
        if self.filepath:
            return OK
        else:
            return NOT_FOUND

    def process_request(self,request_str):
        code = self.parse(request_str)
        response_lines = ['{} {} {}'.format(PROTOCOL,code,STATUSES[code])]
        body = ''
        if code == OK:
            mtype, _ = mimetypes.guess_type(self.filepath)
            if mtype:
                self.headers['Content-Type'] = mtype

            filesize = os.path.getsize(self.filepath)
            self.headers['Content-Length'] = str(filesize)
            if self.method == 'GET':
                with open(self.filepath, 'rb') as f:
                    body = f.read(filesize)
        response_lines += [': '.join(item) for item in self.headers.items()]
        self.buffer = ('\r\n'.join(response_lines) + TERMINATOR).encode()
        if body:
            self.buffer+=body

        return self.buffer

async def handle_client(client, doc_root,loop):
    try:
        request = (await loop.sock_recv(client, BUF_SIZE)).decode('utf8')
    except Exception:
        logging.exception("Error while receiving request")
    handler = TinyHttpHandler(doc_root)
    response =  handler.process_request(request)
    try:
        await loop.sock_sendall(client, response)
    except Exception:
        logging.exception("Error while sending response")
    client.close()

class OTUServer:
    def __init__(self,ip, port, doc_root):
        self.ip = ip
        self.port = port
        self.doc_root = doc_root

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        self.server.listen(8)
        self.server.setblocking(False)

    def close(self):
        self.server.shutdown(socket.SHUT_RDWR)

    async def run(self,num_workers):
        loop = asyncio.get_event_loop()
        async with AioPool(size=num_workers, loop=loop) as pool:
            while True:
                client, _ = await loop.sock_accept(self.server)
                await pool.spawn(handle_client(client, self.doc_root, loop))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="HTTP server")
    parser.add_argument("-i", "--ip", default="localhost", help="Host to listen")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port to listen")
    parser.add_argument("-w", "--workers", type=int, default=5, help="Number of worker processes")
    parser.add_argument("-r", "--doc_root", default="./",
                        help="Document root")

    args = parser.parse_args()

    logging.basicConfig(filename=None, level=logging.INFO, format='[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    server = OTUServer(args.ip, args.port, args.doc_root)
    loop = asyncio.get_event_loop()

    try:
        logging.info("Server successfully started at %s:%s.\nNumber of workers: %i\nDocument root: %s"%(args.ip,args.port,
                                                                                            args.workers,args.doc_root))
        loop.run_until_complete(server.run(args.workers))
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt. Stopping...")
    except Exception as e:
        print (str(e))
    finally:
        loop.close()
        server.close()
        logging.info("Server stopped")





