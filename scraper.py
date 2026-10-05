import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_sve_dokumente():
    base_url = "https://gradcazin.gov.ba/dokumenti?page={}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    svi_dokumenti = []
    stranica = 0
    
    print("🚀 Pokrećem preuzimanje svih metapodataka sa sajta Grada Cazina...")
    
    while True:
        url = base_url.format(stranica)
        print(f"🔍 Skeniram stranicu {stranica + 1}...")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            tabela = soup.find('table', class_='cols-3')
            
            if not tabela or not tabela.find('tbody'):
                break
                
            redovi = tabela.find('tbody').find_all('tr')
            if not redovi:
                break
                
            for red in redovi:
                kolone = red.find_all('td')
                if len(kolone) == 3:
                    a_tag = kolone[0].find('a')
                    strong_tag = kolone[0].find('strong')
                    
                    naziv = strong_tag.text.strip() if strong_tag and strong_tag.text.strip() else (a_tag.text.strip() if a_tag else "Bez naziva")
                    link = "https://gradcazin.gov.ba" + a_tag['href'] if a_tag else ""
                    kategorija = kolone[1].text.strip()
                    godina = kolone[2].text.strip()
                    
                    svi_dokumenti.append({
                        "naziv": naziv,
                        "kategorija": kategorija,
                        "godina": godina,
                        "link": link
                    })
            
            stranica += 1
            time.sleep(1) # Pauza da ne opteretimo server
            
        except Exception as e:
            print(f"❌ Greška: {e}")
            break

    # Čuvanje u CSV fajl
    df = pd.DataFrame(svi_dokumenti)
    df.to_csv('data.csv', index=False, encoding='utf-8-sig')
    print(f"\n✅ GOTOVO! Sačuvano ukupno {len(df)} dokumenata u 'data.csv'.")
    input("Pritisni Enter za izlaz...")

if __name__ == "__main__":
    scrape_sve_dokumente()