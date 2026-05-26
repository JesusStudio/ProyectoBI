import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
import numpy as np

# --- Reconstruir fecha desde año, mes, dia (todos INT) ---
df = dataset[['año', 'mes', 'dia', 'toneladas_recolectadas']].dropna()
df['fecha'] = pd.to_datetime(dict(
    year=df['año'].astype(int),
    month=df['mes'].astype(int),
    day=df['dia'].astype(int)
))
df = df.groupby('fecha')['toneladas_recolectadas'].sum().reset_index()
df = df.sort_values('fecha')

df['ordinal'] = df['fecha'].map(pd.Timestamp.toordinal)

# --- Modelo de regresión ---
X = df['ordinal'].values.reshape(-1, 1)
y = df['toneladas_recolectadas'].values
model = LinearRegression().fit(X, y)

# --- Fechas futuras (30 días) ---
last_date = df['fecha'].max()
future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=30)
future_ordinal = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
future_pred = model.predict(future_ordinal)

# --- Gráfico ---
fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#0f1117')

ax.plot(df['fecha'], y, color='#4fc3f7', linewidth=2, label='Histórico')
ax.plot(future_dates, future_pred, color='#ff7043', linewidth=2,
        linestyle='--', label='Predicción')
ax.fill_between(future_dates, future_pred * 0.92, future_pred * 1.08,
                color='#ff7043', alpha=0.15)

ax.set_title('Predicción de Toneladas Recolectadas', color='white',
             fontsize=13, pad=12)
ax.tick_params(colors='#aaaaaa')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
fig.autofmt_xdate()
for spine in ax.spines.values():
    spine.set_edgecolor('#333333')
ax.legend(facecolor='#1c1c2e', labelcolor='white')
ax.yaxis.label.set_color('#aaaaaa')

plt.tight_layout()
plt.show()