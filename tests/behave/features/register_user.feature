Feature: Register a new user
    
  In order to be able to buy food
  As a customer
  I need to create an account

  Scenario: Valid JSON
    When I submit the JSON
    """
    {
      "name": "Lucas Vasconcelos",
      "email": "lucas@email.com",
      "phone": "(85) 90000-0000",
      "cpf": "000.000.000-00",
      "password": "password123"
    }
    """
    Then the API returns the http status code 201 

  Scenario: Invalid JSON
    When I submit the JSON
    """
    {
      "name": "Lucas Vasconcelos"
    }
    """
    Then the API returns the http status code 400
