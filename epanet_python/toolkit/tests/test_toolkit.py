

#
#  test_toolkit.py
#
#  Created:    October 19, 2018
#  Author:     Michael E. Tryby
#              US EPA - ORD/NRMRL
#

import os

import pytest
import os.path as osp

import epanet.toolkit.toolkit as en


DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
INPUT_FILE_NET_1 = os.path.join(DATA_PATH, 'Net1.inp')
REPORT_FILE_TEST = os.path.join(DATA_PATH, 'test.rpt')
OUTPUT_FILE_TEST = os.path.join(DATA_PATH, 'test.out')


def test_createdelete():

    _handle = en.proj_create()
    assert(_handle != None)

    _handle = en.proj_delete(_handle)
    assert(_handle == None)


def test_run():
    _handle = en.proj_create()

    en.proj_run(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
    assert osp.isfile(REPORT_FILE_TEST) == True
    assert osp.isfile(OUTPUT_FILE_TEST) == True

    en.proj_delete(_handle)


def test_openclose():
    _handle = en.proj_create()
    en.proj_open(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)

    en.proj_close(_handle)
    en.proj_delete(_handle)


def test_savereopen():
    input_file_reopen = os.path.join(DATA_PATH, 'test_reopen.inp')

    _handle = en.proj_create()

    en.proj_open(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
    en.proj_savefile(_handle, input_file_reopen)
    en.proj_close(_handle)

    _handle = en.proj_delete(_handle)

    _handle = en.proj_create()

    en.proj_open(_handle, input_file_reopen, REPORT_FILE_TEST, OUTPUT_FILE_TEST)
    en.proj_close(_handle)

    _handle = en.proj_delete(_handle)


@pytest.fixture()
def handle(request):
    _handle = en.proj_create()
    en.proj_open(_handle, INPUT_FILE_NET_1, REPORT_FILE_TEST, OUTPUT_FILE_TEST)

    def close():
        en.proj_close(_handle)
        en.proj_delete(_handle)

    request.addfinalizer(close)
    return _handle


def test_hyd_step(handle):
     en.hydr_open(handle)

     en.hydr_init(handle, en.SaveOption.NOSAVE)

     while True:
         time = en.hydr_run(handle)

         step = en.hydr_next(handle)

         if not step > 0.:
             break

     en.hydr_close(handle)


def test_qual_step(handle):
    en.hydr_solve(handle)

    en.qual_open(handle)

    en.qual_init(handle, en.SaveOption.NOSAVE)

    while True:
        time = en.qual_run(handle)

        step = en.qual_next(handle)

        if not step > 0.:
            break

    en.qual_close(handle)


def test_report(handle):

    nlinks = en.proj_getcount(handle, en.CountType.LINKS)
    assert nlinks == 13

    en.hydr_solve(handle)
    en.qual_solve(handle)

    en.rprt_set(handle, 'NODES ALL')
    en.rprt_writeresults(handle)
    assert osp.isfile(REPORT_FILE_TEST) == True


def test_analysis(handle):
    test_value = [];

    for code in en.Option:
        test_value.append(en.anlys_getoption(handle, code))

    funits = en.anlys_getflowunits(handle)
    assert en.FlowUnits(funits) == en.FlowUnits.GPM

    test_value.clear()
    ref_value = [86400, 3600, 300, 7200, 0, 3600, 0, 360, 0, 0, 0, 0, 0, 0, 3600, 0]
    for code in en.TimeParameter:
        test_value.append(en.anlys_gettimeparam(handle, code))
    assert test_value == ref_value

    qualinfo = en.anlys_getqualinfo(handle)
    assert qualinfo == [1, 'Chlorine' ,'mg/L', 0]



def test_node(handle):
    index = en.node_getindex(handle, '10')
    assert index == 1

    id = en.node_getid(handle, index)
    assert id == '10'

    type = en.node_gettype(handle, index)
    assert en.NodeType(type) == en.NodeType.JUNCTION

    coord = en.node_getcoord(handle, index)
    assert coord == [20.0, 70.0]


def test_demand(handle):
    index = en.node_getindex(handle, '22')
    count = en.dmnd_getcount(handle, index)
    assert count == 1

    model = en.dmnd_getmodel(handle)
    assert model == [0, 0.0, 0.0, 0.5]

    base = en.dmnd_getbase(handle, index, count)
    assert base == 200.0

    ptrn = en.dmnd_getpattern(handle, index, count)
    assert ptrn == 1

    en.dmnd_setname(handle, index, count, 'default')
    name = en.dmnd_getname(handle, index, count)
    assert name == 'default'


def test_link(handle):
    index = en.link_getindex(handle, '10')
    assert index == 1

    id = en.link_getid(handle, index)
    assert id == '10'

    type = en.link_gettype(handle, index)
    assert en.LinkType(type) == en.LinkType.PIPE

    nodes = en.link_getnodes(handle, index)
    assert nodes == [1, 2]

    test_value = []
    ref_value = [18.0, 10530.0, 100.0, 0.0, 1.0, 100.0, -0.5, -1.0, 0.0, 0.0, 0.0, 0.0]
    for code in range(en.LinkProperty.SETTING.value):
        test_value.append(en.link_getvalue(handle, index, en.LinkProperty(code)))
    assert test_value == pytest.approx(ref_value)


def test_pump(handle):
    index = en.link_getindex(handle, "9")
    assert index == 13

    type = en.link_gettype(handle, index)
    assert en.LinkType(type) == en.LinkType.PUMP

    type = en.pump_gettype(handle, index)
    assert en.PumpType(type) == en.PumpType.POWER_FUNC


def test_pattern(handle):
    index = en.ptrn_getindex(handle, "1")
    assert index == 1

    length = en.ptrn_getlength(handle, index)
    assert length == 12

    test_value = []
    ref_value = [1.0, 1.2, 1.4, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.6, 0.8]
    for i in range(1, length+1):
        test_value.append(en.ptrn_getvalue(handle, index, i))
    assert test_value == pytest.approx(ref_value)

    value = en.ptrn_getavgvalue(handle, index)
    assert value == pytest.approx(1.0)


def test_curve(handle):
    index = en.curv_getindex(handle, "1")
    assert index == 1

    length = en.curv_getlength(handle, index)
    assert length == 1

    type = en.curv_gettype(handle, index)
    assert en.CurveType(type) == en.CurveType.PUMP_CURVE

    value = en.curv_getvalue(handle, index, length)
    assert value == [1500.0, 250.0]


def test_simplecontrol(handle):

    value = en.scntl_get(handle, 1)
    assert value == [0, 13, 1.0, 11, 110.0]

    value.clear()
    value = en.scntl_get(handle, 2)
    assert value == [1, 13, 0.0, 11, 140.0]


WARNING_TEST_INP = os.path.join(DATA_PATH, 'test_warnings.inp')
WARNING_TEST_RPT = os.path.join(DATA_PATH, 'test_warnings.rpt')
WARNING_TEST_OUT = os.path.join(DATA_PATH, 'test_warnings.out')

@pytest.fixture()
def handle_warn(request):
    _handle = en.proj_create()
    en.proj_open(_handle, WARNING_TEST_INP, WARNING_TEST_RPT, WARNING_TEST_OUT)

    def close():
        en.proj_close(_handle)
        en.proj_delete(_handle)

    request.addfinalizer(close)
    return _handle


import warnings
warnings.simplefilter("default")

def test_hyd_warning(handle_warn):
    with pytest.warns(Warning):
        en.hydr_open(handle_warn)
        en.hydr_init(handle_warn, en.SaveOption.NOSAVE)

        while True:
            time = en.hydr_run(handle_warn)

            step = en.hydr_next(handle_warn)

            if not step > 0.:
                break

        en.hydr_close(handle_warn)


def test_exception(handle_warn):
    with pytest.raises(Exception):
        #en.hydr_open(handle_warn)
        en.hydr_init(handle_warn, en.SaveOption.NOSAVE)

        while True:
            time = en.hydr_run(handle_warn)

            step = en.hydr_next(handle_warn)

            if not step > 0.:
                break

        en.hydr_close(handle_warn)
