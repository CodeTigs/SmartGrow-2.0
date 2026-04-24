import requests
import datetime

url = "https://smartgrow-ajtn.onrender.com/leituras"

def testar_cenario(nome, temp, umid_solo):
    print(f"\n🧪 TESTE: {nome}")
    print(f"   Simulando temperatura: {temp}°C")
    print(f"   Simulando umidade do solo: {umid_solo}%")
    
    dados = {
        "temperatura_celsius": temp,
        "umidade_solo": umid_solo
    }
    
    try:
        # Envia para a nuvem
        response = requests.post(url, json=dados)
        
        if response.status_code == 200:
            resultado = response.json()
            estado = resultado['estado_atual']
            
            print("✅ RESPOSTA DA NUVEM:")
            print(f"   --> Irrigação: {estado['nivel_irrigacao']:.1f}%")
            print(f"   --> Ventilação: {estado['velocidade_ventilacao']:.1f}%")
            print(f"   --> Iluminação: {estado['nivel_iluminacao']:.1f}% (Time-Based)")
            
            # Análise Rápida
            if estado['nivel_irrigacao'] > 30:
                print("   💧 AÇÃO ESP32: LIGAR BOMBA (Proporcional)")
            else:
                print("   🛑 AÇÃO ESP32: MANTER DESLIGADO (Zona Morta)")
                
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    print("🌍 TESTE DE INTEGRAÇÃO REMOTA - SMARTGROW")
    print("   Conectando a: " + url)
    
    # Cenário ESP32 (T:21.4 H:92.1 S:27.0)
    # Ignorando umidade do ar (H) pois não é enviada para a API
    testar_cenario("Cenário ESP32 Atual", temp=21.4, umid_solo=27.0)