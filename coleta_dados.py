import pandas as pd
import requests
import io
from datetime import datetime
import os

def baixar_historico_2025():
    print("--- INICIANDO ROBÔ (FONTE: Football-Data.co.uk) ---")
    
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
        
        # 2. Filtrar apenas 2025
        df['Ano'] = df['Date'].dt.year
        df_2025 = df[df['Ano'] == 2025].copy()
        
        if df_2025.empty:
            print("⚠️ Aviso: Jogos de 2025 não encontrados no arquivo fonte.")
            return

        # 3. Selecionar e Traduzir Colunas
        df_final = df_2025[['Date', 'Time', 'Home', 'HG', 'AG', 'Away', 'Res']].copy()
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
        nome_arquivo = "brasileirao_2025_completo.csv"
        df_final.to_csv(nome_arquivo, index=False)

        print("\n" + "="*60)
        print(f"✅ SUCESSO! ARQUIVO GERADO: {nome_arquivo}")
        print(f"Total de jogos processados: {len(df_final)}")
        print("="*60)
        
        # Mostra uma amostra pequena no log só para confirmar
        print(df_final.tail().to_string(index=False)) 

    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        exit(1) # Isso avisa o GitHub que deu erro

if __name__ == "__main__":
    baixar_historico_2025()
