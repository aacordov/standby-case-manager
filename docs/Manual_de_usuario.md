# 📖 Manual de Usuario - Standby Case Manager

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Inicio de Sesión](#inicio-de-sesión)
3. [Panel Principal](#panel-principal)
4. [Gestión de Casos](#gestión-de-casos)
5. [Búsqueda y Filtros](#búsqueda-y-filtros)
6. [Command Palette](#command-palette)
7. [Gestión de Archivos](#gestión-de-archivos)
8. [Dashboard y Estadísticas](#dashboard-y-estadísticas)
9. [Gestión de Usuarios](#gestión-de-usuarios)
10. [Importar y Exportar](#importar-y-exportar)
11. [Configuración de Perfil](#configuración-de-perfil)
12. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## 📌 Introducción

Standby Case Manager es un sistema diseñado para gestionar casos de operación de manera eficiente. Este manual te guiará paso a paso en el uso de todas sus funcionalidades.

### Roles de Usuario

El sistema cuenta con tres roles principales:

| Rol | Permisos | Descripción |
|:----|:---------|:------------|
| **👑 Admin** | Acceso total | Gestión completa de casos, usuarios y configuración |
| **✍️ Ingreso** | Crear/Editar | Puede crear y modificar casos, pero no eliminarlos |
| **👁️ Consulta** | Solo lectura | Visualización de casos sin capacidad de modificación |

---

## 🔐 Inicio de Sesión

### Acceso al Sistema

1. Abre tu navegador web y accede a `http://localhost:3000`
2. Verás la pantalla de inicio de sesión

### Credenciales

Ingresa tus credenciales proporcionadas por el administrador:

```
Email: tu-email@empresa.com
Contraseña: tu-contraseña-segura
```

### Cambio de Tema

Antes de iniciar sesión, puedes cambiar entre tema claro y oscuro haciendo clic en el ícono 🌙/☀️ en la esquina superior derecha.

### Primer Inicio de Sesión

Si es tu primera vez:

1. Usa las credenciales proporcionadas
2. Se recomienda cambiar tu contraseña inmediatamente
3. Ve a **Perfil > Cambiar Contraseña**

---

## 🏠 Panel Principal

Una vez iniciada la sesión, verás el panel principal con:

### Barra de Navegación Superior

- **Logo**: Click para volver al inicio
- **Buscador**: Campo de búsqueda global
- **Command Palette**: Botón con ícono de comando (⌘)
- **Notificaciones**: Campana para ver alertas
- **Usuario**: Avatar con menú desplegable

### Menú Lateral

- 📊 **Tablero**: Vista general y estadísticas
- ➕ **Nuevo Caso**: Crear un caso nuevo
- 📤 **Importar/Exportar**: Gestión masiva de casos
- 👥 **Usuarios**: Gestión de usuarios (solo Admin)
- 💻 **Desarrolladores**: Información del equipo

---

## 📋 Gestión de Casos

### Ver Lista de Casos

1. Click en **Tablero** en el menú lateral
2. Verás una tabla con todos los casos
3. Cada caso muestra:
   - Código del caso
   - Servicio/Plataforma
   - Estado (Abierto, Standby, En Monitoreo, Cerrado)
   - Prioridad (🔴 Crítico, 🟠 Alto, 🟡 Medio, 🟢 Bajo)
   - Responsable
   - Fecha de actualización

### Crear Nuevo Caso

1. Click en **Nuevo Caso** en el menú lateral
2. Completa el formulario:
   ```
   - Código: Identificador único (ej: HP-0001)
   - Servicio/Plataforma: Sistema afectado
   - Prioridad: Crítico / Alto / Medio / Bajo
   - Estado: Abierto (por defecto)
   - Responsable: Usuario asignado
   - Novedades: Descripción del caso
   ```
3. Click en **Guardar Caso**

### Editar un Caso

1. En el Tablero, click en **Ver** junto al caso
2. Se abrirá la vista detallada
3. Click en **Editar**
4. Modifica los campos necesarios
5. Click en **Guardar Cambios**

### Ver Detalles de un Caso

1. Click en **Ver** junto a cualquier caso
2. Se abrirá un panel con:
   - Información completa del caso
   - Observaciones/comentarios
   - Historial de cambios
   - Archivos adjuntos
   - Auditoría de acciones

### Cambiar Estado de un Caso

En la vista detallada o edición:

1. Selecciona el nuevo estado:
   - 🔵 **Abierto**: Caso nuevo o reabierto
   - 🟡 **Standby**: En espera
   - 🟠 **En Monitoreo**: Requiere seguimiento
   - 🟢 **Cerrado**: Caso resuelto

### Agregar Observaciones

1. En la vista detallada del caso
2. Scroll hasta la sección de observaciones
3. Escribe tu comentario en el campo de texto
4. Click en **Agregar Observación**

### Eliminar un Caso (Solo Admin)

1. Abre el caso
2. Click en el menú ⋮ (tres puntos)
3. Selecciona **Eliminar**
4. Confirma la acción

> ⚠️ **Advertencia**: Esta acción no se puede deshacer

---

## 🔍 Búsqueda y Filtros

### Búsqueda Rápida

En el Tablero:

1. Usa el campo de búsqueda en la parte superior
2. Escribe palabras clave
3. Los resultados se filtrarán automáticamente

Puedes buscar por:
- Código de caso
- Servicio/Plataforma
- Responsable
- Comentarios

### Filtros Avanzados

#### Por Fecha

Click en el selector de fechas y elige:

- **Presets rápidos**:
  - 📅 Último mes (1M)
  - 📅 Últimos 3 meses (3M)
  - 📅 Últimos 6 meses (6M)
  - 📅 Personalizado

- **Rango personalizado**:
  1. Click en "Personalizado"
  2. Selecciona fecha inicio
  3. Selecciona fecha fin
  4. Click en "Aplicar"

#### Por Prioridad

- 🔴 Crítico
- 🟠 Alto
- 🟡 Medio
- 🟢 Bajo

#### Por Estado

- 🔵 Abierto
- 🟡 Standby
- 🟠 En Monitoreo
- 🟢 Cerrado

#### Por Servicio/Plataforma

Escribe el nombre del servicio en el campo correspondiente.

#### Por Responsable

Escribe el nombre del responsable en el campo correspondiente.

### Limpiar Filtros

Click en el botón **Limpiar** para resetear todos los filtros.

---

## ⌨️ Command Palette

El Command Palette te permite acceder rápidamente a cualquier función del sistema.

### Abrir Command Palette

- **Atajo de teclado**: `Ctrl + K` (Windows/Linux) o `Cmd + K` (Mac)
- **Botón**: Click en el ícono ⌘ en la barra superior

### Comandos Disponibles

```
🔍 Buscar casos...
➕ Crear nuevo caso
📤 Importar/Exportar casos
👥 Ver usuarios
📊 Ir a tablero
⚙️ Configuración
🚪 Cerrar sesión
```

### Navegación

1. Escribe para filtrar comandos
2. Usa ↑ ↓ para moverte entre opciones
3. Presiona Enter para ejecutar

---

## 📂 Gestión de Archivos

### Subir Archivos

#### Método 1: Drag & Drop

1. Abre un caso
2. Ve a la sección "Evidencias"
3. Arrastra los archivos desde tu explorador
4. Suéltalos en el área designada

#### Método 2: Click

1. Click en **📎 Adjuntar archivos**
2. Selecciona archivos de tu computadora
3. Click en **Abrir**

### Formatos Soportados

- 📄 Documentos: PDF, DOC, DOCX, TXT
- 🖼️ Imágenes: JPG, PNG, GIF, WEBP
- 📊 Hojas de cálculo: XLS, XLSX, CSV
- 📦 Comprimidos: ZIP, RAR
- 📝 Logs: LOG, TXT

### Tamaño Máximo

- Por archivo: 10 MB
- Total por caso: 100 MB

### Previsualizar Archivos

1. Click en el archivo en la lista
2. Se abrirá una vista previa (para PDFs e imágenes)
3. Click fuera para cerrar

### Descargar Archivos

1. Hover sobre el archivo
2. Click en el ícono de descarga ⬇️

### Eliminar Archivos (Solo Admin/Ingreso)

1. Hover sobre el archivo
2. Click en el ícono de eliminar 🗑️
3. Confirma la acción

---

## 📊 Dashboard y Estadísticas

### Vista General

El dashboard muestra:

#### Métricas Principales

- 📈 **Total de Casos**: Cantidad total en el sistema
- 🔵 **Casos Abiertos**: Casos sin resolver
- 🟡 **En Standby**: Casos en espera
- 🟠 **En Monitoreo**: Casos bajo seguimiento
- 🟢 **Cerrados**: Casos completados

#### Gráficos

1. **Casos por Estado**
   - Visualización de distribución actual
   - Actualizados en tiempo real

2. **Casos por Prioridad**
   - Gráfico mostrando criticidad
   - Útil para priorizar trabajo

3. **Casos por Servicio**
   - Distribución por plataforma
   - Identifica áreas con más incidentes

### Actualización de Datos

- **Auto-refresh**: Activa el toggle para actualización automática cada 30 segundos
- **Manual**: Los datos se actualizan al cargar la página

---

## 👥 Gestión de Usuarios

> **Nota**: Solo disponible para usuarios con rol Admin

### Ver Lista de Usuarios

1. Click en **Usuarios** en el menú
2. Verás todos los usuarios registrados

### Crear Nuevo Usuario

1. Click en **+ Nuevo Usuario**
2. Completa el formulario:
   ```
   Nombre completo: Nombre del usuario
   Email: correo@empresa.com
   Rol: Admin / Ingreso / Consulta
   Contraseña inicial: mínimo 8 caracteres
   ```
3. Click en **Crear Usuario**

### Editar Usuario

1. Click en el usuario
2. Modifica los campos necesarios
3. Click en **Guardar**

### Cambiar Rol

1. Abre el usuario
2. Selecciona el nuevo rol
3. Click en **Guardar**

### Desactivar Usuario

1. Abre el usuario
2. Toggle en "Estado activo"
3. Confirma

> **Nota**: Los usuarios desactivados no pueden iniciar sesión

### Eliminar Usuario

1. Click en ⋮ junto al usuario
2. Selecciona **Eliminar**
3. Confirma la acción

> ⚠️ Se reasignarán automáticamente sus casos abiertos

---

## 📤 Importar y Exportar

El sistema cuenta con un módulo dedicado para importar y exportar casos de manera masiva.

### Acceder al Módulo

1. En el menú lateral, click en **📤 Importar/Exportar**
2. Verás dos secciones principales:
   - **Importación de Casos**
   - **Exportación de Casos**

---

### Importar Casos

#### Importación con Observaciones

Esta opción permite importar casos con múltiples observaciones asociadas:

**Pasos:**

1. En la sección **Importar Casos**, selecciona:
   - **Archivo de Casos** (requerido): Excel con la información de los casos
   - **Archivo de Observaciones** (opcional): Excel con las observaciones

2. Click en **Importar Casos**

3. Verás el resultado de la importación:
   ```
   ✅ 158 casos importados correctamente
   ✅ 0 casos actualizados
   ✅ 429 observaciones importadas
   ```

#### Formato de Archivos

**Archivo de Casos** (`casos_para_import.xlsx`):

| Columna | Requerido | Ejemplo | Descripción |
|---------|-----------|---------|-------------|
| codigo | ✅ | HP-0001 | Identificador único |
| servicio_o_plataforma | ✅ | HP | Nombre del servicio |
| estado | ✅ | CaseStatus.ABIERTO | Estado del caso |
| prioridad | ✅ | Priority.ALTO | Nivel de prioridad |
| sby_responsable | ❌ | Andrea Coello | Nombre del responsable |
| fecha_inicio | ❌ | 2024-01-19 | Fecha de apertura |
| fecha_fin | ❌ | 2024-03-15 | Fecha de cierre (si aplica) |
| novedades_y_comentarios | ❌ | Descripción detallada | Información del caso |

**Valores válidos para Estado:**
- `CaseStatus.ABIERTO` o `ABIERTO`
- `CaseStatus.STANDBY` o `STANDBY`
- `CaseStatus.EN_MONITOREO` o `EN_MONITOREO`
- `CaseStatus.CERRADO` o `CERRADO`

**Valores válidos para Prioridad:**
- `Priority.CRITICO` o `CRITICO`
- `Priority.ALTO` o `ALTO`
- `Priority.MEDIO` o `MEDIO`
- `Priority.BAJO` o `BAJO`

---

**Archivo de Observaciones** (`observaciones_para_import.xlsx`):

| Columna | Requerido | Ejemplo | Descripción |
|---------|-----------|---------|-------------|
| case_codigo | ✅ | HP-0001 | Código del caso relacionado |
| content | ✅ | [ABIERTO] Primera actualización | Contenido de la observación |
| created_at | ✅ | 2024-01-19 | Fecha de la observación |
| responsable_momento | ❌ | MVI | Responsable en ese momento |
| estado_momento | ❌ | ABIERTO | Estado en ese momento |

---

#### Validaciones Automáticas

El sistema validará:
- ✅ Columnas requeridas presentes
- ✅ Formato de enums (estados, prioridades)
- ✅ Formato de fechas (acepta múltiples formatos)
- ✅ Existencia de casos para observaciones
- ✅ Duplicados (actualiza en lugar de duplicar)

#### Manejo de Duplicados

- Si un caso con el mismo **código** ya existe, el sistema lo **actualizará** en lugar de crear uno nuevo
- Si una observación con el mismo contenido ya existe para un caso, se **omitirá**

#### Manejo de Errores

Si hay errores durante la importación, verás un resumen detallado:

```
⚠️ Importación completada con algunos errores

Casos importados: 155
Casos actualizados: 3
Observaciones importadas: 425

Errores en Casos (2):
• Fila 15: Campo 'codigo' es requerido
• Fila 23: Estado inválido: 'PENDIENTE'

Errores en Observaciones (4):
• Fila 8: Caso 'HP-9999' no encontrado
• Fila 12: Campo 'content' es requerido
```

---

### Exportar Casos

#### Exportación Completa (Casos + Observaciones)

Exporta todos los casos con sus observaciones en un archivo Excel con 2 hojas:

**Pasos:**

1. En la sección **Exportar Casos**, bajo **Exportación Completa (Casos + Observaciones)**
2. Click en **Excel** o **CSV**
3. El archivo se descargará automáticamente como `casos_y_observaciones_export.xlsx`

**Contenido del archivo Excel:**
- **Hoja 1 - "Casos"**: Información completa de todos los casos
- **Hoja 2 - "Observaciones"**: Todas las observaciones vinculadas con `case_codigo`

**Columnas en la hoja "Casos":**
- codigo, servicio_o_plataforma, estado, prioridad
- sby_responsable, fecha_inicio, fecha_fin
- novedades_y_comentarios, observaciones
- creado_por_id, created_at, updated_at

**Columnas en la hoja "Observaciones":**
- id, case_codigo, numero_observacion
- content, created_by_id, created_at

---

#### Exportación Simple (Solo Casos)

Exporta únicamente la información de casos en un solo archivo:

**Pasos:**

1. Bajo **Exportación Simple (Solo Casos)**, click en:
   - **Excel** (formato .xlsx)
   - **CSV** (formato .csv)
   - **TSV** (formato .tsv)

2. El archivo se descargará con todos los casos actuales

**Cuándo usar cada formato:**
- **Excel (.xlsx)**: Para análisis en hojas de cálculo con formato
- **CSV**: Para importar en otras herramientas o bases de datos
- **TSV**: Para compatibilidad con sistemas legacy

---

### Casos de Uso Comunes

#### 📋 Backup de Datos

```
Objetivo: Respaldar todos los casos y observaciones

1. Ir a Importar/Exportar
2. Click en "Excel" bajo Exportación Completa
3. Guardar archivo con fecha: backup_casos_2025-01-19.xlsx
4. Guardar en ubicación segura
```

#### 🔄 Migrar Datos de Excel Legacy

```
Objetivo: Importar datos de formato antiguo

1. Usar script de transformación (si aplica)
2. Generar casos_para_import.xlsx y observaciones_para_import.xlsx
3. En Importar/Exportar, seleccionar ambos archivos
4. Click en "Importar Casos"
5. Verificar resultados
```

#### 📊 Análisis en Excel

```
Objetivo: Analizar datos fuera del sistema

1. Exportar casos (Exportación Simple - Excel)
2. Abrir en Microsoft Excel o Google Sheets
3. Crear tablas dinámicas y gráficos
4. Generar reportes personalizados
```

#### 🔁 Actualización Masiva

```
Objetivo: Actualizar múltiples casos a la vez

1. Exportar casos actuales
2. Modificar datos en Excel (responsables, estados, etc.)
3. Re-importar el archivo modificado
4. El sistema actualizará los casos existentes
```

#### 📥 Importación Inicial

```
Objetivo: Cargar casos por primera vez

1. Descargar plantilla de ejemplo (si disponible)
2. Completar con datos de casos
3. Opcional: Crear archivo de observaciones
4. Importar ambos archivos
5. Verificar que todos los casos se importaron correctamente
```

---

### Tips y Mejores Prácticas

#### ✅ Preparación de Archivos

- **Usa las plantillas**: Si es tu primera vez, usa los archivos de ejemplo
- **Revisa los datos**: Verifica que no haya espacios extra o caracteres especiales
- **Fechas consistentes**: Usa formato ISO (YYYY-MM-DD) para mayor compatibilidad
- **Códigos únicos**: Asegúrate de que cada caso tenga un código único

#### ✅ Durante la Importación

- **Empieza pequeño**: Prueba con 5-10 casos primero
- **Revisa errores**: Lee cuidadosamente los mensajes de error
- **Backup previo**: Exporta tus datos actuales antes de importaciones grandes
- **Verifica resultados**: Revisa que los casos importados se vean correctos

#### ✅ Exportaciones

- **Filtra antes**: Si solo necesitas ciertos casos, aplica filtros en el Tablero primero
- **Nombramiento**: Usa nombres descriptivos con fecha (ej: casos_enero_2025.xlsx)
- **Respaldos regulares**: Exporta semanalmente para tener backups

#### ⚠️ Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Missing required columns" | Falta una columna obligatoria | Agrega la columna faltante |
| "Estado inválido" | Valor no permitido en estado | Usa valores válidos: ABIERTO, STANDBY, EN_MONITOREO, CERRADO |
| "Caso no encontrado" | Observación referencia caso inexistente | Verifica que el case_codigo sea correcto |
| "Código duplicado" | Ya existe un caso con ese código | El sistema lo actualizará automáticamente |

---

## ⚙️ Configuración de Perfil

### Acceder a tu Perfil

1. Click en tu avatar (esquina superior derecha)
2. Selecciona **Mi Perfil**

### Información Personal

Puedes actualizar:
- Nombre completo
- Email
- Teléfono (opcional)
- Zona horaria

### Cambiar Contraseña

1. Ve a **Mi Perfil > Seguridad**
2. Completa:
   ```
   Contraseña actual: ********
   Nueva contraseña: ********
   Confirmar nueva contraseña: ********
   ```
3. Click en **Cambiar Contraseña**

**Requisitos de contraseña**:
- Mínimo 8 caracteres
- Al menos una mayúscula
- Al menos un número
- Al menos un carácter especial (recomendado)

### Preferencias

Personaliza tu experiencia:

- **Tema**: Claro / Oscuro / Auto (según sistema)
- **Idioma**: Español (actual)
- **Notificaciones**: Activar/desactivar
- **Formato de fecha**: DD/MM/YYYY o MM/DD/YYYY
- **Zona horaria**: Selecciona tu zona local

### Avatar

Tu avatar se genera automáticamente basado en tu email (hash único y colorido).

---

## ❓ Preguntas Frecuentes

### ¿Cómo recupero mi contraseña?

1. En la pantalla de login, click en "¿Olvidaste tu contraseña?"
2. Ingresa tu email
3. Recibirás un link de recuperación
4. Sigue las instrucciones del email

### ¿Por qué no puedo editar un caso?

Verifica que:
- Tengas rol de Admin o Ingreso
- El caso no esté cerrado (los casos cerrados requieren permisos especiales)
- Tengas permisos sobre ese caso específico

### ¿Cómo cambio la zona horaria?

1. Ve a **Mi Perfil > Preferencias**
2. Selecciona tu zona horaria
3. Click en **Guardar**
4. Los timestamps se ajustarán automáticamente

### ¿Puedo recuperar un caso eliminado?

No, la eliminación es permanente. Solo usuarios Admin pueden eliminar casos. Por seguridad, los casos importantes no deben eliminarse, sino cerrarse.

### ¿Cuál es el límite de casos?

No hay límite definido. El sistema puede manejar miles de casos eficientemente gracias a la paginación y filtros optimizados.

### ¿Se guardan automáticamente los cambios?

No, debes hacer click en **Guardar** para que los cambios persistan. Sin embargo, los borradores se guardan localmente en tu navegador.

### ¿Cómo sé si hay actualizaciones en un caso?

- Los casos actualizados recientemente aparecen primero si ordenas por fecha
- Puedes usar el filtro de fecha para ver casos de los últimos días

### ¿Puedo trabajar offline?

No, Standby Case Manager requiere conexión a internet para funcionar correctamente. Los datos se sincronizan en tiempo real.

### ¿Los archivos se respaldan?

Sí, todos los archivos se almacenan de forma segura en el servidor y se respaldan diariamente mediante snapshots automáticos.

### ¿Cuántas observaciones puede tener un caso?

No hay límite. Un caso puede tener desde cero hasta miles de observaciones. Cada observación tiene su propia fecha y autor.

### ¿Puedo exportar solo ciertos casos?

Sí. Primero aplica los filtros que desees en el Tablero (por fecha, estado, prioridad, etc.), luego ve a Importar/Exportar. La exportación respetará los filtros activos.

### ¿Qué pasa si importo casos que ya existen?

El sistema detecta duplicados por el campo `codigo`. Si un caso ya existe, actualizará su información en lugar de crear uno nuevo.

### ¿Cómo reporto un bug?

1. Click en tu avatar
2. Selecciona **Reportar problema**
3. Describe el problema detalladamente
4. Incluye pasos para reproducir el error
5. Envía el reporte

---

## 📞 Soporte Técnico

Si necesitas ayuda adicional:

- 📧 **Email de Soporte**:
  - **Allan Córdova**: [aacordov@gmail.com](mailto:aacordov@gmail.com)
  - **José Briones**: [josmbrio@gmail.com](mailto:josmbrio@gmail.com)
  - **Larry Sánchez**: [lajasanc@gmail.com](mailto:lajasanc@gmail.com)
  - **Ronny Ortiz**: [ronny.ortiz.54@hotmail.com](mailto:ronny.ortiz.54@hotmail.com)

- 💬 **Horario de atención**: Lunes a Viernes, 9:00 AM - 6:00 PM

- 🐛 **Reportar bugs**: Usa la opción "Reportar problema" en tu perfil

---

**Última actualización**: Enero 2026  
**Versión del manual**: 2.3.0  
**Sistema**: Standby Case Manager v2.2.3