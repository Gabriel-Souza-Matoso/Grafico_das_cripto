from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as og
from dash.exceptions import PreventUpdate
from dados import DadosCripto
import logging

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
# =-=-=- funções do style -=-=-=
'''
style = {
    # --- Geral ---
    'width': 'largura do elemento (ex: "100%", "400px")',
    'height': 'altura do elemento (ex: "100vh", "300px")',
    'padding': 'espaçamento interno (ex: "10px")',
    'margin': 'espaçamento externo (ex: "auto", "10px 20px")',
    'backgroundColor': 'cor de fundo (ex: "#1e1e1e", "red")',
    'color': 'cor do texto (ex: "white", "#00ffcc")',
    'fontSize': 'tamanho do texto (ex: "16px")',
    'fontWeight': 'peso da fonte ("normal", "bold", "lighter")',
    'textAlign': 'alinhamento de texto ("left", "center", "right")',
    'border': 'borda (ex: "1px solid white")',
    'borderRadius': 'arredondamento de cantos (ex: "8px")',
    'boxShadow': 'sombra externa (ex: "0 0 10px #00ffcc")',

    # --- Flexbox ---
    'display': '"flex" para ativar flexbox',
    'flexDirection': 'direção do conteúdo ("row" ou "column")',
    'justifyContent': 'alinhamento horizontal ("flex-start", "center", "flex-end", "space-between", "space-around", "space-evenly")',
    'alignItems': 'alinhamento vertical ("flex-start", "center", "flex-end", "stretch")',
    'gap': 'espaço entre elementos (ex: "10px")',

    # --- Grid ---
    'display': '"grid" para ativar grid layout',
    'gridTemplateColumns': 'define colunas (ex: "1fr 2fr 1fr")',
    'gridTemplateRows': 'define linhas (ex: "100px auto 50px")',
    'gridTemplateAreas': 'define áreas nomeadas (ex: "header header" "menu content")',
    'gridArea': 'nome da área para um elemento (ex: "header")',
    'rowGap': 'espaço entre linhas (ex: "10px")',
    'columnGap': 'espaço entre colunas (ex: "20px")',

    # --- Posicionamento absoluto ---
    'position': '"absolute", "relative", "fixed", "sticky"',
    'top': 'posição do topo (ex: "10px")',
    'bottom': 'posição inferior (ex: "20px")',
    'left': 'posição à esquerda (ex: "0")',
    'right': 'posição à direita (ex: "0")',
    'zIndex': 'ordem de empilhamento (ex: "10" acima de "1")'
}
'''

# --- inicio e fim das datas dos dataframes ----
'''
---- data minima ---
btc = 2014-09-17
bnb = 2017-11-09
eth = 2017-11-09
sol = 2020-04-10
xrp =  2017-11-09

--- data maxima ---
btc = 2024-09-08
bnb = 2024-09-08
eth = 2024-09-08
sol = 2024-09-08
xrp = 2024-09-08
'''


class Dashboard:
    def __init__(self):
        self.app = Dash()
        self.cripto = DadosCripto("dados/BTC_USD_daily_data.csv")
        self.dados_cripto = self.cripto.retornar_todo_df()
        self.tipo_cripto = self.cripto.retornar_tipo_da_cripto()
        self.data_inicial = None
        self.data_final = None
        self.df_valor_entre_datas = None
        self.grafico_entre_datas = False
        self.minimo_datas = {
            'Bitcoin (BTC)': '2014-09-17',
            'Binance (BNB)': '2017-11-09',
            'Ethereum (ETH)': '2017-11-09',
            'Solana (SOL)': '2020-04-10',
            'XRP (XRP)': '2017-11-09'
        }


    def abrir_grafico(self):
        try:
            # --- vai criar um grafico ---
            grafico = og.Figure()
            # --- vai deixar o grafico em formato de linha ---
            if self.grafico_entre_datas == False:
                grafico.add_trace(og.Scatter(
                    x=self.dados_cripto["Date"], y=self.dados_cripto["Close"].round(2),
                    mode='lines',
                    name='Preço da Cripto',
                    line=dict(color='#b0bec5', width=2, shape='spline')
                ))
            else:
                grafico.add_trace(og.Scatter(
                    x=self.df_valor_entre_datas["Date"], y=self.df_valor_entre_datas["Close"].round(2),
                    mode='lines',
                    name='Preço da Cripto',
                    line=dict(color='#b0bec5', width=2, shape='spline')
                ))
            tipo_cripto = self.cripto.retornar_tipo_da_cripto()
            logging.info(tipo_cripto)
            grafico.update_layout(
                title=f'Histórico de Preço da Criptomoeda {tipo_cripto}',
                xaxis_title='Data',
                yaxis_title='Preço (USD)',
                template='plotly_dark',
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
                font=dict(color='white', size=14))
            return grafico
        except:
            logging.warning("erro ao abrir grafico")

    def layout(self):
        self.app.layout = html.Div(
            children=[
                html.H1(
                    children='Grafico do valor das cripitos',
                    style={
                        'display': "flex",
                        'justifyContent': 'center',
                        'flexDirection': 'top',
                        'color': '#b0bec5'
                    }
                ),
                dcc.Dropdown(
                    id="selecionar_cripto",
                    options=[
                        {'label': "Bitcoin (BTC)", 'value': 'dados/BTC_USD_daily_data.csv'},
                        {'label': "Binance (BNB)", 'value': 'dados/BNB_USD_daily_data.csv'},
                        {'label': "Ethereum (ETH)", 'value': 'dados/ETH_USD_daily_data.csv'},
                        {'label': "Solana (SOL)", 'value': 'dados/SOL_USD_daily_data.csv'},
                        {'label': "XRP (XRP)", 'value': 'dados/XRP_USD_daily_data.csv'}
                    ],
                    value='dados/BTC_USD_daily_data.csv',
                    style={
                        "backgroundColor": "#b0bec4",
                        "color": "#1e1e1e"
                    }
                ),
                dcc.Graph(
                    id='grafico_criptos',
                    figure=self.abrir_grafico()
                ),
                html.H2(children="obter grafico entre datas (dia-mes-ano)",
                        style=self.retornar_estilo_fontes_centralizado()),
                dcc.DatePickerRange(
                    id="calendario_distancia_das_datas",
                    min_date_allowed= self.minimo_datas[self.cripto.retornar_tipo_da_cripto()],
                    max_date_allowed='2024-09-08',
                    start_date= None,
                    end_date=None,
                    display_format='YYYY/MM/DD',
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "backgroundColor": "#1e1e1e",
                        "color": "#1e1e1e"
                    }
                )
            ],
            style={
                'backgroundColor': "#1e1e1e",
                'color': "#1e1e1e",
                'padding': "100px",
                'gap': '30px'
            }
        )
        self.__callback_atualizar_grafico()

    def style_inputs_datas(self, input=None):
        if input == 1:
            style = {
                'color': "#1e1e1e",
                'marginRight': '0px',
                'marginLeft': '330px',
            }
        else:
            style = {
                'color': "#1e1e1e",
                'marginRight': '250px',
                'marginLeft': '300px'
            }
        return dict(style)

    def retornar_estilo_fontes_centralizado(self):
        style = {
            'display': 'flex',
            'justifyContent': 'center',
            'color': "#b0bec5",
        }
        return dict(style)

    def __callback_atualizar_grafico(self):
        @self.app.callback(
            Output('grafico_criptos', "figure"),
            Input("selecionar_cripto", "value"),
            Input("calendario_distancia_das_datas", "start_date"),
            Input("calendario_distancia_das_datas", "end_date")
        )
        def atualizar_grafico(cripto_path, data_inicio, data_final):
            self.cripto = DadosCripto(cripto_path)
            self.dados_cripto = self.cripto.retornar_todo_df()

            if data_inicio and data_final:
                self.df_valor_entre_datas = self.cripto.valores_entre_datas(
                    data_inicio, data_final
                )
                self.grafico_entre_datas = True
                print(self.grafico_entre_datas)
            else:
                self.grafico_entre_datas = False

            return self.abrir_grafico()

    def abrir_janela(self):
        self.layout()
        self.app.run(debug=True)
