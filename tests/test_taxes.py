from taxes import Taxer 

from nose import with_setup 
from nose.tools import assert_equals 


def test_net_income():
    # test state w/ no state taxes 
    t = Taxer('Fla.', 'Single')
    salary = 120000
    net_income = t.net_income(salary) 
    assert_equals(net_income, 93328.75, 'Net Income is wrong for Fla')

def test_state_tax():
    # test state w/ no state taxes 
    t = Taxer('Fla.', 'Single')
    salary = 120000
    state_tax = t.state_tax(salary)
    assert_equals(state_tax, 0, 'State tax should be 0 but is ' + str(state_tax))

def test_federal_tax():
    # test state w/ no state taxes 
    t = Taxer('Fla.', 'Single')
    salary = 120000
    federal_tax = t.federal_tax(salary)
    assert_equals(federal_tax, 26671.25, 'Federal tax should be '+ str(federal_tax))


