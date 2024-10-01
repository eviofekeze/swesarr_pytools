import datetime

import pytest
from swesarr_pytools.data_tools import ReadSwesarr


@pytest.fixture
def read_swesarr_v1():
    return ReadSwesarr(flight_path="/opt/project/resources/swesarr_data/GRMCT1_13801_19005_010_191106_225_XX_01",
                       version="v1")

@pytest.fixture
def read_swesarr_v3():
    return ReadSwesarr(flight_path="/opt/project/resources/swesarr_data_v3/19004_011",
                       version="v3")


def test_get_data_files(read_swesarr_v1 , read_swesarr_v3):
    expected_list_v1 = ['GRMCT1_13801_19005_010_191106_13225VH_XX_01.tif',
                        'GRMCT1_13801_19005_010_191106_17225VH_XX_01.tif',
                        'GRMCT1_13801_19005_010_191106_09225VV_XX_01.tif',
                        'GRMCT1_13801_19005_010_191106_17225VV_XX_01.tif',
                        'GRMCT1_13801_19005_010_191106_13225VV_XX_01.tif',
                        'GRMCT1_13801_19005_010_191106_09225VH_XX_01.tif']

    expected_list_v3 = ['SWESARR_northdescend_BasicOps_SWProgXcvr_Box2_2019Nov05-15.31.58.297411_2019Nov05-15.33.36'
                        '.745263_XVV_MC_neg.tif',
                        'SWESARR_northdescend_BasicOps_SWProgXcvr_Box2_2019Nov05-15.31.58.297411_2019Nov05-15.33.36'
                        '.745263_KlVV_MC_neg.tif',
                        'SWESARR_northdescend_BasicOps_SWProgXcvr_Box2_2019Nov05-15.31.58.297411_2019Nov05-15.33.36'
                        '.745263_XVVINC_MC_neg.mli.inc_deg.tif',
                        'SWESARR_northdescend_BasicOps_SWProgXcvr_Box2_2019Nov05-15.31.58.297411_2019Nov05-15.33.36'
                        '.745263_XVH_MC_neg.tif',
                        'SWESARR_northdescend_BasicOps_SWProgXcvr_Box2_2019Nov05-15.31.58.297411_2019Nov05-15.33.36'
                        '.745263_KhVH_MC_neg.tif',
                        'SWESARR_northdescend_BasicOps_SWProgXcvr_Box2_2019Nov05-15.31.58.297411_2019Nov05-15.33.36'
                        '.745263_KlVH_MC_neg.tif',
                        'SWESARR_northdescend_BasicOps_SWProgXcvr_Box2_2019Nov05-15.31.58.297411_2019Nov05-15.33.36'
                        '.745263_KhVV_MC_neg.tif',
                        'SWESARR_northdescend_BasicOps_SWProgXcvr_Box2_2019Nov05-15.31.58.297411_2019Nov05-15.33.36'
                        '.745263_XVVOFNA_MC_neg.mli.offnadir_deg.tif']

    assert read_swesarr_v1.get_data_files() == expected_list_v1
    assert read_swesarr_v3.get_data_files() == expected_list_v3


