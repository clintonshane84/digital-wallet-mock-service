from flask import Flask
from flask_migrate import Migrate

from models.user_model import db
from user_management.user_handlers import UserInfo, UserCreation, UserStatusUpdate, UserBalance, UserTransactions, \
    TransactionReversal, WalletTransaction, WalletAccounts


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register your routes
    app.add_url_rule('/api/wallet/user/<user_uuid>', view_func=UserInfo.get_user_info, methods=['GET'])
    app.add_url_rule('/api/wallet/user/create', view_func=UserCreation.create_user, methods=['POST'])
    app.add_url_rule('/api/wallet/user/<user_uuid>/status', view_func=UserStatusUpdate.update_user_status,
                     methods=['POST'])
    app.add_url_rule('/api/wallet/user/<user_uuid>/balance', view_func=UserBalance.get_user_balance, methods=['GET'])
    app.add_url_rule('/api/wallet/user/<user_uuid>/transactions', view_func=UserTransactions.get_user_transactions,
                     methods=['GET'])
    app.add_url_rule('/api/wallet/transaction/reverse', view_func=TransactionReversal.reverse_transaction,
                     methods=['POST'])
    app.add_url_rule('/api/wallet/transaction', view_func=WalletTransaction.process_transaction, methods=['POST'])
    app.add_url_rule('/api/wallet/accounts', view_func=WalletAccounts.get_wallet_accounts, methods=['GET'])

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
