import plotly.plotly as py
import plotly.graph_objs as go

def graph(points):
    """ Generate Plotly graph. """
    data = [go.Scatter(
        x=[x for x, _ in points],
        y=[y for _, y in points],
        mode='markers'
    )]

    layout = go.Layout(title="Expedition",
                       xaxis={'title': "time"},
                       annotations=[{'text': 'simple annotation',
                                     'x': 0, 'xref': 'paper',
                                     'y': 0, 'yref': 'paper'}]
    )

    figure = go.Figure(data=data, layout=layout)
    url = py.plot(figure, share='private', filename='line-scatter')
    return url

