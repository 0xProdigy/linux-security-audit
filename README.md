# 🛡️ Linux Security Audit

**Linux Security Audit** es una herramienta post-explotación escrita en Python que permite recolectar de manera sigilosa información clave de un sistema Linux, utilizando solo comandos nativos ("Living off the Land").

Permite ejecutar auditorías en modo silencioso, ya sea imprimiendo la salida directamente por consola o guardándola opcionalmente en un archivo en memoria (`/dev/shm`) para evitar dejar rastros en disco.

---

## ✅ ¿Qué hace esta herramienta?

Reúne información crítica del sistema que puede ser útil para análisis de seguridad, reconocimiento post-explotación o auditorías rápidas.

### 🔍 Recolecta:

- **🖥 Información del sistema**
  - Sistema operativo, kernel, CPU, arquitectura
- **📊 Recursos**
  - Uso de CPU, RAM, disco
- **🌐 Red**
  - Interfaces configuradas y estadísticas de tráfico
  - Puertos en escucha (sin usar `ss`, `netstat` ni `lsof`)
- **🔧 Servicios**
  - Servicios activos (`systemctl`, `/etc/init.d/`)
  - Crontab del sistema
- **👥 Usuarios y privilegios**
  - Usuarios (`/etc/passwd`)
  - Grupos (`/etc/group`)
  - Sudoers (`/etc/sudoers`, `/etc/sudoers.d/`)
- **📂 Archivos SUID/SGID**
  - Reporte simple, sin comandos ruidosos como `find`

---

## ⚙️ Requisitos

- Python 3.x
- Linux con herramientas estándar (`top`, `df`, `ip`, `systemctl`, etc.)
- Permisos de superusuario para máxima cobertura (recomendado)

---

## 🚀 Uso

```bash
# Mostrar ayuda (sin parámetros)
python3 audit.py

# Modo silencioso, solo imprime en consola (sin dejar rastros)
python3 audit.py -nosave

# Guarda log en memoria (/dev/shm) — ⚠ deja artefactos
python3 audit.py -save

## 🧠 Filosofía del proyecto

- **Sigilo:** no genera tráfico ni actividad sospechosa.
- **Nativo:** no usa librerías externas ni herramientas intrusivas.
- **Versátil:** útil tanto para administradores como para investigadores de seguridad ofensiva.

---

## 📁 Salida

- En modo `-save`, el resultado se guarda en:

  ```bash
  /dev/shm/audit-log.txt 
