import cgi
import json
import re

from http.server import BaseHTTPRequestHandler
from urllib import parse
from pythonping import ping

from constants import *
from exceptions import AccountNotFoundException, BalanceIsClosedException, InsufficientFundsException
from dbmanager import get_account_by_uuid, change_balance, update_holds
from utilities import get_response_json, get_response_addition


class ServerHandler(BaseHTTPRequestHandler):

    # set need headers
    def _set_headers(self, status=HTTP_200):
        self.send_response(status)
        self.send_header('content-type', 'application/json')
        self.end_headers()

    # send response
    def _send_response(self, status, success, description={}, addition={}):
        self._set_headers(status=status)
        self.wfile.write(get_response_json(status=status, success=success, addition=addition, description=description))

    def do_GET(self):
        url_obj = parse.urlparse(self.path)
        path = url_obj.path  # url path

        # API method 'api/ping'
        if re.match(PING_REGEX, path):
            description = {
                'server_status': SERVER_STATUS_STR,
                'port': PORT_OUTER,
                'host': HOST,
                'ping': [str(p) for p in ping(HOST, verbose=True)],
            }

            self._send_response(status=HTTP_200, success=True, description=description)
            return

        #  API method 'api/status'
        if re.match(STATUS_REGEX, path):
            r = re.search(UUID_REGEX, url_obj.query)

            if r:  # check uuid existence in url
                uuid = r.group(1)  # uuid group = 1
                try:
                    account = get_account_by_uuid(uuid)
                    self._send_response(status=HTTP_200, success=True, addition=get_response_addition(account))
                except AccountNotFoundException as err:
                    self._send_response(status=HTTP_404, success=False, description={'error_message': err.msg})
            else:
                self._send_response(status=HTTP_404, success=False, description={'error_message': VALID_UUID_MSG})
            return

        # 404 http response for unsupported urls
        self._send_response(status=HTTP_404, success=False, description={'error_message': PAGE_NOT_FOUND})

    def do_POST(self):
        url_obj = parse.urlparse(self.path)
        path = url_obj.path  # url path

        # API method '/api/update/holds'
        if re.match(UPDATE_HOLDS_REGEX, path):
            res_lines = update_holds()  # number records updated

            # Gets message based on number records updated
            if res_lines:
                msg = UPDATED_ALL_BALANCES_MSG
            else:
                msg = EMPTY_HOLDS

            self._send_response(status=HTTP_200, success=True, description={'info_message': msg})
            return

        # Determine add or subtract method has been called and get message and is_topup variables
        if re.match(ADD_REGEX, path):
            is_topup = True
            info_message = TOPPED_UP_BALANCE
        if re.match(SUBTRACT_REGEX, path):
            is_topup = False
            info_message = HOLDS_UPDATED

        # API methods '/api/add' and 'api/subtract'
        if re.match(ADD_REGEX, path) or re.match(SUBTRACT_REGEX, path):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            length = int(self.headers.get('content-length'))

            if ctype == 'application/json':
                try:
                    data = json.loads(self.rfile.read(length))
                    addition = data['addition']  # get object with uuid, and sum for adding or subtracting balance
                    value = addition['sum']  # value for adding or subtracting balance

                    if value > 0:
                        # Update account balance and get updated account
                        account = change_balance(uuid=addition['uuid'], value=addition['sum'], is_topup=is_topup)

                        self._send_response(status=HTTP_200, success=True, addition=get_response_addition(account),
                                            description={'info_message': info_message})
                    else:
                        self._send_response(status=HTTP_400, success=False,
                                            description={'error_message': NEGATIVE_SUM_MSG})

                except (json.decoder.JSONDecodeError, KeyError):
                    self._send_response(status=HTTP_400, success=False, description={'error_message': INVALID_JSON_MSG})
                except AccountNotFoundException as err:
                    self._send_response(status=HTTP_404, success=False, description={'error_message': err.msg})
                except BalanceIsClosedException as err:
                    self._send_response(status=HTTP_400, success=False, description={'error_message': err.msg})
                except InsufficientFundsException as err:
                    self._send_response(status=HTTP_400, success=False, description={'error_message': err.msg})

            else:
                self._send_response(status=HTTP_400, success=False,
                                    description={'error_message': UNSUPPORTED_MT_MSG + ctype})
            return

        # 404 http response for unsupported urls
        self._send_response(status=HTTP_404, success=False, description={'error_message': PAGE_NOT_FOUND})
