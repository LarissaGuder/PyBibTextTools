# Copyright (c) 2006-2017  Andrey Golovigin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import unicode_literals

import re

from pybtex.py3compat import fix_unicode_literals_in_doctest
from pybtex.utils import deprecated

terminators = '.', '?', '!'
delimiter_re = re.compile(r'([\s\-])')
whitespace_re = re.compile(r'\s+')


@deprecated('0.19', 'use str.capitalize() instead')
def capfirst(s):
    return s[0].upper() + s[1:] if s else s


def is_terminated(text):
    """
    Return True if text ends with a terminating character.

    >>> is_terminated('')
    False
    >>> is_terminated('.')
    True
    >>> is_terminated('Done')
    False
    >>> is_terminated('Done. ')
    False
    >>> is_terminated('Done.')
    True
    >>> is_terminated('Done...')
    True
    >>> is_terminated('Done!')
    True
    >>> is_terminated('Done?')
    True
    >>> is_terminated('Done?!')
    True
    """

    return text.endswith(terminators)


def add_period(text):
    """Add a period to the end of text, if needed.

    >>> print(add_period(''))
    <BLANKLINE>
    >>> print(add_period('.'))
    .
    >>> print(add_period('Done'))
    Done.
    >>> print(add_period('Done. '))
    Done. .
    >>> print(add_period('Done.'))
    Done.
    >>> print(add_period('Done...'))
    Done...
    >>> print(add_period('Done!'))
    Done!
    >>> print(add_period('Done?'))
    Done?
    >>> print(add_period('Done?!'))
    Done?!
    """

    if text and not is_terminated(text):
        return text + '.'
    return text


@fix_unicode_literals_in_doctest
def abbreviate(text, split=delimiter_re.split):
    """Abbreviate the given text.

    >> abbreviate('Name')
    u'N'
    >> abbreviate('Some words')
    u'S. w.'
    >>> abbreviate('First-Second')
    u'F.-S.'
    """

    def abbreviate(part):
        if part.isalpha():
            return part[0] + '.'
        else:
            return part

    return ''.join(abbreviate(part) for part in split(text))


def normalize_whitespace(string):
    r"""
    Replace every sequence of whitespace characters with a single space.

    >>> print(normalize_whitespace('abc'))
    abc
    >>> print(normalize_whitespace('Abc def.'))
    Abc def.
    >>> print(normalize_whitespace(' Abc def.'))
    Abc def.
    >>> print(normalize_whitespace('Abc\ndef.'))
    Abc def.
    >>> print(normalize_whitespace('Abc\r\ndef.'))
    Abc def.
    >>> print(normalize_whitespace('Abc    \r\n\tdef.'))
    Abc def.
    >>> print(normalize_whitespace('   \nAbc\r\ndef.'))
    Abc def.
    """

    return whitespace_re.sub(' ', string.strip())


def width(string):
    r"""
    Get the width of the typeset string, in relative units.  Similar to
    BibTeX's width$, but does not care about any "special characters".

    >>> width('')
    0
    >>> width('abc')
    1500
    >>> width('ab{c}')
    2500
    >>> width(r"ab{\'c}")
    3278
    >>> width(r"ab{\'c{}}")
    4278
    >>> width(r"ab{\'c{}")
    3778
    >>> width(r"ab{\'c{d}}")
    4834
    """

    from pybtex.charwidths import charwidths
    return sum(charwidths.get(char, 0) for char in string)


def tie_or_space(word, tie='~', space=' ', enough_chars=3, other_word=None):
    n_chars = len(word)
    if other_word is not None:
        n_chars = min(n_chars, len(other_word))

    if n_chars < enough_chars:
        return tie
    else:
        return space
