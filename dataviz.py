#handling data using pandas
import pandas as pd
import plotly.express as px
from dash import Dash,dcc,html,Input,Output,callback
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
iotdb=myclient['uvt_iotdp']
temp_data=iotdb["temp"]
alarm_data=iotdb["alarm"]
motor_data=iotdb["motor"]
data_pnt=15

app =Dash(__name__)
app.layout=html.Div(
    [
        html.H1('UVT IoT Practicles',style={'color':'blue'}),
        html.H2('Demonstration for network students'),
        html.Div(
            [
                html.H1('temperature graph'),
                dcc.Graph(id="temp_graph")
            ]
        ),
        html.Div(
            [
                html.H1('alarm graph'),
                dcc.Graph(id="alarm_graph")
            ]
        ),
        html.Div(
            [
                html.H1('motor graph'),
                dcc.Graph(id="motor_graph")
            ]
        ),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,
            n_intervals=0
        )    
    ]   
)

@callback(Output('temp_graph','figure'),Input('interval-component','n_intervals'))
def update_temp_fig(n):
    data=list(temp_data.find()) if len(list(temp_data.find()))<data_pnt else list(temp_data.find())[-data_pnt:]
    data_frame=pd.DataFrame(data)
    temp_fig=px.line(data_frame,x="time",y="temp")
    return temp_fig

@callback(Output('alarm_graph','figure'),Input('interval-component','n_intervals'))
def update_alarm_fig(n):
    data=list(alarm_data.find()) if len(list(alarm_data.find()))<data_pnt else list(alarm_data.find())[-data_pnt:]
    alarm_df=pd.DataFrame(data)
    alarm_df['status'].replace({'on':1,'off':0},inplace=True)
    data_frame=pd.DataFrame(alarm_df)
    alarm_fig=px.scatter(data_frame,x="time",y="status")
    return alarm_fig

@callback(Output('motor_graph','figure'),Input('interval-component','n_intervals'))
def update_motor_fig(n):
    data=list(motor_data.find()) if len(list(motor_data.find()))<data_pnt else list(motor_data.find())[-data_pnt:]
    data_frame=pd.DataFrame(data)
    motor_fig=px.scatter(data_frame,x="time",y="speed")
    return motor_fig


if __name__=='__main__':
    app.run(debug=True)
    