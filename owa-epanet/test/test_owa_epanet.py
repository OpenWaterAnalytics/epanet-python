# -*- coding: utf-8 -*-

import os
import pytest
import epanet.toolkit as en
from test.data import example_1_path


timesteps = [3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 1954, 1646, 3600,
             3600, 3600, 3600, 3600, 3600, 3600, 3600, 3600, 2490, 1110, 3600, 0]
wq_times = [86100, 85800, 85500, 85200, 84900, 84600, 84300, 84000, 83700, 83400, 83100, 82800, 82500, 82200, 81900,
            81600, 81300, 81000, 80700, 80400, 80100, 79800, 79500, 79200, 78900, 78600, 78300, 78000, 77700, 77400,
            77100, 76800, 76500, 76200, 75900, 75600, 75300, 75000, 74700, 74400, 74100, 73800, 73500, 73200, 72900,
            72600, 72300, 72000, 71700, 71400, 71100, 70800, 70500, 70200, 69900, 69600, 69300, 69000, 68700, 68400]


def clean_dir():
    if os.path.exists('report.rpt'):
        os.remove('report.rpt')
    if os.path.exists('output.out'):
        os.remove('output.out')
    if os.path.exists('saved_inp_file.inp'):
        os.remove('saved_inp_file.inp')


def test_create_project():
    epanet_proj = en.createproject()
    assert str(type(epanet_proj)) == '<class \'SwigPyObject\'>'


def test_open():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    clean_dir()


def test_close():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.close(ph=epanet_proj)
    clean_dir()


def test_run_project():
    epanet_proj = en.createproject()
    en.runproject(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out', pviewprog=None)
    clean_dir()


def test_get_count():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    num_nodes = en.getcount(ph=epanet_proj, object=en.NODECOUNT)
    assert(num_nodes == 11)
    num_links = en.getcount(ph=epanet_proj, object=en.LINKCOUNT)
    assert(num_links == 13)
    num_tanks = en.getcount(ph=epanet_proj, object=en.TANKCOUNT)
    assert(num_tanks == 2)
    num_pat = en.getcount(ph=epanet_proj, object=en.PATCOUNT)
    assert(num_pat == 1)
    num_curv = en.getcount(ph=epanet_proj, object=en.CURVECOUNT)
    assert (num_curv == 1)
    num_contr = en.getcount(ph=epanet_proj, object=en.CONTROLCOUNT)
    assert (num_contr == 2)
    en.close(ph=epanet_proj)
    clean_dir()


def test_save_inp_file():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.saveinpfile(ph=epanet_proj, filename='saved_inp_file.inp')
    assert os.path.isfile('saved_inp_file.inp')
    clean_dir()


def test_openh():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    res = en.openH(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert not res
    clean_dir()


def test_inith():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.openH(ph=epanet_proj)
    res = en.initH(ph=epanet_proj, initFlag=0)
    en.close(ph=epanet_proj)
    assert not res
    clean_dir()


def test_runh():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.openH(ph=epanet_proj)
    en.initH(ph=epanet_proj, initFlag=0)
    res = en.runH(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert res == 0
    clean_dir()


def test_nexth():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.openH(ph=epanet_proj)
    en.initH(ph=epanet_proj, initFlag=0)
    en.runH(ph=epanet_proj)
    res = en.nextH(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert res == 3600
    clean_dir()


def test_closeh():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.openH(ph=epanet_proj)
    en.initH(ph=epanet_proj, initFlag=0)
    res = en.closeH(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert not res
    clean_dir()


def test_inith_runh_nexth():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.openH(ph=epanet_proj)
    en.initH(ph=epanet_proj, initFlag=0)
    tlist = []
    while True:
        en.runH(ph=epanet_proj)
        t = en.nextH(ph=epanet_proj)
        tlist.append(t)
        if t <= 0:
            break
    en.closeH(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert tlist == timesteps
    clean_dir()


def test_solveh_solveq():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.solveH(ph=epanet_proj)
    en.solveQ(ph=epanet_proj)
    en.report(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert os.path.isfile('output.out')
    clean_dir()


def test_initq_runq_nextq():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.solveH(ph=epanet_proj)
    en.openQ(ph=epanet_proj)
    en.initQ(ph=epanet_proj, saveFlag=1)
    tlist = []
    while True:
        en.runQ(ph=epanet_proj)
        t = en.nextQ(ph=epanet_proj)
        tlist.append(t)
        if t <= 0:
            break
    en.closeQ(ph=epanet_proj)
    en.report(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert tlist == timesteps
    clean_dir()


def test_stepq():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.solveH(ph=epanet_proj)
    en.openQ(ph=epanet_proj)
    en.initQ(ph=epanet_proj, saveFlag=1)
    tlist = []
    while True:
        en.runQ(ph=epanet_proj)
        tleft = en.stepQ(ph=epanet_proj)
        tlist.append(tleft)
        if tleft <= 0:
            break
    en.closeQ(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert tlist[:60] == wq_times
    clean_dir()


def test_getqualtype():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    qual_type = en.getqualtype(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert qual_type == [1, 0]
    clean_dir()


def test_set_qualtype():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.setqualtype(ph=epanet_proj, qualType=2, chemName='Age', chemUnits='seconds', traceNode=None)
    qual_type = en.getqualtype(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert qual_type == [2, 0]
    clean_dir()


def test_water_age_sim():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.setqualtype(ph=epanet_proj, qualType=2, chemName='Age', chemUnits='hours', traceNode=None)
    en.solveH(ph=epanet_proj)
    en.openQ(ph=epanet_proj)
    en.initQ(ph=epanet_proj, saveFlag=1)
    num_nodes = en.getcount(ph=epanet_proj, object=en.NODECOUNT)
    age_list = []
    while True:
        node_age_list = []
        en.runQ(ph=epanet_proj)
        t = en.nextQ(ph=epanet_proj)
        for i in range(1, num_nodes*1):
            node_qual = en.getnodevalue(ph=epanet_proj, index=i, property=en.QUALITY)
            node_age_list.append(node_qual)
        age_list.append(node_age_list)
        if t <= 0:
            break
    en.closeQ(ph=epanet_proj)
    en.closeH(ph=epanet_proj)
    en.close(ph=epanet_proj)
    assert age_list[26] == [1.0, 2.2141675704376946, 12.939125434025273, 24.44152992466322, 13.174235412569542,
                            24.441519659540887, 15.679376648181817, 21.97064181429266, 19.048343501261524, 1.0]
    clean_dir()


# this test is failing due to a seg fault
def _test_add_node():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.addnode(ph=epanet_proj, id='33', nodeType=en.JUNCTION)
    num_nodes = en.getcount(ph=epanet_proj, object=en.NODECOUNT)
    assert num_nodes == 12
    clean_dir()


def test_getnodeindex():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    node_ids = ['10', '11', '12', '13', '21', '22', '23', '31', '32', '9', '2']
    node_idx = []
    for node_id in node_ids:
        node_idx.append(en.getnodeindex(ph=epanet_proj, id=node_id))
    assert node_idx == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    clean_dir()


def test_getnodeid():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    node_idx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    node_id = []
    for nidx in node_idx:
        node_id.append(en.getnodeid(ph=epanet_proj, index=nidx))
    assert node_id == ['10', '11', '12', '13', '21', '22', '23', '31', '32', '9', '2']
    clean_dir()


def test_add_link():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    en.addlink(ph=epanet_proj, id='L123', linkType=en.PIPE, fromNode='10', toNode='12')
    num_links = en.getcount(ph=epanet_proj, object=en.LINKCOUNT)
    assert num_links == 14
    clean_dir()


def test_setnodevalue():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    num_nodes = en.getcount(ph=epanet_proj, object=en.NODECOUNT)
    elev_list = []
    demand_list = []
    pattern_list=[]
    emitter_list = []
    initqual_list = []
    tank_level_list = []
    for node_ind in range(1, num_nodes+1):
        # elevation
        elev = en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.ELEVATION)
        en.setnodevalue(ph=epanet_proj, index=node_ind, property=en.ELEVATION, value=elev + 1)
        elev_list.append(en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.ELEVATION))
        # base demand
        demand = en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.BASEDEMAND)
        en.setnodevalue(ph=epanet_proj, index=node_ind, property=en.BASEDEMAND, value=demand + 1)
        demand_list.append(en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.BASEDEMAND))
        # pattern
        en.setnodevalue(ph=epanet_proj, index=node_ind, property=en.PATTERN, value=0)
        pattern_list.append(en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.PATTERN))
        # emitter
        en.setnodevalue(ph=epanet_proj, index=node_ind, property=en.EMITTER, value=0.01)
        emitter_list.append(en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.EMITTER))
        # initqual
        initqual = en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.INITQUAL)
        en.setnodevalue(ph=epanet_proj, index=node_ind, property=en.INITQUAL, value=initqual + 0.1)
        initqual_list.append(en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.INITQUAL))
        # tanklevel
        if en.getnodetype(ph=epanet_proj, index=node_ind) == en.TANK:
            tank_level = en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.TANKLEVEL)
            en.setnodevalue(ph=epanet_proj, index=node_ind, property=en.TANKLEVEL, value=tank_level + 1)
            tank_level_list.append(en.getnodevalue(ph=epanet_proj, index=node_ind, property=en.TANKLEVEL))
    assert elev_list == [711.0, 711.0, 701.0, 696.0, 701.0, 696.0, 691.0, 701.0, 711.0, 801.0, 851.0]
    assert demand_list == [1.0, 151.0, 151.0, 101.0, 151.0, 201.0, 151.0, 101.0, 101.0, 0.0, 0.0]
    assert pattern_list == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert emitter_list == [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.0, 0.0]
    assert initqual_list == [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1]
    assert tank_level_list ==[121.0]
    clean_dir()

def test_setcurve():
    def make_array(values):
        dbl_arr = en.doubleArray(len(values))
        for i in range(len(values)):
            dbl_arr[i] = values[i]
        return dbl_arr

    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    ok = en.addcurve(ph=epanet_proj, id="my_curve")
    curve_index = en.getcurveindex(ph=epanet_proj, id="my_curve")
    xvalues = make_array([1,2,3,4,5])
    yvalues = make_array([1,2,3,4,5])
    en.setcurve(ph=epanet_proj, index=curve_index, xValues=xvalues, yValues=yvalues, nPoints=5)
    count = en.getcurvelen(ph=epanet_proj, index=curve_index)
    assert count == 5

def test_coords():
    epanet_proj = en.createproject()
    en.open(ph=epanet_proj, inpFile=example_1_path, rptFile='report.rpt', outFile='output.out')
    coords = en.getcoord(epanet_proj,1)
    en.setcoord(epanet_proj,1,3,4)
    coords = en.getcoord(epanet_proj,1)
    assert coords[0] == pytest.approx(3)
    assert coords[1] == pytest.approx(4)
