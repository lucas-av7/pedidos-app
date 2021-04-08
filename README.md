# Pedidos-app Backend

## App route list

| Name                                                   | Method   | Path                                         |
|--------------------------------------------------------|----------|----------------------------------------------|
| [login](#login)                                        | POST     | /api/login                                   |
| [users_create](#users_create)                          | POST     | /api/users                                   |
| [users_get](#users_get) *                              | GET      | /api/users/{user_id}                         |
| [users_edit](#users_edit) *                            | PUT      | /api/users/{user_id}                         |
| [users_password_edit](#users_password_edit) *          | PUT      | /api/users/{user_id}/password                |
| [users_address_create](#users_address_create) *        | POST     | /api/users/{user_id}/address                 |
| [users_address_get_all](#users_address_get_all) *      | GET      | /api/users/{user_id}/address                 |
| [users_address_get](#users_address_get) *              | GET      | /api/users/{user_id}/address/{address_id}    |
| [users_address_edit](#users_address_edit) *            | PUT      | /api/users/{user_id}/address/{address_id}    |
| [users_address_delete](#users_address_delete) *        | DELETE   | /api/users/{user_id}/address/{address_id}    |
| [store_create](#store_create) *                        | POST     | /api/store                                   |
| [store_get](#store_get)                                | POST     | /api/store                                   |

\* [Authorization header required](#authorization-header-required)

## Login

### Basic Auth

__Expected Header:__

```http
Authorization: Basic email:password
```

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "Validated successfuly",
  "data": {
    "token": "<token>",
    "exp": "<datetime.utcnow() + timedelta(days=30)>"
  }
}
```

Errors

`[status_code]: [message]`

- 401: Could not verify
- 401: User not found

### Authorization header required

__Expected Header:__

```http
Authorization: Bearer <token>
```

## Route methods expected JSON and response

### users_create

__Expected JSON:__

```json
{
  "name": "Lucas Vasconcelos",
  "email": "lucas@email.com",
  "phone": "(85) 90000-0000",
  "password": "password123"
}
```

__Response:__

Success - 201

```json
{
  "status": "Success",
  "status_code": 201,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "name": "Lucas Vasconcelos",
    "email": "lucas@email.com",
    "phone": "(85) 90000-0000"
  }
}
```

Errors

`[status_code]: [message]`

- 400: Fields missing in JSON
- 400: The values of the JSON have invalid types
- 406: Payload is not a JSON
- 422: E-mail is already in use
- 500: Unable to execute

### users_get

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "User received successfully",
  "data": {
    "id": 1,
    "name": "Lucas Vasconcelos",
    "email": "lucas@email.com",
    "phone": "(85) 90000-0000"
  }
}
```

Errors

`[status_code]: [message]`

- 401: Could not verify
- 500: Unable to execute

### users_edit

__Expected JSON:__

```json
{
  "name": "User edited",
  "email": "edited@email.com",
  "phone": "(85) 90000-0000"
}
```

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "User edited successfully",
  "data": {
    "id": 1,
    "name": "User edited",
    "email": "edited@email.com",
    "phone": "(85) 90000-0000"
  }
}
```

Errors

`[status_code]: [message]`

- 400: Fields missing in JSON
- 401: Could not verify
- 406: Payload is not a JSON
- 500: Unable to execute

### users_password_edit

__Expected JSON:__

```json
{
  "password": "password123",
  "new_password": "newpassword123"
}
```

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "Password edited successfully"
}
```

Errors

`[status_code]: [message]`

- 400: Fields missing in JSON
- 401: Could not verify
- 401: Incorrect password
- 406: Payload is not a JSON
- 500: Unable to execute

### users_address_create

__Expected JSON:__

```json
{
  "street": "Fake street",
  "number": "S/N",
  "district": "Fake district",
  "zipcode": "60000-000",
  "city": "Fake city",
  "state": "Fake state"
}
```

__Response:__

Success - 201

```json
{
  "status": "Success",
  "status_code": 201,
  "message": "Address registered successfully",
  "data": {
    "id": 1,
    "street": "Fake street",
    "number": "S/N",
    "district": "Fake district",
    "zipcode": "60000-000",
    "city": "Fake city",
    "state": "Fake state"
  }
}
```

Errors

`[status_code]: [message]`

- 400: Fields missing in JSON
- 401: Could not verify
- 406: Payload is not a JSON
- 500: Unable to execute

### users_address_get_all

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "Addresses received successfully",
  "data": {
    "user_id": 1,
    "addresses": [{
      "id": 1,
      "street": "Fake street",
      "number": "S/N",
      "district": "Fake district",
      "zipcode": "60000-000",
      "city": "Fake city",
      "state": "Fake state"
    }]
  }
}
```

Errors

`[status_code]: [message]`

- 401: Could not verify
- 500: Unable to execute

### users_address_get

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "Address received successfully",
  "data": {
    "user_id": 1,
    "address": {
      "id": 1,
      "street": "Fake street",
      "number": "S/N",
      "district": "Fake district",
      "zipcode": "60000-000",
      "city": "Fake city",
      "state": "Fake state"
    }
  }
}
```

Errors

`[status_code]: [message]`

- 401: Could not verify
- 404: Address not found
- 500: Unable to execute

### users_address_edit

__Expected JSON:__

```json
{
  "street": "Edited",
  "number": "S/N",
  "district": "Fake district",
  "zipcode": "60000-000",
  "city": "Fake city",
  "state": "Fake state"
}
```

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "Address edited successfully",
  "data": {
    "id": 1,
    "street": "Edited",
    "number": "S/N",
    "district": "Fake district",
    "zipcode": "60000-000",
    "city": "Fake city",
    "state": "Fake state"
  }
}
```

Errors

`[status_code]: [message]`

- 400: Fields missing in JSON
- 401: Could not verify
- 404: Address not found
- 406: Payload is not a JSON
- 500: Unable to execute

### users_address_delete

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "Address deleted successfully"
}
```

Errors

`[status_code]: [message]`

- 401: Could not verify
- 404: Address not found
- 500: Unable to execute

### store_create

__Expected JSON:__

```json
{
  "name": "Fake store",
  "phone": "(85) 90000-0000",
  "street": "Fake street",
  "number": "Fake number",
  "district": "Fake district",
  "city": "Fake city",
  "state": "Fake state"
}
```

__Response:__

Success - 201

```json
{
  "status": "Success",
  "status_code": 201,
  "message": "Store created successfully",
  "data": {
    "name": "Fake store",
    "phone": "(85) 90000-0000",
    "street": "Fake street",
    "number": "Fake number",
    "district": "Fake district",
    "city": "Fake city",
    "state": "Fake state"
  }
}
```

Errors

`[status_code]: [message]`

- 400: Fields missing in JSON
- 400: The database already has a store created
- 406: Payload is not a JSON
- 500: Unable to execute

### store_get

__Response:__

Success - 200

```json
{
  "status": "Success",
  "status_code": 200,
  "message": "Store received successfully",
  "data": {
    "name": "Fake store",
    "phone": "(85) 90000-0000",
    "street": "Fake street",
    "number": "Fake number",
    "district": "Fake district",
    "city": "Fake city",
    "state": "Fake state"
  }
}
```

Errors

`[status_code]: [message]`

- 404: No store created
- 500: Unable to execute

## Error response example

```json
{
  "status": "Error",
  "status_code": 400,
  "message": "Fields missing in JSON"
}
```
