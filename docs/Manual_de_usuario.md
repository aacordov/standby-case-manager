# 📖 Manual de Usuario - Standby Case Manager v2.3.0

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Inicio de Sesión](#inicio-de-sesión)
3. [Panel Principal](#panel-principal)
4. [Gestión de Casos](#gestión-de-casos)
5. [Sistema de Observaciones](#sistema-de-observaciones) 🆕
6. [Timeline y Auditoría](#timeline-y-auditoría) 🆕
7. [Operaciones Masivas](#operaciones-masivas) 🆕
8. [Búsqueda y Filtros](#búsqueda-y-filtros)
9. [Command Palette](#command-palette)
10. [Gestión de Archivos](#gestión-de-archivos)
11. [Dashboard y Estadísticas](#dashboard-y-estadísticas)
12. [Gestión de Usuarios](#gestión-de-usuarios)
13. [Importar y Exportar](#importar-y-exportar)
14. [Configuración de Perfil](#configuración-de-perfil)
15. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 📌 Introducción

Standby Case Manager es un sistema diseñado para gestionar casos de operación de manera eficiente, con funcionalidades avanzadas de auditoría, timeline y control de acceso granular. Este manual te guiará paso a paso en el uso de todas sus funcionalidades.

### Roles de Usuario

El sistema cuenta con tres roles principales con permisos diferenciados:

| Rol | Permisos | Descripción |
|:----|:---------|:------------|
| **👑 ADMIN** | Acceso total | • Gestión completa de casos<br>• **Eliminar casos** (exclusivo)<br>• Gestión de usuarios<br>• Editar cualquier observación<br>• Actualizaciones masivas |
| **✍️ INGRESO** | Crear/Editar | • Crear y modificar casos<br>• Editar cualquier observación<br>• Actualizaciones masivas<br>• Subir archivos<br>• **No puede eliminar casos** |
| **👁️ CONSULTA** | Lectura limitada | • Visualización de casos<br>• Editar **solo sus propias observaciones**<br>• Descargar archivos<br>• **Sin permisos de modificación** |

### Novedades en v2.3.0 🆕

- **Eliminación controlada**: Solo ADMIN puede eliminar casos
- **Observaciones editables**: Edita observaciones individuales con control de permisos
- **Timeline visual**: Ve el historial completo del caso en orden cronológico
- **Auditoría automática**: Todos los cambios se registran automáticamente
- **Operaciones masivas mejoradas**: Actualiza múltiples casos a la vez con auditoría

---

## 🔐 Inicio de Sesión

### Acceso al Sistema

1. Abre tu navegador web y accede a la URL del sistema
   - **Local**: `http://localhost:3000`
   - **Producción**: (URL proporcionada por tu administrador)

2. Verás la pantalla de inicio de sesión

### Credenciales Predeterminadas

Para entornos de desarrollo, existen tres usuarios de prueba:

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| Administrator | `admin@standby.com` | `admin123` | ADMIN |
| Operador | `ingreso@standby.com` | `ingreso123` | INGRESO |
| Consultor | `consulta@standby.com` | `consulta123` | CONSULTA |

> ⚠️ **Importante en Producción**: Cambia estas contraseñas inmediatamente después del primer inicio de sesión.

### Cambio de Tema

Antes de iniciar sesión, puedes cambiar entre tema claro y oscuro:
- Click en el ícono 🌙 (luna) para modo oscuro
- Click en el ícono ☀️ (sol) para modo claro

### Primer Inicio de Sesión

Si es tu primera vez en el sistema:

1. Ingresa con las credenciales proporcionadas por tu administrador
2. **Cambia tu contraseña inmediatamente**:
   - Click en tu avatar (esquina superior derecha)
   - Selecciona **Cambiar Contraseña**
   - Ingresa contraseña actual y nueva contraseña
   - La nueva contraseña debe tener mínimo 8 caracteres

3. Completa tu perfil (opcional pero recomendado)

### Cerrar Sesión

Para salir del sistema de forma segura:
1. Click en tu avatar en la esquina superior derecha
2. Selecciona **Cerrar Sesión**
3. Serás redirigido a la pantalla de login

---

## 🏠 Panel Principal

Una vez iniciada la sesión, verás el panel principal con varios componentes:

### Barra de Navegación Superior

- **Logo**: Click para volver al dashboard principal
- **Buscador Global**: Campo de búsqueda rápida (disponible en todas las vistas)
- **Command Palette**: Botón con ícono ⌘ para acceso rápido a funciones
- **Notificaciones**: Campana 🔔 para ver alertas y actualizaciones
- **Avatar de Usuario**: Menú desplegable con opciones de perfil

### Menú Lateral

El menú lateral incluye las siguientes opciones (visibilidad según rol):

- 📊 **Tablero**: Vista general con todos los casos y estadísticas
- ➕ **Nuevo Caso**: Formulario para crear caso (INGRESO/ADMIN)
- 📤 **Importar/Exportar**: Gestión masiva de casos (INGRESO/ADMIN)
- 👥 **Usuarios**: Administración de usuarios (solo ADMIN)
- 💻 **Desarrolladores**: Información del equipo de desarrollo

### Atajos de Teclado Globales

| Atajo | Función |
|-------|---------|
| `Ctrl + K` / `Cmd + K` | Abrir Command Palette |
| `Ctrl + /` | Ver lista de atajos |
| `Esc` | Cerrar modales/diálogos |

---

## 📋 Gestión de Casos

### Ver Lista de Casos

1. Click en **Tablero** en el menú lateral
2. Verás una tabla paginada con todos los casos
3. Cada caso muestra:
   - **Código del caso**: Identificador único
   - **Servicio/Plataforma**: Sistema o servicio afectado
   - **Estado**: 
     - 🔵 **ABIERTO**: Caso nuevo o sin resolver
     - 🟡 **STANDBY**: En espera de información/acción
     - 🟠 **EN_MONITOREO**: Requiere seguimiento activo
     - 🟢 **CERRADO**: Caso resuelto
   - **Prioridad**:
     - 🔴 **CRÍTICO**: Afecta servicios críticos
     - 🟠 **ALTO**: Requiere atención prioritaria
     - 🟡 **MEDIO**: Importancia estándar
     - 🟢 **BAJO**: Puede esperar
   - **Responsable SBY**: Usuario asignado
   - **Última actualización**: Fecha y hora del último cambio

### Paginación

En la parte inferior de la tabla verás:
- **Registros por página**: Selector para mostrar 10, 20, 50 o 100 casos
- **Navegación**: Botones para ir a primera, anterior, siguiente y última página
- **Información**: "Mostrando X de Y casos"

### Crear Nuevo Caso

**Permisos necesarios**: INGRESO o ADMIN

1. Click en **Nuevo Caso** en el menú lateral (o `Ctrl + K` → "Crear nuevo caso")
2. Completa el formulario con los siguientes campos:

   **Campos Obligatorios**:
   - **Código**: Identificador único del caso (ej: `HP-0001`, `VPN-2024-001`)
     - No puede estar duplicado
     - Recomendación: Usa un formato consistente
   
   - **Servicio/Plataforma**: Sistema o servicio afectado
     - Ejemplos: "VPN Corporativa", "Servidor Web Principal", "Base de Datos Clientes"
   
   - **Prioridad**: Selecciona según criticidad
   
   - **Motivo**: Descripción detallada del caso
     - Qué ocurrió
     - Cuándo se detectó
     - Impacto

   **Campos Opcionales**:
   - **Responsable SBY**: Asignar a un usuario específico
   - **Observaciones Iniciales**: Comentarios o notas adicionales
     - Se guardará como primera observación del caso

3. Click en **Guardar Caso**
4. El sistema te mostrará una confirmación y te redirigirá al caso creado

**Notas Importantes**:
- El estado inicial siempre es **ABIERTO**
- Se registra automáticamente quién creó el caso
- Si agregas observaciones iniciales, se crea automáticamente en el sistema de observaciones

### Ver Detalles de un Caso

1. En el Tablero, click en el botón **Ver** (👁️) junto al caso
2. Se abrirá la vista detallada que incluye:

   **Sección de Información Principal**:
   - Código, servicio, prioridad, estado
   - Responsable asignado
   - Fechas de inicio y fin (si aplica)
   - Usuario que creó el caso

   **Sección de Observaciones** 🆕:
   - Lista cronológica de todas las observaciones
   - Información de quién escribió cada observación
   - Indicador de ediciones (si fueron modificadas)
   - Opción de editar tus propias observaciones

   **Timeline del Caso** 🆕:
   - Visualización cronológica de toda la actividad
   - Eventos de creación, observaciones, y cambios
   - Detalles de quién realizó cada acción

   **Archivos Adjuntos**:
   - Lista de evidencias subidas
   - Preview de imágenes y PDFs
   - Opciones de descarga

### Editar un Caso

**Permisos necesarios**: INGRESO o ADMIN

1. En la vista detallada, click en **Editar**
2. Modifica los campos necesarios:
   - Código del caso
   - Servicio/Plataforma
   - Prioridad
   - Estado
   - Responsable
   - Motivo
   - **Nueva observación** (se agregará a la lista)
   - Fecha de cierre (para casos cerrados)

3. Click en **Guardar Cambios**

**Auditoría Automática** 🆕:
- Todos los cambios se registran automáticamente
- Se guarda el valor anterior y el nuevo valor
- Puedes ver el historial en el Timeline

### Eliminar un Caso 🆕

**Permisos necesarios**: Solo ADMIN

> ⚠️ **Advertencia Crítica**: Esta acción es **IRREVERSIBLE**. Se eliminarán permanentemente:
> - El caso principal
> - Todas las observaciones
> - Todos los archivos adjuntos
> - Todo el historial de auditoría

**Procedimiento**:

1. Abre el caso que deseas eliminar
2. Click en el menú ⋮ (tres puntos verticales) en la esquina superior derecha
3. Selecciona **Eliminar Caso**
4. Aparecerá un diálogo de confirmación
5. Escribe el código del caso para confirmar
6. Click en **Confirmar Eliminación**

**Protecciones del Sistema**:
- Solo usuarios ADMIN pueden eliminar casos
- Se requiere confirmación explícita
- Los casos con estado CERRADO requieren confirmación adicional
- Se elimina en cascada todas las relaciones (observaciones, archivos, auditoría)

**Recomendaciones**:
- En lugar de eliminar, considera cerrar el caso
- Exporta el caso antes de eliminarlo si necesitas un respaldo
- Verifica que no haya información crítica antes de proceder

---

## 📝 Sistema de Observaciones 🆕

El sistema de observaciones ha sido completamente refactorizado en la versión 2.3.0 para proporcionar mayor control y trazabilidad.

### Agregar una Nueva Observación

**Disponible para**: Todos los roles

1. En la vista detallada del caso
2. Scroll hasta la sección "Observaciones"
3. En el campo de texto, escribe tu comentario o nota
4. Click en **Agregar Observación**
5. La observación aparecerá inmediatamente en la lista

**Características**:
- Las observaciones se ordenan cronológicamente (más reciente al final)
- Se registra automáticamente quién escribió la observación
- Incluye timestamp de creación

### Ver Observaciones

Cada observación muestra:
- **Contenido**: Texto de la observación
- **Autor**: Nombre del usuario que la creó
- **Fecha de Creación**: Cuándo se escribió
- **Indicador de Edición**: Si fue modificada, muestra "Editado" y cuándo

### Editar una Observación 🆕

**Control de Permisos**:
- **CONSULTA**: Solo puede editar sus propias observaciones
- **INGRESO**: Puede editar cualquier observación
- **ADMIN**: Puede editar cualquier observación

**Procedimiento**:

1. Localiza la observación que deseas editar
2. Click en el ícono de **Editar** (✏️) junto a la observación
   - Si no ves el ícono, no tienes permisos para editar esa observación
3. Modifica el texto en el campo que aparece
4. Click en **Guardar**
5. La observación mostrará el indicador "Editado" con la fecha

**Notas Importantes**:
- No se puede eliminar una observación, solo editarla
- El sistema mantiene registro de cuándo fue editada
- Los cambios aparecen en el Timeline del caso

### Mejores Prácticas

✅ **Hazlo Bien**:
- Sé claro y conciso en tus observaciones
- Incluye fecha/hora si mencionas eventos específicos
- Usa observaciones para comunicación del equipo
- Documenta acciones tomadas y resultados

❌ **Evita**:
- Información sensible en observaciones (usa canales seguros)
- Editar observaciones de otros sin razón válida
- Eliminar información importante al editar

---

## 📜 Timeline y Auditoría 🆕

El Timeline proporciona una vista cronológica completa de toda la actividad relacionada con un caso.

### Acceder al Timeline

1. Abre un caso en vista detallada
2. Scroll hasta la sección **Timeline** o click en la pestaña correspondiente
3. Verás todos los eventos ordenados cronológicamente

### Tipos de Eventos en el Timeline

#### 1. **Creación del Caso** (CREATE)
- **Qué muestra**: Información inicial del caso
- **Incluye**: 
  - Motivo del caso
  - Servicio/plataforma
  - Prioridad inicial
  - Responsable inicial
  - Usuario creador

#### 2. **Observaciones** (OBSERVATION)
- **Qué muestra**: Cada observación agregada al caso
- **Incluye**:
  - Contenido de la observación
  - Quién la escribió
  - Cuándo se agregó
  - Si fue editada

#### 3. **Cambios en el Caso** (AUDIT - UPDATE)
- **Qué muestra**: Modificaciones a los campos del caso
- **Incluye**:
  - Qué campo cambió
  - Valor anterior
  - Valor nuevo
  - Quién hizo el cambio
  - Cuándo se realizó

Ejemplo:
```
Estado: ABIERTO → EN_MONITOREO
Prioridad: MEDIO → CRÍTICO
Responsable: Juan Pérez → María García
```

#### 4. **Actualizaciones Masivas** (AUDIT - BULK_UPDATE)
- **Qué muestra**: Cambios realizados mediante operaciones masivas
- **Incluye**: Misma información que UPDATE pero con indicador de bulk

#### 5. **Evidencias Adjuntas** (AUDIT - EVIDENCE)
- **Qué muestra**: Archivos subidos al caso
- **Incluye**:
  - Nombre del archivo
  - Tipo de archivo
  - Tamaño
  - Quién lo subió

### Interpretar el Timeline

**Código de Colores**:
- 🟦 **Azul**: Creación y eventos de sistema
- 🟩 **Verde**: Observaciones y comentarios
- 🟨 **Amarillo**: Cambios y actualizaciones
- 🟥 **Rojo**: Eventos críticos o eliminaciones

**Filtros** (si disponible):
- Por tipo de evento
- Por usuario
- Por rango de fechas

### Usos del Timeline

**Para Auditoría**:
- Verificar quién hizo qué cambios
- Revisar cumplimiento de procesos
- Investigar incidentes

**Para Seguimiento**:
- Ver evolución del caso
- Identificar cuellos de botella
- Analizar tiempos de respuesta

**Para Comunicación**:
- Mantener al equipo informado
- Documentar decisiones
- Justificar acciones tomadas

---

## ⚡ Operaciones Masivas 🆕

Las operaciones masivas permiten actualizar múltiples casos simultáneamente, ahorrando tiempo y asegurando consistencia.

### Acceder a Operaciones Masivas

1. En el **Tablero**, verás una lista de casos
2. Selecciona los casos que deseas modificar:
   - Click en el checkbox de cada caso
   - O usa "Seleccionar todos" para casos visibles
3. Aparecerá un menú flotante con acciones disponibles

### Acciones Masivas Disponibles

#### 1. Cerrar Casos en Lote

**Uso**: Cerrar múltiples casos resueltos a la vez

**Procedimiento**:
1. Selecciona los casos a cerrar
2. Click en **Cerrar Casos**
3. Confirma la acción
4. Todos los casos seleccionados cambiarán a estado CERRADO

**Auditoría**: Se crea un registro de auditoría por cada caso con:
- Cambio de estado: [estado anterior] → CERRADO
- Usuario que realizó la acción
- Timestamp de la operación
- Tipo: BULK_UPDATE

#### 2. Asignar Responsable en Lote

**Uso**: Reasignar múltiples casos a un nuevo responsable

**Procedimiento**:
1. Selecciona los casos
2. Click en **Asignar Responsable**
3. Escribe el nombre del nuevo responsable
4. Click en **Aplicar**

**Auditoría**: Se registra el cambio de responsable en cada caso

#### 3. Cambiar Prioridad en Lote

**Uso**: Actualizar la prioridad de múltiples casos

**Procedimiento**:
1. Selecciona los casos
2. Click en **Cambiar Prioridad**
3. Selecciona la nueva prioridad:
   - CRÍTICO
   - ALTO
   - MEDIO
   - BAJO
4. Click en **Aplicar**

**Auditoría**: Se registra el cambio de prioridad en cada caso

### Permisos para Operaciones Masivas

- **INGRESO**: Puede realizar operaciones masivas
- **ADMIN**: Puede realizar operaciones masivas
- **CONSULTA**: No tiene acceso a operaciones masivas

### Consideraciones Importantes

**Seguridad**:
- Se requiere confirmación para todas las operaciones masivas
- No se pueden deshacer las operaciones (pero sí están auditadas)
- Solo afecta casos seleccionados explícitamente

**Límites**:
- Máximo 100 casos por operación masiva
- Las operaciones se procesan de forma atómica (todas o ninguna)

**Auditoría Completa**:
- Cada caso recibe su propio registro de auditoría
- Puedes ver en el Timeline que fue una operación masiva
- Se mantiene trazabilidad completa

### Mejores Prácticas

✅ **Recomendado**:
- Usa filtros para seleccionar casos relacionados
- Verifica la selección antes de aplicar
- Comunica al equipo sobre cambios masivos importantes

❌ **Evita**:
- Seleccionar "todos" sin revisar la lista
- Hacer operaciones masivas sin confirmar primero
- Cambiar estados sin verificar que sean apropiados

---

## 🔍 Búsqueda y Filtros

El sistema de búsqueda y filtros te permite encontrar casos específicos rápidamente.

### Búsqueda Rápida

**Campo de Búsqueda Global** (disponible en todas las vistas):

1. Click en el campo de búsqueda en la barra superior
2. Escribe tu término de búsqueda
3. Los resultados se filtrarán en tiempo real

**Busca por**:
- Código de caso
- Servicio o plataforma
- Motivo del caso
- Nombre del responsable

**Características**:
- Búsqueda insensible a mayúsculas/minúsculas
- Búsqueda parcial (encuentra "VPN" en "VPN Corporativa")
- Resultados instantáneos

### Filtros Avanzados

En el **Tablero**, verás un panel de filtros avanzados:

#### Filtro por Fecha

**Presets Rápidos**:
- 📅 **Último mes (1M)**: Casos de los últimos 30 días
- 📅 **Últimos 3 meses (3M)**: Casos de los últimos 90 días
- 📅 **Últimos 6 meses (6M)**: Casos de los últimos 180 días
- 📅 **Este año**: Casos del año actual
- 📅 **Personalizado**: Define tu propio rango

**Rango Personalizado**:
1. Click en "Personalizado"
2. Selecciona **Fecha de Inicio** en el calendario
3. Selecciona **Fecha de Fin** en el calendario
4. Click en **Aplicar**

**Nota sobre Zonas Horarias** 🌍:
- El sistema detecta automáticamente tu zona horaria
- Las búsquedas se ajustan a tu hora local
- Las fechas se muestran en tu zona horaria pero se almacenan en UTC

#### Filtro por Estado

Selecciona uno o varios estados:
- ☑️ ABIERTO
- ☑️ STANDBY
- ☑️ EN_MONITOREO
- ☑️ CERRADO

**Multi-selección**: Puedes seleccionar múltiples estados para ver casos en cualquiera de ellos.

#### Filtro por Prioridad

Selecciona una o varias prioridades:
- ☑️ CRÍTICO
- ☑️ ALTO
- ☑️ MEDIO
- ☑️ BAJO

#### Filtro por Servicio/Plataforma

1. Click en el campo "Servicio/Plataforma"
2. Escribe el nombre del servicio (búsqueda parcial)
3. Los resultados se filtrarán automáticamente

Ejemplos:
- "VPN" encontrará "VPN Corporativa", "VPN Regional", etc.
- "Web" encontrará "Servidor Web", "Aplicación Web", etc.

#### Filtro por Responsable

1. Click en el campo "Responsable SBY"
2. Escribe el nombre del responsable (búsqueda parcial)
3. Los resultados se filtrarán automáticamente

### Combinar Filtros

Puedes combinar múltiples filtros para búsquedas precisas:

**Ejemplo 1**: Casos críticos abiertos en VPN
```
Estado: ABIERTO
Prioridad: CRÍTICO
Servicio: VPN
```

**Ejemplo 2**: Casos de Juan del último mes
```
Fecha: Último mes (1M)
Responsable: Juan
```

### Limpiar Filtros

Para resetear todos los filtros:
- Click en el botón **Limpiar Filtros** o **Reset**
- Todos los filtros volverán a su estado predeterminado

### Guardar Búsquedas Favoritas

(Funcionalidad futura planificada)

---

## ⌨️ Command Palette

El Command Palette es una herramienta de productividad que permite acceso rápido a cualquier función del sistema sin usar el mouse.

### Abrir Command Palette

**Métodos**:
- **Atajo de teclado**: 
  - Windows/Linux: `Ctrl + K`
  - Mac: `Cmd + K`
- **Botón**: Click en el ícono ⌘ en la barra superior

### Usar Command Palette

1. El Command Palette se abrirá como modal centrado
2. Verás una lista de comandos disponibles
3. **Buscar**: Escribe para filtrar comandos
4. **Navegar**: Usa ↑ ↓ para moverte entre opciones
5. **Ejecutar**: Presiona `Enter` para ejecutar el comando seleccionado
6. **Cerrar**: Presiona `Esc` o click fuera del modal

### Comandos Disponibles

#### Navegación
```
📊 Ir a Tablero          - Lleva al dashboard principal
➕ Crear Nuevo Caso      - Abre el formulario de nuevo caso
👥 Ver Usuarios          - Accede a gestión de usuarios (ADMIN)
📤 Importar/Exportar     - Accede al módulo de import/export
```

#### Acciones Rápidas
```
🔍 Buscar Casos...       - Enfoca el campo de búsqueda
🔄 Actualizar Página     - Recarga los datos actuales
📊 Ver Estadísticas      - Muestra métricas del sistema
```

#### Sistema
```
⚙️ Configuración         - Abre configuración del usuario
🌙 Cambiar Tema          - Alterna entre modo claro/oscuro
🚪 Cerrar Sesión         - Cierra tu sesión de forma segura
```

### Tips de Productividad

**Usa Palabras Clave**:
- Escribe "nuevo" para crear un caso
- Escribe "stats" para ver estadísticas
- Escribe "users" para gestión de usuarios

**Comandos Frecuentes**:
- Memoriza los atajos de tus acciones más comunes
- El Command Palette recuerda tus comandos recientes

**Navegación Rápida**:
- Es más rápido que usar el menú lateral
- Perfecto para usuarios power users

---

## 📂 Gestión de Archivos

El sistema permite adjuntar evidencias y documentación a cada caso.

### Subir Archivos

#### Método 1: Drag & Drop (Recomendado)

1. Abre un caso
2. Ve a la sección **Evidencias** o **Archivos Adjuntos**
3. Arrastra los archivos desde tu explorador de archivos
4. Suéltalos en el área designada con el ícono 📎
5. Los archivos se subirán automáticamente

**Visual**: Verás un área con bordes punteados que dice "Arrastra archivos aquí"

#### Método 2: Selector de Archivos

1. Click en **📎 Adjuntar Archivos** o **Subir Evidencia**
2. Se abrirá el explorador de archivos de tu sistema operativo
3. Selecciona uno o varios archivos
4. Click en **Abrir**
5. Los archivos comenzarán a subirse

#### Método 3: Pegar desde Portapapeles

1. Copia una imagen (Ctrl+C)
2. En la sección de archivos, presiona Ctrl+V
3. La imagen se subirá automáticamente

### Formatos Soportados

**Documentos**:
- 📄 PDF (Portable Document Format)
- 📄 DOC, DOCX (Microsoft Word)
- 📄 TXT (Texto plano)
- 📄 RTF (Rich Text Format)

**Imágenes**:
- 🖼️ JPG, JPEG (Joint Photographic Experts Group)
- 🖼️ PNG (Portable Network Graphics)
- 🖼️ GIF (Graphics Interchange Format)
- 🖼️ WEBP (formato web moderno)
- 🖼️ BMP (Bitmap)

**Hojas de Cálculo**:
- 📊 XLS, XLSX (Microsoft Excel)
- 📊 CSV (Comma-Separated Values)
- 📊 ODS (OpenDocument Spreadsheet)

**Comprimidos**:
- 📦 ZIP (archivo comprimido)
- 📦 RAR (archivo WinRAR)
- 📦 7Z (7-Zip)

**Logs y Código**:
- 📝 LOG (archivos de log)
- 📝 JSON (JavaScript Object Notation)
- 📝 XML (Extensible Markup Language)
- 📝 SQL (scripts SQL)

### Restricciones de Archivos

**Tamaño Máximo**:
- Por archivo individual: **10 MB**
- Total por caso: **100 MB**
- Archivos más grandes serán rechazados

**Seguridad**:
- Archivos ejecutables (.exe, .bat, .sh) están bloqueados por seguridad
- Scripts potencialmente peligrosos (.js, .vbs) requieren aprobación admin

### Ver y Gestionar Archivos

#### Previsualizar Archivos

**Para PDFs e Imágenes**:
1. Click en el archivo en la lista
2. Se abrirá un visor en modal
3. **Navegación en PDF**: Usa las flechas para cambiar de página
4. **Zoom en Imágenes**: Click para acercar, doble click para ajustar
5. Click fuera del modal o presiona `Esc` para cerrar

**Para otros formatos**:
- Se mostrará información del archivo (nombre, tamaño, tipo)
- Opción de descargar para ver en aplicación externa

#### Descargar Archivos

**Disponible para**: Todos los roles

1. Localiza el archivo en la lista de evidencias
2. Hover sobre el archivo
3. Click en el ícono de **Descargar** ⬇️
4. El archivo se descargará a tu carpeta de descargas

#### Eliminar Archivos

**Permisos necesarios**: INGRESO o ADMIN

1. Localiza el archivo que deseas eliminar
2. Hover sobre el archivo
3. Click en el ícono de **Eliminar** 🗑️
4. Confirma la acción en el diálogo
5. El archivo se eliminará permanentemente

> ⚠️ **Advertencia**: La eliminación de archivos es irreversible

### Información de Archivos

Para cada archivo se muestra:
- **Nombre del archivo**: Nombre original
- **Tipo**: Icono indicando el tipo de archivo
- **Tamaño**: En KB o MB
- **Fecha de carga**: Cuándo se subió
- **Usuario**: Quién lo subió

### Mejores Prácticas

✅ **Recomendado**:
- Usa nombres descriptivos para los archivos
- Organiza evidencias por tipo (screenshots, logs, reportes)
- Comprime archivos múltiples en un ZIP
- Documenta qué contiene cada archivo en una observación

❌ **Evita**:
- Subir información sensible sin encriptar
- Archivos duplicados innecesarios
- Nombres de archivo genéricos ("image1.png", "documento.pdf")
- Subir archivos no relacionados con el caso

---

## 📊 Dashboard y Estadísticas

El Dashboard proporciona una vista general del estado del sistema y métricas clave.

### Acceder al Dashboard

1. Click en **📊 Tablero** en el menú lateral
2. Es la vista predeterminada al iniciar sesión

### Métricas Principales (Cards Superiores)

En la parte superior verás cards con métricas clave:

#### Total de Casos
- **Número**: Cantidad total de casos en el sistema
- **Descripción**: Incluye todos los estados

#### Casos Abiertos 🔵
- **Número**: Casos con estado ABIERTO
- **Indicador**: Casos que requieren atención inmediata
- **Acción**: Click para filtrar solo casos abiertos

#### En Standby 🟡
- **Número**: Casos en espera
- **Descripción**: Casos pausados temporalmente
- **Uso**: Casos esperando información o acción de terceros

#### En Monitoreo 🟠
- **Número**: Casos bajo seguimiento
- **Descripción**: Casos resueltos pero en período de observación
- **Uso**: Asegurar que la solución sea estable

#### Casos Cerrados 🟢
- **Número**: Casos completamente resueltos
- **Descripción**: Casos finalizados exitosamente

### Métricas por Prioridad

Visualización de la distribución de casos según prioridad:

- 🔴 **Crítico**: Casos de máxima prioridad
- 🟠 **Alto**: Requieren atención prioritaria
- 🟡 **Medio**: Importancia estándar
- 🟢 **Bajo**: Pueden esperar

### Gráficos y Visualizaciones

#### 1. Gráfico de Casos por Estado

**Tipo**: Gráfico de dona o barras
**Muestra**: Distribución actual de casos por estado
**Actualización**: Tiempo real

**Uso**:
- Identificar carga de trabajo actual
- Ver balance entre estados
- Detectar acumulación de casos

#### 2. Gráfico de Casos por Prioridad

**Tipo**: Gráfico de barras o pastel
**Muestra**: Distribución de casos por nivel de criticidad
**Actualización**: Tiempo real

**Uso**:
- Priorizar recursos
- Identificar áreas críticas
- Planificar asignaciones

#### 3. Casos por Servicio/Plataforma

**Tipo**: Gráfico de barras horizontal
**Muestra**: Top 10 servicios con más casos
**Actualización**: Tiempo real

**Uso**:
- Identificar servicios problemáticos
- Asignar recursos de mantenimiento
- Detectar patrones de fallas

#### 4. Evolución de Casos en el Tiempo

**Tipo**: Gráfico de líneas
**Muestra**: Tendencia de casos abiertos vs cerrados
**Período**: Últimos 30, 90 o 180 días

**Uso**:
- Analizar tendencias
- Evaluar desempeño del equipo
- Planificación a futuro

### Filtros del Dashboard

Aplica filtros globales a todas las visualizaciones:

- **Rango de fechas**: Última semana, mes, trimestre, año
- **Servicio específico**: Enfoca en un servicio particular
- **Responsable**: Filtra casos de un usuario específico

### Actualización de Datos

**Actualización Automática**:
1. Toggle "Auto-refresh" en la esquina superior derecha
2. Los datos se actualizarán cada 30 segundos
3. Útil para monitoreo en tiempo real

**Actualización Manual**:
- Click en el botón **🔄 Actualizar**
- Los datos se recargarán inmediatamente
- Se muestra timestamp de última actualización

### Exportar Datos del Dashboard

1. Click en **📊 Exportar Reporte**
2. Selecciona formato:
   - PDF: Reporte visual con gráficos
   - Excel: Datos tabulares para análisis
   - PNG: Capturas de gráficos individuales

### Personalización del Dashboard

(Funcionalidad planificada para versión futura)

---

## 👥 Gestión de Usuarios

> **Nota**: Esta sección es exclusiva para usuarios con rol **ADMIN**.

### Acceder a Gestión de Usuarios

1. Click en **👥 Usuarios** en el menú lateral
2. Verás la lista completa de usuarios del sistema

### Ver Lista de Usuarios

La tabla de usuarios muestra:
- **Nombre**: Nombre completo del usuario
- **Email**: Correo electrónico (usado para login)
- **Rol**: ADMIN, INGRESO, o CONSULTA
- **Estado**: Activo o Inactivo
- **Último acceso**: Fecha y hora de última sesión
- **Acciones**: Botones para editar o eliminar

### Crear Nuevo Usuario

1. Click en **+ Nuevo Usuario** o **Crear Usuario**
2. Completa el formulario:

   **Campos Obligatorios**:
   - **Nombre Completo**: Nombre y apellido del usuario
   - **Email**: Correo corporativo (debe ser único)
   - **Contraseña Inicial**: Mínimo 8 caracteres
     - Debe incluir letras y números
     - Recomendado: incluir mayúsculas y caracteres especiales
   - **Rol**: Selecciona según permisos necesarios:
     - ADMIN: Control total del sistema
     - INGRESO: Crear y editar casos
     - CONSULTA: Solo lectura

   **Campos Opcionales**:
   - **Teléfono**: Número de contacto
   - **Departamento**: Área o equipo
   - **Notas**: Información adicional

3. Click en **Crear Usuario**

**Confirmación**:
- El usuario recibirá un email con sus credenciales (si está configurado)
- Se recomienda que cambie su contraseña en el primer inicio de sesión

### Editar Usuario

1. Localiza el usuario en la lista
2. Click en el botón **Editar** (✏️)
3. Modifica los campos necesarios:
   - Nombre
   - Email (verificar que no esté duplicado)
   - Rol (cambiar permisos)
   - Estado (activar/desactivar)
4. Click en **Guardar Cambios**

**Restricciones**:
- No puedes cambiar tu propio rol
- No puedes desactivarte a ti mismo
- Debe haber al menos un usuario ADMIN activo

### Cambiar Rol de Usuario

**Importante**: Cambiar el rol afecta inmediatamente los permisos del usuario.

**De CONSULTA a INGRESO**:
- Obtiene permisos de creación y edición
- Puede realizar operaciones masivas
- Puede subir archivos

**De INGRESO a ADMIN**:
- Obtiene acceso completo
- Puede gestionar usuarios
- Puede eliminar casos

**De ADMIN a INGRESO/CONSULTA**:
- Pierde permisos administrativos
- Requiere confirmación adicional
- Verifica que haya otro ADMIN activo

### Desactivar Usuario

Desactivar un usuario es preferible a eliminarlo:

1. Abre el usuario
2. Toggle en **Estado Activo** para desactivar
3. Confirma la acción

**Efectos de Desactivación**:
- El usuario no puede iniciar sesión
- Sus casos asignados permanecen
- Su información y auditoría se mantienen
- Puede reactivarse en cualquier momento

**Cuándo Desactivar**:
- Usuario de licencia (vacaciones, permisos)
- Usuario que cambió de área
- Usuario en proceso de salida

### Eliminar Usuario

> ⚠️ **Precaución**: La eliminación es permanente e irreversible.

1. Localiza el usuario
2. Click en el menú ⋮ (tres puntos)
3. Selecciona **Eliminar Usuario**
4. Confirma la acción

**Efectos de Eliminación**:
- Se elimina el usuario completamente
- Sus casos permanecen pero sin asignación directa
- Las observaciones y auditoría se mantienen (con ID de usuario)
- No se puede recuperar

**Recomendación**: Prefiere desactivar en lugar de eliminar.

### Restablece Contraseña de Usuario

Como ADMIN, puedes restablecer contraseñas:

1. Abre el usuario
2. Click en **Restablecer Contraseña**
3. El sistema generará una contraseña temporal
4. Cópiala y envíala al usuario de forma segura
5. El usuario debe cambiarla en su próximo inicio de sesión

### Auditoría de Usuarios

Ver acciones realizadas por un usuario:

1. Abre el usuario
2. Ve a la pestaña **Actividad** o **Auditoría**
3. Verás:
   - Casos creados
   - Casos modificados
   - Últimos accesos al sistema
   - Acciones administrativas

---

## 📤 Importar y Exportar

El módulo de Importación/Exportación permite gestionar casos de manera masiva mediante archivos Excel o CSV.

### Acceder al Módulo

1. En el menú lateral, click en **📤 Importar/Exportar**
2. Verás dos secciones principales:
   - **Importación de Casos**
   - **Exportación de Casos**

---

### Importar Casos

#### Preparar el Archivo

**Formato Soportado**: Excel (.xlsx) o CSV (.csv)

**Estructura del Archivo**:

Descarga la **plantilla de importación** para asegurar el formato correcto:
1. Click en **📥 Descargar Plantilla**
2. Abre el archivo en Excel o Google Sheets

**Columnas Requeridas**:

| Columna | Tipo | Descripción | Ejemplo |
|---------|------|-------------|---------|
| codigo | Texto | Código único del caso | HP-0001 |
| servicio_o_plataforma | Texto | Servicio afectado | VPN Corporativa |
| prioridad | Texto | CRITICO, ALTO, MEDIO, BAJO | ALTO |
| motivo | Texto | Descripción del problema | Falla en autenticación |
| estado | Texto (opcional) | ABIERTO, STANDBY, EN_MONITOREO, CERRADO | ABIERTO |
| sby_responsable | Texto (opcional) | Nombre del responsable | Juan Pérez |
| observaciones | Texto (opcional) | Comentarios separados por \| | Obs 1\|Obs 2\|Obs 3 |

**Ejemplo de Datos**:
```
codigo,servicio_o_plataforma,prioridad,motivo,estado,sby_responsable,observaciones
HP-0001,VPN Corporativa,CRITICO,Falla autenticación,ABIERTO,Juan Pérez,Usuario reporta error|Se investiga causa
HP-0002,Servidor Web,ALTO,Lentitud,EN_MONITOREO,María García,Reinicio aplicado|Monitoreando
HP-0003,Base de Datos,MEDIO,Backup fallido,CERRADO,Carlos López,Problema resuelto
```

#### Importación con Múltiples Observaciones

Para agregar varias observaciones a un caso:
- Separa cada observación con el carácter `|` (pipe)
- Ejemplo: `Observación 1|Observación 2|Observación 3`
- Cada observación se guardará como entidad separada
- Se mantiene el orden cronológico

#### Realizar la Importación

1. Prepara tu archivo según la plantilla
2. Click en **Seleccionar Archivo** o arrastra el archivo
3. El sistema validará el formato automáticamente
4. Verás un preview de los datos a importar
5. Revisa que la información sea correcta
6. Click en **Importar Casos**

**Proceso de Importación**:
- El sistema procesa cada fila
- Se validan todos los campos
- Se crean los casos y observaciones
- Se muestra un reporte de resultados

#### Reporte de Importación

Después de importar verás:
- ✅ **Casos importados exitosamente**: Cantidad
- ⚠️ **Casos con advertencias**: Casos importados con notas
- ❌ **Casos con errores**: Cantidad de casos no importados
- 📋 **Detalle de errores**: Fila y razón del error

**Errores Comunes**:
- Código duplicado (ya existe en el sistema)
- Prioridad inválida (no es CRITICO, ALTO, MEDIO o BAJO)
- Estado inválido
- Campos requeridos vacíos
- Formato de fecha incorrecto

#### Importación desde Sistema Legacy

Para migrar casos de sistemas antiguos:

1. Click en **Importar desde Legacy**
2. Selecciona el archivo del sistema antiguo
3. El sistema mapeará automáticamente los campos
4. Revisa el mapeo y ajusta si es necesario
5. Click en **Iniciar Migración**

**Mapeo Automático**:
- El sistema reconoce formatos comunes
- Convierte estados a la nomenclatura nueva
- Ajusta campos de fecha y hora

---

### Exportar Casos

#### Exportación Básica

**Exportar Todos los Casos**:

1. En la sección **Exportación**, selecciona el formato:
   - 📊 **Excel (.xlsx)**: Recomendado para análisis y edición
   - 📄 **CSV (.csv)**: Compatible con múltiples aplicaciones
   - 📋 **TSV (.tsv)**: Tab-separated values

2. Click en **Exportar Todos los Casos**
3. El archivo se descargará automáticamente

#### Exportación con Filtros

Para exportar solo casos específicos:

1. Aplica filtros en el Tablero:
   - Por fecha
   - Por estado
   - Por prioridad
   - Por servicio
   - Por responsable

2. En el módulo de exportación, click en **Exportar Casos Filtrados**
3. Solo se exportarán los casos que cumplan los filtros

#### Exportación con Observaciones

**Formato Especial** que incluye todas las observaciones:

1. Selecciona **Exportar con Observaciones**
2. Elige el formato (Excel o CSV)
3. El archivo incluirá:
   - Información básica del caso
   - Todas las observaciones (cada una en su columna o fila)
   - Metadatos de observaciones (autor, fecha)
   - Timeline de cambios

**Estructura del Excel**:
- **Hoja 1**: Casos (información principal)
- **Hoja 2**: Observaciones (detalladas)
- **Hoja 3**: Auditoría (opcional)

#### Exportación Programada

(Funcionalidad planificada para versión futura)

#### Opciones Avanzadas de Exportación

**Personalizar Columnas**:
1. Click en **⚙️ Opciones de Exportación**
2. Selecciona las columnas que deseas incluir
3. Reordena arrastrando
4. Click en **Exportar**

**Columnas Disponibles**:
- Información básica (código, servicio, prioridad, estado)
- Fechas (creación, última actualización, cierre)
- Usuarios (creador, responsable)
- Observaciones (todas o resumen)
- Archivos adjuntos (lista de nombres)
- Auditoría (cambios realizados)

### Casos de Uso Comunes

#### Respaldo Periódico

1. Exporta todos los casos mensualmente
2. Guarda el archivo en ubicación segura
3. Documentación de cumplimiento y auditoría

#### Reportes para Gerencia

1. Filtra casos por período (último mes/trimestre)
2. Exporta con todas las observaciones
3. Genera reporte ejecutivo en Excel

#### Migración entre Ambientes

1. Exporta casos de desarrollo/staging
2. Importa en ambiente de producción
3. Valida que todo se haya migrado correctamente

#### Análisis de Datos

1. Exporta a Excel con todas las columnas
2. Usa tablas dinámicas para análisis
3. Genera gráficos personalizados

---

## ⚙️ Configuración de Perfil

### Acceder a Configuración

1. Click en tu **avatar** en la esquina superior derecha
2. Selecciona **Perfil** o **Configuración**

### Información Personal

**Editar tus datos**:
- Nombre completo
- Email (verificar si cambias)
- Teléfono
- Departamento

**Nota**: Algunos campos pueden estar bloqueados por el administrador.

### Cambiar Contraseña

**Requisitos de Seguridad**:
- Mínimo 8 caracteres
- Al menos una letra mayúscula
- Al menos un número
- Recomendado: incluir caracteres especiales

**Procedimiento**:
1. Ve a **Cambiar Contraseña**
2. Ingresa tu **contraseña actual**
3. Ingresa la **nueva contraseña**
4. Confirma la **nueva contraseña**
5. Click en **Guardar**

**Consejos**:
- No uses información personal obvia
- No reutilices contraseñas de otros sitios
- Cambia tu contraseña periódicamente (cada 90 días recomendado)

### Preferencias de Notificaciones

Configura cómo quieres recibir notificaciones:

**Tipos de Notificaciones**:
- ✉️ Email: Notificaciones por correo
- 🔔 Push: Notificaciones en navegador
- 📱 SMS: Mensajes de texto (si está configurado)

**Eventos**:
- ☑️ Caso asignado a mí
- ☑️ Cambios en mis casos
- ☑️ Menciones en observaciones
- ☑️ Recordatorios de casos pendientes
- ☑️ Resumen diario/semanal

### Configuración de Interfaz

**Tema**:
- ☀️ Claro
- 🌙 Oscuro
- 🔄 Automático (según hora del día)

**Idioma**:
- Español (predeterminado)
- Inglés (si está disponible)

**Zona Horaria**:
- Ajusta según tu ubicación
- Afecta visualización de fechas y horas
- No afecta datos almacenados (siempre UTC)

**Densidad de Interfaz**:
- Cómoda: Más espacio entre elementos
- Compacta: Más información en pantalla

### Privacidad y Seguridad

**Sesiones Activas**:
- Ve dispositivos con sesión activa
- Cierra sesiones remotas si es necesario
- Protege tu cuenta

**Registro de Actividad**:
- Revisa tus últimas acciones
- Detecta actividad sospechosa
- Audita tu propio uso

### Exportar Mis Datos

Solicita una copia de toda tu información:

1. Ve a **Privacidad y Datos**
2. Click en **Solicitar Mis Datos**
3. Recibirás un email cuando esté listo
4. Descarga el archivo ZIP con tu información

**Incluye**:
- Casos creados y modificados por ti
- Tus observaciones
- Archivos que subiste
- Historial de actividad

---

## ❓ Preguntas Frecuentes

### General

**P: ¿Puedo acceder desde mi móvil?**
R: Sí, la interfaz es responsive y funciona en dispositivos móviles. Para mejor experiencia, usa la vista horizontal en tablets.

**P: ¿Qué navegadores son compatibles?**
R: Chrome, Firefox, Safari y Edge (versiones actuales). No soportamos Internet Explorer.

**P: ¿Los datos están seguros?**
R: Sí, usamos encriptación HTTPS, autenticación JWT y almacenamiento seguro. Los backups son automáticos.

### Gestión de Casos

**P: ¿Puedo eliminar un caso? 🆕**
R: Solo los usuarios ADMIN pueden eliminar casos. Esta acción es irreversible y elimina también observaciones, archivos y auditoría.

**P: ¿Cómo sé quién modificó un caso? 🆕**
R: Ve al Timeline del caso. Allí verás todos los cambios con el nombre del usuario y fecha/hora exacta.

**P: ¿Puedo editar observaciones de otros usuarios? 🆕**
R: Depende de tu rol:
- CONSULTA: Solo tus propias observaciones
- INGRESO/ADMIN: Cualquier observación

**P: ¿Qué pasa si dos usuarios editan el mismo caso simultáneamente?**
R: El sistema maneja concurrencia. El último cambio guardado prevalece y ambos usuarios ven una notificación.

### Observaciones

**P: ¿Puedo eliminar una observación?**
R: No, solo editarla. Esto asegura trazabilidad completa.

**P: ¿Las observaciones editadas muestran el cambio?**
R: Sí, se muestra un indicador "Editado" con la fecha de edición.

**P: ¿Cuántas observaciones puedo agregar?**
R: Sin límite. Sin embargo, considera la legibilidad y relevancia.

### Operaciones Masivas 🆕

**P: ¿Cuántos casos puedo actualizar a la vez?**
R: Máximo 100 casos por operación. Para más, realiza múltiples operaciones.

**P: ¿Se pueden deshacer las operaciones masivas?**
R: No hay función de deshacer, pero todos los cambios están auditados. Puedes revertir manualmente viendo el Timeline.

**P: ¿Qué pasa si falla una operación masiva?**
R: La operación es atómica: o se aplica a todos los casos o a ninguno.

### Archivos

**P: ¿Qué pasa con los archivos si elimino un caso?**
R: Se eliminan permanentemente junto con el caso. Haz backup si es necesario.

**P: ¿Puedo subir archivos desde mi móvil?**
R: Sí, pero la experiencia es mejor en desktop. Puedes tomar fotos y subirlas directamente.

**P: ¿Los archivos tienen backup?**
R: Sí, hay backups automáticos diarios. Contacta al administrador para restauraciones.

### Búsqueda y Filtros

**P: ¿La búsqueda es en tiempo real?**
R: Sí, los resultados se actualizan mientras escribes.

**P: ¿Puedo guardar mis filtros favoritos?**
R: Esta funcionalidad está planificada para una versión futura.

**P: ¿Cómo busco por múltiples criterios?**
R: Usa los filtros avanzados en el Dashboard. Puedes combinar estado, prioridad, fecha, etc.

### Importación/Exportación

**P: ¿Qué formato debo usar para importar?**
R: Excel (.xlsx) o CSV (.csv). Descarga la plantilla para asegurar el formato correcto.

**P: ¿Puedo importar casos con observaciones múltiples?**
R: Sí, separa cada observación con `|` en la columna de observaciones.

**P: ¿Qué pasa si hay códigos duplicados al importar?**
R: Esos casos se saltarán y aparecerán en el reporte de errores. Debes cambiar el código o eliminar el caso existente primero.

### Performance

**P: ¿El sistema se vuelve lento con muchos casos?**
R: No, la paginación y los índices de base de datos aseguran buen rendimiento. Si notas lentitud, contacta al administrador.

**P: ¿Cada cuánto se actualizan las estadísticas?**
R: En tiempo real. Puedes activar auto-refresh para actualización automática cada 30 segundos.

### Seguridad y Acceso

**P: ¿Por cuánto tiempo permanezco logueado?**
R: 30 minutos de inactividad. El token se renueva automáticamente con actividad.

**P: ¿Puedo tener múltiples sesiones abiertas?**
R: Sí, puedes estar logueado en múltiples dispositivos simultáneamente.

**P: ¿Qué hago si olvidé mi contraseña?**
R: Usa la opción "Olvidé mi contraseña" en la pantalla de login o contacta al administrador.

### Soporte y Ayuda

**P: ¿Dónde reporto un problema?**
R: Usa el botón "Reportar Problema" en el menú de usuario o contacta a:
- Email: support@standbymanager.com
- Interno: Equipo de TI

**P: ¿Hay capacitación disponible?**
R: Sí, solicita una sesión de capacitación al administrador del sistema.

**P: ¿Cómo sugiero una mejora?**
R: Usa el formulario de "Sugerencias" en el menú de usuario o contacta directamente al equipo de desarrollo.

---

## 📞 Soporte y Contacto

### Equipo de Desarrollo

- **Allan Córdova**: [aacordov@gmail.com](mailto:aacordov@gmail.com)
- **José Briones**: [josmbrio@gmail.com](mailto:josmbrio@gmail.com)
- **Larry Sánchez**: [lajasanc@gmail.com](mailto:lajasanc@gmail.com)
- **Ronny Ortiz**: [ronny.ortiz.54@hotmail.com](mailto:ronny.ortiz.54@hotmail.com)

### Canales de Soporte

- 📧 **Email de Soporte**: support@standbymanager.com
- 💬 **Chat Interno**: Canal #soporte-standby (si aplica)
- 📞 **Teléfono**: (Extensión proporcionada por tu organización)
- 🐛 **Reportar Bug**: [GitHub Issues](https://github.com/rortiz-09/standby-case-manager/issues)

### Horario de Atención

- **Lunes a Viernes**: 8:00 AM - 6:00 PM
- **Respuesta esperada**: 24-48 horas (días hábiles)
- **Emergencias**: Contacto 24/7 para usuarios ADMIN

---

## 📚 Recursos Adicionales

- 📘 **Documentación Técnica**: Para desarrolladores y administradores
- 🔧 **API Reference**: Documentación de la API REST
- 🎓 **Video Tutoriales**: (En desarrollo)
- 📖 **Changelog**: Historial de versiones y cambios

---

**Versión del Manual**: 2.3.0  
**Última actualización**: Enero 26, 2026  
**Desarrollado con ❤️ por el equipo de Standby Case Manager**
