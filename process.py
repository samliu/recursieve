# process.py
#
# Reads data file and calculates total monthly spend.
#
# Initial Author: Sam Liu <sam@ambushnetworks.com>
#
# MIT License (see repo).
import click
from decimal import Decimal
from collections import defaultdict


class CashflowCalculator(object):
    """Calculates cashflow."""
    def __init__(self, data_file):
        """Read data file and save line items."""
        # These variables record categorical and total spend.
        self.total_spend = 0
        self.sum_per_category = defaultdict(float)
        self.net_per_category = defaultdict(float)

        # These variables record income.
        self.total_income = 0

        # These variables record savings.
        self.total_savings_dollars = 0
        self.total_savings_percent = 0

        # Open data file and save all lines.
        self.data_file = data_file
        try:
            raw_text = open(data_file)
            self.unprocessed_lines = raw_text.readlines()
        except Exception as e:
            print e

        # Color printer.
        self.printer = ColorPrinter()

    def monthly_report(self):
        """Generate monthly cashflow report."""
        self.printer.println("\nMonthly Cashflow Report", color="UNDERLINE")

        current_category = None
        for line in self.unprocessed_lines:
            # Category title.
            if line.startswith("## "):
                try:
                    category = line.split("## ")
                    current_category = category[1].strip()
                    continue
                except Exception as e:
                    print "Error: misformatted category title."

            # Income.
            if line.startswith("+"):
                item = line.split("+ ")[1]
                # Pull out the first term as dollar amt as float.
                dollar_amt = item.split(" ")[0]
                dollar_amt = dollar_amt.strip('$')
                dollar_amt = float(dollar_amt)

                # Pull out rest of the item as the description.
                description = " ".join(line.split(" ")[2:])
                self.total_income += dollar_amt
                self.net_per_category[current_category] += dollar_amt

            # Savings.
            if line.startswith("~"):
                try:
                    item = line.split("~ ")[1]

                    #  Find savings % or $ amt.
                    item = item.split(' ')[0]
                    if item.startswith('$'):
                        dollar_amt = item.strip('$')
                        dollar_amt = float(dollar_amt)
                        self.total_savings_dollars += dollar_amt
                    if item.endswith('%'):
                        percent_amt = item.strip('%')
                        percent_amt = float(percent_amt)
                        self.total_savings_percent += percent_amt

                    # Pull out rest of the item as the description.
                    description = " ".join(line.split(" ")[2:])

                except Exception as e:
                    print "Error: misformatted savings line."
                    print e

            # Line item.
            if line.startswith("-"):
                try:
                    item = line.split("- ")[1]

                    # Pull out the first term as dollar amt as float.
                    dollar_amt = item.split(" ")[0]
                    dollar_amt = dollar_amt.strip('$')
                    dollar_amt = float(dollar_amt)

                    # Pull out rest of the item as the description.
                    description = " ".join(line.split(" ")[2:])

                    self.sum_per_category[current_category] += dollar_amt
                    self.net_per_category[current_category] -= dollar_amt
                    self.total_spend += dollar_amt

                except Exception as e:
                    print "Error: misformatted line item."
                    print e

        # Category Spend.
        for category in self.sum_per_category:
            expenditure = unicode(self.sum_per_category[category])
            print ("Spending "
                   "\033[91m${0}\033[0m"  # Red amt.
                   " in category "
                   "\033[1m{1}.\033[0m"  # Bold white category.
                   "").format(expenditure, category)

        self.printer.println("\nSummary", color="UNDERLINE")
        # Total income.
        self.printer.println("Total income this month was: ${0}.".format(
                             self.total_income), color="PALEGREEN")

        # Total Spend.
        self.printer.println("Spend is ${0} total per month.".format(
                             self.total_spend), color="FAILRED")


        # Net saved.
        total_saved_by_percent_salary = (self.net_per_category['Salary'] *
            self.total_savings_percent * 0.01)
        net_saved = total_saved_by_percent_salary + self.total_savings_dollars
        self.printer.println(
            "Net saved this month was: "
            "${0} ({1}% of Salary + ${2} other savings).".format(
                net_saved, self.total_savings_percent,
                self.total_savings_dollars), color="FADEDGREEN")

        # Net disposable income.
        net_difference = self.total_income - self.total_spend - net_saved
        if net_difference < 0:
            self.printer.println(
                "Net disposable income this month was: ${0}.".format(
                    net_difference), color="FAILRED")
        else:
            self.printer.println(
                "Net disposable income this month was: ${0}.".format(
                    net_difference), color="OKGREEN")

class ColorPrinter(object):
    """Class to print with color."""
    def __init__(self):
        self.colors = {
            "FAILRED":      '\033[91m',
            "FADEDGREEN":   '\033[95m',
            "OKGREEN":      '\033[92m',
            "PALEGREEN":    '\033[93m',
            "ENDC":         '\033[0m',
            "BOLDWHITE":    '\033[1m',
            "UNDERLINE":    '\033[4m',
        }

    def println(self, text, color='NONE'):
        if color in self.colors:
            print self.colors[color] + text + self.colors['ENDC']
        else:
            print text


@click.command()
@click.option('--filename', default='data.md',
              help='Which file to read data from.')
def cli(filename):
    """Program to calculate cashflow from specially annotated markdown file."""
    cashflow_calculator = CashflowCalculator(filename)

    # Install dotfiles one by one, prompting user for each one if there is an
    # override.
    cashflow_calculator.monthly_report()


if __name__ == "__main__":
    cli()
