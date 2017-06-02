import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from os.path import expanduser
home = expanduser("~")

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

fn = home +'/stpt.txt'


def animate(i):
            pullData = open(fn,'r').read()

            dataArray = pullData.split('\n')
            ax1.clear()
            
            yar = []
            zar=[]
            num=len(dataArray[0].split(','))


            for i in range(1,num-1):
                y=[]
                x=[]
                j=0
                for eachLine in dataArray:
                      if len(eachLine)>1:
                            temp = eachLine.split(',')[i]
                            j=j+1

                            y.append(float(temp)/5*9+32)
                            x.append(j)
                ax1.plot(x,y) 

            ax1.set_ylabel('Temp Set Point [degF]')					
            ax1.set_xticks([])
            ax1.set_xticklabels([])

            ax2.clear()


            y=[]
            x=[]
            j=0
            z=[]
            for eachLine in dataArray:
                      if len(eachLine)>1:
                            temp = eachLine.split(',')[num-1]
                            j=j+1
                            y.append(float(temp)/1000)
                            x.append(j)
                            ti = eachLine.split(',')[0]
                            z.append(ti.split('+')[0].split('T')[1])


            ax2.plot(x,y) 
            ax2.set_ylabel('Total Building Power [kW]')
            if len(x)>1:
                xar=[0,len(x)/4,len(x)/2,len(x)/4*3,len(x)-1]
                zar=[z[0],z[len(x)/4],z[len(x)/2],z[len(x)/4*3],z[len(x)-1]]
                ax2.set_xticks(xar)

                ax2.set_xticklabels(zar,rotation=45)	

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

