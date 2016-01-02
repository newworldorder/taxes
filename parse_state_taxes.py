from collections import OrderedDict 
import cPickle 
import sys 

ODD_BALLS = set(['Ill.', 'Colo.', 'Mich.', 'Ind.'])

def no_vals(vals):
    return all(map(lambda val: 'none' in val or 'n.a.' in val, vals))
    
def convert_rates(rates):
    l = []
    for rate in rates:
        l.append(float(rate[:-1]) * .01)
    return l 

def convert_brackets(brackets):
    l = []
    for bracket in brackets:
        l.append(int(bracket[1:].replace(',', '')))
    l.append(sys.maxint)
    return l 

def make_brackets(status):
    rates = convert_rates(status[0])
    brackets = convert_brackets(status[1])
    bracket_rows = zip(brackets, brackets[1:])
    rows = [bracket_rows[0]]
    for (low, high) in bracket_rows[1:]:
        rows.append((low+1, high))
    s = map_bracket2rate(rows, rates)
    return s

def map_bracket2rate(bracket_rows, rates):
    d = OrderedDict() 
    for i in range(len(rates)):
            d[bracket_rows[i]] = rates[i]
    return d 

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
    
    for k in s_dict.keys():
        print ''
        print k 
        print s_dict[k]

    cPickle.dump(s_dict, open('state_taxes.pkl', 'w'))
