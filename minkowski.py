import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.grid_helper_curvelinear import GridHelperCurveLinear
from mpl_toolkits.axisartist import Subplot
from matplotlib.widgets import CheckButtons

c = 299800000 #speed of light
velocity = -0.4*c #set to whatever you want homie
beta = velocity/c
gamma = math.sqrt(1/(1-(beta**2)))
print gamma

lorentz = np.zeros(shape=(2,2))
lorentz[0] = [gamma,-gamma*beta]
lorentz[1] = [-gamma*beta,gamma]
print lorentz

invlorentz = np.linalg.inv(lorentz)

x_pts = []
y_pts = []

observerGridEnabled = True
travelerGridEnabled = False
lightConesEnabled = False

def drawMinkowski():
    
    global fig
    global ax1
    global ax2


    def tr(x,y):
        x,y = np.asarray(x), np.asarray(y)
        return lorentz[0][0]*x + lorentz[0][1]*y, lorentz[1][0]*x + lorentz[1][1]*y
    def inv_tr(x,y):
        return invlorentz[0][0]*x + invlorentz[0][1]*y, invlorentz[1][0]*x + invlorentz[1][1]*y

    grid_helper = GridHelperCurveLinear((tr,inv_tr))
    ax1 = Subplot(fig, 1, 1, 1, grid_helper=grid_helper)
    
    fig.add_subplot(ax1)

    xx,yy = tr([3,6],[5.0,10.])
    #ax1.plot(xx, yy)
    
    pos1 = ax1.get_position()
    pos2 = [pos1.x0 + 0.09, pos1.y0,  pos1.width, pos1.height]
    ax1.set_position(pos2)

    ax1.set_aspect(1.)
    ax1.set_xlim(-10,10.)
    ax1.set_ylim(-10,10.)


    ax1.axis["t"]=ax1.new_floating_axis(0,0.)
    ax1.axis["t2"]=ax1.new_floating_axis(1,0.)
    ax1.grid(travelerGridEnabled)
    ax1.set_xlabel("x'")
    ax1.set_ylabel("ct'")

    ax2 = fig.add_axes(ax1.get_position(), frameon=False)
    ax2.xaxis.set_ticks_position('top')
    ax2.yaxis.set_ticks_position('right')
    ax2.set_xlim(-10,10.)
    ax2.set_ylim(-10,10.)
    ax2.set_aspect(1.)
    ax2.axvline(0)
    ax2.axhline(0)
    ax2.set_xlabel("x")
    ax2.xaxis.set_label_position('top')
    ax2.set_ylabel("ct")
    ax2.yaxis.set_label_position('right')
    ax2.grid(observerGridEnabled)

fig = plt.figure()
rax = plt.axes([0.01, 0.01, 0.23, 0.28])
check = CheckButtons(rax, ('Observers grid', 'Travelers grid', 'Light Cones'), (observerGridEnabled, travelerGridEnabled, lightConesEnabled))
def checkBoxes(lbl):

    global observerGridEnabled
    global travelerGridEnabled
    global lightConesEnabled

    if lbl == "Observers grid":
        print "toggling observers grid"
        observerGridEnabled = not observerGridEnabled
        ax2.grid(observerGridEnabled)
    elif lbl == "Travelers grid":
        print "toggling travelers grid"
        travelerGridEnabled = not travelerGridEnabled
        ax1.grid(travelerGridEnabled)
    elif lbl == "Light Cones":
        print "toggling light cones"
        recalculateConstants(0.25);
        ax1.remove()
        ax2.remove()
        drawMinkowski()
    plt.draw()


def recalculateConstants(b): #takes beta
    
    global beta
    global velocity
    global gamma
    global lorentz
    global invlorentz


    print "redrawing for beta=",b
    
    beta = -b
    velocity = b*c 
    gamma = math.sqrt(1/(1-(beta**2)))
    print gamma

    lorentz = np.zeros(shape=(2,2))
    lorentz[0] = [gamma,-gamma*beta]
    lorentz[1] = [-gamma*beta,gamma]
    print lorentz

    invlorentz = np.linalg.inv(lorentz)

def onpick(event):
    m_x, m_y = event.x, event.y
    x, y = ax2.transData.inverted().transform([m_x, m_y])
    x_pts.append(x)
    y_pts.append(y)
    print "x%d y%d" % (x,y) 
    ax2.scatter(x_pts,y_pts)
    fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', onpick)

check.on_clicked(checkBoxes)

drawMinkowski();
plt.show()
