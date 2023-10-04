''' Present an interactive function explorer with slider widgets.

Scrub the sliders to change the period & phase of the transiting planet. 

Use the shiny command to run the example by executing:

    shiny run --reload eclipse.py

at your command prompt. In your browser, navigate to the URL provided.

'''
from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np

from kepio import kepio

# Set up data
t,f,e = kepio("kplr011517719-2013098041711_llc.fits")
x0 = t
y = f
period_start = 2.0

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
        ui.input_slider("period", "Period", min=1, max=6, 
                        value=period_start, step=1e-3),
        ui.input_slider("T0", "Phase", min=0, max=1, value=0, step=1e-2),
        ),
        ui.panel_main(
            ui.output_plot("my_widget"),
        ),
    ),
)


def server(input, output, session):
    @output
    @render.plot(alt="Kepler Data")
    def my_widget():
        # Get the current slider values
        p = input.period()
        t = input.T0()

        # Generate the new curve
        x = ((x0 - t) % p) / p
        # y = np.sin(x0) + errs

        # fig, ax = plt.subplots()
        plt.plot(x,y,'.',alpha=0.5)

        # return fig

app = App(app_ui, server)