from astropy import constants as const
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

G       = const.G.value
M_sun   = const.M_sun.value
R_sun   = const.R_sun.value


M_earth = const.M_earth.value
M_jup   = const.M_jup.value

a_merc  = const.au.value*0.387098
a_venus = const.au.value*0.723332
a_earth = const.au.value
a_mars  = const.au.value*1.523679 
a_jup   = const.au.value*5.204267
a_sat   = const.au.value*9.5826
a_ur    = const.au.value*19.2184
a_ne    = const.au.value*30.110387

def d_theta_dt(r):
    return np.sqrt(G*M_sun*r**(-3.))

# You probably won't need this if you're embedding things in a tkinter plot...
#plt.ion()

fig = plt.figure(1)
ax = fig.add_subplot(111)

thetas = [0,
          0,
          0,
          0,
          0,
          0,
          0,
          0] # intial theta

a = [a_merc,
     a_venus,
     a_earth,
     a_mars,
     a_jup,
     a_sat,
     a_ur,
     a_ne] # semimajor axis of orbit

circles = [plt.Circle((0,0),aa,color='white',fill=False,alpha=0.5) for aa in a] # draws in orbital path

circles = [ax.add_artist(circle) for circle in circles]

x = [x*np.cos(theta) for x,theta in zip(a,thetas)]
y = [x*np.sin(theta) for x,theta in zip(a,thetas)]

ax.set_xlim([-1.1*a_ne,1.1*a_ne]) 
ax.set_ylim([-1.1*a_ne,1.1*a_ne])
plt.axis('off') # no need for axis am i rite



#ax.plot(0,0,'yo')#, markersize=20) # the sun
styles = ['sienna',
          'orange',
          'blue',
          'red',
          'darkgoldenrod',
          'khaki',
          'navy',
          'darkturquoise'] # color of dots

def plot(ax,x,y,style):  # function used to create initial image
    graph = ax.plot(x,y,marker='o',color=style)[0]
    return graph

graphs = [plot(ax,xx,yy,style) for xx,yy,style in zip(x,y,styles)] # dots inside image


day = 0
seconds = 24*3600
fig.patch.set_facecolor('black')
def replot(a, theta, graph): 
    theta = theta + d_theta_dt(a)*seconds
    x = a*np.cos(theta)
    y = a*np.sin(theta)

    graph.set_xdata(x)
    graph.set_ydata(y)

    return theta,graph


def animate(day): 
    ax.set_title('day:'+str(int(day%365.25)),color='white')
    
    for j,graph in enumerate(graphs):
        thetas[j],graphs[j] = replot(a[j],thetas[j],graph)
    
    return graphs



ani=animation.FuncAnimation(fig,animate,np.arange(0,1e6), interval=75) #not entirely sure how this works, but ill take it
plt.show()

