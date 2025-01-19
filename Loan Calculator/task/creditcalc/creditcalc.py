import math
import argparse

def validate_args(args):
    """
    Validate the input arguments and return True if there are any incorrect parameters.
    """
    conditions = [
        args.type not in ['annuity', 'diff'],
        args.type == 'diff' and args.payment is not None,
        args.interest is None,
        sum(value is not None for value in vars(args).values()) < 4,
        args.payment is not None and args.payment < 0,
        args.principal is not None and args.principal < 0,
        args.periods is not None and args.periods < 0,
        args.interest is not None and args.interest < 0
    ]
    if any(conditions):
        print('Incorrect parameters')
        return True
    return False

def calculate_annuity(args, nominal_interest_rate):
    """
    Calculate and print details for annuity payments, including overpayment.
    """
    if args.periods is None:
        x = args.payment / (args.payment - nominal_interest_rate * args.principal)
        base = 1 + nominal_interest_rate
        number_of_months = math.ceil(math.log(x, base))
        years, months = divmod(number_of_months, 12)
        if years > 0:
            print(f'It will take {years} years and {months} months to repay this loan!')
        else:
            print(f'It will take {months} months to repay this loan!')
        overpayment = (args.payment * number_of_months) - args.principal
        print(f'Overpayment = {overpayment}')

    if args.payment is None:
        monthly_payment = math.ceil(args.principal * (nominal_interest_rate * ((1 + nominal_interest_rate) ** args.periods) /
                                                      (((1 + nominal_interest_rate) ** args.periods) - 1)))
        print(f'Your monthly payment = {monthly_payment}!')
        overpayment = (monthly_payment * args.periods) - args.principal
        print(f'Overpayment = {overpayment}')

    if args.principal is None:
        loan_principal = int(args.payment / ((nominal_interest_rate * (1 + nominal_interest_rate) ** args.periods) /
                                             (((1 + nominal_interest_rate) ** args.periods) - 1)))
        print(f'Your loan principal = {loan_principal}!')
        overpayment = (args.payment * args.periods) - loan_principal
        print(f'Overpayment = {overpayment}')

def calculate_differentiated(args, nominal_interest_rate):
    """
    Calculate and print details for differentiated payments, including overpayment.
    """
    sum_of_differentiated_payment = 0
    for m in range(1, args.periods + 1):
        differentiated_payment = math.ceil(
            (args.principal / args.periods) +
            (nominal_interest_rate * (args.principal - ((args.principal * (m - 1)) / args.periods)))
        )
        sum_of_differentiated_payment += differentiated_payment
        print(f'Month {m}: payment is {differentiated_payment}')

    overpayment = sum_of_differentiated_payment - args.principal
    print(f'\nOverpayment = {overpayment}')

def main():
    """
    Main function to parse arguments and compute the loan details.
    """
    parser = argparse.ArgumentParser(description='This program computes all the parameters of the loan')
    parser.add_argument('--payment', type=float, help='The payment amount. It can be calculated using the provided principal, interest, and number of months.')
    parser.add_argument('--principal', type=int, help='The loan principal. It can be calculated using the interest, annuity payment, and number of months.')
    parser.add_argument('--periods', type=int, help='The number of months needed to repay the loan. It is calculated based on the interest, annuity payment, and principal.')
    parser.add_argument('--interest', type=float, help='The interest rate specified without a percent sign. Note that it must always be provided.')
    parser.add_argument('--type', type=str, help='The type of payment: "annuity" or "diff" (differentiated). This must always be provided.')

    args = parser.parse_args()

    # Validate arguments
    if validate_args(args):
        return

    # Calculate nominal interest rate
    nominal_interest_rate = (args.interest / 100) / 12

    # Calculate loan details based on type
    if args.type == 'annuity':
        calculate_annuity(args, nominal_interest_rate)
    elif args.type == 'diff':
        calculate_differentiated(args, nominal_interest_rate)

if __name__ == '__main__':
    main()
