from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as og
from dados import DadosCripto

'''
Coluna          | Significado
                |
Date	        |A data da cotação (formato Ano-Mes-Dia).
Open	        |Preço de abertura da cripto no início do dia.
High	        |Maior preço registrado durante o dia.
Low	            |Menor preço registrado durante o dia.
Close           |Preço de fechamento (último preço do dia).
Adj Close       |Preço ajustado de fechamento (normalmente igual ao Close para criptos).
Volume	        |Volume negociado naquele dia (quantidade de criptos transacionada).
'''


class Dashboard:
    def __init__(self):
        self.app = Dash()
        self.cripto = DadosCripto("dados/BTC_USD_daily_data.csv")
        self.dados_cripto = self.cripto.retornar_todo_df()
        self.tipo_cripto = self.cripto.retornar_tipo_da_cripto

    def abrir_grafico(self):
        try:
            fig = og.Figure()
            fechamento = self.cripto.retornar_todo_df("Close")
            fig.add_trace(og.Scatter(
                x= self.dados_cripto["Date"], y=round(fechamento,2),
                mode='lines',
                name='Preço da Cripto',
                line=dict(color='blue')
            ))
            return fig
        except:
            return None

    def layout(self):
        grafico = self.abrir_grafico()
        self.app.layout = html.Div(children=[
            html.H1(children='Grafico do valor das cripitos'),
            html.Div(children=""),
            dcc.Dropdown(id="selecionar_cripto",
                         options=[
                             {'label': "Binance (BNB)", 'value': 'dados/BNB_USD_daily_data.csv'},
                             {'label': "Bitcoin (BTC)", 'value': 'dados/BTC_USD_daily_data.csv'},
                             {'label': "Ethereum (ETH)", 'value': 'dados/ETH_USD_daily_data.csv'},
                             {'label': "Solana (SOL)", 'value': 'dados/SOL_USD_daily_data.csv'},
                             {'label': "XRP (XRP)", 'value': 'dados/XRP_USD_daily_data.csv'}],
                         value='dados/BTC_USD_daily_data.csv',
                         ),
            dcc.Graph(
                id='grafico_criptos',
                figure= self.abrir_grafico()
            )
        ])
        self.__callback()

    def __callback(self):
        @self.app.callback(
            Output("grafico_criptos", "figure"),
            Input("selecionar_cripto", "value")
        )
        def escolher_tipo_da_cripto(value):
            self.cripto = DadosCripto(value)
            self.dados_cripto = self.cripto.retornar_todo_df()
            self.tipo_cripto = self.cripto.retornar_tipo_da_cripto
            return self.abrir_grafico()
    def abrir_janela(self):
        self.layout()
        self.app.run(debug=True)
