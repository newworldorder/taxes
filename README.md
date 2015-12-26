# taxes

This module computes federal taxes and state taxes for a given gross salary. 

# API 

- `net_income(gross_income, status)` returns the net income for the given `gross_income` (and `status`) given the federal and state taxes previously specified.  
- `federal_tax(gross_income, status)` returns the federal tax associated with `gross_income` and `status`
- `federal_tax_brackets(federal_brackets)` sets the federal tax brackets
- `state_tax(gross_income)` returns the state tax associated with `gross_income`
- `state_tax_brackets(state_brackets)` sets the state tax brackets  

# Data Structures

- `federal_brakets` is a dictionary where the key corresponds to a `status` (see `status` below) which returns another dictionary of brackets where keys correpsonds to dollar ranges, and the values correspond to the percentage of tax for that range. 
- `gross_income` is a float
- `status` is the federal income tax classification asscociated with the gross income, which is one of the following: "Single", "Joint", "Separate", and "Head" (for head of household).  
- `state_brakets` is a dictionary where the key is a tuple of two items, the low end of the bracket and the high end of the bracket and value is a float representing the tax percentage



