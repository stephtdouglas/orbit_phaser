''' Present an interactive function explorer with slider widgets.

Scrub the sliders to change the period & phase of the transiting planet. 

Use the shiny command to run the example by executing:

    shiny run --reload eclipse.py

at your command prompt. In your browser, navigate to the URL provided.

'''
from shiny import App, render, ui, reactive, module
import matplotlib.pyplot as plt
import numpy as np

from kepio import kepio, search_mast

period_start = 2.0
default_target = "KIC 6922244"
default_author = "Kepler"
default_sector = 4

def get_lc(target_name=default_target, author=default_author,
           sector=default_sector):
    # t,f,e = kepio("kplr011517719-2013098041711_llc.fits")

    kw = {"author":author,"cadence":"long"}
    if author=="Kepler":
        kw["quarter"] = sector
    elif author=="K2":
        kw["campaign"] = sector 
    elif author=="TESS":
        k2["sector"] = sector

    t,f,e = search_mast(target_name, **kw)
    x0 = t
    y = f

    return x0, y

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("period", "Period", min=0.01, max=6, 
                            value=period_start, step=1e-2),
            ui.input_slider("T0", "Phase", min=0, max=1, value=0, step=1e-2),
            ui.input_text("target", "Target name", placeholder=default_target),
            ui.input_text("sector", "Quarter, Campaign, or Sector", placeholder=default_sector),
            ui.input_select("author", "Mission", {"kepler": "Kepler", "k2": "K2", "tess":"TESS"}),

        ),
        ui.panel_main(
            ui.output_plot("my_widget"),
        ),
    ),
)


def server(input, output, session):

    @reactive.Calc
    def target():
        # Load the data
        x0, y = get_lc(input.target())
        return x0, y
        
    # @reactive.Calc
    # def phase_lc():
    #     x0, y = target()

    #     # Get the current slider values
    #     p = input.period()
    #     t = input.T0()

    #     # Generate the new curve
    #     x = ((x0 - t) % p) / p
    #     # y = np.sin(x0) + errs

    #     # Return values
        # return x

    @output
    @render.plot(alt="Kepler Data")
    def my_widget():
        x0, y = target()

        # Get the current slider values
        p = input.period()
        t = input.T0()

        # Generate the new curve
        x = ((x0 - t) % p) / p

        # x = phase_lc()

        # fig, ax = plt.subplots()
        plt.plot(x,y,'.',alpha=0.5)

        # return fig

app = App(app_ui, server)