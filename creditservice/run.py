from sys import argv
from http.server import HTTPServer

from constants import PORT
from dbmanager import init_database
from service import ServerHandler


def run(server_class=HTTPServer, handler_class=ServerHandler, port=PORT):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('Server is running on port {0}...'.format(port))
	httpd.serve_forever()


if __name__ == '__main__':
	# create basic table
	init_database()

	# run server
	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()
