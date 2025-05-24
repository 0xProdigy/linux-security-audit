# 🛡️ Linux Security Audit

Linux Security Audit es una herramienta de línea de comandos escrita en Python que permite realizar una auditoría rápida y automatizada del estado de seguridad y configuración básica de un sistema Linux.

Este script genera un informe completo en texto plano, almacenado en la carpeta `/dev/shm/`, que cubre múltiples aspectos del sistema relacionados con el rendimiento, los servicios y la seguridad. Es ideal para administradores de sistemas, equipos DevSecOps o cualquier persona interesada en comprender el estado operativo y la exposición de su sistema Linux.

---

## ✅ ¿Qué analiza este script?

- **Información del sistema**: nombre del SO, versión del kernel, arquitectura y CPU.
- **Uso de recursos**: consumo actual de CPU, RAM y disco.
- **Red**: interfaces de red configuradas y puertos en escucha.
- **Servicios**: servicios activos mediante `systemctl` y scripts en `/etc/init.d/`.
- **Tareas programadas**: contenido del `crontab` del sistema.
- **Usuarios y permisos**:
  - Usuarios del sistema (`/etc/passwd`)
  - Grupos (`/etc/group`)
  - Configuración de `sudoers`
- **Archivos críticos**:
  - Archivos con permisos `SUID/SGID` que pueden representar riesgos de escalada de privilegios.

---

## 💡 ¿Por qué es útil?

Este script es una base sólida para integrarlo en pipelines de auditoría o revisiones de configuración en entornos Linux. Puede utilizarse para:

- Crear snapshots del estado de un sistema.
- Detectar configuraciones inseguras o cambios inesperados.
- Aprender cómo inspeccionar manualmente elementos clave de la seguridad en Linux.

---

## ⚙️ Requisitos

- Python 3.x
- Linux con utilidades estándar (`top`, `df`, `ss`, `ip`, `systemctl`, etc.)
- Permisos de superusuario para auditar completamente (sudo recomendado)

---

## 🧠 Filosofía del proyecto

- **Sigilo**: no genera tráfico ni actividad sospechosa.
- **Nativo**: no usa librerías externas ni herramientas intrusivas.
- **Versátil**: útil tanto para administradores como para investigadores de seguridad ofensiva.

---

## 📁 Salida

- En modo `-save`, el resultado se guarda en:
  
  ```bash
  /dev/shm/audit-log.txt
