import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from getData import League
import plotly.graph_objs as go


app = dash.Dash()
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})


colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

def format_dataframe(df):
    players = df.index.values
    x_data = [i+1 for i in range(df.shape[1])]
    y_data = [[df.iloc[i][col] for col in df.columns] for i in range(len(df))]
    return players, x_data, y_data

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    #html.Link(href='/assets/main.css', rel='stylesheet'),
    html.H1('Visualize your Fantasy Premier League classic mini-league', style={'text-align': 'center'}),

    html.Div(dcc.Input(
        id='leagueID',
        placeholder='Enter leagueID',
        type='text',
        value='',
        ),
        style={'text-align': 'center', 'padding':'15px', 'display':'inline-block'}
    ),
    html.Button('Submit', id='button', style={'text-align': 'center', 'display':'inline-block'}),
    html.P('Select the number of players from the league to be tracked:'),
    dcc.Slider(
        id='players-slider',
        min=1,
        max=50,
        value=20,
        marks={
            1: {'label': '1'},
            10: {'label': '10'},
            20: {'label': '20'},
            30: {'label': '30'},
            40: {'label': '40'},
            0: {'label': '50'},
        },
    ),

    html.H1(style={'padding':'10px'}),

    dcc.Graph(id='league-progression', style={'height': 1000})
])
@app.callback(
    dash.dependencies.Output('league-progression', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('players-slider', 'value'), dash.dependencies.State('leagueID', 'value')])
def update_output(n_clicks, slider_value, leagueid_value):
    if not leagueid_value:
        return
    league = League()
    leaguename, df = league.main(leagueid_value, 34, slider_value)
    if isinstance(df, str):
        return {
            'data': [],
            'layout': go.Layout(
            title= df,
        )
    }
    players, x, y = format_dataframe(df)

    return {
        'data': [
            go.Scatter(
                x=x,
                y=y[i],
                name=players[i]
                ) for i in range(len(players))
        ],
        'layout': go.Layout(
            title= 'League data for ' + leaguename,
            height=1000,
            xaxis={'title': 'Gameweek'},
            yaxis={'title': 'Points'}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
