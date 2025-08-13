# digital-wallet-mock-service

The digital-wallet-mock-service is a simple Flask-based application designed to manage and simulate wallet transactions for users. It supports operations such as creating a user, updating user information, handling wallet transactions (such as deposits, withdrawals, and adjustments), and querying transaction histories.

## Features

- User management (create, update)
- Transaction processing (create, reverse, query)
- Balance inquiries
- Transaction history retrieval

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/wallet-microservice.git
   cd wallet-microservice
   ```

2. **Set up a Virtual Environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**

   Set the required environment variables:

   ```bash
   export FLASK_APP=main.py
   export FLASK_ENV=development  # Set to 'production' in a production environment
   ```

5. **Initialize the Database**

   First, run the database migrations:

   ```bash
   flask db upgrade
   ```

   To initialize the database with a test user:

   ```bash
   flask shell
   >>> from models.user_model import init_db, app
   >>> init_db(app)
   ```

6. **Run the Application**

   ```bash
   flask run
   ```

   The service will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### User Management

- **Create User**
  - **Method:** POST
  - **Endpoint:** `/api/wallet/user/create`
  - **Payload:**

    ```json
    {
      "firstname": "John",
      "lastname": "Doe",
      "username": "johndoe",
      "email": "john.doe@example.com"
    }
    ```

- **Get User Transactions**
  - **Method:** GET
  - **Endpoint:** `/api/wallet/user/{user_uuid}/transactions`

### Transaction Processing

- **Process Transaction**
  - **Method:** POST
  - **Endpoint:** `/api/wallet/transaction`
  - **Payload:**

    ```json
    {
      "user_uuid": "user-uuid",
      "type": "deposit",
      "amount": 100.00
    }
    ```

- **Get User Balance**
  - **Method:** GET
  - **Endpoint:** `/api/wallet/user/{user_uuid}/balance`

## Contributing

Contributions to this project are welcome. Please submit a pull request with your changes.
