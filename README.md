# RecurSieve

Simple visualization of monthly recurring costs vs monthly income. I'm using it
to track my monthly finances.

I find this approach simpler than using mint.com or other services. I keep track
of all services that cost me money per month, and can run the script again to
see how removing certain services affects my disposable income. This also lets
me factor in saving goals, 401k planned contributions, and account for other
income during the month.

## Install
```python
pip install -r requirements.txt
```

## Usage
```bash
python recursieve.py --filename=example.md
```
```
Monthly Cashflow Report
Spending $18.0 in category Entertainment.
Spending $305.5 in category Utilities.
Spending $16.25 in category Online Services.
Spending $1800.0 in category Rent.
Spending $520.6 in category Loans.
Spending $100.0 in category Insurance.

Summary
Total income this month was: $4690.0.
Spend is $2760.35 total per month.
Net saved this month was: $569.0 (10.0% of Salary + $100.0 other savings).
Net disposable income this month was: $1360.65.
```
