import json


# Build and encode json for response
def get_response_json(status=200, success=True, addition={}, description={}):
    return json.dumps({
        'status': status,
        'success': success,
        'addition': addition,
        'description': description
    }).encode()


# Build addition for response json
def get_response_addition(user):
    return {
        'uuid': str(user.uuid),
        'full_name': user.full_name,
        'balance': user.balance,
        'holds': user.holds,
        'is_opened': user.is_opened
    }
