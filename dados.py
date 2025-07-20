import pandas as pd
import logging


class DadosCripto:
    def __init__(self, tipo_da_cripto_csv):
        self.tipo_cripito = tipo_da_cripto_csv
        self.dados = pd.read_csv(tipo_da_cripto_csv)
        self.dia_da_cripto = self.dados["Date"]
        self.valor_MAX = self.dados["High"]
        self.valor_MIN = self.dados["Low"]
        self.valor_inicial_diario = self.dados["Open"]
        self.valor_final_diario = self.dados["Close"]

    def valores_por_data_especifica(self, dia, mes, ano):
        ''' essa função retorna todas as informações de valores de um dia especifico, tais informações com
        valor que a cripto teve no inicio do dia, valor que a cripto teve np fim do dia, maior valor que a cripto teve no dia,
        menor valor que a cripto teve no dia
        '''

        data_especifica = self.__organizar_data(dia=dia, mes=mes, ano=ano)
        valores_do_dia = self.dados.loc[self.dia_da_cripto == data_especifica]

        valor_inicial_diario = valores_do_dia["Open"]
        valor_final_diario = valores_do_dia["Close"]
        maior_valor_diario = valores_do_dia["High"]
        menor_valor_diario = valores_do_dia["Low"]

        valor_inicial_diario = round(valor_inicial_diario, 2)
        valor_final_diario = round(valor_final_diario, 2)
        return list(map(float, valor_inicial_diario)), list(map(float, valor_final_diario)), list(
            map(float, maior_valor_diario)), list(map(float, menor_valor_diario))

    def __organizar_data(self, dia, mes, ano, retornar_quantidade_de_dias_do_mes=None):
        ''' essa função é responsavel por organizar as datas informadas nas demais funções em forma de string
         e de forma que seja compativel com a organização dos data frames utilizados no codigo
        '''
        dia, mes, ano = map(int, (dia, mes, ano))
        if (dia < 10) and (mes < 10):   data_organizada = f"{str(ano)}-0{str(mes)}-0{str(dia)}"
        if (dia < 10) and (mes >= 10):   data_organizada = f"{str(ano)}-{str(mes)}-0{str(dia)}"
        if (dia >= 10) and (mes < 10):  data_organizada = f"{str(ano)}-0{str(mes)}-{str(dia)}"
        if (dia >= 10) and (mes >= 10): data_organizada = f"{str(ano)}-{str(mes)}-{str(dia)}"

        # --- logica que vai verificar a quantidade de dias do mes ---
        if retornar_quantidade_de_dias_do_mes != None:
            bixesto = False
            meses_de_31_dias = [1, 3, 5, 7, 8, 10, 12]

            if (ano % 4 == 0):
                bixesto = True

            if mes in meses_de_31_dias:
                limite_de_dias_por_mes = 32
            elif (mes not in meses_de_31_dias) and (mes != 2):
                limite_de_dias_por_mes = 31
            elif (mes == 2) and (bixesto == False):
                limite_de_dias_por_mes = 29
            else:
                limite_de_dias_por_mes = 30

            return limite_de_dias_por_mes

        return data_organizada

    def valores_de_um_mes_inteiro(self, mes, ano, df_inteiro=None):
        '''
        essa função retorna todos os valores diarios de um mes de um ano espefico
        inputs = mes, anos, df_inteiro (opcional, caso queira que a função retorne o dataframe inteiro do mes)
        output = datas, valores finais diarios, valores iniciais diarios
        '''
        # --- variaveis que vão guardar valores espeficios do mes ---
        valor_inicial_diario = []
        valor_final_diario = []
        datas_dos_valores = []

        limite_de_dias_por_mes = self.__organizar_data(0, 0, 0, 0)
        for i in range(1, limite_de_dias_por_mes, 1):
            try:
                data_loop = self.__organizar_data(dia=i, mes=mes, ano=ano)
                valor_do_loop = self.dados.loc[self.dia_da_cripto == data_loop]
                valor_inicial_diario.append(round(valor_do_loop["Open"].iloc[0], 2))
                valor_final_diario.append(round(valor_do_loop["Close"].iloc[0], 2))
                datas_dos_valores.append(valor_do_loop["Date"].iloc[0])
            except:
                logging.warning(f"erro ao guardar informações do dia {i}")
                pass
        if df_inteiro != None: return valor_do_loop

        valor_inicial_diario_exato = list(map(float, valor_inicial_diario))
        valor_final_diario_exato = list(map(float, valor_final_diario))

        return list(datas_dos_valores), list(valor_inicial_diario_exato), list(valor_final_diario_exato)

    def valores_de_um_ano_inteiro(self, ano, df_inteiro):
        # --- variaveis que vão guardar valores espeficios do mes ---
        valor_inicial_diario = []
        valor_final_diario = []
        datas_dos_valores = []
        for j in range(1, 13, 1):
            limite_de_dias_por_mes = self.__organizar_data(0, 0, 0, 0)
            for i in range(1, limite_de_dias_por_mes + 1, 1):
                try:
                    data_loop = self.__organizar_data(dia=i, mes=j, ano=ano)
                    valor_do_loop = self.dados.loc[self.dia_da_cripto == data_loop]
                    valor_inicial_diario.append(round(valor_do_loop["Open"].iloc[0], 2))
                    valor_final_diario.append(round(valor_do_loop["Close"].iloc[0], 2))
                    datas_dos_valores.append(valor_do_loop["Date"].iloc[0])
                except:
                    logging.warning(f"erro ao guardar informações do dia {i} do mes {j}")
                    pass

        if df_inteiro != None: return valor_do_loop

        valor_inicial_diario_exato = list(map(float, valor_inicial_diario))
        valor_final_diario_exato = list(map(float, valor_final_diario))

        return list(datas_dos_valores), list(valor_inicial_diario_exato), list(valor_final_diario_exato)

    def valores_entre_datas(self, dia_inicio, mes_inicio, ano_inicio, dia_fim, mes_fim, ano_fim):
        '''
        essa funçãos retorna o dataframe inteiro entre datas
        '''

        guardar_valores_diarios_finais = []
        guardar_valores_diarios_iniciais = []
        guardar_datas = []

        data_final = self.__organizar_data(dia_fim, mes_fim, ano_fim)
        data_lida_atualmente = 0
        controle_dos_loops = 0
        while True:
            if data_lida_atualmente == data_final: break
            if controle_dos_loops == 0:
                for j in range(mes_inicio, 12, 1):
                    limite_de_dias_do_mes = self.__organizar_data(0, 0, 0, 0)
                    for i in range(dia_inicio, limite_de_dias_do_mes, 1):
                        try:
                            if data_lida_atualmente == data_final: break
                            data_lida_atualmente = self.__organizar_data(i, j, ano_inicio)
                            df_do_periodo = self.dados.loc[self.dia_da_cripto == data_lida_atualmente]
                            guardar_datas.append(df_do_periodo["Date"].iloc[0])
                            guardar_valores_diarios_iniciais.append(df_do_periodo["Open"].iloc[0])
                            guardar_valores_diarios_finais.append(df_do_periodo["Close"].iloc[0])
                        except:
                            pass
                controle_dos_loops += 1
            else:
                for j in range(1, 12, 1):
                    limite_de_dias_do_mes = self.__organizar_data(0, 0, 0, 0)
                    if data_lida_atualmente == data_final: break
                    for i in range(1, limite_de_dias_do_mes, 1):
                        try:
                            if data_lida_atualmente == data_final: break
                            data_lida_atualmente = self.__organizar_data(i, j, ano_inicio + controle_dos_loops, None)
                            df_do_periodo = self.dados.loc[self.dia_da_cripto == data_lida_atualmente]
                            guardar_datas.append(df_do_periodo["Date"].iloc[0])
                            guardar_valores_diarios_iniciais.append(round(df_do_periodo["Open"].iloc[0], 2))
                            guardar_valores_diarios_finais.append(round(df_do_periodo["Close"].iloc[0], 2))
                        except:
                            pass
                controle_dos_loops += 1
        logging.info(data_lida_atualmente, data_final)
        guardar_valores_diarios_finais_limpo = list(map(float, guardar_valores_diarios_finais))
        guardar_valores_diarios_iniciais_limpo = list(map(float, guardar_valores_diarios_iniciais))

        return list(guardar_datas), list(guardar_valores_diarios_iniciais_limpo), list(
            guardar_valores_diarios_finais_limpo)

    def retornar_todo_df(self, coluna=None):
        match coluna:
            case "Date":
                return self.dia_da_cripto
            case "Close":
                return self.valor_final_diario
            case "Open":
                return self.valor_inicial_diario
            case "High":
                return self.valor_MAX
            case "Low":
                return self.valor_MIN
            case _:
                return self.dados

    def retornar_tipo_da_cripto(self):
        match self.tipo_cripito:
            case 'BNB_USD_daily_data.csv':
                return "Binance (BNB)"
            case "BTC_USD_daily_data.csv":
                return "Bitcoin (BTC)"
            case 'ETH_USD_daily_data.csv':
                return "Ethereum (ETH)"
            case "SOL_USD_daily_data.csv":
                return "Solana (SOL)"
            case "XRP_USD_daily_data.csv":
                return "XRP ()"


if __name__ == "__main__":
    teste = DadosCripto("dados/BTC_USD_daily_data.csv")
    data, valores_iniciais, valores_finais = teste.valores_entre_datas(23, 2, 2018, 27, 7, 2019)
    print(f"dias: {data}\nvalor inicial do dia:{valores_iniciais}\nvalor final do dia:{valores_finais}")
