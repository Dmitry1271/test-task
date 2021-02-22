# Credit Service

## Start

    For start server you need download Docker 
    Then start start-script.sh from cloned task folder by command:
    
    # bash start-script.sh


## Open
    http://localhost


## API methods
    * GET
        * /api/ping (server working status)
        * /api/status (account info)
            * params: uuid
    * POST
        * /api/add (top up balance)
        * /api/subtract (subtract balance)

    
### For POST methods /api/add and /api/subtract need json in format:
    {   
        "addition": {
            "uuid": "account_uuid",
            "sum": value for adding or subtracting account balance
        }
    }
    
