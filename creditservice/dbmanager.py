import uuid as uuid_model

from models import db, Account
from exceptions import AccountNotFoundException, BalanceIsClosedException, InsufficientFundsException
from constants import DOES_NOT_EXIST_MSG, BALANCE_IS_CLOSED_MSG, INSUFFICIENT_FUNDS_MSG


# Create basic table to database
def init_database():
	with db:
		db.create_tables((Account, ))


# Create new accounts for account_list
def create_new_accounts(account_list):
	with db:
		Account.insert_many(account_list).execute()


# Delete accounts by list of uuid
def delete_accounts(uuid_list):
	with db:
		return Account.delete().where(Account.uuid.in_(uuid_list)).execute()


# Just return account
def get_account_by_uuid(uuid):
	with db:
		res = Account.select().where(Account.uuid == uuid)
		if res:
			account = next(iter(res))
			return account
		else:
			raise AccountNotFoundException(DOES_NOT_EXIST_MSG)


# Get accounts by uuid list
def get_accounts_by_uuid_list(uuid_list):
	with db:
		return Account.select().where(Account.uuid.in_(uuid_list))


# Do add: Top up balance by value, if is_topup=True
# Do subtract: Raise holds by value, if is_topup=False
# For both operations account should be opened
def change_balance(uuid, value, is_topup):
	with db:
		res = Account.select().where(Account.uuid == uuid)
		if not res:
			raise AccountNotFoundException(DOES_NOT_EXIST_MSG)

		account = next(iter(res))
		if not account.is_opened:
			raise BalanceIsClosedException(BALANCE_IS_CLOSED_MSG)

		if is_topup:
			account.balance += int(value)
		else:
			if account.balance - account.holds - value > 0:
				account.holds += int(value)
			else:
				raise InsufficientFundsException(INSUFFICIENT_FUNDS_MSG)
		account.save()
		return account


# Update all account balances subtracting their holds, if holds < balance and balance is opened
def update_holds():
	with db:
		query = Account.update(
			balance=Account.balance - Account.holds,
			holds=0
		).where(
			(Account.holds > 0) &
			(Account.balance >= Account.holds) &
			(Account.is_opened == True)
		)
		return query.execute()
