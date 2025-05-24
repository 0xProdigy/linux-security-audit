🛡️ Linux Security Audit
Linux Security Audit es una herramienta de línea de comandos escrita en Python que permite realizar una auditoría rápida y automatizada del estado de seguridad y configuración básica de un sistema Linux.

Este script genera un informe completo en texto plano, almacenado en la carpeta logs/, que cubre múltiples aspectos del sistema relacionados con el rendimiento, los servicios y la seguridad. Es ideal para administradores de sistemas, equipos DevSecOps o cualquier persona interesada en comprender el estado operativo y la exposición de su sistema Linux.

✅ ¿Qué analiza este script?
Información del sistema: nombre del SO, versión del kernel, arquitectura y CPU.

Uso de recursos: consumo actual de CPU, RAM y disco.

Red: interfaces de red configuradas y puertos en escucha.

Servicios: servicios activos mediante systemctl y scripts en /etc/init.d/.

Tareas programadas: contenido del crontab del sistema.

Usuarios y permisos:

Usuarios del sistema (/etc/passwd)

Grupos (/etc/group)

Configuración de sudoers

Archivos críticos con permisos SUID/SGID, que pueden representar riesgos de escalada de privilegios.

💡 ¿Por qué es útil?
Este script es una base sólida para integrarlo en pipelines de auditoría o revisiones de configuración en entornos Linux. Puede utilizarse para:

Crear snapshots del estado de un sistema.

Detectar configuraciones inseguras o cambios inesperados.

Aprender cómo inspeccionar manualmente elementos clave de la seguridad en Linux.

⚙️ Requisitos
Python 3.x

Linux con utilidades estándar (top, df, ss, ip, systemctl, etc.)

Permisos de superusuario para auditar completamente (sudo recomendado)
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
