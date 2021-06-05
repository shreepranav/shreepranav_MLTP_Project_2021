# This module contains functions that will test each of the three functions bryant, dpllt and dnf-eg
from equality_logic_algorithms.bryant import bryant
from equality_logic_algorithms.dpllt import dpllt
from equality_logic_algorithms.dnf_eg import dnf_eg

from test_cases import *

# Testing Bryant: Ten test cases of the form test_formula*_bryant()
def test_formula1_bryant():
    assert bryant(formula1) == z3.unsat

def test_formula2_bryant():
    assert bryant(formula2) == z3.sat
    
def test_formula3_bryant():
    assert bryant(formula3) == z3.sat
    
def test_formula4_bryant():
    assert bryant(formula4) == z3.sat

def test_formula5_bryant():
    assert bryant(formula5) == z3.sat
    
def test_formula6_bryant():
    assert bryant(formula6) == z3.sat

def test_formula7_bryant():
    assert bryant(formula7) == z3.sat
    
def test_formula8_bryant():
    assert bryant(formula8) == z3.unsat
    
def test_formula9_bryant():
    assert bryant(formula9) == z3.unsat

def test_formula10_bryant():
    assert bryant(formula10) == z3.sat

def test_formula11_bryant():
    assert bryant(formula11) == z3.unsat

def test_formula12_bryant():
    assert bryant(formula12) == z3.sat

# Testing DPLL(T): Ten test cases of the form test_formula*_dpllt()
def test_formula1_dpllt():
    assert dpllt(formula1) == z3.unsat
    
def test_formula2_dpllt():
    assert dpllt(formula2) == z3.sat
    
def test_formula3_dpllt():
    assert dpllt(formula3) == z3.sat
    
def test_formula4_dpllt():
    assert dpllt(formula4) == z3.sat

def test_formula5_dpllt():
    assert dpllt(formula5) == z3.sat

def test_formula6_dpllt():
    assert dpllt(formula6) == z3.sat
    
def test_formula7_dpllt():
    assert dpllt(formula7) == z3.sat
    
def test_formula8_dpllt():
    assert dpllt(formula8) == z3.unsat

def test_formula9_dpllt():
    assert dpllt(formula9) == z3.unsat
    
def test_formula10_dpllt():
    assert dpllt(formula10) == z3.sat
    
def test_formula11_dpllt():
    assert dpllt(formula11) == z3.unsat

def test_formula12_dpllt():
    assert dpllt(formula12) == z3.sat
    
# Testing DNF+Equality Graph: Ten test cases of the form test_formula*_dnf_eg()
def test_formula1_dnf_eg():
    assert dnf_eg(formula1) == z3.unsat
    
def test_formula2_dnf_eg():
    assert dnf_eg(formula2) == z3.sat
    
def test_formula3_dnf_eg():
    assert dnf_eg(formula3) == z3.sat

def test_formula4_dnf_eg():
    assert dnf_eg(formula4) == z3.sat    
    
def test_formula5_dnf_eg():
    assert dnf_eg(formula5) == z3.sat
    
def test_formula6_dnf_eg():
    assert dnf_eg(formula6) == z3.sat
    
def test_formula7_dnf_eg():
    assert dnf_eg(formula7) == z3.sat
    
def test_formula8_dnf_eg():
    assert dnf_eg(formula8) == z3.unsat
    
def test_formula9_dnf_eg():
    assert dnf_eg(formula9) == z3.unsat
    
def test_formula10_dnf_eg():
    assert dnf_eg(formula10) == z3.sat

def test_formula11_dnf_eg():
    assert dnf_eg(formula11) == z3.unsat

def test_formula12_dnf_eg():
    assert dnf_eg(formula12) == z3.sat