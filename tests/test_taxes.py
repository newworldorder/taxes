from taxes import Taxer 

from nose import with_setup 
from nose.tools import assert_equals 

t = None

def setup_test():
    global t
    t = Taxer() 

@with_setup(setup_test)
def test_net_income():
    # test state w/ no state taxes 
    t.set_state_status('Fla.', 'Single')
    salary = 120000
    net_income = t.net_income(salary, 'Single') 
    assert_equals(net_income, 93328.75, 'Net Income is wrong for Fla')

@with_setup(setup_test)
def test_state_tax():
    # test state w/ no state taxes 
    t.set_state_status('Fla.', 'Single')
    salary = 120000
    state_tax = t.state_tax(salary)
    assert_equals(state_tax, 0, 'State tax should be 0 but is ' + str(state_tax))

@with_setup(setup_test)
def test_federal_tax():
    # test state w/ no state taxes 
    t.set_state_status('Fla.', 'Single')
    salary = 120000
    federal_tax = t.federal_tax(salary)
    assert_equals(federal_tax, 26671.25, 'Federal tax should be '+ str(federal_tax))


