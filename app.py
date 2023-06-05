import whisper
import pandas as pd
from pytube import YouTube as yt

import dash_mantine_components as dmc
from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output, State

app = Dash(__name__)

#--------------Layout and Styling--------------#

app.layout = html.Div([
    # Header and logo
    dmc.Title(
        children=[
            html.Img(
                src='assets/logo.png',
                style={'width': '30px', 'height': '30px', 'vertical-align': 'middle',
                       'margin-right': '10px', 'margin-bottom': '7px'}
            ),
            'YouTube Transcriber'
        ],
        order=1,
        align='center',
        color='red'
    ),
    # YouTube URL text input
    dmc.TextInput(
        id='youtube-url-input',
        style={'width': '400px'},
        placeholder='Enter YouTube URL',
        type='url'),
    # Loading indicator, appears whenever anything is still processing
    dcc.Loading(
        id='table-loading',
        color='red',
        children=[
            # DataTable via Dash, houses transcription text and segment timestamps
            dash_table.DataTable(
            id='transcription-table',
            columns=[{'name': i, 'id': i} for i in ['Segment Start',
                                                    'Segment End',
                                                    'Transcription']],
            style_table={'width': '100%', 'margin-top': '20px'},  
            style_cell={'padding': '10px', 'text-align': 'left', 'white-space': 'normal',
                        'height': 'auto', 'font-family': 'sans-serif'},
            style_header={'font-weight': 'bold'},
            page_size=20),
            # Download fetches and delivers CSV payload when clicked, disabled when no data is present
            dmc.Button('Download as CSV', id='csv-download-button', disabled=True,
                       color='red', style={'margin-top': '5px'}),
            dcc.Download(id='download-csv')
            ]       
        )
    ]
)

#--------------Callbacks and Functions--------------#

@app.callback(
    Output('transcription-table', 'data'),
    Input('youtube-url-input', 'value'),
    prevent_initial_call=True
)

def process_input(youtube_url):
    '''
    Processes the input YouTube URL and transcribe the audio using OpenAI Whisper transcription engine.
    Uses 'base' model and sets fp16=False to suppress CPU warnings. Segment columns are changed
    from a running tally of seconds to HH:MM:SS timestamps.
    
    Args:
        youtube_url (str): The URL of the YouTube video to be transcribed.
    
    Returns:
        dict: Collection of key-value pairs with renamed keys 'Segment Start', 'Segment End', and 'Transcription'.
    '''
    if youtube_url:
        # Audio pull and Whisper transcription
        audio_file = yt(youtube_url).streams.filter(only_audio=True).first().download(filename='yt_audio.mp4')
        whisper_model = whisper.load_model('base')
        transcription = whisper_model.transcribe(audio_file, fp16=False)
        
        # Data manipulation
        df = pd.DataFrame(transcription['segments'], columns=['start', 'end', 'text'])
        df['start'] = pd.to_datetime(df['start'], unit='s').dt.strftime('%H:%M:%S')
        df['end'] = pd.to_datetime(df['end'], unit='s').dt.strftime('%H:%M:%S')
        df = df.rename(columns={'start': 'Segment Start', 'end': 'Segment End', 'text': 'Transcription'})
        data = df.to_dict('records')
        return data

@app.callback(
    Output('download-csv', 'data'),
    Input('csv-download-button', 'n_clicks'),
    State('transcription-table', 'data'),
    State('youtube-url-input', 'value'),
    prevent_initial_call=True
)

def download_csv(n_clicks, data, youtube_url):
    '''
    Download the data as a CSV file via button click.
    
    Args:
        n_clicks (int): Button click tracking.
        data (list): A list of dictionaries containing the transcriptions.
        youtube_url (str): The URL of the YouTube video used to gather the video title.
    
    Returns:
        dict: DataFrame content (base64 encoded), uses string sender when 'to_csv' writer is used.
    '''
    if n_clicks and data:
        video_title = yt(youtube_url).title
        df = pd.DataFrame(data)
        # File name is the title of the video for tracking and convenience
        csv = dcc.send_data_frame(df.to_csv, filename=video_title + '.csv')
        return csv
    
@app.callback(
    Output('csv-download-button', 'disabled'),
    Input('transcription-table', 'data'),
    prevent_initial_call=True
)

def enable_download_button(data):
    '''
    The 'Download as CSV' button is disabled by default, this just enables it when there is
    something to download.
    '''
    return not bool(data)

#--------------Initialization--------------#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
