''' Present an interactive function explorer with slider widgets.

Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve eclipse.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/eclipse

in your browser.

'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

from kepio import kepio

t,f,e = kepio("kplr011517719-2013098041711_llc.fits")

x0 = t
y = f

# Set up data
# N = 500
# x0 = np.linspace(0, 10*np.pi, N)
period = 2.0
x = (x0 % period) / period
# errs = np.random.randn(N)*0.1
# y = np.sin(x0) + np.sin(x0*2 + np.pi/3) + errs
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=600, title="My Kepler Light Curve",
              tools="crosshair,pan,reset,save,wheel_zoom"
              ,x_range=[0,1]
              # y_range=[-2.5, 2.5])
              )

plot.circle('x', 'y', source=source, size=10, alpha=0.6)


# Set up widgets
text = TextInput(title="title", value='My Kepler Light Curve')
period = Slider(title="period", value=2, start=1, end=5, step=0.0001)
T0 = Slider(title="T_0", value=0, start=0, end=1, step=0.001)

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    p = period.value
    t = T0.value

    # Generate the new curve
    x = ((x0 - t) % p) / p
    # y = np.sin(x0) + errs

    source.data = dict(x=x, y=y)

for w in [period, T0]:
    w.on_change('value', update_data)


# # Set up layouts and add to document
curdoc().add_root(row(plot, column(text, period, T0)))
curdoc().title = "Eclipse"
