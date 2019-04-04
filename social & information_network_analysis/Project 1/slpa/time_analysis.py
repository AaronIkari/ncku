import matplotlib.pyplot as plt
import csv
import numpy as np

datas = list()
with open ('time_analysis.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
    for row in reader:
        data = list()
        for cell in row:
            data.append( float(cell.split('=')[1].strip(' ')) )
        datas.append(data)

datas = np.asarray(datas)

fig, ax = plt.subplots()

NMI, = ax.plot(list(datas[:,1]), list(datas[:,3]), 'b-o')
ANC, = ax.plot(list(datas[:,1]), list(datas[:,4]), 'r-o')
plt.xticks( np.arange(15, 31, step=1) )
ax.legend([NMI, ANC], ['NMI','ANC'])
ax.set(xlabel='Iterations', title='SLPA (Threshold=0.3)')
ax.grid()
fig.savefig('time')
ax.cla()

COM, = ax.plot(list(datas[:,1]), list(datas[:,2]), 'g-o')
plt.xticks( np.arange(15, 31, step=1) )
ax.legend([COM], ['# communities'])
ax.set(xlabel='Iterations', ylabel='Number of communities', title='SLPA (Threshold=0.3)')
ax.grid()
fig.savefig('communities')

