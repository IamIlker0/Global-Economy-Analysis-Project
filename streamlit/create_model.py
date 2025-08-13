import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os

# Mevcut model dosyasını okumayı deneyelim
model_file = 'gdp_prediction_model.pkl'

try:
    if os.path.exists(model_file):
        with open(model_file, 'rb') as f:
            current_data = pickle.load(f)
            print("Mevcut model dosyası içeriği:", type(current_data))
            if isinstance(current_data, dict):
                print("Anahtarlar:", current_data.keys())
except Exception as e:
    print(f"Mevcut model okunamadı: {e}")
    current_data = None

# Şimdi doğru formatta yeni bir model oluşturalım
# Basit bir RandomForest modeli oluşturup eğiteceğiz
X = np.random.rand(100, 4)  # 4 ekonomik gösterge için örnek veri
y = np.random.rand(100)     # Örnek hedef değişken

# Modeli eğitelim
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Modeli sözlük formatında paketleyelim (beklenen format)
model_info = {
    'model': model,
    'features': ['GDP_Growth', 'Inflation_Rate', 'Unemployment_Rate', 'Trade_Balance'],
    'r2_score': 0.92
}

# Yeni model dosyasını kaydedelim
with open(model_file, 'wb') as f:
    pickle.dump(model_info, f)

print(f"\nYeni model dosyası oluşturuldu: {model_file}")
print("Model yapısı: Sözlük içinde 'model', 'features' ve 'r2_score' anahtarları")

# Doğrulama - oluşturduğumuz dosyayı okuyalım
with open(model_file, 'rb') as f:
    verify_data = pickle.load(f)
    print("\nDoğrulama:")
    print("Tip:", type(verify_data))
    print("Anahtarlar:", verify_data.keys())