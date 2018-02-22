''' Present an interactive function explorer with slider widgets.

Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve eclipse.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/eclipse

in your browser.

'''
from __future__ import division, print_function, absolute_import

import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Dropdown
from bokeh.plotting import figure

from kepio import kepio

lightcurves = {}
t840, f840, e840 = kepio("kplr011517719-2013098041711_llc.fits.txt")
lightcurves["Kepler 840"] = {"t":np.float64(t840),"f":f840,"e":e840}
t488, f488, e488 = kepio("kplr010904857-2013131215648_llc.fits.txt")
lightcurves["Kepler 488"] = {"t":np.float64(t488),"f":f488,"e":e488}


# Set up data
s = "Kepler 840"
x0,y = lightcurves[s]["t"],lightcurves[s]["f"]
current_period = np.float64(2)
x = (x0 % current_period) / current_period
source = ColumnDataSource(data=dict(x=x, y=y))


# Set up plot
plot = figure(plot_height=400, plot_width=600, title=s,
              tools="crosshair,pan,reset,save,wheel_zoom"
              ,x_range=[0,1]
              # y_range=[-2.5, 2.5])
              )

plot.circle('x', 'y', source=source, size=10, alpha=0.6)


# Set up widgets
text = TextInput(title="Period (Refine)", value=str(current_period))
period = Slider(title="Period", value=current_period, start=1, end=10, step=0.0001)
# T0 = Slider(title="Time_0", value=x[0], start=x[0], end=x[100], step=x[1]-x[0])
t = 0

menu = [("Kepler 840", "Kepler 840"), ("Kepler 488", "Kepler 488")]
star = Dropdown(label="Object", button_type="warning", menu=menu)

def update_from_slider(attrname, old, new):

    # Get the current lightcurve
    s = star.value

    # Get the current slider values
    p = period.value
    # t = T0.value

    # Generate the new curve
    x0, y = lightcurves[s]["t"], lightcurves[s]["f"]
    x = ((x0 - t) % p) / p
    # y = np.sin(x0) + errs

    source.data = dict(x=x, y=y)

    plot.title.text = s

def update_from_text(attrname, old, new):

    # Get the current lightcurve
    s = star.value

    # Get the current slider values
    p = np.float64(text.value)
    # t = T0.value

    # Generate the new curve
    x0, y = lightcurves[s]["t"], lightcurves[s]["f"]
    x = ((x0 - t) % p) / p
    # y = np.sin(x0) + errs

    source.data = dict(x=x, y=y)

    plot.title.text = s



for w in [star, period]:
    w.on_change('value', update_from_slider)

text.on_change('value',update_from_text)


# Set up layouts and add to document
inputs = widgetbox(star, period, text)

curdoc().add_root(row(inputs, plot, width=1000))
curdoc().title = "Eclipse"
