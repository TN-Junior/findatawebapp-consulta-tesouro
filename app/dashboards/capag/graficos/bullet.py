import plotly.graph_objects as go


def bullet(titulo, valor, limite):
    fig = go.Figure(go.Indicator(
        mode="gauge",
        value=valor,
        domain={'x': [0.3, 1], 'y': [0.2, 1]},
        title=titulo,
        # delta = {'reference': 200},
        gauge={
            'shape': "bullet",
            'axis': {'range': [None, limite * 1.1]},
            'threshold': {
                'line': {'color': "blue", 'width': 2},
                'thickness': 1,
                'value': limite},
            'steps': [
                {'range': [0, limite], 'color': "lightgray"},
                {'range': [limite, limite * 1.1],
                 'color': "#FA8072"}]}))
    fig.update_layout(height=200)
    return fig
