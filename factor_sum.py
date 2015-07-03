#!/usr/bin/env python3.3

import os
import sys
import argparse
import re
import collections
import fractions
import cmd

__all__ = [
    'Sum',
    'lcm',
    'arthimetic_sum',
    'multiples_sum',
    'main'
]

class Sum:
    """ 
    The core class that's used to setup and run the calculation
    """
    divisors = set()
    maximum = None
    minimum = 0

    def _sorted_divisors(self):
        """
        Helper method that prepares the set of divisors before summing
        """
        cooked_divisors = None
        for n in self.divisors:
            if not cooked_divisors:
                cooked_divisors = [n]
            else:
                idx = 0

                for i,m in enumerate(cooked_divisors):
                    if m < n:
                        if n % m == 0:
                            break
                        else:
                            idx = i + 1
                    elif m == n:
                        break
                    elif m % n == 0:
                        cooked_divisors.pop(i)
                else:
                    cooked_divisors.insert(idx,n)

        return cooked_divisors

    def add(self, divisors):
        """
        Add divisors. Returns divisors that have actually been added
        """
        effective_divisors = set(divisors) - self.divisors 
        self.divisors = self.divisors ^ effective_divisors
        return effective_divisors

    def remove(self, divisors):
        """
        Remove divisors. Returns divisors that have actually been removed
        """
        effective_divisors = self.divisors & set(divisors)
        self.divisors = self.divisors - effective_divisors
        return effective_divisors

    def clear(self):
        """
        Reset the set of divisors
        """
        self.divisors = set()

    def compute_sum(self):
        """
        Compute the sum
        """
        s = 0
        divisors = self._sorted_divisors()
        for i,n in enumerate(divisors):
            s += multiples_sum(n, self.maximum, self.minimum)
            for m in divisors[:i]:
                s -= multiples_sum(lcm(n,m), self.maximum, self.minimum)
        return s

class QuitShell(Exception):
    """
    Expection raised in SumShell that's used to terminate the shell
    """
    pass
        
class SumShell(cmd.Cmd):
    """
    Interactive shell
    """
    intro = 'Tool for summing factors.  Type help or ? to list commands.\n'
    prompt = '>> '

    def __init__(self,sum_class = Sum()):
        self.divisors = sum_class
        super().__init__()

    def cmdloop(self, intro=None):
        if not intro:
            intro = self.intro

        self.stdout.write(intro)

        while True:
            try:
                super().cmdloop(intro="")
                self.postloop()
            except KeyboardInterrupt:
                self.stdout.write('\n')
            except QuitShell:
                break

    def _pp_list(self,l):
        """
        Pretty print a list
        """
        if l:
            last = l.pop()
            if l:
                return '{0} and {1}'.format(', '.join([str(x) for x in l]), last)
            else:
                return '{0}'.format(last)
        else:
            return None

    def do_add_divisors(self, arg):
        """
        Add numbers to the list of divisors
        """
        try:
            if not arg:
                raise argparse.ArgumentTypeError('the following arguments are required: INT')

            divisors =  self.divisors.add(_parse_ints(arg))
            if divisors:
                self.stdout.write(self._pp_list(divisors))
                self.stdout.write(' added to the list of divisors\n')
            else:
                self.stdout.write('No divisors added\n')
        except argparse.ArgumentTypeError as e:
            self.stdout.write('useage: add_divisors INT [INT ...]\n')
            self.stdout.write('add_divisors: error: {0}\n'.format(str(e)))

    def do_del_divisors(self, arg):
        """
        Remove numbers from the list of divisors
        """
        try:
            if not arg:
                raise argparse.ArgumentTypeError('the following arguments are required: INT')

            divisors =  self.divisors.remove(_parse_ints(arg))
            if divisors:
                self.stdout.write(self._pp_list(divisors))
                self.stdout.write(' removed from the list of divisors\n')
            else:
                self.stdout.write('No divisors removed\n')
        except argparse.ArgumentTypeError as e:
            self.stdout.write('useage: del_divisors INT [INT ...]\n')
            self.stdout.write('del_divisors: error: {0}\n'.format(str(e)))

    def do_clear_divisors(self, arg):
        """
        Clear the list of divisors
        """
        if not arg:
            self.divisors.clear()
        else:
            self.stdout.write('useage: clear\n')

    def do_sum(self, arg):
        """
        Compute the sum. This can only be done after a limit and at lest one
        divisor has been set.
        """
        if not arg:
            if self.divisors.maximum and self.divisors.divisors:
                self.stdout.write('%d\n' % self.divisors.compute_sum())
            elif self.divisors.divisors:
                self.stdout.write('You must add a maxiumum before computing the sum\n')
            elif self.divisors.maximum:
                self.stdout.write('You must add a divisor before computing the sum\n')
            else:
                self.stdout.write('You must add at least one divisor and a maximum before computing the sum\n')
        else:
            self.stdout.write('useage: sum\n')

    def do_EOF(self, arg):
        self.do_quit(arg)

    def do_max(self, arg):
        """
        Set the upper limit. Only numbers less than or equal to this will be
        summed
        """
        try:
            self.divisors.maximum = _parse_int(arg)
            self.stdout.write('The maximum has been set to %s\n' % self.divisors.maximum)
        except argparse.ArgumentTypeError as e:
            self.stdout.write('useage: max INT\n')
            self.stdout.write('max: error: {0}\n'.format(str(e)))

    def do_min(self, arg):
        """
        Set the lower limit. Only numbers less than or equal to this will be
        summed
        """
        try:
            self.divisors.minimum = _parse_int(arg)
            self.stdout.write('The minimum has been set to %s\n' % self.divisors.minimum)
        except argparse.ArgumentTypeError as e:
            self.stdout.write('useage: min INT\n')
            self.stdout.write('min: error: {0}\n'.format(str(e)))

    def do_print_divisors(self, arg):
        """
        Lists the current divisors
        """
        if not arg:
            if self.divisors.divisors:
                for d in self.divisors.divisors:
                    self.stdout.write('{0} '.format(d))
                self.stdout.write('\n')
            else:
                self.stdout.write('There are no divisors set\n')
        else:
            self.stdout.write('useage: list\n')

    def do_print_limits(self, arg):
        """
        Print any limits that have been set
        """
        if not arg:
            if self.divisors.maximum:
                self.stdout.write('Maximum: %d\n' %  self.divisors.maximum)
            else:
                self.stdout.write('Maximum not set\n')

            if self.divisors.minimum:
                self.stdout.write('Minimum: %d\n' %  self.divisors.minimum)
            else:
                self.stdout.write('Minimum not set\n')
        else:
            self.stdout.write('useage: limits\n')

    def do_quit(self, arg):
        """
        Quits the interactive shell
        """
        self.stdout.write('Bye!\n')
        raise QuitShell()

def _parse_format_string(raw_format_str, *tokens):
    """
    Helper function to parse a format string passed in from the command line
    """
    def _parse_format_tokens(sub_match):
        keys = ''.join([k for k,v in tokens])
        token_dict = dict(tokens)
        match = re.match('^([0\-])?([1-9][0-9]*)?(['+keys+'])$', sub_match.group(1))
        sub = ''
        if match:
            sub = '{' + token_dict[match.group(3)] + ':'
            if match.group(2):
                if match.group(1):
                    if '-' in match.group(1):
                        sub += '<' + match.group(2)
                    elif '0' in match.group(1):
                        sub += '0>' + match.group(2)
                else:
                    sub += '>' + match.group(2)
            sub += '}'
        else:
            raise argparse.ArgumentTypeError( 'Invalid format string "%{0}"'.format(sub_match.group(1)))

        return sub

    cooked_parts = []
    raw_format_str = multiple_replace(
        raw_format_str,
        ('}', '}}'),
        ('{','{{'),
        ('\\a', '\a'),
        ('\\b', '\b'),
        ('\\f', '\f'),
        ('\\n', '\n'),
        ('\\r', '\r'),
        ('\\t', '\t'),
        ('\\v', '\v'),
    )

    for raw_part in raw_format_str.split('%%'):
        cooked_parts.append(
            re.sub(
                '%([^a-zA-Z]*[a-zA-Z])',
                _parse_format_tokens,
                raw_part
            ))
    return '%'.join(cooked_parts)

def _parse_int(raw_n):
    """
    Helper function that parses a user input integer
    If the passed argument is not a postive integer None is returned
    """
    if re.match('^\s*(\+\s*)?[0-9]+\s*$', raw_n):
        return int(raw_n.strip(' +'))
    else:
        raise argparse.ArgumentTypeError( 'Value must be a postive integer' )

def _parse_ints(raw_list):
    """
    Helper function that parses an array of user input integers
    If any of the list elements are invalid None is returned
    """
    cooked_list = []
    for raw_n in re.split('\s+',raw_list):
        cooked_n = _parse_int(raw_n)
        if cooked_n:
            cooked_list.append(cooked_n)
        else:
            raise argparse.ArgumentTypeError( 'Value must be space seperated list of postive integera' )

    return cooked_list


def lcm(n,m):
    """
    Returns the lowser common multiple of n and m
    """
    return abs(n*m)//fractions.gcd(n,m)

def arthimetic_sum(n, max_i, min_i=0):
    """
    Computes n * (min_i + (min_i + 1) + ... + max_i)
    """
    s = n * ((max_i * ( max_i + 1) - min_i * (min_i - 1)) // 2)
    return s

def multiples_sum(n, max_value, min_value=0):
    """
    Computes the sum of all multiples of n that are greater than or equal to
    min_value and less than or equal to max_value.
    """
    if min_value == 0:
        return arthimetic_sum(n, max_value//n, 1)
    else:
        return arthimetic_sum(n, max_value//n, ((min_value-1)//n) + 1)

def multiple_replace(string, *key_values):
    """
    Replaces multiple values in string
    """
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]

    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)

    return pattern.sub(replacement_function, string)

def _parse_args(prog, raw_args):
    """
    Parse and validates command line arguments and returns
    a populated namespace argument
    """
    def _positive_integer(arg):
        if re.match('^\s*(\+\s*)?[0-9]+\s*$', arg):
            return int(arg.strip(' +'))
        else:
            raise argparse.ArgumentTypeError( 'Value must be a postive integer' )

    parser = argparse.ArgumentParser(
        prog = prog,
        description = 'Sums postive numbers that divisable by a passed set of\
            numbers. Assumes there a large number of numbers to add - this\
            script is not optimized to add a small number of large numbers.'
    )
    parser.add_argument(
        '-m',
        metavar='MIN',
        dest='minimum',
        type=_parse_int,
        help='Only numbrs greater than or equal to MIN will be included in the sum. Defaults to 0.',
        default = 1
    )
    parser.add_argument(
        '-f',
        metavar='FORMAT_STR',
        dest='format_str',
        help='Format string that will be used in output',
        type = lambda arg: _parse_format_string(arg, ('s','sum'))
    )
    parser.add_argument(
        '-i',
        dest='interactive_mode',
        action='store_true',
        help='Use interactive mode',
        default=False
    )
    parser.add_argument(
        '-M',
        metavar='MAX',
        dest='maximum',
        help='Only numbers less than or equal to MAX will be included in the sum.',
        type=_parse_int
    )
    parser.add_argument(
        '-d',
        metavar='DIVISOR_LIST',
        dest='divisors',
        type = _parse_ints,
        help='Accepts a string of space seperated postive integers.\
            Only numbers that divisable by at least one number in this list\
            are included in the sum.',
    )
    args = parser.parse_args(raw_args)

    if not args.interactive_mode:
        if not args.divisors:
            parser.error('DIVISOR_LIST must be set when not using interactive mode')

        if not args.maximum:
            parser.error('MAX must be set when not using interactive mode')

    if args.maximum and args.minimum and args.maximum <= args.minimum:
        parser.error('MAX must be strictly less than MIN')

    if not args.format_str:
        args.format_str = 'Sum: {sum}\n'

    return args

def main(argv = None):
    if not argv:
        argv = sys.argv 

    prog = os.path.basename(argv[0])
    
    args = _parse_args(prog, argv[1:])
    s = Sum()

    if args.divisors:
        s.add(args.divisors)

    if args.maximum:
        s.maximum = args.maximum

    if args.minimum:
        s.minimum = args.minimum

    if args.interactive_mode:
        SumShell(s).cmdloop()
    else:
        sys.stdout.write(args.format_str.format(sum = s.compute_sum()))
    return 0

if __name__ == '__main__':
    sys.exit(main())
