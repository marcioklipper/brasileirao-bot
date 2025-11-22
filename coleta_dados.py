import soccerdata as sd
import pandas as pd
from datetime import datetime
import os

# Configurações
os.environ["SOC_CACHE"] = "e" 

def atualizar_brasileirao():
    print("--- INICIANDO ROBÔ ---")
    
    try:
        # 1. Conecta à ESPN
        print("1. Conectando à ESPN...")
        espn = sd.ESPN(leagues="BRA-Serie A", seasons=["2024", "2025"])
        
        # 2. Baixa a tabela
        print("2. Baixando dados...")
        schedule = espn.read_schedule(force_cache=True)
        
        # 3. Limpa e seleciona colunas
        df_jogos = schedule.reset_index()
        # Aqui selecionamos as colunas mais importantes
        df_jogos = df_jogos[['date', 'season', 'round', 'home_team', 'home_score', 'away_score', 'away_team', 'game_id']]
        
        # --- AQUI ESTÁ A PRÉ-VISUALIZAÇÃO ---
        print("\n" + "="*50)
        print("PRÉ-VISUALIZAÇÃO DOS DADOS (Primeiras 5 linhas):")
        print("="*50)
        # O .to_string() força o python a mostrar todas as colunas sem cortar
        print(df_jogos.head().to_string()) 
        print("="*50 + "\n")
        # ------------------------------------

        # 4. Salva
        df_jogos.to_csv("resultados_brasileirao.csv", index=False)
        print("✅ Arquivo salvo com sucesso!")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    atualizar_brasileirao()
