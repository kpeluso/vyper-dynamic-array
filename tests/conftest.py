# @noticed Much is borrowed from Uniswap Vyper contracts

import os
import pytest
from pytest import raises

from web3 import Web3
from web3.contract import Contract, ImplicitContract
import eth_tester
from eth_tester import EthereumTester, PyEVMBackend

from eth_tester.exceptions import TransactionFailed
from vyper import compiler

'''
# run tests with:             pytest -v tests/
'''

setattr(eth_tester.backends.pyevm.main, 'GENESIS_GAS_LIMIT', 10**9)
setattr(eth_tester.backends.pyevm.main, 'GENESIS_DIFFICULTY', 1)

# Testing Helpers # # # # # # # # # # # # # # # # # # # # 

@pytest.fixture
def tester():
    return EthereumTester(backend=PyEVMBackend())

@pytest.fixture
def w3(tester):
    w3 = Web3(Web3.EthereumTesterProvider(tester))
    w3.eth.setGasPriceStrategy(lambda web3, params: 0)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    return w3

@pytest.fixture
def assert_fail():
    def assert_fail(func):
        with raises(Exception):
            func()
    return assert_fail

def create_contract(w3, path):
    wd = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(wd, os.pardir, path)) as f:
        source = f.read()
    bytecode = '0x' + compiler.__compile(source).hex()
    abi = compiler.mk_full_signature(source)
    return w3.eth.contract(abi=abi, bytecode=bytecode)

@pytest.fixture
def counter(w3):
    deploy = create_contract(w3, 'contracts/counter.vy')
    tx_hash = deploy.constructor().transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=deploy.abi
    )
    return ImplicitContract(contract)

@pytest.fixture
def sda(w3):
    deploy = create_contract(w3, 'contracts/Simple_DynamicArray_uint.vy')
    tx_hash = deploy.constructor().transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=deploy.abi
    )
    return ImplicitContract(contract)

@pytest.fixture
def da(w3):
    deploy = create_contract(w3, 'contracts/DynamicArray_uint.vy')
    tx_hash = deploy.constructor().transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=deploy.abi
    )
    return ImplicitContract(contract)

@pytest.fixture
def da_str(w3):
    deploy = create_contract(w3, 'contracts/DynamicArray_str.vy')
    tx_hash = deploy.constructor().transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=deploy.abi
    )
    return ImplicitContract(contract)

@pytest.fixture
def automated_testing(w3, assert_fail):
    def automated_testing(da, test_vals): # 17 assertions
        a0, a1, a2 = w3.eth.accounts[:3]
        ls1, ls2, ls3 = (0,1,2)
        v1, v2, v2b, v3, rand = test_vals
        da.reserveList(transact={'from': a0}) # ls1
        da.reserveList(transact={'from': a0}) # ls2
        da.reserveList(transact={'from': a1}) # ls3
        assert da.maxLs() == 3
        assert da.length(ls1) == 0
        assert da.length(10) == 0
        assert_fail(lambda: da.get(10, 18, transact={'from': a1}))
        assert_fail(lambda: da.append(0, 1, transact={'from': a1}))
        da.append(ls1, v1, transact={'from': a0})
        da.append(ls1, v2, transact={'from': a0})
        da.append(ls1, v3, transact={'from': a0})
        assert da.length(ls1) == 3
        assert_fail(lambda: da.set(ls1, 1, rand, transact={'from': a1}))
        da.set(ls1, 1, v2b, transact={'from': a0})
        assert da.get(ls1, 1) == v2b
        assert_fail(lambda: da.remove(ls1, 1, transact={'from': a1}))
        assert_fail(lambda: da.remove(ls2, 0, transact={'from': a0}))
        assert_fail(lambda: da.remove(ls1, 10, transact={'from': a0}))
        da.remove(ls1, 1, transact={'from': a0})
        assert da.length(ls1) == 2
        assert da.get(ls1, 1) == v3
        assert_fail(lambda: da.detach(ls1, transact={'from': a1}))
        da.detach(ls1, transact={'from': a0})
        assert da.length(ls1) == 1
        assert_fail(lambda: da.get(ls1, 1))
        assert da.get(ls1, 0) == v1
    return automated_testing

@pytest.fixture
def da_data():
    return (1, 2, 4, 3, 666)

@pytest.fixture
def da_str_data():
    return ('1', '2', '4', '3', '666')
