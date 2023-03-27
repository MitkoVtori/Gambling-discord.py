import time


class Bank:

    def __init__(self, user_id, balance=500, money_in_bank=0, owed_money=0):
        self._user_id = user_id
        self._balance = balance
        self._money_in_bank = money_in_bank
        self._owed_money = owed_money

    def bankrupt(self, start):
        end = time.time()
        if end - start > 432_000: # 5 days
            self._balance = 500
            self._money_in_bank = 0
            self._owed_money = 0
            return "You bankrupted because you owe money to the bank for more than 5 days. Your game restarts and starts from the beginning."
        return False

    def payback(self):
        if self._balance >= self._owed_money:
            self._balance -= self._owed_money
            self._owed_money = 0
            return "You no longer owe the bank"
        return f"You don't have enough money.{' You may want to withdraw from your deposits.' if self._money_in_bank > 0 else ''}"

    def time_in_bank(self, start): # mix-in
        end = time.time()
        time_in_bank = end - start
        result = ((time_in_bank/600000) * self._money_in_bank) + self._money_in_bank
        return result

    def deposit(self, amount, start_time=0, owe_money_start_time=0):

        if self._owed_money > 0:
            if type(self.bankrupt(owe_money_start_time)) is not bool:
                return self.bankrupt(owe_money_start_time)
            return "You can't deposit if you owe money."

        if amount <= self._balance:

            if self._money_in_bank > 0:
                self._money_in_bank = self.time_in_bank(start_time)

            self._money_in_bank += amount
            self._balance -= amount

            start = time.time()
            return [f"${amount:.2f} deposited.", start]

        return "You don't have enough money to deposit that amount."

    def withdraw(self, start, deposited=False, amount=0):
        def get_deposited_money():
            result = self.time_in_bank(start)
            self._money_in_bank = 0
            return result

        def get_from_deposited_money():
            self._money_in_bank = self.time_in_bank(start)
            if self._money_in_bank >= amount:
                self._money_in_bank -= amount
                return amount
            return "Not enough money in the bank"

        def withdraw_money():
            if self._owed_money > 0:
                return "You can't withdraw money until you don't pay what you owe."

            maximum_money_to_withdraw = 1_000
            additional_money_to_withdraw = (self._balance * 0.10) + self._balance

            if additional_money_to_withdraw > 0:
                result = maximum_money_to_withdraw + additional_money_to_withdraw

            else:
                result = maximum_money_to_withdraw

            if result <= amount:
                self._balance += amount
                self._owed_money = amount * 1.10
                start_owed_money = time.time()
                return [f"You have withdrawn ${amount}", start_owed_money]

            return f"You can't withdraw that amount at the moment. The maximum you can withdraw is ${result}"


        if deposited and amount > 0:
            return get_from_deposited_money()

        elif deposited:
            return get_deposited_money()

        return withdraw_money()

    def __repr__(self):
        return f"<@{self._user_id}>\nBalance: ${self._balance:.2f}\nBank balance: ${self._money_in_bank:.2f}\nOwes: ${self._owed_money:.2f}"

