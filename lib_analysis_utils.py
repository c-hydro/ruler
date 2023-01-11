"""
Library Features:

Name:          lib_analysis_utils
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20221227'
Version:       '1.0.0'
"""

#######################################################################################
# Libraries
import logging
import math
import psutil
from psutil._common import bytes2human
from psutil._common import pcputimes
from copy import deepcopy

from lib_info_args import logger_name

# Logging
log_stream = logging.getLogger(logger_name)
#######################################################################################


# -------------------------------------------------------------------------------------
# Method to split size parts (value and units)
def split_size_parts(size_string):

    if size_string is not None:
        size_alpha_list, size_numeric_list = None, None
        for size_elem in size_string:
            if size_elem.isalpha():
                if size_alpha_list is None:
                    size_alpha_list = []
                size_alpha_list.append(size_elem)
            elif size_elem.isnumeric() or size_elem == '.':
                if size_numeric_list is None:
                    size_numeric_list = []
                size_numeric_list.append(size_elem)
            else:
                log_stream.error(' ===> Object "size_string" must be defined only by character or numbers')
                raise NotImplemented('Case not implemented yet')

        if size_numeric_list is None:
            log_stream.error(' ===> Object "size_string" must be defined by a part that defined the value')
            raise RuntimeError('Obj "size_string" must be defined by list of two elements (value and units)')
        if size_alpha_list is None:
            log_stream.error(' ===> Object "size_string" must be defined by a part that defined the units')
            raise RuntimeError('Obj "size_string" must be defined by list of two elements (value and units)')

        # join elements to create a string
        size_numeric_string = ''.join(size_numeric_list)
        size_alpha_string = ''.join(size_alpha_list).upper()
        # create a list to save value and units
        size_list = [size_numeric_string, size_alpha_string]

    else:
        log_stream.error(' ===> Object "size_string" is defined by NoneType')
        raise RuntimeError('Obj "size_string" must be defined by list of two elements (value and units)')

    return size_list
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# method to check whitespace in size string
def check_size_whitespaces(size_string):
    return any(size_elem.isspace() for size_elem in size_string)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# convert field from bytes to human
def convert_bytes2human_obj(dict_memory_bytes):
    dict_memory_human = {}
    for memory_key, memory_value in dict_memory_bytes.items():
        if memory_key != 'percent':
            memory_value = bytes2human(memory_value)
        dict_memory_human[memory_key] = memory_value
        # print('%-10s : %7s' % (name.capitalize(), value))
    return dict_memory_human
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# convert value from bytes to human
# https://stackoverflow.com/questions/56243676/python-human-readable-to-byte-conversion
def convert_bytes2human_value(byte, size_type='short'):

    size_name_long = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    size_name_short = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")

    size_value, size_unit = None, None
    if byte == 0:
        size_value, size_unit = 0, 'B'
    else:
        byte = int(byte)
        index = int(math.floor(math.log(byte, 1024)))
        power = math.pow(1024, index)
        size_value = round(byte / power, 2)

        if size_unit in size_name_long:
            size_name = deepcopy(size_name_long)
        elif size_unit in size_name_short:
            size_name = deepcopy(size_name_short)
        else:
            log_stream.error(' ===> Variable "size_unit" is not supported in long and short names')
            raise NotImplemented('Case not implemented yet')

        if size_type == 'long':
            size_unit = size_name_long[index]
        elif size_type == 'short':
            size_unit = size_name_short[index]
        else:
            log_stream.error(' ===> Variable "size_type" set to "' + size_type + '" is not supported')
            raise NotImplemented('Case not implemented yet')

    return size_value, size_unit
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# convert field from human to bytes
# https://stackoverflow.com/questions/56243676/python-human-readable-to-byte-conversion
def convert_human2bytes_value(size_obj):

    size_name_long = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    size_name_short = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")

    if isinstance(size_obj, str):
        if check_size_whitespaces(size_obj):
            size_obj = size_obj.split()             # divide '1 GB' into ['1', 'GB']
        else:
            size_obj = split_size_parts(size_obj)   # divide '1GB' into ['1', 'GB']
    elif isinstance(size_obj, list):
        if size_obj.__len__() == 2:
            pass
        else:
            log_stream.error(' ===> Object "size" list is not in supported format')
            raise NotImplemented('Case not implemented yet')
    else:
        log_stream.error(' ===> Object "size" can be defined by string or list')
        raise NotImplemented('Case not implemented yet')

    size_value, size_unit = float(size_obj[0]), size_obj[1]
    if size_value == 0:
        byte = 0
    else:

        if size_unit in size_name_long:
            size_name = deepcopy(size_name_long)
        elif size_unit in size_name_short:
            size_name = deepcopy(size_name_short)
        else:
            log_stream.error(' ===> Variable "size_unit" is not supported in long and short names')
            raise NotImplemented('Case not implemented yet')

        idx = size_name.index(size_unit)        # index in list of sizes determines power to raise it to
        factor = 1024 ** idx                    # ** is the "exponent" operator - you can use it instead of math.pow()
        byte = size_value * factor

    return byte
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# method to convert string to value
def convert_string2num_value(size_obj):
    if isinstance(size_obj, str):
        if check_size_whitespaces(size_obj):
            size_obj = size_obj.split()
        else:
            size_obj = split_size_parts(size_obj)
    size_value, size_unit = float(size_obj[0]), size_obj[1]
    return size_value
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# method to convert human value to desired units
def convert_human_unit(size_obj_start, size_unit='G', size_format='{:0.3}', size_separator=''):

    size_name_long = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    size_name_short = ("B", "K", "M", "G", "T", "P", "E", "Z", "Y")

    size_byte = convert_human2bytes_value(size_obj_start)

    if size_unit in size_name_long:
        size_name = deepcopy(size_name_long)
    elif size_unit in size_name_short:
        size_name = deepcopy(size_name_short)
    else:
        log_stream.error(' ===> Variable "size_unit" is not supported in long and short names')
        raise NotImplemented('Case not implemented yet')

    idx = size_name.index(size_unit)  # index in list of sizes determines power to raise it to
    factor = 1024 ** idx

    size_value = size_byte / factor
    size_string = size_format.format(size_value)
    size_obj_end = size_separator.join([size_string, size_unit])

    return size_obj_end
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# convert memory from obj to dict
def convert_obj2dict(obj_nt):
    obj_dict = {}
    for obj_name in obj_nt._fields:
        obj_value = getattr(obj_nt, obj_name)
        obj_dict[obj_name] = obj_value
    return obj_dict
# -------------------------------------------------------------------------------------
