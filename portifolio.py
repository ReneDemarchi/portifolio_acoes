import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


combinacao = pd.read_csv('combinacoes_1000.csv')
dados_combinacao = combinacao.to_dict(orient='records')
df = pd.read_excel('1.Cotações Diárias Atividade 1.xlsx')
dados = df.to_dict(orient='records')
lista_alp = []
lista_brf = []
lista_cemig = []
lista_embraer = []
lista_marfrig = []


for inx ,linha in enumerate(dados):
    if inx == 0:
        pass
    else:
        valor_alpargatas = dados[inx]['Alpargatas ON']/dados[inx-1]['Alpargatas ON']-1
        valor_BRF = dados[inx]['BRF SA ON']/dados[inx-1]['BRF SA ON']-1
        valor_cemig = dados[inx]['Cemig ON'] / dados[inx - 1]['Cemig ON'] - 1
        valor_embraer = dados[inx]['Embraer ON'] / dados[inx - 1]['Embraer ON'] - 1
        valor_marfrig = dados[inx]['Marfrig ON'] / dados[inx - 1]['Marfrig ON'] - 1
        lista_alp.append(valor_alpargatas)
        lista_brf.append(valor_BRF)
        lista_cemig.append(valor_cemig)
        lista_embraer.append(valor_embraer)
        lista_marfrig.append(valor_marfrig)
selic = (1 + 0.1365) ** (1/252) - 1
calculo = []


for idx, porcentagem in enumerate(dados_combinacao):
    retorno = []
    for linha in range(len(lista_alp)):
        retorno.append(
            porcentagem['Numero_1'] * lista_alp[linha] +
            porcentagem['Numero_2'] * lista_brf[linha] +
            porcentagem['Numero_3'] * lista_cemig[linha] +
            porcentagem['Numero_4'] * lista_embraer[linha] +
            porcentagem['Numero_5'] * lista_marfrig[linha]
        )
    valor = sum(retorno) / len(lista_alp)
    desvio = np.std(retorno, ddof=1)
    valor_desvio = {"Retorno Esperado": valor, 'Risco': desvio, 'Índice Sharpe': (valor - selic) / desvio, 'porcentagem Alpargatas ON': f'{porcentagem['Numero_1']}','porcentagem BRF SA ON': f'{porcentagem['Numero_2']}','porcentagem Cemig ON':f'{porcentagem['Numero_3']}','porcentagem Embraer ON':f'{porcentagem['Numero_4']}','porcentagem Marfrig ON':f'{porcentagem['Numero_5']}'}
    calculo.append(valor_desvio)



df_grafico = pd.DataFrame(calculo)
df_resultado_ordenado = df_grafico.sort_values(by="Índice Sharpe", ascending=False).reset_index(drop=True)
excel_path = "melhores_portfolios.xlsx"
df_resultado_ordenado.to_excel(excel_path, index=False)
plt.figure(figsize=(8,6))
plt.scatter(df_grafico['Risco'], df_grafico['Retorno Esperado'], c=df_grafico['Índice Sharpe'], cmap='viridis', s=10)
plt.colorbar(label='Índice Sharpe')
plt.xlabel('Risco (Desvio Padrão)')
plt.ylabel('Retorno Esperado')
plt.title('Portfólios - Retorno vs Risco vs Sharpe')
plt.xlim(left=0)
plt.axhline(y=selic, color='black', linestyle='--', linewidth=1.5, label=f'SELIC = {selic:.4f}')
melhor = df_grafico.loc[df_grafico['Índice Sharpe'].idxmax()]
plt.scatter(melhor['Risco'], melhor['Retorno Esperado'], color='red', s=10, label='Melhor Portfólio')
plt.legend()
png_path = "Portfolios_risco_retorno.png"
plt.savefig(png_path, dpi=300, bbox_inches='tight')
