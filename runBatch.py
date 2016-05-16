'''
Created on 2015-02-24
author: trabuzin at gmail dot com
'''

import Raw2Record
import readRaw
import toRecord

reader = readRaw.Reader(Raw2Record.settings.globalworkdir, r'X:/dev/N44_WP7/01_PSSE_Resources/Snapshots/N44_20150101')

lista = reader.getListOfRawFiles()
for snapshot in lista:
    # Opening the current snapshot in PSS/E
    reader.openRaw(snapshot)
    # Reading all of the components from the PSS/E to reader object
    reader.readBusNumbers()

    reader.readVoltageLevels()
    reader.readVoltageAngles()

    reader.readMachines()
    reader.readMachinePowers()

    reader.readLoads()
    reader.readLoadPowers()

    reader.readTrafos()
    reader.readTrafoRatios()

    # Creating the dictionaries for each of the components from the reader object
    buses = reader.createBusDict()
    machines = reader.createMachineDict()
    loads = reader.createLoadDict()
    trafos = reader.createTrafoDict()

    # Instantiating the record object and writing component dictionaries to the record file
    record = toRecord.Record(Raw2Record.settings.globalworkdir, snapshot, reader.caseName, buses, machines, loads, trafos)
    record.writeVoltages()
    record.writeMachines()
    record.writeLoads()
    record.writeTrafos()
    record.closeRecord()
