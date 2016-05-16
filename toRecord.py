'''
Created on 2015-02-24
author: trabuzin at gmail dot com
'''

import os


class Record():
    '''
    Class defining how Modelica record file is created
    '''

    def __init__(self, workdir, rawfilepath, caseName, buses, machines, loads, trafos):
        '''
        Constructor:
            - Store dictionary of buses
            - Open a record file
            - Write the beginning of the file
        '''
        self.buses = buses
        self.machines = machines
        self.loads = loads
        self.trafos = trafos
        self.caseName = caseName
        assert(os.path.isfile(rawfilepath))
        self.recordPath = workdir + '/' + rawfilepath.split('/')[-2]
        if not os.access(self.recordPath, os.F_OK):
            os.mkdir(self.recordPath)
        self.recordFile = open(self.recordPath + r'/%s.mo' % (self.caseName), 'w+')
        self.recordFile.write('record PF_results\n //Power flow results for the snapshot %s\n \n   extends Modelica.Icons.Record; \n' % (self.caseName))


    def writeVoltages(self):
        self.recordFile.write('record Voltages\n')
        for key in self.buses.keys():
            self.recordFile.write('// Bus number %s\n' % (key))
            self.recordFile.write('   parameter Real V%s = %f; \n' % (key, self.buses[key]['voltage']))
            self.recordFile.write('   parameter Real A%s = %f; \n' % (key, self.buses[key]['angle']))
        self.recordFile.write('end Voltages;\n')

    def writeMachines(self):
        self.recordFile.write('record Machines\n')
        for machine in self.machines.keys():
            self.recordFile.write('// Machine %s\n' % (machine))
            self.recordFile.write('   parameter Real P%s = %f; \n' % (machine, self.machines[machine]['P']))
            self.recordFile.write('   parameter Real Q%s = %f; \n' % (machine, self.machines[machine]['Q']))
        self.recordFile.write('end Machines;\n')

    def writeLoads(self):
        self.recordFile.write('record Loads\n')
        for load in self.loads.keys():
            self.recordFile.write('// Load %s\n' % (load))
            self.recordFile.write('   parameter Real PL%s = %f; \n' % (load, self.loads[load]['P']))
            self.recordFile.write('   parameter Real QL%s = %f; \n' % (load, self.loads[load]['Q']))
        self.recordFile.write('end Loads;\n')

    def writeTrafos(self):
        self.recordFile.write('record Trafos\n')
        for trafo in self.trafos.keys():
            self.recordFile.write('// 2WindingTrafo %s\n' % (trafo))
            self.recordFile.write('   parameter Real t1_%s = %f; \n' % (trafo, self.trafos[trafo]['t1']))
            self.recordFile.write('   parameter Real t2_%s = %f; \n' % (trafo, self.trafos[trafo]['t2']))
        self.recordFile.write(r'end Trafos;\n')

    def closeRecord(self):
        self.recordFile.write('Voltages voltages;\n')
        self.recordFile.write('Machines machines;\n')
        self.recordFile.write('Loads loads;\n')
        self.recordFile.write('Trafos trafos;\n')
        self.recordFile.write('end PF_results;')
