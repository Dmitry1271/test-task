# Credit Service


## Start


### For start server you need download Docker start start-script.sh from cloned task folder by command:
bash start-script.sh


## Open
    http://localhost


## API methods
    * GET
        * /api/status (account info)
            * params: uuid
    * POST
        * /api/ping (server working status)
        * /api/add (top up balance)
        * /api/subtract (subtract balance)

    
### For POST methods /api/add and /api/add need json in format
    {
        "uuid": "account_uuid",
        "sum": value for adding or subtracting account balance
    }
    