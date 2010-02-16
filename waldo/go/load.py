# -*- coding: utf-8 -*-
# Copyright (C) 2009-2010, Luis Pedro Coelho <lpc@cmu.edu>
# vim: set ts=4 sts=4 sw=4 expandtab smartindent:
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

from __future__ import division
from models import Term
from sqlalchemy.orm import sessionmaker
import gzip
from os import path

_basedir = path.dirname(path.abspath(__file__))
_datadir = path.abspath(path.join(_basedir, '../../data'))
_inputfilename = 'gene_ontology.1_2.obo'

def load(dirname=None, create_session=None):
    '''
    nr_entries = load(dirname={data/}, create_session={backend.create_session})

    Load Gene Ontology OBO file into database

    Parameters
    ----------
      dirname : Directory containing GO files
      create_session : a callable object that returns an sqlalchemy session
    Returns
    -------
      nr_entries : Nr of entries
    '''
    if dirname is None: dirname = _datadir
    if create_session is None:
        import waldo.backend
        create_session = waldo.backend.create_session
    session = create_session()
    filename = path.join(dirname, _inputfilename)
    if not path.exists(filename) and path.exists(filename + '.gz'):
        input = gzip.GzipFile(filename + '.gz')
    else:
        input = file(filename)

    id = None
    in_term = False
    loaded = 0
    for line in input:
        line = line.strip()
        if line in ('[Term]', '[Typedef]'):
            if id is not None and not is_obsolete:
                term = Term(id, name, namespace)
                session.add(term)
                loaded += 1
            is_a = []
            is_obsolete = False
            id = None
            in_term = (line == '[Term]')
        if not in_term:
            continue
        if line.find(':') > 0:
            code, content = line.split(':',1)
            content = content.strip()
            if code == 'id':
                id = content
            elif code == 'name':
                name = content
            elif code == 'is_a':
                content,_ = content.split('!')
                content = content.strip()
                is_a.append(content)
            elif code == 'is_obsolete':
                is_obsolete = True
            elif code == 'namespace':
                namespace = content

    session.commit()
    return loaded