"""
Copyright (C) 2020

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import itertools

import numpy as np
import matplotlib.pyplot as plt

import lamarckian
from lamarckian.ec.mutation.integer import CODING
from lamarckian.ec.mutation.integer.bitwise import Mutation


def main():
    config = lamarckian.util.config.read(os.path.dirname(lamarckian.__file__) + '.yml')
    encoding = np.array([(-3000, 5000), (-1000, 4000)], np.int)
    mutation = Mutation(encoding, config=config, **{**config['mutation'][CODING], **dict(prob=1)})
    parent = np.array([np.random.randint(lower, upper) for lower, upper in zip(*encoding.T)])
    fig = plt.figure()
    ax = fig.gca()
    ax.plot(*parent, 'o', c='k')
    ax.text(*parent, 'p')
    for _, prop in zip(range(500), itertools.cycle(plt.rcParams['axes.prop_cycle'])):
        child = mutation(parent)
        ax.plot(*child, '.', c=prop['color'])
    fig.tight_layout()
    plt.show()
    plt.close(fig)


if __name__ == '__main__':
    main()
