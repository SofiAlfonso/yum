# Dockerfile para YUM - Aplicación Django de Recetas
# Autor: Ana Sofía Alfonso

# Usar imagen base de Python
FROM python:3.12-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY yum/ .

# Crear directorios necesarios
RUN mkdir -p /app/staticfiles /app/media

# Crear script de entrada
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Ejecutando migraciones..."\n\
python manage.py migrate --noinput\n\
echo "Compilando mensajes de traducción..."\n\
python manage.py compilemessages\n\
echo "Recolectando archivos estáticos..."\n\
python manage.py collectstatic --noinput\n\
echo "Iniciando servidor con Gunicorn..."\n\
exec gunicorn yum.wsgi:application --bind 0.0.0.0:8000 --workers 3\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Exponer puerto 8000
EXPOSE 8000

# Usar el script de entrada
CMD ["/app/entrypoint.sh"]

