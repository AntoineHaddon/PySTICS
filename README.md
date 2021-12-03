# PySTICS
Python library to run STICS, write inputs and load model outputs

# Dependencies
STICS : [https://www6.paca.inrae.fr/stics/](https://www6.paca.inrae.fr/stics/)

Python libarires : numpy, pandas 

# Usage

USM class initialized with the name of the directory containing the usm and the usm name

```
import PySTICS as sti

corn = sti.usm(dirUSM, usmName) 
```

To run a simulation, set the directory containing the command line executable JavaSticsCmd.exe 
```
corn.JavaSticsDir = '...'
corn.run()
```

Setting an irrigation or fertilization calendar 
```
import numpy as np
irrigCal = np.array([ [207,30.0], [226,30.0] ])
corn.writeIrrigCal(irrigCal)

fertiCal = np.array([ [120,80.0], [200,50.0] ])
corn.writeFertiCal(fertiCal)
```


Loading and plotting outputs
```
simData = corn.loadData()

import matplotlib.pyplot as plt
plt.plot(simData.index, simData['HR(1)'] ) 
plt.show()

```
