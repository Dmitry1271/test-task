# Service port in docker container
PORT = 8000

# Service port
PORT_OUTER = 80

#localhost
HOST = 'localhost'

# Database path
DB_PATH = 'db/database.db'

# uuid url param match regex
UUID_REGEX = 'uuid=([0-9a-fA-F\\-]{36})'

# server status
SERVER_STATUS_STR = 'Server is running...'

# HTTP statues
HTTP_200 = 200
HTTP_400 = 400
HTTP_404 = 404

# API methods regexes
PING_REGEX = '^/api/ping?(\\?.+)?$'
STATUS_REGEX = '^/api/status?(\\?.+)?$'
ADD_REGEX = '^/api/add?(\\?.+)?$'
SUBTRACT_REGEX = '^/api/subtract/?(\\?.+)?$'
UPDATE_HOLDS_REGEX = '^/api/update/holds?(\\?.+)?$'

# Error description messages
NEGATIVE_SUM_MSG = 'Sum should be positive integer'
INSUFFICIENT_FUNDS_MSG = 'Insufficient funds on account balance'
DOES_NOT_EXIST_MSG = 'Account does not exist'
BALANCE_IS_CLOSED_MSG = 'Account balance is closed'
UNSUPPORTED_MT_MSG = 'Unsupported media type: '
INVALID_JSON_MSG = 'Invalid requested json'
VALID_UUID_MSG = 'Valid account uuid required'
PAGE_NOT_FOUND = 'Page not found'

# Info description messages
UPDATED_ALL_BALANCES_MSG = 'All balances have been successfully updated with holds'
UPDATED_BALANCE_MSG = 'Account balance has been successfully updated'
EMPTY_HOLDS = 'All holds are empty'
TOPPED_UP_BALANCE = 'Account balance has been successfully topped up'
HOLDS_UPDATED = 'Account holds has been successfully updated'
