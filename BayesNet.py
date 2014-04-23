#!/usr/bin/env python3

import sys, re, copy

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

    def normalize(self, dist):
        """
        Normalize distribution.

        Args:
            dist:   List of probability corresponding to True and False

        Returns:
            normalized tuple

        >>> print("%.3f, %.3f" % Net('alarm.bn').normalize([0.00059224, 0.0014919]))
        0.284, 0.716
        """
        return tuple(x * 1/(sum(dist)) for x in dist)

    def toposort(self):
        """
        Topological sort on the set of variables.

        >>> Net('alarm.bn').toposort() 
        ['B', 'E', 'A', 'J', 'M']
        """
        variables = list(self.net.keys())
        variables.sort()
        s = set()
        l = []
        while len(s) < len(variables):
            for v in variables:
                if v not in s and all(x in s for x in self.net[v]['parents']):
                    s.add(v)
                    l.append(v)
        return l

    def querygiven(self, Y, e):
        """
        Calculate P(y | parents(Y))

        >>> net = Net('alarm.bn')
        >>> e = {'B': False, 'E': True, 'A': False}
        >>> net.querygiven('A', e)
        0.71
        """
        # if Y has no parents
        if self.net[Y]['prob'] != -1:
            prob = self.net[Y]['prob'] if e[Y] else 1 - self.net[Y]['prob']

        # if Y has at least 1 parent
        else:
            # get the value of parents of Y
            parents = tuple(e[p] for p in self.net[Y]['parents'])

            # query for prob of Y = y
            prob = self.net[Y]['condprob'][parents] if e[Y] else 1 - self.net[Y]['condprob'][parents]
        return prob

    def enum_ask(self, X, e):
        """
        Calculate the distribution over the query variable X using enumeration.

        Args:
            X:  The query variable.
            e:  Dictionary of evidence variables and observed values.

        Returns:
            Distribution over X as a tuple (t, f).
        """
        dist = []
        for x in [False, True]:
            # make a copy of the evidence set
            e = copy.deepcopy(e)

            # extend e with value of X
            e[X] = x

            # topological sort
            variables = self.toposort()

            # enumerate
            dist.append(self.enum_all(variables, e))

        # normalize & return
        return self.normalize(dist)

    def enum_all(self, variables, e):
        """
        Enumerate over variables.

        Args:
            variables:  List of variables, topologically sorted
            e:          Dictionary of the evidence set in form of 'var': True/False.

        Returns:
            probability as a real number
        """
        if len(variables) == 0:
            return 1.0
        Y = variables[0]
        if Y in e:
            ret = self.querygiven(Y, e) * self.enum_all(variables[1:], e)
        else:
            probs = []
            e2 = copy.deepcopy(e)
            for y in [True, False]:
                e2[Y] = y
                probs.append(self.querygiven(Y, e2) * self.enum_all(variables[1:], e2))
            ret = sum(probs)

        print("%-14s | %-20s = %.8f" % (
                ' '.join(variables),
                ' '.join('%s=%s' % (v, 't' if e[v] else 'f') for v in e),
                ret
            ))
        return ret

    def elim_ask(self, X, e):
        """
        Calculate the distribution over the query variable X using elimination.

        Args:
            X:  The query variable.
            e:  Dictionary of evidence variables and observed values.

        Returns:
            Distribution over X as a tuple (t, f).
        """
        pass

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
    if match:
        X = match.group(1).strip()
        e = match.group(2).strip().split(',')
        edict = dict((x[0], True if x[2] == 't' else False) for x in e)
    else:
        match = re.match(r'P\((.*)\)', q)
        X = match.group(1).strip()
        e = []
        edict = {}
     
    #  call function
    dist = net.enum_ask(X, edict) if alg == 'enum' else net.elim_ask(X, edict)
    print("\nRESULT:")
    for prob, x in zip(dist, [False, True]):
        print("P(%s = %s | %s) = %.8f" %
                (X,
                't' if x else 'f',
                ', '.join('%s = %s' % tuple(v.split('=')) for v in e),
                prob))

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
    import doctest
    doctest.testmod()
    main()