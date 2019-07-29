# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 09:22:17 2019

@author: gbessardon
"""
import os
def readconf(fn):
    text = open(fn,'r')
    nodata=255
    for t in text:
        if not t.startswith('#'):
            a=t.split('=')
            if len(a)>1:
                if 'Sand_reference' in a[0]:
                    Sand_ref=a[1].split('\n')[0]
                    if Sand_ref.startswith('~'):
                         Sand_ref=Sand_ref.replace('~',os.path.expanduser('~'))
                    if Sand_ref.startswith('$HOME'):
                         Sand_ref=Sand_ref.replace('$HOME',os.path.expanduser('~'))
                if 'Clay_reference' in a[0]:
                    Clay_ref=a[1].split('\n')[0]
                    if Clay_ref.startswith('~'):
                         Clay_ref=Clay_ref.replace('~',os.path.expanduser('~'))
                    if Clay_ref.startswith('$HOME'):
                         Clay_ref=Clay_ref.replace('$HOME',os.path.expanduser('~'))
                if 'Sand_national' in a[0]:
                    Sand_nat=a[1].split('\n')[0]
                    if Sand_nat.startswith('~'):
                         Sand_nat=Sand_nat.replace('~',os.path.expanduser('~'))
                    if Sand_nat.startswith('$HOME'):
                         Sand_nat=Sand_nat.replace('$HOME',os.path.expanduser('~'))
                if 'Clay_national' in a[0]:
                    Clay_nat=a[1].split('\n')[0]
                    if Clay_nat.startswith('~'):
                         Clay_nat=Clay_nat.replace('~',os.path.expanduser('~'))
                    if Clay_nat.startswith('$HOME'):
                         Clay_nat=Clay_nat.replace('$HOME',os.path.expanduser('~'))
                if 'nodata_reference' in a[0]:
                    noref=float(a[1])               
                if 'nodata_national' in a[0]:
                    nonat=float(a[1])
                if 'Outsand' in a[0]:
                    fnsand=a[1].split('\n')[0]
                    if fnsand.startswith('~'):
                         fnsand=fnsand.replace('~',os.path.expanduser('~'))
                    if fnsand.startswith('$HOME'):
                         fnsand=fnsand.replace('$HOME',os.path.expanduser('~'))
                if 'Outclay' in a[0]:
                    fnclay=a[1].split('\n')[0]
                    if fnclay.startswith('~'):
                         fnclay=fnclay.replace('~',os.path.expanduser('~'))
                    if fnclay.startswith('$HOME'):
                         fnclay=fnclay.replace('$HOME',os.path.expanduser('~'))

    return(Sand_ref,Clay_ref,Sand_nat,Clay_nat,noref,nonat,fnsand,fnclay)
