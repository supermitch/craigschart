import plotly.plotly as py
import plotly.graph_objs as go


def graph(points, category='', search_string=''):
    """ Generate Plotly graph and return URL. """
    data = [go.Scatter(
        x=[x for x, _ in points],
        y=[y for _, y in points],
        mode='markers+text',
        text=['<a href="http://www.strava.com">Text A</a>', 'Text B', 'Text C'],
        textposition='top',
    )]

    layout = go.Layout(title="Results for Category {} with Query '{}'".format(category, ' '.join(search_string)),
                       xaxis={'title': 'Odometer (km)'},
                       yaxis={'title': 'Price ($)'},
    )

    figure = go.Figure(data=data, layout=layout)
    return py.plot(figure, share='private', filename='line-scatter')

