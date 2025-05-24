# 🛡️ Linux Security Audit

**Linux Security Audit** es una herramienta de línea de comandos escrita en Python diseñada para realizar auditorías rápidas, sigilosas y automatizadas del estado de un sistema Linux.

Genera un informe completo en texto plano que cubre aspectos clave del sistema: recursos, usuarios, servicios, configuraciones sensibles y condiciones potencialmente inseguras. El log puede guardarse temporalmente en memoria (`/dev/shm/`) para evitar dejar rastros en disco.

---

## ✅ ¿Qué analiza esta herramienta?

- ### 🖥️ Información del sistema:
  - Nombre del sistema operativo y versión del kernel.
  - Arquitectura y procesador.
  - Uso actual de CPU, memoria y disco.

- ### 🌐 Red:
  - Interfaces activas.
  - Puertos en escucha (conexiones locales).

- ### 🔧 Servicios:
  - Servicios activos (`systemctl`).
  - Scripts en `/etc/init.d/`.

- ### ⏰ Tareas programadas:
  - Revisión del `crontab` del sistema.

- ### 👤 Usuarios y permisos:
  - Usuarios definidos (`/etc/passwd`).
  - Grupos del sistema (`/etc/group`).
  - Análisis básico y sigiloso de privilegios (sin leer `/etc/sudoers` directamente).
  - Listado de archivos en `/etc/sudoers.d/` (sin abrirlos, salvo permisos).

- ### 🔍 Análisis de entorno:
  - Variables de entorno expuestas.
  - Shells por defecto de los usuarios.
  - Aliases definidos por defecto en el sistema.

- ### ⚠️ Comprobaciones de seguridad (vuln_checks):
  - Usuario en grupos privilegiados.
  - Directorios con permisos `world-writable` en `/tmp`, `/dev/shm`, etc.
  - Versión del kernel (para identificación de posibles exploits).

---

## 💡 ¿Por qué es útil?

Esta herramienta proporciona una base sólida para:

- Revisiones post-explotación discretas.
- Auditorías periódicas en entornos DevSecOps.
- Análisis forense básico.
- Estudiantes e investigadores que desean aprender cómo inspeccionar la seguridad de un sistema sin herramientas invasivas.

---

## ⚙️ Requisitos

- Linux (cualquier distribución con utilidades básicas estándar)
- Python 3.x
- Utilidades del sistema: `top`, `df`, `ss`, `ip`, `systemctl`, etc.
- Permisos root **no requeridos**, pero recomendados para inspección completa.

---

## 🔐 Filosofía del proyecto

| Principio   | Descripción |
|------------|-------------|
| 🕵️ **Sigilo**     | Evita modificar el sistema o dejar rastros. Usa `/dev/shm` como ubicación temporal opcional. |
| 🔌 **Nativo**     | No requiere librerías externas ni dependencias complejas. |
| ⚔️ **Versátil**   | Útil tanto en auditorías defensivas como ofensivas. |
| 🧱 **Modularidad** | Código organizado en módulos reutilizables (`system_info`, `environment_info`, `vuln_checks`, etc.) |

---

## 📝 Uso

```bash
python3 audit.py -save      # Guarda el log en /dev/shm/audit-log.txt
python3 audit.py -nosave    # Solo salida por consola (modo sigiloso)
```

## 📁 Salida

- En modo `-save`, el resultado se guarda en:
  
  ```bash
  /dev/shm/audit-log.txt

## 🚀 Estado actual

- 🟢 Estable y funcional.
- 🔄 En desarrollo activo para agregar más controles discretos y personalización.
