import plotly.graph_objects as go

def myLineChart(df, title='Chart'):
    candlestick = go.Scatter(x=df['date'],  y=df['close'])


    myline = go.Scatter(x=df['date'],y=df['close'])

    peaksDf = df[df.peaks.eq(1)]
    peaks = go.Scatter(x=peaksDf['date'],y=peaksDf['close'], mode='markers', marker_color='rgb(0,255,0)')

    dipsDf = df[df.dips.eq(1)]
    dips = go.Scatter(x=dipsDf['date'],y=dipsDf['close'], mode='markers', marker_color='rgb(255,0,0)')


    divs1 = df[df.rsi_divergence.eq(1)]
    divs1s = go.Scatter(x=divs1['date'],y=divs1['close'], mode='markers', marker_color='rgb(0,0,255)')


    fig = go.Figure(data=[candlestick,myline,peaks, dips, divs1s])
    fig.update_layout(
    title={
        'text': title,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    fig.show()