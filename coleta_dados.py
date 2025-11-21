import soccerdata as sd
import pandas as pd
from datetime import datetime
import os

# Configuração para evitar bloqueios e gerenciar cache
os.environ["SOC_CACHE"] = "e" 

def atualizar_brasileirao():
    print("Iniciando coleta de dados do FBref...")
    
    # 1. Conecta ao FBref (fonte gratuita)
    # Puxa dados de 2024 e 2025 (para garantir histórico e futuro)
    fbref = sd.FBref(leagues="BRA-Serie A", seasons=["2024", "2025"])
    
    # 2. Baixa a tabela de jogos (Placares)
    print("Baixando tabela de jogos...")
    schedule = fbref.read_schedule(force_cache=True)
    
    # 3. Tenta baixar detalhes (Quem fez o gol)
    try:
        print("Baixando detalhes das partidas...")
        match_stats = fbref.read_player_match_stats(stat_type="summary", force_cache=True)
        match_stats.to_csv("detalhes_gols_jogadores.csv")
    except Exception as e:
        print(f"Aviso: Detalhes ainda não disponíveis ou erro na coleta: {e}")

    # 4. Salva o arquivo principal
    schedule.to_csv("resultados_brasileirao.csv")
    print(f"Sucesso! Dados salvos em {datetime.now()}")

if __name__ == "__main__":
    atualizar_brasileirao()
