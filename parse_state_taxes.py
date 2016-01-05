from collections import OrderedDict 
import cPickle 
import sys 

# Colo. 4.63% of federal taxable income 
# Ind. 3.3% of federal taxable income 
# Ill. 3.75% of federal taxable income 
# Mich. 4.25% of adjusted gross income with modification 

ODD_BALLS = set(['Ill.', 'Colo.', 'Mich.', 'Ind.'])

def convert_brackets(brackets):
    """Convert bracket dollar values to integers. An example 
    conversion is as follows: before: $32,322, after: 32322

    Args:
      brackets - a list of strings representing dollar amounts

    Returns:
      a list containing integer representations of the brackets
    """
    l = []
    for bracket in brackets:
        l.append(int(bracket[1:].replace(',', '')))
    l.append(sys.maxint)
    return l 

def convert_rates(rates):
    """Convert the rates into decimal format.  An example 
    conversion is as follows: before: 3.2%, after: .032

    Args:
      rates - a list of string represented percentages

    Returns:
      a list containing float value less than 1 
    """
    l = []
    for rate in rates:
        l.append(float(rate[:-1]) * .01)
    return l 

def make_brackets(status):
    """Create brackets that map to rates. 

    Args:
      status - tuple with list of textual rates
               and a list of textual brackets/
               dollar amounts
    
    Returns:
      an ordered dictionary that maps brackets to
      rates 
    """
    rates = convert_rates(status[0])
    brackets = convert_brackets(status[1])
    bracket_rows = zip(brackets, brackets[1:])
    rows = [bracket_rows[0]]
    for (low, high) in bracket_rows[1:]:
        rows.append((low+1, high))
    s = map_bracket2rate(rows, rates)
    return s

def make_flat_tax(tax_rate):
    """Create a tax rate for all brackets. 
    
    Args:
      tax_rate - the float value (< 1) that is 
                 the tax rate to applied for all
                 dollar amounts 

    Returns:
      a dictionary containing a tax rate for all 
      dollar amounts for all statuses 
    """
    return {'Single':{(0, sys.maxint): tax_rate}, 
            'Joint':{(0, sys.maxint): tax_rate}}

def map_bracket2rate(bracket_rows, rates):
    """Associate bracket entries to tax rates. 

    Args: 
      bracket_rows - list of tuples of dollar amounts
                     represented as integers 
    
    Returns:
      a dictionary containing mappings from a bracket
      to a tax rate (float)  
    """
    d = OrderedDict() 
    for i in range(len(rates)):
            d[bracket_rows[i]] = rates[i]
    return d 

def no_vals(vals):
    """Checks if all values are `none` or `n.a.`

    Args:
      vals - a list of string values 
    
    Returns:
      True if all values contain `none` or `n.a.`,
      False otherwise 
    """
    return all(map(lambda val: 'none' in val or 'n.a.' in val, vals))

if __name__ == '__main__':
    filename = 'state_tax_parsed.output'
    lines = []
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    single_rate = []
    single_bracket = []
    married_rate = []
    married_bracket = []
    states = {}
    state = ''
    for line in lines[4:]:
        tokens = line.split('|')
        if all(map(lambda item: item == '', tokens)):
            if state:
                states[state] = [(single_rate, single_bracket),
                                 (married_rate, married_bracket)]
                single_rate = []
                single_bracket = []
                married_rate = []
                married_bracket = []
            continue 
        if line[0].isalpha():
            parts = tokens[0].split()
            state = parts[0]
        if tokens[1] != '':
            single_rate.append(tokens[1])
        if tokens[3] != '':
            single_bracket.append(tokens[3])
        if tokens[4] != '':
            married_rate.append(tokens[4])
        if tokens[6] != '':
            married_bracket.append(tokens[6])

    states[state] = [(single_rate, single_bracket),
                     (married_rate, married_bracket)]
    s_dict = {}
    for k in states.keys():
        d = {}
        if k in ODD_BALLS:
            continue 
        (single, married) = states[k]
        if no_vals(single[0]):
            s_dict[k] = {"Single":"None", "Joint":"None"}
            continue 
        s = make_brackets(single)
        d["Single"] = s
        m = make_brackets(married)
        d["Joint"] = m
        s_dict[k] = d 

    # handle odd ball cases
    s_dict['Colo.'] = make_flat_tax(.0463)
    s_dict['Ind.'] = make_flat_tax(.033)
    s_dict['Ill.'] = make_flat_tax(.0375)
    s_dict['Mich.'] = make_flat_tax(.0425)

    for k in s_dict.keys():
        print ''
        print k 
        print s_dict[k]

    cPickle.dump(s_dict, open('state_taxes.pkl', 'w'))
