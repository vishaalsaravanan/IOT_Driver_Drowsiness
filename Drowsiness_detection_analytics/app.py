
import pandas as pd
import firebase_admin
import pyrebase
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime


config=  {
                    
                "apiKey": "AIzaSyC_9MN-e2kLYGoXEa-ujZhMJ5KEDhxrxv0",
                "authDomain": "drowsi-6f166.firebaseapp.com",
                "databaseURL": "https://drowsi-6f166-default-rtdb.firebaseio.com",
                "projectId": "drowsi-6f166",
                "storageBucket": "drowsi-6f166.appspot.com",
                "messagingSenderId": "198177358258",
                "appId": "1:198177358258:web:220473766070b40a1224ab",
                "measurementId": "G-FD48W8GKN9"
                }
    
if not firebase_admin._apps:
       cred_obj = firebase_admin.credentials.Certificate('serviceAccountKey.json')
       default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL': 'https://drowsi-6f166-default-rtdb.firebaseio.com/'})
       firebase=pyrebase.initialize_app(config)
db = firebase.database()
users = db.get()
 
l = []
for user in users.each():
     l.append(user.val())

df = pd.DataFrame(l)
df.columns

df1 = df

'''
from datetime import datetime

timestamp = df1.blinks
dt_object = datetime.fromtimestamp(timestamp)
'''


     

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Drowsiness Detection", style={    'color': '#FFFFFF',
                                                                'font-size': '48px',
                                                                'font-weight': 'bold',
                                                                'text-align': 'center',
                                                                'margin': '0 auto',}
                ),
                html.P(
                    children="Analyze the behavior of Drivers",
               
                    style = {   'color': '#CFCFCF',
                                'margin': '4px auto',
                                'text-align': 'center',
                                'max-width': '384px',},
                ),
            ],
           style = {    'background-color': '#222222',
                        'height': '256px',
                        'display': 'flex',
                        'flex-direction': 'column',
                        'justify-content': 'center'}
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            'data': [
                                {'x': df1.name.values, 'y': df1.total_blink, 'type': 'bar', 'name': 'Blinks'},
                                {'x': df1.name.values, 'y': df1.totaldrowsiness, 'type': 'bar', 'name': 'Drowsiness Alerts'},
                                {'x': df1.name.values, 'y': df1.total_yawns, 'type': 'bar', 'name': 'Yawn Count'},
                                {'x': df1.name.values, 'y': df1.trips, 'type': 'bar', 'name': 'Trips'},
                            ],
                            "layout": {
                                "title": {
                                    "text": "Drivers' Performance",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True},
                                "yaxis": {
                                    
                                    "fixedrange": True,
                                },
                              
                            },
                        },
                    ),
                    style = {    'margin-bottom': '24px',
                                 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)'},
                ),
                
            ],
            style = {   'margin-right': 'auto',
                        'margin-left': 'auto',
                        'max-width': '1024px',
                        'padding-right': '10px',
                        'padding-left': '10px',
                        'margin-top': '32px'},
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
               
                        config={"displayModeBar": False},
                        figure={
                "data": [
                    {
                        "x": ['Total Blinks', 'Drowsiness Count','Yawn Count','Trips'],
                        "y": df.iloc[2,3:7].values,
                        "type": "lines",
                        'name': "Harish",
                    },
                    {
                        "x": ['Total Blinks', 'Drowsiness Count','Yawn Count','Trips'],
                        "y": df.iloc[1,3:7].values,
                        "type": "lines",
                        'name': 'Vishal',
                    },
                ],
                "layout": {"title": "Driver: Harish"},
            },style={'width': '70%'}
                    ),
                    style = {    'margin-bottom': '24px',
                                 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)'},
                ),
                
            ],
            style = {   'margin-right': 'auto',
                        'margin-left': 'auto',
                        'max-width': '1024px',
                        'padding-right': '10px',
                        'padding-left': '10px',
                        'margin-top': '32px'},
        ),    
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
               
                        config={"displayModeBar": False},
                        figure={
            'data': [
                {'x': ['Total Blinks', 'Drowsiness Count','Yawn Count','Trips'], 'y': df.iloc[0,3:7].values, 'type': 'bar', 'name': 'Blinks'},

            ],
            'layout': {
                'title': "Driver: John Wick"
            }
        }, style={'width': '70%'}
                    ),
                    style = {    'margin-bottom': '24px',
                                 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)'},
                ),
                
            ],
            style = {   'margin-right': 'auto',
                        'margin-left': 'auto',
                        'max-width': '1024px',
                        'padding-right': '10px',
                        'padding-left': '10px',
                        'margin-top': '32px'},
        ), 
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
               
                        config={"displayModeBar": False},
                        figure={
            'data': [
                {'x': ['Total Blinks', 'Drowsiness Count','Yawn Count','Trips'], 'y': df.iloc[1,3:7].values, 'type': 'bar', 'name': 'Blinks'},

            ],
            'layout': {
                'title': "Driver: Vishal"
            }
        }, style={'width': '70%'}
                    ),
                    style = {    'margin-bottom': '24px',
                                 'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)'},
                ),
                
            ],
            style = {   'margin-right': 'auto',
                        'margin-left': 'auto',
                        'max-width': '1024px',
                        'padding-right': '10px',
                        'padding-left': '10px',
                        'margin-top': '32px'},
        ),                     
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)