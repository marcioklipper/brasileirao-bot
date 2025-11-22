import requests
import pandas as pd
from datetime import datetime
import json
import time

def atualizar_brasileirao_direto():
    print("--- INICIANDO COLETA DIRETA (SEM LIBRARY) ---")
    
    # ID do Brasileirão Série A no FotMob é 268
    # ID da Temporada 2024 (o calendário 2025 ainda não saiu na API, usaremos 2024 para teste)
    url = "https://www.fotmob.com/api/leagues?id=268&season=2024"
    
    # Truque: Fingir que somos um navegador Chrome comum para não ser bloqueado
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        print("1. Acessando API do FotMob direto...")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Erro ao acessar site: {response.status_code}")
            return

        data = response.json()
        
        # O FotMob entrega os jogos dentro de 'matches' -> 'allMatches'
        print("2. Processando dados recebidos...")
        todos_jogos = data['matches']['allMatches']
        
        lista_jogos = []
        
        for jogo in todos_jogos:
            # Extraindo dados com segurança
            data_jogo = jogo.get('pageUrl', '').split('/')[2] if 'pageUrl' in jogo else '' # Tenta pegar data da URL
            # Ou converte timestamp se disponível
            
            linha = {
                'Rodada': jogo.get('round', ''),
                'Data_Hora': jogo.get('status', {}).get('utcTime', ''),
                'Status': 'Finalizado' if jogo.get('status', {}).get('finished') else 'Agendado',
                'Time_Mandante': jogo.get('home', {}).get('name', ''),
                'Gols_Mandante': jogo.get('home', {}).get('score', 0),
                'Gols_Visitante': jogo.get('away', {}).get('score', 0),
                'Time_Visitante': jogo.get('away', {}).get('name', ''),
                'ID_Jogo': jogo.get('id', '')
            }
            lista_jogos.append(linha)

        # Cria Tabela
        df = pd.DataFrame(lista_jogos)
        
        # Tratamento de Data (opcional, para ficar bonito)
        try:
            df['Data_Hora'] = pd.to_datetime(df['Data_Hora']).dt.strftime('%d/%m/%Y %H:%M')
        except:
            pass

        # --- PRÉ-VISUALIZAÇÃO ---
        print("\n" + "="*50)
        print(f"Foram encontrados {len(df)} jogos.")
        print("AMOSTRA (Últimos 5 jogos):")
        print(df.tail(5).to_string())
        print("="*50 + "\n")
        # ------------------------

        # Salva
        df.to_csv("resultados_brasileirao.csv", index=False)
        print("✅ SUCESSO! Arquivo salvo.")

    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    atualizar_brasileirao_direto()
