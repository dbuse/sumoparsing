# -*- coding: utf-8 -*-
"""
Sumo output file parsing helpers.
"""
from __future__ import print_function, unicode_literals, absolute_import

import collections
import warnings

import lxml.etree as ET

from .xmldescriptions import xml_type_configs

_fieldconverter = collections.namedtuple(
    '_fieldconverter',
    ('newname', 'convert'),
)


def _iterparse_plain_xml(xml_file, tag, fields, **ignored_kwd):
    """Yield records for every ``tag'' item in sumo xml file."""
    # prepare fields table
    fconvert = {
        fname: _fieldconverter(
            fconf['newname'] if isinstance(fconf, dict) else fname,
            fconf['func'] if isinstance(fconf, dict) else fconf
        )
        for fname, fconf in fields.items()
    }
    # set up parser to read source file and filter only ``tag''-items
    iterparser = ET.iterparse(
        source=xml_file,
        events=('start', ),
        tag=[tag],
        encoding='utf-8'
    )
    for _event, elem in iterparser:
        # convert values and yield result
        yield {fconvert[field].newname: fconvert[field].convert(value)
               for field, value in elem.attrib.items()
               if field in fields}
        elem.clear()


def _iterparse_nested_xml(xml_file, tags, fields, **ignored_kwd):
    """Yield a record for each element of the lowest tag in sumo xml file."""
    # prepare fields table
    fconvert = {
        tag: {
            fname: _fieldconverter(
                fconf['newname'] if isinstance(fconf, dict) else fname,
                fconf['func'] if isinstance(fconf, dict) else fconf
            )
            for fname, fconf in tagfields.items()
        }
        for tag, tagfields in fields.items()
    }
    # set up parser to read source file and filter only ``tag''-items
    iterparser = ET.iterparse(
        source=xml_file,
        events=('start', 'end'),
        tag=[tags],
        recover=True,
        encoding='utf-8'
    )
    # separate non-bottomlevel tags as containers
    container_tags = set(tags[:-1])
    container_fields = dict()
    for event, elem in iterparser:
        if event == 'start':
            if elem.tag in container_tags:
                # starting container tag -> update stored fields
                for fname, fconf in fconvert[elem.tag].items():
                    try:
                        container_fields[fconf.newname] = fconf.convert(
                            elem.get(fname)
                        )
                    except TypeError as exc:
                        warnings.warn(
                            "Could not read/convert field {}[{}]: '{}'".format(
                                elem.tag,
                                fname,
                                str(exc)
                            )
                        )
            else:
                # starting bottom-level tag -> yield record
                fconf = fconvert[elem.tag]
                res = {
                    fconf[key].newname: fconf[key].convert(val)
                    for key, val in elem.attrib.items()
                }
                res.update(container_fields)
                yield res
                del res
        else:
            # any closing tag -> cleanup
            elem.clear()


def is_plain_xml(filetype):
    """Return true if xml file type is plain (not nested)."""
    if 'tag' in xml_type_configs[filetype]:
        return True
    elif 'tags' in xml_type_configs[filetype]:
        return False
    else:
        raise KeyError(
            'Unknown configuration type for file type {}'.format(filetype)
        )


def iterparse_xml(xml_file, filetype):
    """Yield records from ``xml_file'' according to schema of ``filetype''."""
    conf = xml_type_configs[filetype]
    if is_plain_xml(filetype):
        yield from _iterparse_plain_xml(xml_file, **conf)
    else:
        yield from _iterparse_nested_xml(xml_file, **conf)


def get_result_field_types(filetype):
    """Return mapping of fieldname:result_type for fields of ``filetype''."""
    if is_plain_xml(filetype):
        return dict([
            (fconf['newname'], fconf['func'])
            if isinstance(fconf, dict)
            else (fname, fconf)
            for fname, fconf in xml_type_configs[filetype]['fields'].items()
        ])
    return dict([
        (fconf['newname'], fconf['func'])
        if isinstance(fconf, dict)
        else (fname, fconf)
        for _tag, tagfields in xml_type_configs[filetype]['fields'].items()
        for fname, fconf in tagfields.items()
    ])
