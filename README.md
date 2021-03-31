# Pedidos-app Backend

## App route list

| Name                                                   | Method   | Path                                         |
|--------------------------------------------------------|----------|----------------------------------------------|
| [users_create](#users_create)                          | POST     | /api/users                                   |
| [users_address_create](#users_address_create)          | POST     | /api/users/{user_id}/address                 |
| [users_address_edit](#users_address_edit)              | POST     | /api/users/{user_id}/address/{address_id}    |

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
      "email": "lucas@email.com"
}
```

Errors

`[status_code]: [message]`

- 400: Fields missing in JSON
- 400: The values of the JSON have invalid types
- 406: Payload is not a JSON
- 422: E-mail is already in use

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
    "user_id": 1,
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
- 406: Payload is not a JSON

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
    "user_id": 1,
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
- 406: Payload is not a JSON

## Error response example

```json
{
  "status": "Error",
  "status_code": 400,
  "message": "Fields missing in JSON"
}
```
