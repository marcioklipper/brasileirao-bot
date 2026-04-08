import pandas as pd
import requests
import io
from datetime import datetime

def baixar_historico_2026():
    print("\n--- INICIANDO ROBÔ (FONTE: Football-Data.co.uk) ---")
    
    # URL estável que não bloqueia robôs
    url_csv = "https://www.football-data.co.uk/new/BRA.csv"
    
    try:
        print(f"1. Baixando arquivo bruto...")
        headers = {'User-Agent': 'Mozilla/5.0'} # Boa prática simples
        s = requests.get(url_csv, headers=headers).content
        
        # Lê o CSV
        df = pd.read_csv(io.StringIO(s.decode('utf-8')))
        
        # 1. Converter data
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        
        # 2. Filtrar apenas 2026
        df['Ano'] = df['Date'].dt.year
        df_2026 = df[df['Ano'] == 2026].copy()
        
        if df_2026.empty:
            print("⚠️ Aviso: Jogos de 2026 não encontrados no arquivo fonte.")
            print("Isso é comum se o campeonato ainda não começou ou os dados não foram atualizados na fonte.")
            return

        # 3. Selecionar e Traduzir Colunas
        df_final = df_2026[['Date', 'Time', 'Home', 'HG', 'AG', 'Away', 'Res']].copy()
        df_final.columns = ['Data', 'Hora', 'Mandante', 'Gols_Mandante', 'Gols_Visitante', 'Visitante', 'Resultado']
        
        # --- TRADUÇÃO H/A/D ---
        mapa_resultado = {
            'H': 'Mandante', # Home Win
            'A': 'Visitante',# Away Win
            'D': 'Empate'    # Draw
        }
        df_final['Resultado'] = df_final['Resultado'].map(mapa_resultado)
        # ----------------------

        # Formatação final da data
        df_final['Data'] = df_final['Data'].dt.strftime('%d/%m/%Y')

        # 4. Salvar Arquivo
        nome_arquivo = "brasileirao_2026_completo.csv"
        df_final.to_csv(nome_arquivo, index=False)

        print("\n" + "="*60)
        print(f"✅ SUCESSO! ARQUIVO GERADO: {nome_arquivo}")
        print(f"Total de jogos processados: {len(df_final)}")
        print("="*60)
        
        # Mostra uma amostra pequena no log só para confirmar
        print(df_final.tail().to_string(index=False)) 

    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        exit(1) # Isso avisa o GitHub/Terminal que deu erro

if __name__ == "__main__":
    # O robô aguarda um comando explícito para rodar
    print("Robô pronto para execução.")
    comando = input("Digite 'rodar' e pressione Enter para iniciar a extração: ").strip().lower()
    
    if comando == 'rodar':
        baixar_historico_2026()
    else:
        print("Comando não reconhecido ou execução cancelada. Encerrando...")
