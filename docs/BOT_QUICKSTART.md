# 🚀 Quickstart - Telegram Bot

Guía rápida para poner en marcha el bot de predicciones deportivas.

## ⚡ Setup Rápido (5 minutos)

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Crear Bot en Telegram

1. Abre Telegram
2. Busca **@BotFather**
3. Envía: `/newbot`
4. Elige un nombre: `Sports Prediction Bot` (o el que prefieras)
5. Elige un username: `sports_pred_bot` (o el que prefieras, debe terminar en `_bot`)
6. **Copia el token** que te da BotFather

### 3. Configurar Token

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Copia el ejemplo
cp .env.example .env

# Edita .env y pega tu token
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 4. Preparar Base de Datos

```bash
# Migrar
python manage.py migrate

# Importar valores Pd de Gematrinator
python manage.py import_pd_values
```

### 5. ¡Ejecutar el Bot!

```bash
python manage.py runbot
```

Verás:
```
Starting Telegram Bot...
Bot started successfully!
Commands available:
  /start - Welcome message
  /help - Show help
  /predict L=<value> day=<day> sport=<sport>
  ...
```

### 6. Probar en Telegram

1. Abre Telegram
2. Busca tu bot por el username que elegiste
3. Envía: `/start`
4. Prueba una predicción:
   ```
   /predict L=6.32 day=14 sport=NBA
   ```

## ✅ Verificación Local (Sin Telegram)

Si quieres probar sin configurar Telegram:

```bash
python test_bot.py
```

Esto ejecuta todos los tests y muestra que todo funciona correctamente.

## 📱 Comandos del Bot

### `/start`
Mensaje de bienvenida

### `/help`
Lista de todos los comandos

### `/predict L=6.32 day=14 sport=NBA`
Hacer una predicción

### `/compare prediction=10.35 vegas=219.5`
Comparar con línea de Vegas

### `/condensed 14`
Ver valor Pd del día 14

### `/formula`
Ver explicación de la fórmula

### `/sports`
Ver multiplicadores por deporte

## 🎯 Ejemplo Completo

```
Usuario: /predict L=6.32 day=14 sport=NBA

Bot:
┌─────────────────────────────────────────┐
│   SPORTS PREDICTION CALCULATOR          │
├─────────────────────────────────────────┤
│ Fecha: January 13, 2026
│ Día del mes: 14                         │
│ Deporte: NBA                            │
│                                         │
│ INPUTS:                                 │
│ • Linear Regression (L): 6.32           │
│ • Condensed Number (Pd): 5              │
│ • Sport Multiplier (s): 1.15            │
│                                         │
│ CÁLCULO:                                │
│ Paso 1: C = (L + 5·Pd) / 2             │
│         C = (6.32 + 25) / 2            │
│         C = 15.66                       │
│                                         │
│ Paso 2: N = numerological_reduction(C)  │
│         N = 9                           │
│                                         │
│ Paso 3: T = N × s                      │
│         T = 9 × 1.15                   │
│                                         │
│ PREDICCIÓN: 10.35 puntos                │
└─────────────────────────────────────────┘
```

## ⚙️ Deportes Soportados

- **NBA**, **WNBA**, **NCAA_BASKETBALL** → 1.15
- **NFL**, **NCAA_FOOTBALL** → 1.06
- **MLB**, **NCAA_BASEBALL** → 0.90
- **NHL**, **NCAA_HOCKEY** → 1.20
- **MLS**, **SOCCER**, **PREMIER_LEAGUE**, etc. → 1.10
- **UFC**, **UFC_TITLE**, **MMA** → 1.25

## 🐛 Troubleshooting

### Bot no responde
```bash
# 1. Verifica que el bot esté corriendo
python manage.py runbot

# 2. Verifica el token en .env
cat .env | grep TELEGRAM_BOT_TOKEN

# 3. Verifica que BotFather te dio el token correcto
```

### "No Pd value found"
```bash
# Importa los valores Pd
python manage.py import_pd_values
```

### Error al instalar dependencias
```bash
# Usa un virtual environment
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📚 Más Información

Ver **BOT_README.md** para documentación completa.

---

¡Listo! Tu bot está funcionando. 🎉
