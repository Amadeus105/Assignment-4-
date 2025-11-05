from prometheus_client import start_http_server, Gauge, Counter, Histogram, Info
import requests
import time
import random
import psutil
from datetime import datetime

# Weather metrics
temperature = Gauge('weather_temperature_celsius', 'Current temperature in Celsius')
humidity = Gauge('weather_humidity_percent', 'Current humidity percentage')
pressure = Gauge('weather_pressure_hpa', 'Current atmospheric pressure')
wind_speed = Gauge('weather_wind_speed_ms', 'Wind speed in m/s')
uv_index = Gauge('weather_uv_index', 'UV index')

# Exchange rate metrics
usd_eur_rate = Gauge('exchange_usd_eur', 'USD to EUR exchange rate')
usd_gbp_rate = Gauge('exchange_usd_gbp', 'USD to GBP exchange rate')
usd_jpy_rate = Gauge('exchange_usd_jpy', 'USD to JPY exchange rate')

# Cryptocurrency metrics
btc_usd_rate = Gauge('crypto_btc_usd', 'Bitcoin to USD rate')
eth_usd_rate = Gauge('crypto_eth_usd', 'Ethereum to USD rate')

# System metrics (from local machine)
custom_cpu_usage = Gauge('custom_cpu_usage_percent', 'CPU usage percentage')
custom_memory_usage = Gauge('custom_memory_usage_percent', 'Memory usage percentage')
custom_disk_usage = Gauge('custom_disk_usage_percent', 'Disk usage percentage')

# API metrics
api_call_duration = Histogram('api_call_duration_seconds', 'API call duration', ['api'])
failed_api_calls = Counter('failed_api_calls_total', 'Total failed API calls')
successful_api_calls = Counter('successful_api_calls_total', 'Total successful API calls')

# Info metric
exporter_info = Info('exporter_info', 'Information about the custom exporter')

def get_weather_data():
    """Simulate weather data with realistic variations"""
    try:
        # Realistic weather simulation
        base_temp = 20  # Base temperature
        temp_variation = random.uniform(-5, 5)
        humidity_val = 60 + random.uniform(-20, 20)
        pressure_val = 1013 + random.uniform(-10, 10)
        wind_val = 5 + random.uniform(0, 15)
        uv_val = random.randint(1, 11)  # UV index 1-11
        
        temperature.set(base_temp + temp_variation)
        humidity.set(max(0, min(100, humidity_val)))  # Clamp 0-100
        pressure.set(pressure_val)
        wind_speed.set(wind_val)
        uv_index.set(uv_val)
        
        successful_api_calls.inc()
        return True
        
    except Exception as e:
        print(f"Weather data error: {e}")
        failed_api_calls.inc()
        return False

def get_exchange_rates():
    """Get real exchange rates from Frankfurter API"""
    try:
        with api_call_duration.labels(api='frankfurter').time():
            url = "https://api.frankfurter.app/latest?from=USD&to=EUR,GBP,JPY"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            usd_eur_rate.set(data['rates']['EUR'])
            usd_gbp_rate.set(data['rates']['GBP'])
            usd_jpy_rate.set(data['rates']['JPY'])
            
        successful_api_calls.inc()
        return True
        
    except Exception as e:
        print(f"Exchange rate API error: {e}")
        # Set fallback values
        usd_eur_rate.set(0.85 + random.uniform(-0.05, 0.05))
        usd_gbp_rate.set(0.75 + random.uniform(-0.05, 0.05))
        usd_jpy_rate.set(110 + random.uniform(-5, 5))
        failed_api_calls.inc()
        return False

def get_crypto_rates():
    """Get cryptocurrency rates from CoinGecko API"""
    try:
        with api_call_duration.labels(api='coingecko').time():
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            btc_usd_rate.set(data['bitcoin']['usd'])
            eth_usd_rate.set(data['ethereum']['usd'])
            
        successful_api_calls.inc()
        return True
        
    except Exception as e:
        print(f"Crypto API error: {e}")
        # Set fallback values
        btc_usd_rate.set(30000 + random.uniform(-5000, 5000))
        eth_usd_rate.set(2000 + random.uniform(-500, 500))
        failed_api_calls.inc()
        return False

def get_system_metrics():
    """Get custom system metrics"""
    try:
        custom_cpu_usage.set(psutil.cpu_percent())
        custom_memory_usage.set(psutil.virtual_memory().percent)
        custom_disk_usage.set(psutil.disk_usage('/').percent)
        return True
    except Exception as e:
        print(f"System metrics error: {e}")
        return False

def update_exporter_info():
    """Update exporter information"""
    exporter_info.info({
        'version': '1.0.0',
        'start_time': datetime.now().isoformat(),
        'student_name': 'Your Name',
        'assignment': '4',
        'metrics_count': '15'
    })

if __name__ == '__main__':
    # Start up the server to expose the metrics
    start_http_server(8000)
    print("Custom exporter started on port 8000")
    update_exporter_info()
    
    cycle_count = 0
    while True:
        start_time = time.time()
        cycle_count += 1
        
        print(f"\n--- Cycle {cycle_count} ---")
        
        # Update all metrics
        weather_success = get_weather_data()
        exchange_success = get_exchange_rates()
        crypto_success = get_crypto_rates()
        system_success = get_system_metrics()
        
        # Record overall duration
        overall_duration = time.time() - start_time
        api_call_duration.labels(api='overall').observe(overall_duration)
        
        print(f"Update completed in {overall_duration:.2f}s")
        print(f"Success: Weather={weather_success}, Exchange={exchange_success}, Crypto={crypto_success}, System={system_success}")
        
        # Wait 20 seconds before next update
        time.sleep(20)