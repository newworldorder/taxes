from collections import OrderedDict 
import sys 

FED_L1 = .1
FED_L2 = .15
FED_L3 = .25
FED_L4 = .28
FED_L5 = .33
FED_L6 = .35
FED_L7 = .396

class Taxer(object):
	def __init__(self):
		self.federal_brackets = self._federal_tax_brackets()
		self.state_brackets = self._CA_tax_brackets()

	def _CA_tax_brackets(self):
		"""Return CA tax brackets. 
		Source: http://www.bankrate.com/finance/taxes/state-taxes-california.aspx
		1 percent on the first $7,749 of taxable income.
		2 percent on taxable income between $7,750 and $18,371.
		4 percent on taxable income between $18,372 and $28,995.
		6 percent on taxable income between $28,996 and $40,250.
		8 percent on taxable income between $40,251 and $50,869.
		9.3 percent on taxable income between $50,870 and 259,844.
		10.3 percent on taxable income between $259,845 and 311,812.
		11.3 percent on taxable income between $311,813 and $519,687.
		12.3 percent on taxable income of $519,688 and above.
		A 1 percent surcharge, the Mental Health Services Tax, is collected on taxable incomes of $1 million or more,
		"""
		d = OrderedDict() 
		d[(1, 7749)] = .01
		d[(7750, 18371)] = .02
		d[(18372, 28995)] = .04
		d[(28996, 40250)] = .06
		d[(40251, 50869)] = .08
		d[(50870, 259844)] = .093
		d[(259845, 311812)] = .103
		d[(311813, 519687)] = .113
		d[(519688, 999999)] = .123
		d[(1000000, sys.maxint)] = .133

		return d 

	def federal_tax(self, gross_income, status):
		"""Compute federal tax for `gross_income` and filing `stats`.

		Args:
			gross_income - the gross income of filer 
			status - the filing status of the filer 

		Returns:
			a float representing the federal tax 
		"""
		pass

	def federal_tax_brackets(self, federal_brackets):
		"""Set the federal tax brackets.

		Args:
			federal_brackets - dictionary containing status values as keys and
							   brackets (dictionaries) as values 
		"""
		pass

	def net_income(self, gross_income, status):
		"""Return the net income associated with `gross_income` and `status`.

		Args:
			gross_income - the gross income of the filer
			status - the filing status of the filer

		Returns:
			a float representing the net income after taxes have been removed
		"""
		pass 

	def state_tax(self, gross_income):
		"""Comptue state tax for `gross_income`.

		Args:
			gross_income - the gross income of the filer

		Returns:
			a float representing the state tax
		"""
		pass 

	def state_tax_brackets(self, state_brackets):
		"""Set the state tax brackets.

		Args:
			state_brackets - a dictionary containing dollar ranges in a tuple as
							 the key and the tax rate as the value 
		"""
		pass

	def _federal_tax_brackets(self):
		"""Return the federal tax brackets. 
		Source: http://www.efile.com/tax-service/tax-calculator/tax-brackets/
		(2015)
		Tax Rate   Single	            Married/Joint&Widow(er)	Married/Separate	 Head of Household
		10%	       $1 - $9,225	        $1 - $18,450	        $1 - $9,225	         $1 - $13,150
		15%	       $9,226 to $37,450	$18,451 to $74,900	    $9,226 to $37,450	 $13,151 to $50,200
		25%	       $37,451 to $90,750	$74,901 to $151,200	    $37,451 to $75,600	 $50,201 to $129,600
		28%	       $90,751 to $189,300	$151,201 to $230,450	$75,601 to $115,225	 $129,601 to $209,850
		33%	       $189,301 to $411,500	$230,451 to $411,500	$115,226 to $205,750 $209,851 to $411,500
		35%	       $411,501 to $413,200	$411,501 to $464,850	$205,751 to $232,425 $411,501 to $439,200
		39.6%	   over $413,200	    over $464,850	        over $232,425	     over $439,200
		"""
		single = OrderedDict()
		single[(1, 9225)] = FED_L1
		single[(9226, 37450)] = FED_L2
		single[(37451, 90750)] = FED_L3
		single[(90751, 189300)] = FED_L4
		single[(189301, 411500)] = FED_L5
		single[(411501, 413200)] = FED_L6
		single[(413200, sys.maxint)] = FED_L7

		joint = OrderedDict()
		joint[(1, 18450)] = FED_L1
		joint[(18451, 74900)] = FED_L2
		joint[(74901, 151200)] = FED_L3
		joint[(151201, 230450)] = FED_L4
		joint[(230451, 411500)] = FED_L5
		joint[(411501, 464850)] = FED_L6
		joint[(464851, sys.maxint)] = FED_L7

		separate = OrderedDict()
		separate[(1, 9225)] = FED_L1
		separate[(9226, 37450)] = FED_L2
		separate[(37451, 75600)] = FED_L3
		separate[(75601, 115225)] = FED_L4
		separate[(115226, 205750)] = FED_L5
		separate[(205751, 232425)] = FED_L6
		separate[(232426, sys.maxint)] = FED_L7

		head = OrderedDict() 
		head[(1, 13150)] = FED_L1
		head[(13151, 50200)] = FED_L2
		head[(50201, 129600)] = FED_L3
		head[(129601, 209850)] = FED_L4
		head[(209851, 411500)] = FED_L5
		head[(411501, 439200)] = FED_L6
		head[(439201, sys.maxint)] = FED_L7

		d = dict() 
		d['Single'] = single
		d['Joint'] = joint
		d['Separate'] = separate
		d['Head'] = head
		return d 

if __name__ == '__main__':
	t = Taxer()
	print t.federal_brackets
	print t.state_brackets
