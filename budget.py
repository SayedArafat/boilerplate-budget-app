class Category:
    def __init__(self, category_name):
        self.name = category_name
        self.ledger = []
        self.record = {}
        # print("Category Created", category_name)

    def deposit(self, amount, description=''):
        self.record = {'amount': float(amount), 'description': description}
        self.ledger.append(self.record)

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.record = {'amount': float(-amount), 'description': description}
            self.ledger.append(self.record)
            return True
        else:
            return False

    def get_balance(self):
        total_balance = 0
        for elements in self.ledger:
            total_balance += elements.get('amount', 0)

        # print('Total:', end=' ')
        return total_balance

    def transfer(self, amount, instance):
        if self.check_funds(amount):
            self.withdraw(amount, description=f'Transfer to {instance.name}')
            instance.deposit(amount, description=f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        balance = self.get_balance()
        if amount > balance:
            return False
        else:
            return True

    def __str__(self):
        output = ''
        description = ''
        total_budget = self.get_balance()
        for line_num in range(len(self.ledger)):
            if line_num == 0:
                output += f'{self.name}'.center(30, '*') + '\n'

            for i in range(23):
                try:
                    description += self.ledger[line_num].get('description', 0)[i]
                except IndexError:
                    pass
            amount = self.ledger[line_num].get('amount', 0)
            output += f'{description:23}{amount:7.2f}\n'
            # print(description)
            description = ''

            if self.ledger[-1] == self.ledger[line_num]:
                output += f'Total: {total_budget:.2f}'

        return output


def create_spend_chart(categories):
    return_string = ''
    total_Expenditure = 0
    per_category_expenditure = 0
    per_category_expenditure_list = []
    expenditure_percentage = []

    for instance in categories:
        for history in instance.ledger:
            if history.get('amount') < 0:
                total_Expenditure += abs(history.get('amount'))
                per_category_expenditure += abs(history.get('amount'))
        per_category_expenditure_list.append(per_category_expenditure)
        per_category_expenditure = 0
    for cost in per_category_expenditure_list:
        expenditure_percentage.append(round((cost / total_Expenditure) * 100, 1))

    range_list = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    max_name_length = max([len(instance.name) for instance in categories])
    for line in range(13):
        if line <= 10:
            if line == 0:
                return_string += 'Percentage spent by category\n'
            return_string += f'{range_list[line]:3}|'
            for i in range(len(categories)):
                if expenditure_percentage[i] > range_list[line] - 4.5:
                    return_string += ' o '
                else:
                    return_string += '   '
            return_string += ' \n'

        elif line == 11:
            return_string += '    '
            for i in range(len(categories)):
                return_string += '---'
                if i == range(len(categories))[-1]:
                    return_string += '-\n'

        else:
            return_string += '    '
            for chars in range(max_name_length):
                for i in categories:
                    # print('*')
                    try:
                        return_string += f' {i.name[chars] } '
                    except IndexError:
                        return_string += '   '
                if chars != range(max_name_length)[-1]:
                    return_string += ' \n    '
                else:
                  return_string += ' '
    # return_string += str(expenditure_percentage)
    return return_string
