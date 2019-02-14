# @title Testing Dynamic Arrays v1
# @author Kenny Peluso - kennyp.herokuapp.com
# @notice Influenced heavily by Uniswap Vyper contracts
# @notice Use at your own risk

def test_sda_uint(sda, w3, assert_fail): # 3 assertions
    # test simple dynamic array for uint
    sda.append(1)
    sda.append(1)
    sda.append(2)
    assert sda.length() == 3
    assert sda.get(1) == 1
    assert sda.get(2) == 2

def test_da_uint(da, da_data, automated_testing): 
    automated_testing(da, da_data)

def test_da_str(da_str, da_str_data, automated_testing): # 17 assertions
    automated_testing(da_str, da_str_data)
