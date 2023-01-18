from astropy import constants as const
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

G       = const.G.value
M_sun   = const.M_sun.value

a_earth = const.au.value
a_jup   = const.au.value*5.204267
#a_hai   = const.au.value*17.8

def f_x(x,y,x_dot,delta_t):
    
    x_new  = x + x_dot*delta_t
    
    x_ddot = -G*M_sun*np.cos(np.arctan2(y,x))/(x*x+y*y)
    
    x_dot  = x_dot + x_ddot*delta_t 
    
    return x_new, x_dot

def f_y(x,y,y_dot,delta_t):
    
    y_new  = y + y_dot*delta_t
    
    y_ddot = -G*M_sun*np.sin(np.arctan2(y,x))/(x*x+y*y)
    
    y_dot  = y_dot + y_ddot*delta_t 

    return y_new, y_dot


fig = plt.figure(1)
ax = fig.add_subplot(111)

x       = np.array([a_earth, a_jup],dtype=np.float64)
y       = np.array([0, 0],dtype=np.float64)

x_dot   = np.array([0, 0],dtype=np.float64)
y_dot   = np.array([2.978473e4*4/5., 1.306e4],dtype=np.float64)

#

a = [a_earth,
     a_jup] # semimajor axis of orbit

circles = [plt.Circle((0,0),aa,color='white',fill=False,alpha=0.5) for aa in a] # draws in orbital path

circles = [ax.add_artist(circle) for circle in circles]


ax.set_xlim([-1.1*a_jup,1.1*a_jup]) 
ax.set_ylim([-1.1*a_jup,1.1*a_jup])
plt.axis('off') # no need for axis am i rite


styles = ['blue',
          'darkgoldenrod'] # color of dots

def plot(ax,x,y,style):  # function used to create initial image
    graph = ax.plot(x,y,marker='o',color=style)[0]
    return graph

graphs = [plot(ax,xx,yy,style) for xx,yy,style in zip(x,y,styles)] # dots inside image

delta_t = 1*3600 #seconds in a day
fig.patch.set_facecolor('black')
def replot(xx,yy,xx_dot,yy_dot, graph): 

    xx_new,xx_dot_new = f_x(xx,yy,xx_dot,delta_t)
    yy_new,yy_dot_new = f_y(xx,yy,yy_dot,delta_t)

    graph.set_xdata(xx_new)
    graph.set_ydata(yy_new)

    return xx_new,xx_dot_new,yy_new,yy_dot_new,graph


def animate(day): 
    ax.set_title('day:'+str(int(day/24.)),color='white')
    
    for j,graph in enumerate(graphs):
        x[j],x_dot[j],y[j],y_dot[j],graph = replot(x[j],y[j],x_dot[j],y_dot[j],graph)
    
    return graphs



ani=animation.FuncAnimation(fig,animate,np.arange(0,1e6), interval=0.001) #not entirely sure how this works, but ill take it
plt.show()

