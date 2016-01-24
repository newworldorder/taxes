from collections import OrderedDict
import cPickle
import os  
import sys

FED_L1 = .1
FED_L2 = .15
FED_L3 = .25
FED_L4 = .28
FED_L5 = .33
FED_L6 = .35
FED_L7 = .396

class Taxer(object):
    def __init__(self, state = 'Calif.', federal_status = 'Single', 
                 state_status = 'Single'):
        """Initialize object.

        Args:
            state - the state of the filer
            federal_status - the filer's status at the federal level
            state_status - the filer's status at the state level
        """
        pkl_file = 'state_taxes.pkl'
        if os.path.exists(pkl_file):
            self.states_taxes = cPickle.load(open(pkl_file))
        self.possible_states = sorted(self.states_taxes.keys())
        ok = self._set_state_status(state, state_status)
        if not ok:
            sys.stderr.write('\nInvalid state or state status, quitting...\n')
            exit()
        self.state = state
        self.state_status = state_status 
        ok = self._set_federal_tax_brackets(federal_status)
        if not ok:
            sys.stderr.write('\nInvalid federal status provided, quitting...\n')
            exit()
        self.federal_status = federal_status

    def _acc_taxes(self, gross_income, brackets):
        """Accumulate taxes for the given bracket.

        Args:
            gross_income - the income of the filer
            brackets - the income tax brackets

        Returns:
            a float representing the sum of the taxes applied to the gross_income
        """
        done = False
        acc = 0
        if 'None' == brackets:
            return acc 
        for (low, high) in brackets.keys():
            if gross_income <= high:
                done = True
                diff  = gross_income - low + 1
                acc += diff * brackets[(low, high)]
            else:
                diff = high - low + 1
                acc += diff * brackets[(low, high)]
            if done: break
        return acc

    def _set_federal_tax_brackets(self, status):
        """Return the federal tax brackets.

        Source: http://www.efile.com/tax-service/tax-calculator/tax-brackets/   (2015)

        Tax Rate     Single                Married/Joint&Widow(er) Married/Separate     Head of Household
        10%          $1 - $9,225           $1 - $18,450            $1 - $9,225          $1 - $13,150
        15%          $9,226 to $37,450     $18,451 to $74,900      $9,226 to $37,450    $13,151 to $50,200
        25%          $37,451 to $90,750    $74,901 to $151,200     $37,451 to $75,600   $50,201 to $129,600
        28%          $90,751 to $189,300   $151,201 to $230,450    $75,601 to $115,225  $129,601 to $209,850
        33%          $189,301 to $411,500  $230,451 to $411,500    $115,226 to $205,750 $209,851 to $411,500
        35%          $411,501 to $413,200  $411,501 to $464,850    $205,751 to $232,425 $411,501 to $439,200
        39.6%        over $413,200         over $464,850           over $232,425        over $439,200
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

        if status not in d:
            return False
        
        self.federal_brackets = d[status]
        return True

    def _set_state_status(self, state, status):
        """Set the state tax according to the filer's status.

        Args:
            state - the state of the filer
            status - the filing status of the filer

        Returns:
            False if the state or status doesn't exist, True otherwise
        """
        state_map = {}
        if state not in self.states_taxes:
            sys.stderr.write(state + ' does not exist') 
            return False
        state_map = self.states_taxes[state]

        if status not in state_map:
            sys.stderr.write(status + ' does not exist') 
            return False

        self.state_brackets = state_map[status]
       
        return True 

    def federal_tax(self, gross_income):
        """Compute federal tax for `gross_income`.

        Args:
            gross_income - the gross income of filer

        Returns:
            a float representing the federal tax
        """           
        return self._acc_taxes(gross_income, self.federal_brackets)

    def net_income(self, gross_income):
        """Return the net income associated with `gross_income`.

        Args:
            gross_income - the gross income of the filer

        Returns:
            a float representing the net income after taxes have been removed
        """
        total_tax = self.federal_tax(gross_income) + self.state_tax(gross_income)
        return gross_income - total_tax

    def state_tax(self, gross_income):
        """Compute state tax for `gross_income`.

        Args:
            gross_income - the gross income for filer

        Returns:
            a float representing the state tax amount
        """
        return self._acc_taxes(gross_income, self.state_brackets)

if __name__ == '__main__':
    t = Taxer('Calif.', 'Joint', 'Joint')
    salary = 30000
    net_income = t.net_income(salary)
    print 'Annual Net Income:', net_income
    print 'State Taxes:', t.state_tax(salary)
    print 'Federal Taxes:', t.federal_tax(salary)
    print 'Percentage of Annual Net Income:', net_income / salary
    print 'Biweekly Net Income:', net_income / 24

