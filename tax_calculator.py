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


# Get input from user
try:
    salaryh = float(input("Enter husband yearly salary: "))
    salaryw = float(input("Enter wife yearly salary: "))
except ValueError:
    print("Please enter a valid number")
    exit()
if (salaryh < 0) or (salaryw < 0):
    print("Please enter a valid number")
    exit()

# Calculate the yearly salary tax for each person
taxh, mpfhus = septax(salaryh)
taxw, mpfwife = septax(salaryw)
taxm = jointtax(salaryh, salaryw)

# Results
print("")
print("(a) MPF Mandatory Contribution Based on Personal Income")
print("Husband yearly salary mpf is: HKD {:.2f}".format(mpfhus))
print("Wife yearly salary mpf is: HKD {:.2f}".format(mpfwife))
print("")
print("(b) Salaries Tax To Be Paid If Separate Assessment Assumed")
print("Husband yearly salary tax is: HKD {:.2f}".format(taxh))
print("Wife yearly salary tax is: HKD {:.2f}".format(taxw))
print("Tax to be paid total: HKD {:.2f}".format(taxh + taxw))
print("")
print("(c) Salaries Tax To Be Paid If Married Assessment Assumed")
print("Married yearly salary tax is: HKD {:.2f}".format(taxm))
print("")
print("(d) Recommendation: Whether Joint Assessment Is Recommended")
if taxm < taxh + taxw:
    print("Married assessment is more beneficial")
elif taxm == taxh + taxw:
    print("Both assessments are the same")
else:
    print("Separate assessment is more beneficial")
# to be removed
print("")
print(taxh, mpfhus, taxw, mpfwife, taxm)
