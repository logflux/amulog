#!/usr/bin/env python
# coding: utf-8

"""Modify templates that is generated by external tools.
amulog can import templates that is splitted as a sequence of words,
but many external tools do not provide them in such style.
This script redifine templates by templates
and their corresponding log messages.
"""

import numpy as np

from amulog import lt_common


def _get_variable_mask(mes, matchobj):
    vm = np.array([False] * len(mes))
    d = matchobj.groupdict()
    for k in d:
        vm[matchobj.start(k):matchobj.end(k)] = True
    return vm


def _get_word_span(l_tpl_w, l_tpl_s):
    ws = []
    place = len(l_tpl_s[0])
    for w, s in zip(l_tpl_w, l_tpl_s[1:]):
        place_next = place + len(w)
        ws.append((place, place_next))
        place_next += len(s)
        place = place_next
    return ws


def redefine_tpl(tpl, parsed_line, matchobj=None):
    mes = parsed_line["message"]
    l_tpl_w = parsed_line["words"]
    l_tpl_s = parsed_line["symbols"]

    if matchobj is None:
        from . import tpl_match
        tpl_regex = tpl_match.generate_regex(tpl)
        matchobj = tpl_regex.match(mes)
        if matchobj is None:
            errmes = "message {0} not matched to tpl {1}".format(mes, tpl)
            raise ValueError(errmes)

    vm = _get_variable_mask(mes, matchobj)
    ws = _get_word_span(l_tpl_w, l_tpl_s)

    new_tpl = []
    for w, span in zip(l_tpl_w, ws):
        if True in vm[span[0]:span[1]]:
            new_tpl.append(lt_common.REPLACER)
        else:
            new_tpl.append(w)
    return new_tpl
