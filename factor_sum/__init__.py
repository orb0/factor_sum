#!/usr/bin/env python3.4
# Copyright 2015 Aubrey Stark-Toller <aubrey@deepearth.uk>
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import argparse
import re
import collections
import fractions

__all__ = [
    'Sum',
    'lcm',
    'arthimetic_sum',
    'multiples_sum',
    'main'
]

class Sum(object):
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
        divisors_iter = iter(self.divisors)
        cooked_divisors = [ next(divisors_iter) ]
        for raw_divisor in divisors_iter:
            new_idx = 0
            for idx,cooked_divisor in enumerate(cooked_divisors):
                if cooked_divisor < raw_divisor:
                    if raw_divisor % cooked_divisor == 0:
                        break
                    else:
                        new_idx = idx + 1
                elif cooked_divisor % raw_divisor == 0:
                    cooked_divisors.pop(idx)
            else:
                cooked_divisors.insert(idx, raw_divisor)

        return cooked_divisors

    def add(self, *divisors):
        """
        Add divisors
        """
        self.divisors = self.divisors | set(divisors)

    def remove(self, *divisors):
        """
        Remove divisors
        """
        self.divisors = self.divisors - set(divisors)

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
        for idx,divisor in enumerate(divisors):
            s += multiples_sum(divisor, self.maximum, self.minimum)
            for n in divisors[:idx]:
                s -= multiples_sum(lcm(divisor,n), self.maximum, self.minimum)
        return s

def lcm(n,m):
    """
    Returns the lowser common multiple of n and m
    """
    return abs(n*m)//fractions.gcd(n,m)

def multiples_sum(n, max_value, min_value=0):
    """
    Computes the sum of all multiples of n that are greater than or equal to
    min_value and less than or equal to max_value.
    """
    min_i = ((min_value-1)//n) + 1
    max_i = max_value//n
    return n * ((max_i * ( max_i + 1) - min_i * (min_i - 1)) // 2)

def _parse_int(raw_n):
    """
    Helper function that parses a user input integer
    If the passed argument is not a postive integer None is returned
    """
    if re.match('^\s*(\+\s*)?[0-9]+\s*$', raw_n):
        return int(raw_n.strip(' +'))
    else:
        raise argparse.ArgumentTypeError( 'Value must be a postive integer' )

def _parse_args(prog, raw_args):
    """
    Parse and validates command line arguments and returns
    a populated namespace argument
    """
    parser = argparse.ArgumentParser(
        prog = prog,
        description = 'Sums postive numbers that divisable by at least one \
                       number in a passed set of numbers.'
    )
    parser.add_argument(
        '-m',
        metavar='MIN',
        dest='minimum',
        type=_parse_int,
        help='Only numbers greater than or equal to MIN will be included in \
              the sum. Defaults to 0.',
        default = 1
    )
    parser.add_argument(
        'maximum',
        metavar='MAX',
        help='Only numbers less than or equal to MAX will be included in the \
              sum.',
        type=_parse_int
    )
    parser.add_argument(
        'divisors',
        metavar='DIVISOR',
        nargs = '+',
        type = _parse_int,
        help='A postive integer. Only numbers that divisable by at\
              least one DIVISOR are included in the sum.',
    )
    args = parser.parse_args(raw_args)

    if args.maximum and args.minimum and args.maximum <= args.minimum:
        parser.error('MAX must be strictly less than MIN')

    return args

def main(argv = None):
    if not argv:
        argv = sys.argv 

    prog = os.path.basename(argv[0])
    
    args = _parse_args(prog, argv[1:])
    s = Sum()

    s.add(*args.divisors)
    s.maximum = args.maximum

    if args.minimum:
        s.minimum = args.minimum

    sys.stdout.write(str(s.compute_sum()))
    sys.stdout.write("\n")

if __name__ == '__main__':
    sys.exit(main())
