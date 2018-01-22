#! /usr/bin/python
import struct
from io import SEEK_END

MAGICNUMBER=     516114521
MAXFNAME=  259  #/* Max. # characters in file name         */
MAXMSG  =   79  #/* Max. # characters in message text      */
MAXID   =   31  #/* Max. # characters in ID name           */ 
INTSIZE =    4
REAL4SIZE =  4


_pressureunits= {0:"psi"
                ,1:"meters"   
                ,2:"kPa"}


_statistics=  {0: ""     #none (report time series)
              ,1: "time-averaged values"
              ,2: "minimum values"
              ,3: "maximum values"
              ,4: "ranges"}

_flowunits= {0 : "cubic feet/second"
            ,1 : "gallons/minute"
            ,2 : "million gallons/day"
            ,3 : "Imperial million gallons/day"
            ,4 : "acre-ft/day"
            ,5 : "liters/second"
            ,6 : "liters/minute"
            ,7 : "megaliters/day"
            ,8 : "cubic meters/hour"
            ,9 : "cubic meters/day"
                 }

_waterquality= { 0: ""   #none
                ,1: "chemical"
                ,2: "age"
                ,3: "source trace"
               }

_status=  {0 : "closed (max. head exceeded for pump)"
          ,1 : "temporarily closed"                              
          ,2 : "closed"                                          
          ,3 : "open"                                            
          ,4 : "active (partially open)"                         
          ,5 : "open (max. flow exceeded for pump)"              
          ,6 : "open (flow setting not met for FCV)"             
          ,7 : "open (pressure setting not met for PRV or PSV)"}

_linktype=  {0: "PipeCV"
            ,1: "Pipe"
            ,2: "Pump"   
            ,3: "PRV"    
            ,4: "PSV"    
            ,5: "PBV"    
            ,6: "FCV"    
            ,7: "TCV"    
            ,8: "GPV"}





class OutBinNode(object):
    def __init__(self, outfile, ordinal):
        self.outfile= outfile
        self.ordinal= ordinal
        self._type= "JUNCTION"
    def _read_timeserie(self, varindex):
        return self.outfile._node_timeserie(self.ordinal, varindex)
    @property
    def ID(self):
        "node ID"
        return self.outfile.nodeID(self.ordinal+1)
    @property
    def nodetype(self):
        "node type"
        return self._type
    @property
    def demand(self):
        "node Demand"
        return self._read_timeserie(varindex=0)
    @property
    def head(self):
        "node Head"
        return self._read_timeserie(varindex=1)
    @property
    def pressure(self):
        "node Pressure"
        return self._read_timeserie(varindex=2)
    @property
    def quality(self):
        "node Water Quality"
        return self._read_timeserie(varindex=3)
        
class OutBinLink(object):
    def __init__(self, outfile, ordinal):
        self.outfile= outfile
        self.ordinal= ordinal
    def _read_timeserie(self, varindex):
        return self.outfile._link_timeserie(self.ordinal,
                                            varindex)
    @property
    def ID(self):
        "link ID"
        return self.outfile.linkID(self.ordinal+1)
    @property
    def linktype(self):
        "link type"
        return self.outfile.linktype(self.ordinal+1)
    @property
    def flow(self):
        "link flow"
        return self._read_timeserie(varindex=0)
    @property
    def velocity(self):
        "link velocity"
        return self._read_timeserie(varindex=1)
    @property
    def headloss(self):
        """Headloss per 1000 Units of Length

       (total head for pumps and head loss for valves)"""
        return self._read_timeserie(varindex=2)
    @property
    def quality(self):
        "link Average Water Quality"
        return self._read_timeserie(varindex=3)
    @property
    def status(self):
        "status"
        return [_status[int(x)] for x in self._read_timeserie(varindex=4)]
    @property
    def setting(self):
        """link setting
        
        Roughness coeff. for Pipes,
        Speed for Pumps
        Setting for Valves"""
        return self._read_timeserie(varindex=5)
    @property
    def reactionrate(self):
        "link Reaction Rate"
        return self._read_timeserie(varindex=6)
    @property
    def friction(self):
        "link Friction Factor"
        return self._read_timeserie(varindex=7)


class EpanetOutBin(object):
    """Class wrapper for Epanet binary output file
    
    example code:
    >>> import EpanetOutBin
    >>> with EpanetOutBin("Net1.bin") as a:
    ...    print a.nodes.keys()
    ...    print a.nodes['10'].demand
    ...    print a.flowunits
    ...
    [u'11', u'10', u'13', u'12', u'21', u'22', u'23', u'32', u'31', u'2', u'9']
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    gallons/minute
    
    alternative use open/close:
    >>> import EpanetOutBin
    >>> a= EpanetOutBin("Net1.bin")
    >>> a.open()
    >>> a.nodes['10'].demand
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    >>> a.close()"""

    def __init__(self, nomefilebin):
        self.filename=  nomefilebin

    def open(self):
        f= open(self.filename,"rb")
        self._file= f

        # Prolog Section
        Prolog = struct.unpack("15i",f.read(15*INTSIZE))
        if (Prolog[ 0] != MAGICNUMBER):
          raise Exception("{0} is not a  Epanet binary output file".format(nomefilebin))

        self.CODEVERSION  =Prolog[ 1]
        self._Nnodes       =Prolog[ 2]
        self._Ntanks       =Prolog[ 3]
        self._Nlinks       =Prolog[ 4]
        self._Npumps       =Prolog[ 5]
        self._Nvalves      =Prolog[ 6]
        Tstatflag    =Prolog[11]
        Rstart       =Prolog[12]
        Rstep        =Prolog[13]
        Dur          =Prolog[14]

        f.seek(-3*INTSIZE, SEEK_END)
        self._Nperiods, warn, magic = struct.unpack("3i",f.read(3*INTSIZE))
        if magic != MAGICNUMBER :
          raise Exception("File {0} corrupted or incomplete".format(nomefilebin))

 
        self.prolog_start= 0
        prolog_length = 15*INTSIZE
        prolog_length+= 3*(MAXMSG+1) #title
        prolog_length+= 2*(MAXFNAME+1) #filenames
        prolog_length+= 2*(MAXID+1) #ChemName QUALITY.Units
        prolog_length+= self._Nnodes*(MAXID+1) #nodenames
        prolog_length+= self._Nlinks*(MAXID+1) #linknames
        prolog_length+= self._Nlinks*INTSIZE* 3 #N1, N2, Type
        prolog_length+= self._Ntanks*(INTSIZE+ REAL4SIZE) # Tank[i].Node+ Tank[i].A
        prolog_length+= self._Nnodes*(REAL4SIZE) #node elevations
        prolog_length+= self._Nlinks*REAL4SIZE*2#link lengths & diameters

        self.energy_start= self.prolog_start+ prolog_length
        energy_length = 7*REAL4SIZE*self._Npumps
        energy_length+=REAL4SIZE

        self.dynamic_start= self.energy_start+ energy_length
        self.dynamic_step = 4*REAL4SIZE*self._Nnodes
        self.dynamic_step+= 8*REAL4SIZE*self._Nlinks
        dynamic_lenght= self.dynamic_step* self._Nperiods

        self.epilog_start= self.dynamic_start+dynamic_lenght

        self._nodes= {}
        for i in range(self._Nnodes):
          node= OutBinNode(self, i)
          self._nodes[node.ID]= node

        for i in range(self._Ntanks):
           area= self.tankarea(i)
           if area > 0.0:
              tipo= "TANK"
           else:
              tipo= "RESERVOIR"
           nodo= self._nodes[self.tanknode(i)]
           nodo._type= tipo
           nodo.area= area

        self._links= {}
        for i in range(self._Nlinks):
          link= OutBinLink(self, i)
          self._links[link.ID]= link


    def close(self):
        self._file.close()

    def __enter__(self):
        self.open()
        return self
          
    def __exit__(self ,type, value, traceback):
        self._file.close()
        return False



    @property
    def nodes(self):
        "nodes dictionary (node ID as key)"
        return self._nodes
         
    @property
    def links(self):
        "links dictionary (link ID as key)"
        return self._links


    @property
    def quality(self):
        "Water Quality"
        addr= self.prolog_start+ 7*INTSIZE
        self._file.seek(addr)
        i= struct.unpack("i",self._file.read(INTSIZE))[0]
        return _waterquality[i]

    @property
    def tracenode(self):
        "Node ID for Source Tracing"
        addr= self.prolog_start+ 8*INTSIZE
        self._file.seek(addr)
        i= struct.unpack("i",self._file.read(INTSIZE))[0]
        if i>0:
            return self.nodeID(i)
            
    @property
    def flowunits(self):
        "Flow Units"
        addr= self.prolog_start+ 9*INTSIZE
        self._file.seek(addr)
        i= struct.unpack("i",self._file.read(INTSIZE))[0]
        return _flowunits[i]

    @property
    def pressureunits(self):
        "Pressure Units "
        addr= self.prolog_start+ 10*INTSIZE
        self._file.seek(addr)
        i= struct.unpack("i",self._file.read(INTSIZE))[0]
        return _pressureunits[i]

    @property
    def statistics(self):
        "Time Statistics "
        addr= self.prolog_start+ 11*INTSIZE
        self._file.seek(addr)
        i= struct.unpack("i",self._file.read(INTSIZE))[0]
        return _statistics[i]


    @property
    def title(self):
        "Problem Title"
        addr= self.prolog_start+ 15*INTSIZE
        self._file.seek(addr)
        stri = self._file.read(MAXMSG+1).decode().strip("\x00")+"\n"
        stri+= self._file.read(MAXMSG+1).decode().strip("\x00")+"\n"
        stri+= self._file.read(MAXMSG+1).decode().strip("\x00")
        return stri
        
    @property
    def inputfilename(self):
        "Name of inputfile"
        addr= self.prolog_start+ 15*INTSIZE+ 3*(MAXMSG+1)
        self._file.seek(addr)
        return self._file.read(MAXFNAME+1).decode().strip("\x00")

    @property
    def reportfilename(self):
        "Name of reportfile"
        addr= self.prolog_start+ 15*INTSIZE+ 3*(MAXMSG+1)+ (MAXFNAME+1)
        self._file.seek(addr)
        return self._file.read(MAXFNAME+1).decode().strip("\x00")

    @property
    def chemicalname(self):
        "Name of Chemical"
        addr = self.prolog_start+ 15*INTSIZE
        addr+= 3*(MAXMSG+1)+ 2*(MAXFNAME+1)
        self._file.seek(addr)
        return self._file.read(MAXID+1).decode().strip("\x00")

    @property
    def chemicalunits(self):
        "Chemical Concentration Units "
        addr = self.prolog_start+ 15*INTSIZE
        addr+= 3*(MAXMSG+1)+ 2*(MAXFNAME+1)
        addr+= MAXID+1
        self._file.seek(addr)
        return self._file.read(MAXID+1).decode().strip("\x00")


    @property
    def energy(self):
        "Peak Energy Usage (kw-hrs)"
        addr= self.energy_start+ 7*REAL4SIZE*self._Npumps
        self._file.seek(addr)
        return  struct.unpack("f",self._file.read(REAL4SIZE))[0]
    @property
    def bulk_rrate(self):
        "Average bulk reaction rate (mass/hr)"
        addr= self.epilog_start
        self._file.seek(addr)
        return  struct.unpack("f",self._file.read(REAL4SIZE))[0]
    @property
    def wall_rrate(self):
        "Average wall reaction rate (mass/hr)"
        addr= self.epilog_start+ REAL4SIZE
        self._file.seek(addr)
        return  struct.unpack("f",self._file.read(REAL4SIZE))[0]
    @property
    def tank_rrate(self):
        "Average tank reaction rate (mass/hr)"
        addr= self.epilog_start+ 2*REAL4SIZE
        self._file.seek(addr)
        return  struct.unpack("f",self._file.read(REAL4SIZE))[0]
    @property
    def source_inflowrate(self):
        "Average source inflow rate (mass/hr)"
        addr= self.epilog_start+ 3*REAL4SIZE
        self._file.seek(addr)
        return  struct.unpack("f",self._file.read(REAL4SIZE))[0]
    @property
    def warning(self):
        "Warning Flag: True if warnings were generated"
        addr= self.epilog_start+ 4*REAL4SIZE+ INTSIZE
        self._file.seek(addr)
        return  struct.unpack("i",self._file.read(INTSIZE))[0]==1
      
    def _node_timeserie(self, ordinal, varindex):
        addr = self.dynamic_start
        addr+= varindex*REAL4SIZE*self._Nnodes
        addr+= ordinal* REAL4SIZE
        return self._read_timeserie(addr)

    def _link_timeserie(self, ordinal, varindex):
        addr = self.dynamic_start
        addr+= 4*REAL4SIZE*self._Nnodes
        addr+= varindex*REAL4SIZE*self._Nlinks
        addr+= ordinal* REAL4SIZE
        return self._read_timeserie(addr)

    def _read_timeserie(self, addr):
        x=[]
        for i in range(self._Nperiods):
           self._file.seek(addr)
           val= struct.unpack("f",self._file.read(REAL4SIZE))[0]
           x.append(val)
           addr+=  self.dynamic_step
        return x


    def _read_ID(self, addr):
        self._file.seek(addr)
        return struct.unpack("{0}s".format(MAXID+1),self._file.read(MAXID+1))[0].decode().strip("\x00")
        
    def nodeID(self, index):
        addr = self.prolog_start
        addr+= 15*INTSIZE+3*(MAXMSG+1)+2*(MAXFNAME+1)+ 2*(MAXID+1)
        addr+= (index-1)* (MAXID+1)
        return self._read_ID(addr)
        
    def linkID(self, index):
        addr = self.prolog_start
        addr+= 15*INTSIZE+3*(MAXMSG+1)+2*(MAXFNAME+1)+ 2*(MAXID+1)
        addr+= self._Nnodes* (MAXID+1)
        addr+= (index-1)* (MAXID+1)
        return self._read_ID(addr)

    def linktype(self, index):
        addr = self.prolog_start
        addr+= 15*INTSIZE+3*(MAXMSG+1)+2*(MAXFNAME+1)+ 2*(MAXID+1)
        addr+= self._Nnodes* (MAXID+1)
        addr+= self._Nlinks* (MAXID+1)
        addr+= 2* self._Nlinks* INTSIZE
        addr+= (index-1)* INTSIZE
        self._file.seek(addr)
        val= struct.unpack("i",self._file.read(INTSIZE))[0]
        return _linktype[val]

    def tanknode(self, ordinal):
        addr = self.prolog_start
        addr+= 15*INTSIZE+3*(MAXMSG+1)+2*(MAXFNAME+1)+ 2*(MAXID+1)
        addr+= self._Nnodes* (MAXID+1)
        addr+= self._Nlinks* (MAXID+1)
        addr+= 3* self._Nlinks* INTSIZE
        addr+= ordinal* INTSIZE
        self._file.seek(addr)
        index= struct.unpack("i",self._file.read(INTSIZE))[0]
        return self.nodeID(index)

    def tankarea(self, ordinal):
        addr = self.prolog_start
        addr+= 15*INTSIZE+3*(MAXMSG+1)+2*(MAXFNAME+1)+ 2*(MAXID+1)
        addr+= self._Nnodes* (MAXID+1)
        addr+= self._Nlinks* (MAXID+1)
        addr+= 3* self._Nlinks* INTSIZE
        addr+= self._Ntanks* INTSIZE
        addr+= ordinal* REAL4SIZE
        self._file.seek(addr)
        return struct.unpack("f",self._file.read(REAL4SIZE))[0]














