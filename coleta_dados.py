import soccerdata as sd
import pandas as pd
from datetime import datetime
import os

# Configuração para o robô
os.environ["SOC_CACHE"] = "e" 

def atualizar_brasileirao():
    print("--- INICIANDO ROBÔ (FOTMOB) ---")
    
    try:
        # 1. Conecta ao FOTMOB (Fonte muito mais rápida e estável)
        print("1. Conectando ao servidor do FotMob...")
        # O FotMob geralmente aceita bem o código BRA-Serie A
        fotmob = sd.FotMob(leagues="BRA-Serie A", seasons=["2025"])
        
        # 2. Baixa a tabela de jogos
        print("2. Baixando tabela de jogos...")
        schedule = fotmob.read_schedule()
        
        # 3. Limpeza e Organização
        print("3. Organizando dados...")
        df_jogos = schedule.reset_index()
        
        # Seleciona colunas úteis (O FotMob traz nomes ligeiramente diferentes)
        # Vamos garantir que pegamos data, times e placar
        colunas_desejadas = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'round', 'game_id']
        
        # Filtra apenas as colunas que existem no resultado
        cols_finais = [c for c in colunas_desejadas if c in df_jogos.columns]
        df_final = df_jogos[cols_finais]

        # --- PRÉ-VISUALIZAÇÃO NO LOG ---
        print("\n" + "="*50)
        print("AMOSTRA DOS DADOS BAIXADOS:")
        print(df_final.tail(5).to_string()) # Mostra os últimos 5 jogos
        print("="*50 + "\n")
        # -------------------------------

        # 4. Salva o arquivo
        df_final.to_csv("resultados_brasileirao.csv", index=False)
        print("✅ SUCESSO! Arquivo 'resultados_brasileirao.csv' salvo.")

    except Exception as e:
        print(f"❌ Erro: {e}")
        # Se der erro, mostra detalhes para ajustarmos
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    atualizar_brasileirao()
