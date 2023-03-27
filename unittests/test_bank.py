import time
from unittest import TestCase, main
from source.bank import Bank


class TestBank(TestCase):

    def setUp(self):
        self.bank = Bank("123", 10_000, 0, 0)

    def test_successful_initialization(self):
        self.assertEqual("123", self.bank._user_id)
        self.assertEqual(10_000, self.bank._balance)
        self.assertEqual(0, self.bank._money_in_bank)
        self.assertEqual(0, self.bank._owed_money)

    def test_successful_payback_of_what_you_owe(self):
        self.bank._owed_money = 1
        result = self.bank.payback()
        self.assertEqual(0, self.bank._owed_money)
        self.assertEqual(9_999, self.bank._balance)
        self.assertEqual("You no longer owe the bank", result)

    def test_unsuccessful_payback_you_might_like_to_withdraw_from_deposits(self):
        self.bank._owed_money = 10000000000
        self.bank._money_in_bank = 10
        result = self.bank.payback()
        self.assertEqual(f"You don't have enough money. You may want to withdraw from your deposits.", result)

    def test_unsuccessful_payback(self):
        self.bank._owed_money = 10000000000
        self.bank._money_in_bank = 0
        result = self.bank.payback()
        self.assertEqual(f"You don't have enough money.", result)

    def test_unsuccessful_bankrupt(self):
        result = self.bank.bankrupt(time.time(), 0)
        self.assertEqual(False, result)

    def test_successful_bankrupt(self):
        '''
            This is how the function normally looks like:

                def bankrupt(self, start):
                    end = time.time()

            For this test, the function will look like this:

                def bankrupt(self, start, end):
        '''

        self.bank._money_in_bank = 19
        self.bank._owed_money = 7

        result = self.bank.bankrupt(0, 435_021)

        self.assertEqual(500, self.bank._balance)
        self.assertEqual(0, self.bank._money_in_bank)
        self.assertEqual(0, self.bank._owed_money)
        self.assertEqual("You bankrupted because you owe money to the bank for more than 5 days. Your game restarts and starts from the beginning.", result)

    def test_time_in_bank_returning_more_money(self):
        '''
            This is how the function normally looks like:

                def time_in_bank(self, start): # mix-in
                    end = time.time()

            For this test, the function will look like this:

                def time_in_bank(self, time): # mix-in
        '''

        self.bank._money_in_bank = 10_000
        result = self.bank.time_in_bank(86400)
        self.assertEqual(11_440, result)

    def test_unsuccessful_deposit(self):
        self.bank._owed_money = 0
        amount = self.bank._balance + 5
        result = self.bank.deposit(amount)
        self.assertEqual("You don't have enough money to deposit that amount.", result)

    def test_successful_deposit(self):
        self.bank._balance = 500
        self.bank._money_in_bank = 0
        amount = 300
        result = self.bank.deposit(amount)

        self.assertEqual(300, self.bank._money_in_bank)
        self.assertEqual(200, self.bank._balance)
        self.assertEqual(f"$300.00 deposited.", result[0])

    ''' withdraw tests are NOT required. '''

    def test_repr_string_return(self):
        self.bank._balance = 1
        self.bank._money_in_bank = 10
        self.bank._owed_money = 7
        self.assertEqual(f"<@123>\nBalance: $1.00\nBank balance: $10.00\nOwes: $7.00", repr(self.bank))


if __name__ == '__main__':
    main()