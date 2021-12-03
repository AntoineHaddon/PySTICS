import PySTICS as sti



dir_corn2013 = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'
JavaSticsDir = '/home/ahaddon/Programs/JavaSTICS-1.41-stics-9.1/'

corn2013 = sti.usm(dir_corn2013,'maize_ref_2013',JavaSticsDir) 
# corn2013.run()

simData = corn2013.loadData()
print(simData)
# import matplotlib.pyplot as plt
# [plt.plot(simData['jul'], simData['HR('+str(i)+')'] ) for i in range(1,5)]
# plt.show()

