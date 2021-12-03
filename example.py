import matplotlib.pyplot as plt
import numpy as np

import PySTICS as sti



dir_corn2013 = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'

corn2013 = sti.usm(dir_corn2013,'maize_ferti_2013') 


irrigCal = np.array([ [207,30.0], [226,30.0] ])
# irrigCal = np.array([ [207,30.0], [226,30.0], [230,30.0] ])
corn2013.writeIrrigCal(irrigCal)

fertiCal = np.array([ [120,80.0], [200,50.0] ])
corn2013.writeFertiCal(fertiCal)

# corn2013.set_IniFile("maize_fullNO3_ini.xml")
corn2013.set_IniFile("maize_ini.xml")

corn2013.JavaSticsDir = '/home/ahaddon/Programs/JavaSTICS-1.41-stics-9.1/'
corn2013.run()



simData = corn2013.loadData()
# print(simData)

# plt.plot(simData.index, simData['HR(1)'] ) 
# plt.plot(simData.index, simData['airg(n)'] ) 
plt.plot(simData.index, simData['AZnit(1)'] ) 
plt.show()

