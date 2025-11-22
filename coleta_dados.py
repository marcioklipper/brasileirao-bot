import pandas as pd
import requests
import io

def baixar_historico_2025():
    print("--- BAIXANDO BASE DE DADOS DE 2025 ---")
    
    # Fonte alternativa muito robusta (Football-Data.co.uk)
    # Eles mantêm arquivos CSV limpos de várias ligas, incluindo o Brasil
    url_csv = "https://www.football-data.co.uk/new/BRA.csv"
    
    try:
        print(f"1. Baixando arquivo: {url_csv}")
        s = requests.get(url_csv).content
        
        # Lê o CSV
        df = pd.read_csv(io.StringIO(s.decode('utf-8')))
        
        print(f"2. Arquivo baixado. Total de linhas históricas: {len(df)}")
        
        # --- TRATAMENTO INTELIGENTE DE DADOS ---
        
        # 1. Converter coluna de data (O padrão deles costuma ser dd/mm/yyyy)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
        
        # 2. Criar coluna de Ano
        df['Ano'] = df['Date'].dt.year
        
        # 3. FILTRAR APENAS 2025
        # (Como estamos em Nov/2025, isso deve trazer quase todo o campeonato)
        df_2025 = df[df['Ano'] == 2025].copy()
        
        if len(df_2025) == 0:
            print("⚠️ Aviso: O arquivo baixado ainda não contém jogos registrados com a data '2025'.")
            print("Verificando anos disponíveis no arquivo:", df['Ano'].unique())
            return None

        # 4. Selecionar e Renomear Colunas para Português
        # O arquivo padrão tem: Date, Time, Home, Away, HG (Home Goals), AG (Away Goals), Res (Result)
        df_final = df_2025[['Date', 'Time', 'Home', 'HG', 'AG', 'Away', 'Res']].copy()
        
        df_final.columns = ['Data', 'Hora', 'Mandante', 'Gols_Mandante', 'Gols_Visitante', 'Visitante', 'Resultado']
        
        # Formatar a data para ficar bonita (dd/mm/aaaa)
        df_final['Data'] = df_final['Data'].dt.strftime('%d/%m/%Y')

        print("\n" + "="*60)
        print(f"✅ HISTÓRICO 2025 RECUPERADO COM SUCESSO!")
        print(f"Total de jogos encontrados: {len(df_final)}")
        print("="*60)
        print(df_final.tail(15).to_string(index=False)) # Mostra os últimos 15 jogos
        print("="*60)
        
        # Salva o arquivo pronto
        df_final.to_csv("brasileirao_2025_completo.csv", index=False)
        return df_final

    except Exception as e:
        print(f"❌ Erro ao processar: {e}")
        # Se der erro, imprime as colunas para a gente saber o nome certo
        try:
            print("Colunas disponíveis no arquivo:", df.columns.tolist())
        except:
            pass

# Executar
df = baixar_historico_2025()

pd.set_option('display.max_rows', None)

print("LISTA COMPLETA DE JOGOS:")
print(df)
