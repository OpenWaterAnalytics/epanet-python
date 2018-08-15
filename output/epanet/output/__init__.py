
from enum import Enum, auto

import output as oapi 

class OutputMetadata():
        
    class _Units(Enum):
        FLOW_RATE = auto()
        HYD_HEAD  = auto()
        PRESSURE  = auto()
        CONCEN    = auto()
        VELOCITY  = auto()
        HEADLOSS  = auto()
        RX_RATE   = auto()
        UNITLESS  = auto()
        NONE      = auto() 
    
    _unit_labels = {
        _Units.HYD_HEAD:       ["ft", "m"],
        _Units.VELOCITY:       ["ft/sec", "m/sec"],
        _Units.HEADLOSS:       ["ft/1000ft", "m/Km"], 
        _Units.RX_RATE:        ["mass/hr", "mass/hr"],
        _Units.UNITLESS:       ["unitless", "unitless"],
        _Units.NONE:           ["", ""],
    
        oapi.FlowUnits.CFS:   ["cu ft/s", ""],
        oapi.FlowUnits.GPM:   ["gal/min", ""],
        oapi.FlowUnits.MGD:   ["M gal/day", ""],
        oapi.FlowUnits.IMGD:  ["M Imp gal/day", ""],
        oapi.FlowUnits.AFD:   ["ac ft/day", ""],
        oapi.FlowUnits.LPS:   ["", "L/sec"],
        oapi.FlowUnits.LPM:   ["", "L/min"],
        oapi.FlowUnits.MLD:   ["", "M L/day"],
        oapi.FlowUnits.CMH:   ["", "cu m/hr"],
        oapi.FlowUnits.CMD:   ["", "cu m/day"],
    
        oapi.PressUnits.PSI:  ["psi", ""], 
        oapi.PressUnits.MTR:  ["", "meters"],
        oapi.PressUnits.KPA:  ["", "kPa"],
    
        oapi.ConcUnits.NONE:  [""    , ""], 
        oapi.ConcUnits.MGL:   ["mg/L", "mg/L"],
        oapi.ConcUnits.UGL:   ["ug/L", "ug/L"],
        oapi.ConcUnits.HOURS: ["hrs" , "hrs"], 
        oapi.ConcUnits.PRCNT: ["%"   , "%"]}
                
    def __init__(self, unit_system, flow_unit, press_unit, conc_unit):
        
        self._system = unit_system
        self._flow = flow_unit
        self._press = press_unit
        self._chem = conc_unit
         
        self._metadata= {        
            oapi.NodeAttribute.DEMAND:      ("Demand",          type(self)._unit_labels[self._flow]),
            oapi.NodeAttribute.HEAD:        ("Head",            type(self)._unit_labels[type(self)._Units.HYD_HEAD]),
            oapi.NodeAttribute.PRESSURE:    ("Pressure",        type(self)._unit_labels[self._press]),
            oapi.NodeAttribute.QUALITY:     ("Quality",         type(self)._unit_labels[self._chem]),
         
            oapi.LinkAttribute.FLOW:        ("Flow",            type(self)._unit_labels[self._flow]),
            oapi.LinkAttribute.VELOCITY:    ("Velocity",        type(self)._unit_labels[type(self)._Units.VELOCITY]),
            oapi.LinkAttribute.HEADLOSS:    ("Unit Headloss",   type(self)._unit_labels[type(self)._Units.HEADLOSS]),
            oapi.LinkAttribute.AVG_QUALITY: ("Quality",         type(self)._unit_labels[self._chem]),
            oapi.LinkAttribute.STATUS:      ("Status",          type(self)._unit_labels[type(self)._Units.NONE]),
            oapi.LinkAttribute.SETTING:     ("Setting",         type(self)._unit_labels[type(self)._Units.NONE]),
            oapi.LinkAttribute.RX_RATE:     ("Reaction Rate",   type(self)._unit_labels[type(self)._Units.RX_RATE]),
            oapi.LinkAttribute.FRCTN_FCTR:  ("Friction Factor", type(self)._unit_labels[type(self)._Units.UNITLESS])}        

        
    def get_attribute_metadata(self, attribute):
        return (self._metadata[attribute][0], self._metadata[attribute][1][self._system.value])


class OutputWrapper():
    
    def __init__(self, filename):
        self.filepath = filename
        self.handle = None

        
    def __enter__(self):
        pass
    
    def __exit__(self):    
        pass



if __name__ == "__main__":
    
    attr = oapi.NodeAttribute.QUALITY
    
    om = OutputMetadata()
    
    print(om.get_attribute_metadata(attr))
    

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



# Output Metadata
#
# Node Attributes
#   DEMAND            Demand             FLOW_ 
#   HEAD              Head               LENGTH
#   PRESSURE          Pressure           PRESSURE
#   QUALITY           Quality            CONC_

# Link Attributes
#   FLOW              Flow               FLOW_
#   VELOCITY          Velocity           VELOCITY
#   HEADLOSS          Unit Headloss      HEADLOSS
#   AVG_QUALITY       Quality            CONC_
#   STATUS            Status             NONE         
#   SETTING           Setting            NONE
#   RX_RATE           Reaction Rate      RX_RATE
#   FRCTN_FCTR        Friction Factor    UNITLESS
