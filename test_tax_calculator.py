import unittest

# Define the tax brackets and rates
TAX_BRACKETS = [(0, 50000), (50000, 100000), (100000, 150000),
                (150000, 200000), (200000, float("inf"))]
TAX_RATES = [0.02, 0.06, 0.1, 0.14, 0.17]
STANDARD_RATE = 0.15

# Define the standard tax deduction, basic allowance, MPF rate and Standard Rate Zone for Single and Married
SINGLE_ALLOWANCE = 132000
MARRIED_ALLOWANCE = 264000
MPF_RATE = 0.05
SINGLE_STANDARD_RATE_ZONE = 2022000
MARRIED_STANDARD_RATE_ZONE = 3144000


def septax(salary):
    mpf = salary * MPF_RATE
    if mpf > 18000:
        mpf = 18000
    assessable_income = salary - mpf - SINGLE_ALLOWANCE
    if salary > SINGLE_STANDARD_RATE_ZONE:
        std_septax = (salary - mpf) * STANDARD_RATE
        return std_septax, mpf
    tax_amount = 0
    for i, bracket in enumerate(TAX_BRACKETS):
        if assessable_income <= bracket[0]:
            break
        elif assessable_income > bracket[1]:
            tax_amount += (bracket[1] - bracket[0]) * TAX_RATES[i]
        else:
            tax_amount += (assessable_income - bracket[0]) * TAX_RATES[i]
            break
    if tax_amount < 0:
        tax_amount = 0
    return tax_amount, mpf


def jointtax(salary1, salary2):
    mpfh = salary1 * MPF_RATE
    if mpfh > 18000:
        mpfh = 18000
    mpfw = salary2 * MPF_RATE
    if mpfw > 18000:
        mpfw = 18000
    assessable_income = (salary1 - mpfh) + (salary2 - mpfw) - MARRIED_ALLOWANCE
    if salary1 + salary2 > MARRIED_STANDARD_RATE_ZONE:
        std_jointtax = ((salary1 - mpfh) + (salary2 - mpfw)) * STANDARD_RATE
        return std_jointtax
    mtax_amount = 0
    for i, bracket in enumerate(TAX_BRACKETS):
        if assessable_income <= bracket[0]:
            break
        elif assessable_income > bracket[1]:
            mtax_amount += (bracket[1] - bracket[0]) * TAX_RATES[i]
        else:
            mtax_amount += (assessable_income - bracket[0]) * TAX_RATES[i]
            break
    if mtax_amount < 0:
        mtax_amount = 0
    return mtax_amount


def testTax(salary1, salary2):
    try:
        salary1 = int(salary1)
        salary2 = int(salary2)
    except ValueError:
        return "Please enter a valid number"
    if (salary1 < 0) or (salary2 < 0):
        return "Please enter a valid number"
    taxh, mpfhus = septax(salary1)
    taxw, mpfwife = septax(salary2)
    taxm = jointtax(salary1, salary2)
    assessment = ""
    if taxm < taxh + taxw:
        assessment = "Married assessment is more beneficial"
    elif taxm == taxh + taxw:
        assessment = "Both assessments are the same"
    else:
        assessment = "Separate assessment is more beneficial"
    return taxh, mpfhus, taxw, mpfwife, taxm, assessment


class TestTaxCalculation(unittest.TestCase):
    def test_tax_calculator(self):
        # Test for married couple with both earning below basic allowance
        self.assertEqual(testTax(
            "100000", "100000"), (0, 5000, 0, 5000, 0, 'Both assessments are the same'))
        # Test for married couple with one earning above basic allowance
        self.assertEqual(testTax(
            "100000", "500000"), (0, 5000, 41500, 18000, 35210, "Married assessment is more beneficial"))
        # Test for married couple with both earning above basic allowance
        self.assertEqual(testTax(
            "500000", "500000"), (41500, 18000, 41500, 18000, 101000, "Separate assessment is more beneficial"))
        # Test for married couple with both earning above standard rate zone
        self.assertEqual(testTax(
            "3500000", "3500000"), (522300, 18000, 522300, 18000, 1044600, "Both assessments are the same"))
        # Test for married couple with one earning above standard rate zone
        self.assertEqual(testTax(
            "2500000", "1500000"), (372300, 18000, 211500, 18000, 594600, "Separate assessment is more beneficial"))
        # Test for married couple with non earning above standard rate zone but the joint income is above standard rate zone
        self.assertEqual(testTax(
            "1800000", "1500000"), (262500, 18000, 211500, 18000, 489600, "Separate assessment is more beneficial"))
        # Test for invalid input (negative number)
        self.assertEqual(testTax(
            "-100000", "100000"), "Please enter a valid number")
        # Test for invalid input (string)
        self.assertEqual(testTax(
            "abc", "100000"), "Please enter a valid number")
        # Test for invalid input (float)
        self.assertEqual(testTax(
            "100000.5", "100000"), "Please enter a valid number")


if __name__ == '__main__':
    unittest.main()
