"""
Hugging Face Spaces - Golf Results Golfville
Aplicação Flet para visualização de resultados
"""

import flet as ft
import os

# Import da função main do seu código
from main import main

if __name__ == "__main__":
    # Configurações para Hugging Face
    port = int(os.getenv("FLET_SERVER_PORT", 7860))
    
    print(f"🚀 Starting Flet app on port {port}")
    print(f"🌐 Access: http://0.0.0.0:{port}")
    
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,  # Modo web (não desktop)
        port=port,
        host="0.0.0.0",  # Permite acesso externo
        assets_dir="assets"  # Se você tiver assets
    )