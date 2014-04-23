#!/usr/bin/env python3

import sys, re

class Net:
    """
    Class for Bayesian Network.

    Data structure(s):
        dictionary that maps variable names to a dictonary {
                parents -> list of parents
                children -> list of children
                prob -> probability of the variable if it's independent, else None
                condprob -> dictionary for the conditionary probability table {
                        tuple of values for parents -> probability
                    }
            }

        e.g. for ex2.bn
        {
            'A': {
                'parents': [],
                'children': ['C', 'D'],
                'prob': 0.3,
                'condprob': {}
            },
            
            ...

            'D': {
                'parents': ['A', 'B'],
                'children': [],
                'prob': -1,
                'condprob': {
                    (True, True): 0.7,
                    (True, False): 0.8,
                    ...
                }
            }
        }
    """
    def __init__(self, fname):
        self.vars = set()
        self.net = {}
        lines = []
        with open(fname) as f:
            for line in f:
                if line == '\n':
                    # parse if encounter a blank line
                    self._parse(lines)
                    lines = []
                else:
                    lines.append(line)
        # there is no blank line at the eof
        # but we still have to parse the last part
        if len(lines) != 0:
            self._parse(lines)


    def _parse(self, lines):
        if len(lines) == 1:
            #  single line
            match = re.match(r'P\((.*)\) = (.*)\n', lines[0])
            var, prob = match.group(1).strip(), float(match.group(2).strip())
            self.net[var] = {
                'parents': [], 
                'children': [],
                'prob': prob,
                'condprob': {}
            }
        else:
            # table header
            match = re.match(r'(.*) \| (.*)', lines[0])
            parents, var = match.group(1).split(), match.group(2).strip()
            for p in parents:
                self.net[p]['children'].append(var)
            self.net[var] = {
                'parents': parents,
                'children': [],
                'prob': -1,
                'condprob': {}
            }

            # table entries
            for probline in lines[2:]:
                match = re.match(r'(.*) \| (.*)', probline)
                truth, prob = match.group(1).split(), float(match.group(2).strip())
                truth = tuple(True if x == 't' else False for x in truth)
                self.net[var]['condprob'][truth] = prob

    def enum_ask(self, X, e):
        """
        Calculate the distribution over the query variable X using enumeration.

        Args:
            X:  The query variable.
            e:  Dictionary of evidence variables and observed values.

        Returns:
            Distribution over X as a tuple (t, f).
        """
        pass

    def elim_ask(self, X, e):
        """
        Calculate the distribution over the query variable X using elimination.

        Args:
            X:  The query variable.
            e:  Dictionary of evidence variables and observed values.

        Returns:
            Distribution over X as a tuple (t, f).
        """

def query(fname, alg, q):
    """
    Construct the bayes net, query and return distr.

    Args:
        fname:  File name of the bayes net
        alg:    Algorithm to use (enum or elim)
        q:      Query
    """
    #  construct net
    try:
        net = Net(fname)
    except:
        print('Failed to parse %s' % fname)
        exit()

    #  parse query
    match = re.match(r'P\((.*)\|(.*)\)', q)
    X = match.group(1).strip()
    e = match.group(2).strip().split(',')
    e = dict(x.split('=') for x in e)
     
    #  call function
    if alg == 'enum':
        net.enum_ask(X, e)
    else:
        net.elim_ask(X, e)

def main():
    try:
        fname = sys.argv[1]

        alg = sys.argv[2]
        assert(alg == 'enum' or alg == 'elim')

        q = sys.argv[3]

        query(fname, alg, q)
    except SyntaxError:
        print('Invalid syntax for bayes net file %s' % sys.argv[1])
    except IndexError:
        print('Not enough argument.')
        print('Usage: %s <bayesnet> <enum|elim> <query>' % sys.argv[0])

if __name__=='__main__':
    main()