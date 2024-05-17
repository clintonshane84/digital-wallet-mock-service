from flask import request, jsonify
from models.user_model import User, db, Transaction
from datetime import datetime
import uuid


class UserInfo:
    @staticmethod
    def get_user_info(user_uuid):
        # Query the user details from the database
        user = User.query.filter_by(uuid=user_uuid).first()
        if user:
            response = {
                "returnStatus": "S",
                "userDetails": {
                    "uuid": user.uuid,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "username": user.username,
                    "email": user.email,
                    "created": user.created,
                    "modified": user.modified
                }
            }
            return jsonify(response), 200
        else:
            response = {"returnStatus": "E", "returnMessage": "User not found"}
            return jsonify(response), 404


class UserCreation:
    @staticmethod
    def create_user():
        try:
            data = request.get_json()
            new_user = User(
                uuid=str(uuid.uuid4()),
                firstname=data['firstname'],
                lastname=data['lastname'],
                username=data['username'],
                email=data['email'],
                created=datetime.utcnow(),  # directly use datetime.utcnow() here
                modified=datetime.utcnow()  # and here
            )
            db.session.add(new_user)
            db.session.commit()

            response = {
                "returnStatus": "S",
                "returnMessage": "User created successfully",
                "userDetails": {
                    "uuid": new_user.uuid,
                    "firstname": new_user.firstname,
                    "lastname": new_user.lastname,
                    "username": new_user.username,
                    "email": new_user.email,
                    "created": new_user.created.isoformat() + 'Z',
                    "modified": new_user.modified.isoformat() + 'Z'
                }
            }
            return jsonify(response), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"returnStatus": "E", "returnMessage": "Failed to create user", "error": str(e)}), 500


class UserStatusUpdate:
    @staticmethod
    def update_user_status(user_uuid):
        try:
            data = request.get_json()
            # Verify that the 'status' field is present in the request
            if 'status' not in data:
                return jsonify({"returnStatus": "E", "returnMessage": "Missing 'status' field"}), 400

            # Find the user in the database
            user = User.query.filter_by(uuid=user_uuid).first()
            if not user:
                return jsonify({"returnStatus": "E", "returnMessage": "User not found"}), 404

            # Update user's status
            user.status = data['status']
            user.modified = datetime.utcnow().isoformat() + 'Z'  # Update the modified timestamp

            # Save changes to the database
            db.session.commit()

            response = {
                "returnStatus": "S",
                "returnMessage": "User status updated successfully",
                "account": {
                    "uuid": user.uuid,
                    "status": user.status,
                    "modified": user.modified
                }
            }
            return jsonify(response), 200

        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            return jsonify({"returnStatus": "E", "returnMessage": "Failed to update user status", "error": str(e)}), 500


class UserBalance:
    @staticmethod
    def get_user_balance(user_uuid):
        user = User.query.filter_by(uuid=user_uuid).first()
        if not user:
            return jsonify({"returnStatus": "E", "returnMessage": "User not found"}), 404

        # Calculate the balance by summing all transactions related to this user
        balance = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.user_uuid == user_uuid).scalar() or 0.0

        response = {
            "returnStatus": "S",
            "balance": {
                "uuid": user_uuid,
                "amount": balance,
                "last_updated": datetime.utcnow().isoformat() + 'Z'
            }
        }
        return jsonify(response), 200


class UserTransactions:
    @staticmethod
    def get_user_transactions(user_uuid):
        transaction_type = request.args.get('type', None)
        transaction_type = None if transaction_type == 'all' else transaction_type

        # Retrieve transactions from the database
        query = Transaction.query.filter_by(user_uuid=user_uuid)
        if transaction_type:
            query = query.filter_by(type=transaction_type)

        # Order by created_at to ensure the correct sequence for balance calculation
        transactions = query.order_by(Transaction.created_at).all()

        if not transactions:
            return jsonify({"returnStatus": "E", "returnMessage": "No transactions found"}), 404

        # Calculate the running balance
        running_balance = 0.0
        transactions_data = []
        for tx in transactions:
            running_balance += tx.amount
            transactions_data.append({
                "uuid": str(tx.id),
                "order_uid": tx.user_uuid,
                "type": tx.transaction_type,
                "value": tx.amount,
                "transaction_balance": running_balance,
                "created": tx.created_at.isoformat() + 'Z',
                "modified": tx.modified_at.isoformat() + 'Z'
            })

        response = {
            "returnStatus": "S",
            "transactions": transactions_data
        }
        return jsonify(response), 200


class TransactionReversal:
    @staticmethod
    def reverse_transaction():
        try:
            data = request.get_json()
            transaction_uuid = data.get('transaction_uuid')
            if not transaction_uuid:
                return jsonify({"returnStatus": "E", "returnMessage": "Missing transaction UUID"}), 400

            # Simulating a transaction reversal
            # Assuming we find and can reverse the transaction
            # This is a simplified example with a hardcoded response
            response = {
                "returnStatus": "S",
                "returnMessage": "Transaction reversed successfully",
                "transaction": {
                    "uuid": transaction_uuid,
                    "status": "reversed",
                    "type": "deposit",
                    "value": "200.00",
                    "balance": "1000.50",
                    "created": "2024-04-01T12:00:00Z",
                    "modified": "2024-05-18T12:00:00Z"
                }
            }
            return jsonify(response), 200

        except Exception as e:
            return jsonify({"returnStatus": "E", "returnMessage": "Invalid JSON data", "error": str(e)}), 400


class WalletTransaction:
    @staticmethod
    def process_transaction():
        try:
            data = request.get_json()
            required_fields = ["user_uuid", "type", "amount"]
            if not all(field in data for field in required_fields):
                return jsonify({"returnStatus": "E", "returnMessage": "Missing required fields"}), 400

            user = User.query.filter_by(uuid=data["user_uuid"]).first()
            if not user:
                return jsonify({"returnStatus": "E", "returnMessage": "User not found"}), 404

            new_transaction = Transaction(
                user_uuid=data["user_uuid"],
                amount=data["amount"],
                transaction_type=data["type"],
                created_at=datetime.utcnow(),
                modified_at=datetime.utcnow()
            )
            db.session.add(new_transaction)
            db.session.commit()

            response = {
                "returnStatus": "S",
                "returnMessage": "Transaction processed successfully",
                "transaction": {
                    "id": new_transaction.id,
                    "user_uuid": new_transaction.user_uuid,
                    "type": new_transaction.transaction_type,
                    "amount": new_transaction.amount,
                    "created": new_transaction.created_at.isoformat() + 'Z',
                    "modified": new_transaction.modified_at.isoformat() + 'Z'
                }
            }
            return jsonify(response), 201

        except Exception as e:
            db.session.rollback()
            return jsonify(
                {"returnStatus": "E", "returnMessage": "Failed to process transaction", "error": str(e)}), 500


class WalletAccounts:
    @staticmethod
    def get_wallet_accounts():
        account_uuid = request.args.get('accountUuid', default=None)
        timeframe = request.args.get('timeframe', default='all')
        status = request.args.get('status', default='all')

        # Simulate fetching accounts from a database
        accounts = [
            {
                "uuid": "acc-100",
                "wallet_user_uuid": "123e4567-e89b-12d3-a456-426614174000",
                "account": "Primary",
                "status": "active",
                "created": "2024-04-01T12:00:00Z",
                "modified": "2024-04-02T12:00:00Z"
            },
            {
                "uuid": "acc-101",
                "wallet_user_uuid": "123e4567-e89b-12d3-a456-426614174001",
                "account": "Savings",
                "status": "inactive",
                "created": "2024-04-01T12:00:00Z",
                "modified": "2024-04-02T12:00:00Z"
            }
        ]

        # Filter accounts based on the parameters if specified
        if account_uuid:
            accounts = [acc for acc in accounts if acc['uuid'] == account_uuid]
        if status != 'all':
            accounts = [acc for acc in accounts if acc['status'] == status]

        # Here, we would also need to consider the 'timeframe' for a real implementation
        # This is skipped for brevity and simplicity

        response = {
            "returnStatus": "S",
            "walletAccounts": accounts
        }
        return jsonify(response), 200
