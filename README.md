# Dashboard de Preços de Criptomoedas

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Dash](https://img.shields.io/badge/Dash-v2.0-orange)
![Plotly](https://img.shields.io/badge/Plotly-v5.0-purple)

---

## Descrição

Este projeto consiste em um dashboard interativo para visualização histórica dos preços de várias criptomoedas populares, como Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB), Solana (SOL) e XRP (XRP).  

Utilizando a biblioteca **Dash** para interface web e **Plotly** para gráficos, o dashboard permite ao usuário selecionar diferentes criptomoedas e filtrar os dados por intervalos de datas específicos. Os dados históricos são carregados a partir de arquivos CSV contendo informações diárias de preço.

---

## Funcionalidades

- Visualização gráfica do histórico de preços (preço de fechamento) das criptomoedas.
- Seleção da criptomoeda desejada através de um dropdown.
- Filtro para escolher intervalo de datas para análise.
- Gráficos responsivos e com estilo escuro para melhor experiência visual.

---

## Tecnologias Utilizadas

- [Python 3.8+](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/) - manipulação e tratamento de dados.
- [Dash](https://dash.plotly.com/) - framework para construção da interface web.
- [Plotly](https://plotly.com/python/) - geração dos gráficos interativos.
- [Logging](https://docs.python.org/3/library/logging.html) - para registro de logs e erros.

---

## Estrutura do Projeto

- |`dados/` — pasta contendo os arquivos CSV com os dados históricos das criptomoedas.
    -|`BNB_USD_daily_data.csv`- dados da cripto moeda binance
    -|`BTC_USD_daily_data.csv`- dados da cripto moeda bitcoin
    -|`ETH_USD_daily_data.csv`- dados da cripto moeda etherium
    -|`SOL_USD_daily_data.csv`- dados da cripto moeda solana
    -|`XRP_USD_daily_data.csv`- dados da cripto moeda xrp
- |`graficos.py` — módulo com a classe `Dashboard` que implementa a interface gráfica e os gráficos.
- |`dados.py` — módulo com a classe `DadosCripto` responsável pelo carregamento e manipulação dos dados CSV.
- |`main.py` — script principal que inicializa e executa o dashboard.

---

## Como usar

1. Clone o projeto:  
   `git clone <url-do-repositorio>`

2. Crie e ative um ambiente virtual (opcional, mas recomendado):  
   - Linux/macOS: `python -m venv venv && source venv/bin/activate`  
   - Windows: `python -m venv venv && venv\Scripts\activate`

3. Instale as dependências:  
   `pip install pandas dash plotly`

4. Rode o dashboard:  
   `python main.py`

5. Abra o navegador e acesse:  
   `http://127.0.0.1:8050`

---

## Imagens do programa

### Tela Inicial
![Tela Inicial](assets/graficoentredatas.png)

### grafico entre datas
![Grafico entre datas](assets/graficoentredatas.png)

