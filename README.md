# PySTICS
Python library to run STICS, write inputs and load model outputs


# Example


'''
import PySTICS as sti


dir_corn2013 = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'

corn2013 = sti.usm(dir_corn2013,'maize_ferti_2013') 

import numpy as np
irrigCal = np.array([ [207,30.0], [226,30.0] ])
corn2013.writeIrrigCal(irrigCal)

fertiCal = np.array([ [120,80.0], [200,50.0] ])
corn2013.writeFertiCal(fertiCal)

corn2013.set_IniFile("maize_ini.xml")

corn2013.JavaSticsDir = '/home/ahaddon/Programs/JavaSTICS-1.41-stics-9.1/'
corn2013.run()



simData = corn2013.loadData()

import matplotlib.pyplot as plt
# plt.plot(simData.index, simData['HR(1)'] ) 
plt.show()

'''
