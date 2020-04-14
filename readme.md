Тестовое задание

API приложения для ведения личного бюджета
____________________________

All responses are JSON structures.

**ENDPOINTS**

POST `/api/wallets` 

GET `/api/wallets`

GET `/api/wallets/<pk>`

PUT `/api/wallets/<pk>` 

DELETE `/api/wallets/<pk>` 

GET `/api/operations`

POST `/api/operations` 

DELETE `/api/operations/<pk>` 

____________

**POST** `/api/wallets` 

Create a new wallet

###### **Request parameters**

- name (str, required, unique)
- balance (decimal number, required)

###### **Response parameters**
- id (int)
- name (str)
- balance (decimal number)

###### **Response code**

`201` for success

`400` for error

###### **Request body example**

`{"name": "Account in Imaginary Bank", "balance": 10840000.00}`
 

###### **Response body example**

`{ "id": 1, "name": "Account in Imaginary Bank", "balance": 10840000.00}`


**GET** `/api/wallets` 

Retrieve list of all wallets ordered by date when created


###### **Response body example**

`[
    {
        "id": 1,
        "name": "Account in Imaginary Bank",
        "balance": "10840000.00"
    },
    {
        "id": 2,
        "name": "Second wallet",
        "balance": "15000.00"
    }
]`


**GET** `/api/wallets/<pk>`

Retrieve a wallet with all related operations ordered by date field

###### **Response body example**
 
`{
    "id": 1,
    "name": "Account in Imaginary Bank",
    "balance": "10840500.00",
    "operations": [
        {
            "id": 1,
            "date": "2020-01-01T12:00:00",
            "type": 1,
            "amount": "500.00",
            "comment": "plus 500"
        }
    ]
}`
 
###### **Error body example**
 
`{"detail": "Not found."}`


**PUT** `/api/wallets/<pk>`

For now only wallet name can be edited. Balance field is not editable.
Returns updated wallet object.

###### **Request parameters**
- name (str, required, unique)

###### **Response parameters**
- id
- name
- balance

###### **Request body example**

`{"name": "Account in Imaginary Bank", "balance": 10840000.00}`


**DELETE** `/api/wallets/<pk>`

Delete a wallet by id and all related operations.

###### **Response code**

`204` for success

`400` for error


**POST** `/api/operations`

Create new operation.
Operations are not editable.

###### **Request parameters**
- date (str in format "YYYY-MM-DDThh:mm:ss")
- type (int, 0 for costs, 1 for income)
- amount (positive decimal number, min value = 0.01)
- wallet (int)
- comment (str, optional, may be blank)

###### **Response parameters**
- id (int)
- date (str, format "YYYY-MM-DDThh:mm:ss")
- type (int, 0 for costs, 1 for income)
- amount (positive decimal number)
- wallet (int)
- comment (str, optional, may be blank)

###### **Request body example**

`{"date": "2020-01-01T12:00:00",
    "type": 1,
    "amount": 500.00,
    "comment": "plus 500",
    "wallet": 1}`

###### **Response body example**

`{"id": 1,
    "date": "2020-01-01T12:00:00",
    "type": 1,
    "amount": "500.00",
    "comment": "plus 500",
    "wallet": 1}`

###### **Error body example**

`{ "wallet": [
        "Invalid pk \"3\" - object does not exist." ] }`
        
**GET** `api/operations`

Retrieve a list of all operations ordered by date field

###### **Response parameters**
- id (int)
- date (str, format "YYYY-MM-DDThh:mm:ss")
- type (int, 0 for costs, 1 for income)
- amount (str, positive decimal number)
- wallet (int)
- comment (str, optional, may be blank)


###### **Response body example**
`[
    {
        "id": 1,
        "date": "2020-01-01T12:00:00",
        "type": 1,
        "amount": "500.00",
        "comment": "plus 500",
        "wallet": 1
    },
    {
        "id": 2,
        "date": "2020-01-01T12:00:00",
        "type": 0,
        "amount": "1000.00",
        "comment": "- 1000",
        "wallet": 1
    }
]`

**DELETE** `/api/operations/<pk>` 

Delete operation by id

###### **Response code**

`204` for success