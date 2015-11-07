import plotly.plotly as py
import plotly.graph_objs as go


def graph(points, search_string=""):
    """ Generate Plotly graph and return URL. """
    data = [go.Scatter(
        x=[x for x, _ in points],
        y=[y for _, y in points],
        mode='markers'
    )]

    layout = go.Layout(title="Results for '{}'".format(search_string),
                       xaxis={'title': 'Odometer (km)'},
                       yaxis={'title': 'Price ($)'},
    )

    figure = go.Figure(data=data, layout=layout)
    return py.plot(figure, share='private', filename='line-scatter')

