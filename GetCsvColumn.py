__author__ = 'Lyu Feng'

EXCLUDE_SIGN = '~'
EXCLUDE = lambda x: EXCLUDE_SIGN + str(x)

import csv
import re

class CsvFile(object):
    '''get columns from a comma separated values(csv) file, providing various filter'''
    def __init__(self, filename):
        self._name = filename
        self._header_list = []
        self._dataDict = {}
        self._open_file(self._name)

    def _get_data_dict(self, reader):
        datadict = {}
        for headerindex, column in enumerate(zip(*reader)):
            datadict[self._header_list[headerindex]] = column

        return datadict

    def _open_file(self, filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            self._header_list = reader.next()
            self._dataDict = self._get_data_dict(reader)

    def get_column(self, *header_list, **rule_dict):
        includelist, excludelist, converttype = self._reformat_rule_dict(rule_dict)

        if len(header_list) == 1:
            return self._filter_column(header_list[0], includelist, excludelist, converttype)
        elif len(header_list) > 1:
            return [self._filter_column(header, includelist, excludelist, converttype) for header in header_list]
        else:
            raise Exception('Empty header list!')

    def _reformat_rule_dict(self, rule_dict):
        """
        input: {'SFN': '~[3, 4]', 'CONVERT': <type 'int'>, 'CELL_ID': [1, 4], 'USER_ID': 79}
        output:
        [{'CELL_ID': '1', 'USER_ID': '79'}, {'CELL_ID': '4', 'USER_ID': '79'}],
        [{'SFN': '3'}, {'SFN': '4'}],
        {'CONVERT': <type 'int'>},
        """
        convertType = rule_dict.pop('CONVERT', None)

        seqmatch = re.compile(r'^(\[|\().*(\]|\))$')

        includedict = {}
        for key, value in rule_dict.iteritems():
            if str(value)[0] != EXCLUDE_SIGN:
                if type(value) is list:
                    includedict[key] = value
                else:
                    includedict[key] = [value]

        excludedict = {}
        for key, value in rule_dict.iteritems():
            if str(value)[0] == EXCLUDE_SIGN:
                value = str(value).lstrip(EXCLUDE_SIGN)
                if seqmatch.match(value):
                    excludedict[key] = eval(value)
                else:
                    excludedict[key] = [value]

        # includedict = {'userId': [79], 'cellId': [3, 4]}
        # excludedict = {'sfn': [3, 1]}
        includelist = tuple([{key: str(v)} for key, value in includedict.iteritems() for v in value])
        excludelist = tuple([{key: str(v)} for key, value in excludedict.iteritems() for v in value])

        return includelist, excludelist, convertType

    def _filter_column(self, header, includelist, excludelist, convertType):
        if header not in self._header_list:
            raise Exception('column \"%s\" not found in %s.' % (header, self._name))

        include_unique_keys = list(set([d.keys()[0] for d in includelist]))
        exclude_unique_keys = list(set([d.keys()[0] for d in excludelist]))
        columnarray = []
        for index, data in enumerate(self._dataDict[header]):
            for key in include_unique_keys:
                rowinclude = {key: self._dataDict[key][index]}
                if rowinclude not in includelist:
                    break
            else:
                for key in exclude_unique_keys:
                    rowexclude = {key: self._dataDict[key][index]}
                    if rowexclude in excludelist:
                        break
                else:
                    columnarray.append(convertType(data) if convertType is not None else data)

        return tuple(columnarray)
