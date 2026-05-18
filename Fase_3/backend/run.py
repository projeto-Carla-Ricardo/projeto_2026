#!/usr/bin/env python3
"""
Entry point para a plataforma AILO.
Uso: python run.py
"""
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    print("=" * 60)
    print("  AILO — Artificial Intelligence in a Learning Organization")
    print("  Plataforma de diagnóstico de maturidade organizacional")
    print("=" * 60)
    print(f"  → Frontend: http://localhost:5000")
    print(f"  → API:      http://localhost:5000/api/v1")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
