# -*- coding: utf-8 -*-

#
#  __init__.py - EPANET output package
# 
#  Date Created: August 15, 2018
#
#  Author:     Michael E. Tryby
#              US EPA - ORD/NRMRL
#

'''
A low level pythonic API for the epanet-output dll using SWIG.
'''


__author__ = "Michael Tryby"
__copyright__ = "None"
__credits__ = "Maurizio Cingi"
__license__ = "CC0 1.0 Universal"

__version__ = "0.1.1"
__date__ = "August 15, 2018"

__maintainer__ = "Michael Tryby"
__email__ = "tryby.michael@epa.gov"
__status  = "Development"


from enum import Enum, auto

from epanet.output import output as oapi 


class Units(Enum):
    FLOW_RATE = auto()
    HYD_HEAD  = auto()
    PRESSURE  = auto()
    CONCEN    = auto()
    VELOCITY  = auto()
    HEADLOSS  = auto()
    RX_RATE   = auto()
    UNITLESS  = auto()
    NONE      = auto() 

class RxUnits(Enum):
    MGH       = auto() 
    UGH       = auto()


class OutputMetadata():
    '''
    Simple attribute name and unit lookup.
    '''
    
    _unit_labels_us_ = {
        Units.HYD_HEAD:       "ft",
        Units.VELOCITY:       "ft/sec",
        Units.HEADLOSS:       "ft/1000ft", 
        Units.UNITLESS:       "unitless",
        Units.NONE:           "",
        
        RxUnits.MGH:          "mg/hr",
        RxUnits.UGH:          "ug/hr",
        
        oapi.FlowUnits.CFS:   "cu ft/s",
        oapi.FlowUnits.GPM:   "gal/min",
        oapi.FlowUnits.MGD:   "M gal/day",
        oapi.FlowUnits.IMGD:  "M Imp gal/day",
        oapi.FlowUnits.AFD:   "ac ft/day",
    
        oapi.PressUnits.PSI:  "psi", 
    
        oapi.QualUnits.NONE:  "", 
        oapi.QualUnits.MGL:   "mg/L",
        oapi.QualUnits.UGL:   "ug/L",
        oapi.QualUnits.HOURS: "hrs", 
        oapi.QualUnits.PRCNT: "%"}

    _unit_labels_si_ = {
        Units.HYD_HEAD:       "m",
        Units.VELOCITY:       "m/sec",
        Units.HEADLOSS:       "m/Km", 
        Units.UNITLESS:       "unitless",
        Units.NONE:           "",
    
        RxUnits.MGH:          "mg/hr",
        RxUnits.UGH:          "ug/hr",
        
        oapi.FlowUnits.LPS:   "L/sec",
        oapi.FlowUnits.LPM:   "L/min",
        oapi.FlowUnits.MLD:   "M L/day",
        oapi.FlowUnits.CMH:   "cu m/hr",
        oapi.FlowUnits.CMD:   "cu m/day",
    
        oapi.PressUnits.MTR:  "meters",
        oapi.PressUnits.KPA:  "kPa",
    
        oapi.QualUnits.NONE:  "", 
        oapi.QualUnits.MGL:   "mg/L",
        oapi.QualUnits.UGL:   "ug/L",
        oapi.QualUnits.HOURS: "hrs", 
        oapi.QualUnits.PRCNT: "%"}

               
    def __init__(self, output_handle):
        
        self.units = list()
        # If outputhandle not initialized use default settings
        if output_handle == None: 
            self.units = [oapi.FlowUnits.GPM.value, 
                          oapi.PressUnits.PSI.value, 
                          oapi.QualUnits.NONE.value]
        # Else quary the output api for unit settings
        else:
            for u in oapi.Units:    
                self.units.append(oapi.getunits(output_handle, u))
        
        # Convert unit settings to enums        
        self._flow = oapi.FlowUnits(self.units[0])
        self._press = oapi.PressUnits(self.units[1])
        self._qual = oapi.QualUnits(self.units[2])
        
        # Determine unit system from flow setting
        if self._flow.value <= oapi.FlowUnits.AFD.value:
            self.unit_labels = type(self)._unit_labels_us_
        else:
            self.unit_labels = type(self)._unit_labels_si_    
        
        # Determine mass units from quality settings
        if self._qual == oapi.QualUnits.MGL:
            self._rx_rate = RxUnits.MGH
        elif self._qual == oapi.QualUnits.UGL:
            self._rx_rate = RxUnits.UGH
        else:
            self._rx_rate = Units.NONE          


        self._metadata = {
            oapi.NodeAttribute.DEMAND:      ("Demand",          self.unit_labels[self._flow]),
            oapi.NodeAttribute.HEAD:        ("Head",            self.unit_labels[Units.HYD_HEAD]),
            oapi.NodeAttribute.PRESSURE:    ("Pressure",        self.unit_labels[self._press]),
            oapi.NodeAttribute.QUALITY:     ("Quality",         self.unit_labels[self._qual]),
         
            oapi.LinkAttribute.FLOW:        ("Flow",            self.unit_labels[self._flow]),
            oapi.LinkAttribute.VELOCITY:    ("Velocity",        self.unit_labels[Units.VELOCITY]),
            oapi.LinkAttribute.HEADLOSS:    ("Unit Headloss",   self.unit_labels[Units.HEADLOSS]),
            oapi.LinkAttribute.AVG_QUALITY: ("Quality",         self.unit_labels[self._qual]),
            oapi.LinkAttribute.STATUS:      ("Status",          self.unit_labels[Units.NONE]),
            oapi.LinkAttribute.SETTING:     ("Setting",         self.unit_labels[Units.NONE]),
            oapi.LinkAttribute.RX_RATE:     ("Reaction Rate",   self.unit_labels[self._rx_rate]),
            oapi.LinkAttribute.FRCTN_FCTR:  ("Friction Factor", self.unit_labels[Units.UNITLESS])
        }

        
    def get_attribute_metadata(self, attribute):
        '''
        Takes an attribute enum and returns the name and units in a tuple.
        '''
        return self._metadata[attribute]


# Units of Measurement
#
# Units                     US Customary             SI Metric
#   Concentration              mg/L                     mg/L
#                              ug/L                     ug/L
#   Demand                     flow                     flow
#   Diameter                   in                       mm
#   Efficiency                 percent                  percent
#   Elevation                  feet                     meters
#   Emitter Coefficient        flow/(psi)^1/2           flow/(meters)^1/2
#   Energy                     kilowatt-hours           kilowatt-hours
#   Flow                       CFS                      LPS
#                              GPM                      LPM
#                              MGD                      MLD
#                              IMGD                     CMH
#                              AFD                      CMD
#   Friction Factor            unitless                 unitless
#   Hydraulic Head             feet                     meters
#   Length                     feet                     meters
#   Minor Loss Coefficient     unitless                 unitless
#   Power                      horsepower               kilowatts
#   Pressure                   psi                      meters
#   Reaction Coeff (Bulk)      1/day (1st-order)        1/day
#   Reaction Coeff (Wall)      mass/L/day (0th-order)   mass/L/day
#                              ft/day (1st-order)       meters/day (1st-order)
#   Roughness Coeff            10^-3 feet (DW)          mm (DW)
#                              unitless                 unitless
#   Source Mass Injection      mass/min                 mass/min
#   Velocity                   feet/sec                 meters/sec
#   Volume                     cubic feet               cubic meters
#   Water Age                  hours                    hours
