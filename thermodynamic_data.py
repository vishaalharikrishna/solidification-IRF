#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 18:11:14 2022

@author: hariharan
"""

 
from tc_python import *
import json
import sys


def get_liquidus(calc_obj):
    l=(calc_obj
     .remove_condition(ThermodynamicQuantity.temperature())
     .set_phase_to_fixed("LIQUID", 1.0)
     .calculate()
     .get_value_of(ThermodynamicQuantity.temperature()))
    calc_obj.set_phase_to_entered("LIQUID",1.0).set_condition("T",1000).calculate()
    return l

def get_solidus(calc_obj):
    l=(calc_obj
     .remove_condition(ThermodynamicQuantity.temperature())
     .set_phase_to_fixed("LIQUID", 0.0)
     .calculate()
     .get_value_of(ThermodynamicQuantity.temperature()))
    calc_obj.set_phase_to_entered("LIQUID",1.0).set_condition("T",1000).calculate()
    return l


def set_multiple_conditions(solutes,conc,comp_choice):
    if comp_choice=='mass':
        c="W("
    else:
        c="X("
    temp=["s-c"]
    for i in range(len(solutes)):
        temp.append(c+solutes[i]+")="+str(conc[i]))
    return (' '.join(temp))

def get_slopes(calc_obj,solutes,conc,toriginal,comp_choice):
    mset=[]
    if comp_choice=='mass':
        c="W("
    else:
        c="X("
    for i in range(len(solutes)):
        c_original=conc[i]
        dummy_obj1=calc_obj.set_condition(c+solutes[i]+")", c_original+0.0001)
        t1=get_liquidus(dummy_obj1)
        dummy_obj2=calc_obj.set_condition(c+solutes[i]+")", c_original-0.0001)
        t2=get_liquidus(dummy_obj2)
        mset.append((t1-t2)/(0.0002))
    return mset

    

#Read json file for reading parameters

with open(sys.argv[1], 'r') as myfile:
    data=myfile.read()

# parse file
obj = json.loads(data)

database=obj['Database']
solvent=obj['Base_element']
solutes=obj['Solutes']
conc=obj['alloy_composition']
solid_phase=obj['Solid_phase']
comp_choice=obj["Composition_unit"]
fname=obj["File_name"]


cond= set_multiple_conditions(solutes,conc,comp_choice)

if comp_choice=='mass':
    c="W("
else:
    c="X("

with TCPython() as start:
    # create and configure a single equilibrium calculation
    calculation_setup= (
        start
            .set_cache_folder(os.path.basename(fname[:-4]) + "_cache")
            .select_database_and_elements(database, solutes+[solvent])
            .without_default_phases()
            .select_phase("LIQUID")
            .select_phase(solid_phase)
            .get_system()
            .with_single_equilibrium_calculation()
            .set_condition("T", 1000)
            .run_poly_command(cond)
            .disable_global_minimization()
    )
    dummy=calculation_setup.calculate()
    tl = get_liquidus(calculation_setup)
    obj["Liquidus_temperature"]=tl
    print("Liquidus",tl)
    dummy=calculation_setup.set_condition("T", tl-10.0).calculate()
    ts= get_solidus(calculation_setup)
    obj["Solidus_temperature"]=ts
    print("Solidus",ts)
    m= get_slopes(calculation_setup,solutes,conc,tl,comp_choice)
    obj["Liquidus_slopes"]=m
    print("Slopes",m)
    pobj=calculation_setup.set_condition("T", tl).calculate()
    k=[pobj.get_value_of(c+solid_phase+","+solutes[i]+")")/conc[i] for i in range(len(solutes))]
    obj["partition_coeff"]=k
    print("partition_coeff",k)

with open(fname, 'w') as fp:
    json.dump(obj, fp)
