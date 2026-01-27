import io
import pandas as pd
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Case, CaseCreate, CaseStatus, Priority, Observation, CaseAudit, CaseAuditType, User
from app.auth import get_current_user
import re
from datetime import datetime
from sqlmodel import delete

# Regex to find cases: [STATUS] CASO CODE. DESCRIPTION
CASE_PATTERN = re.compile(r"\[(ABIERTO|CERRADO|EN MONITOREO|STANDBY|PENDIENTE)\]\s*CASO\s*([^.]+)\.?\s*(.*)", re.IGNORECASE | re.DOTALL)


router = APIRouter(prefix="/cases-io", tags=["Import/Export"])


# ==========================================
# NUEVO: IMPORTAR CASOS CON OBSERVACIONES
# ==========================================
@router.post("/import-with-observations", status_code=201)
async def import_cases_with_observations(
    casos_file: UploadFile = File(...),
    observaciones_file: UploadFile = File(None),  # Opcional
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Importa casos y sus observaciones desde dos archivos Excel separados:
    1. casos_para_import.xlsx - Tabla Case
    2. observaciones_para_import.xlsx - Tabla Observation (opcional)
    """
    
    if not casos_file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload Excel file.")

    # ===========================
    # PASO 1: IMPORTAR CASOS
    # ===========================
    casos_contents = await casos_file.read()
    
    try:
        df_casos = pd.read_excel(io.BytesIO(casos_contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing casos file: {str(e)}")

    # Validar columnas requeridas para casos
    required_cols_casos = ['codigo', 'servicio_o_plataforma', 'estado', 'prioridad']
    missing_cols = [col for col in required_cols_casos if col not in df_casos.columns]
    
    if missing_cols:
        raise HTTPException(status_code=400, detail=f"Missing required columns in casos file: {', '.join(missing_cols)}")

    # ✅ FIX: Llenar NaN solo en columnas de texto
    for col in df_casos.columns:
        if df_casos[col].dtype == 'object':
            df_casos[col].fillna('', inplace=True)

    casos_importados = 0
    casos_actualizados = 0
    errores_casos = []
    casos_map = {}  # Mapeo codigo -> case_id para las observaciones

    print(f"\n📥 Importando {len(df_casos)} casos...")

    for index, row in df_casos.iterrows():
        try:
            # Normalizar enums
            try:
                estado_str = str(row['estado']).upper().replace('CASESTATUS.', '')
                estado = CaseStatus[estado_str]
            except:
                estado = CaseStatus.ABIERTO
            
            try:
                prioridad_str = str(row['prioridad']).upper().replace('PRIORITY.', '')
                prioridad = Priority[prioridad_str]
            except:
                prioridad = Priority.MEDIO

            # Parsear fechas
            fecha_inicio = row.get('fecha_inicio', datetime.utcnow())
            if isinstance(fecha_inicio, str):
                try:
                    fecha_inicio = pd.to_datetime(fecha_inicio)
                except:
                    fecha_inicio = datetime.utcnow()
            
            fecha_fin = row.get('fecha_fin', None)
            if fecha_fin and isinstance(fecha_fin, str) and fecha_fin.strip():
                try:
                    fecha_fin = pd.to_datetime(fecha_fin)
                except:
                    fecha_fin = None
            else:
                fecha_fin = None

            created_at = row.get('created_at', fecha_inicio)
            if isinstance(created_at, str):
                try:
                    created_at = pd.to_datetime(created_at)
                except:
                    created_at = fecha_inicio

            updated_at = row.get('updated_at', datetime.utcnow())
            if isinstance(updated_at, str):
                try:
                    updated_at = pd.to_datetime(updated_at)
                except:
                    updated_at = datetime.utcnow()

            codigo = str(row['codigo']).strip()

            # Verificar si el caso ya existe
            result = await session.exec(select(Case).where(Case.codigo == codigo))
            existing_case = result.first()

            if existing_case:
                # Actualizar caso existente
                existing_case.servicio_o_plataforma = str(row['servicio_o_plataforma'])
                existing_case.prioridad = prioridad
                existing_case.estado = estado
                existing_case.sby_responsable = str(row.get('sby_responsable', ''))
                existing_case.motivo = str(row.get('motivo', ''))
                existing_case.observaciones = str(row.get('observaciones', ''))
                existing_case.fecha_inicio = fecha_inicio
                existing_case.fecha_fin = fecha_fin
                existing_case.updated_at = updated_at
                
                session.add(existing_case)
                casos_map[codigo] = existing_case.id
                casos_actualizados += 1
            else:
                # Crear nuevo caso
                new_case = Case(
                    codigo=codigo,
                    servicio_o_plataforma=str(row['servicio_o_plataforma']),
                    prioridad=prioridad,
                    estado=estado,
                    motivo=str(row.get('motivo', '')),
                    sby_responsable=str(row.get('sby_responsable', '')),
                    observaciones=str(row.get('observaciones', '')),
                    creado_por_id=current_user.id,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    created_at=created_at,
                    updated_at=updated_at
                )
                
                session.add(new_case)
                await session.flush()  # Para obtener el ID
                casos_map[codigo] = new_case.id
                casos_importados += 1

        except Exception as e:
            errores_casos.append(f"Fila {index+2}: {str(e)}")

    await session.commit()
    print(f"✅ Casos importados: {casos_importados}, actualizados: {casos_actualizados}")

    # ===========================
    # PASO 2: IMPORTAR OBSERVACIONES (si se proporciona el archivo)
    # ===========================
    observaciones_importadas = 0
    errores_observaciones = []

    if observaciones_file:
        print(f"\n📝 Importando observaciones...")
        
        observaciones_contents = await observaciones_file.read()
        
        try:
            df_observaciones = pd.read_excel(io.BytesIO(observaciones_contents))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing observaciones file: {str(e)}")

        # Validar columnas
        required_cols_obs = ['case_codigo', 'content', 'created_at']
        missing_cols_obs = [col for col in required_cols_obs if col not in df_observaciones.columns]
        
        if missing_cols_obs:
            raise HTTPException(status_code=400, detail=f"Missing required columns in observaciones file: {', '.join(missing_cols_obs)}")

        # ✅ FIX: Llenar NaN solo en columnas de texto
        for col in df_observaciones.columns:
            if df_observaciones[col].dtype == 'object':
                df_observaciones[col].fillna('', inplace=True)

        for index, row in df_observaciones.iterrows():
            try:
                case_codigo = str(row['case_codigo']).strip()
                
                # Buscar el case_id
                if case_codigo not in casos_map:
                    # Buscar en BD si no está en el mapa
                    result = await session.exec(select(Case).where(Case.codigo == case_codigo))
                    case = result.first()
                    if not case:
                        errores_observaciones.append(f"Fila {index+2}: Caso '{case_codigo}' no encontrado")
                        continue
                    case_id = case.id
                else:
                    case_id = casos_map[case_codigo]

                # Parsear fecha de observación
                created_at_obs = row.get('created_at', datetime.utcnow())
                if isinstance(created_at_obs, str):
                    try:
                        created_at_obs = pd.to_datetime(created_at_obs)
                    except:
                        created_at_obs = datetime.utcnow()

                # Verificar si la observación ya existe (evitar duplicados)
                content = str(row['content'])
                result = await session.exec(
                    select(Observation).where(
                        Observation.case_id == case_id,
                        Observation.content == content
                    )
                )
                existing_obs = result.first()

                if not existing_obs:
                    # Crear nueva observación
                    new_observation = Observation(
                        case_id=case_id,
                        content=content,
                        created_by_id=current_user.id,
                        created_at=created_at_obs
                    )
                    
                    session.add(new_observation)
                    observaciones_importadas += 1

            except Exception as e:
                errores_observaciones.append(f"Fila {index+2}: {str(e)}")

        await session.commit()
        print(f"✅ Observaciones importadas: {observaciones_importadas}")

    return {
        "message": f"Importación completada exitosamente",
        "casos_importados": casos_importados,
        "casos_actualizados": casos_actualizados,
        "observaciones_importadas": observaciones_importadas,
        "errores_casos": errores_casos,
        "errores_observaciones": errores_observaciones
    }


# ==========================================
# IMPORTACIÓN SIMPLE (MANTENIDO PARA COMPATIBILIDAD)
# ==========================================
@router.post("/import", status_code=201)
async def import_cases(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Importación simple de casos sin observaciones separadas.
    Mantiene compatibilidad con el formato anterior.
    """
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload Excel or CSV.")

    contents = await file.read()
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

    # Expected columns validation
    required_cols = ['codigo', 'servicio_o_plataforma', 'prioridad', 'motivo']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing_cols)}")

    # ✅ FIX: Llenar NaN solo en columnas de texto
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna('', inplace=True)

    imported_count = 0
    errors = []

    for index, row in df.iterrows():
        try:
            # Check validation for Enum types
            try:
                priority = Priority(row['prioridad'].upper())
            except:
                priority = Priority.MEDIO
            
            try:
                status = CaseStatus(str(row.get('estado', 'ABIERTO')).upper())
            except:
                status = CaseStatus.ABIERTO

            new_case = Case(
                codigo=str(row['codigo']),
                servicio_o_plataforma=str(row['servicio_o_plataforma']),
                prioridad=priority,
                estado=status,
                motivo=str(row['motivo']),
                sby_responsable=str(row.get('sby_responsable', '')),
                observaciones=str(row.get('observaciones', '')),
                creado_por_id=current_user.id,
                created_at=row.get('created_at', row.get('Fecha Inicio', datetime.utcnow())),
                updated_at=row.get('updated_at', row.get('Ultima Actualización', datetime.utcnow()))
            )
            
            # Try parsing dates if they are strings
            if isinstance(new_case.created_at, str):
                try: new_case.created_at = pd.to_datetime(new_case.created_at)
                except: new_case.created_at = datetime.utcnow()
                
            if isinstance(new_case.updated_at, str):
                try: new_case.updated_at = pd.to_datetime(new_case.updated_at)
                except: new_case.updated_at = datetime.utcnow()
            
            # Check duplicate code
            existing = await session.exec(select(Case).where(Case.codigo == new_case.codigo))
            if existing.first():
                errors.append(f"Row {index+2}: Duplicate Code {new_case.codigo}")
                continue

            session.add(new_case)
            imported_count += 1
            
        except Exception as e:
            errors.append(f"Row {index+2}: {str(e)}")

    await session.commit()
    
    return {
        "message": f"Successfully imported {imported_count} cases.",
        "errors": errors
    }


# ==========================================
# IMPORTACIÓN LEGACY (MANTENIDO)
# ==========================================
@router.post("/import-legacy", status_code=201)
async def import_legacy_cases(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Importa casos desde archivos Excel legacy con formato de bitácora semanal.
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload Excel.")

    contents = await file.read()
    
    try:
        # Load '2024' sheet or search for year-like sheets
        xl = pd.ExcelFile(io.BytesIO(contents))
        target_sheet = None
        for sheet in xl.sheet_names:
            if "202" in sheet: # Heuristic for year sheets
                target_sheet = sheet
                break
        
        if not target_sheet:
            target_sheet = xl.sheet_names[0] # Fallback
            
        df = pd.read_excel(io.BytesIO(contents), sheet_name=target_sheet, header=None)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing legacy file: {str(e)}")

    # CONFIG CONSTANTS
    COL_DATE = 1
    COL_RESP = 4
    COL_CONTENT = 25
    
    cases_map = {}
    admin_id = current_user.id
    
    warnings = []
    count_created = 0
    count_updated = 0

    for idx, row in df.iterrows():
        if len(row) < 26: continue
        
        raw_date = row[COL_DATE]
        if pd.isna(raw_date) or str(raw_date).strip() == "":
            continue
            
        try:
            date_val = pd.to_datetime(raw_date)
        except:
            continue
        
        resp = str(row[COL_RESP]).strip() if not pd.isna(row[COL_RESP]) else "Sin Asignar"
        if resp == "nan": resp = "Sin Asignar"
        
        content_block = str(row[COL_CONTENT])
        if pd.isna(row[COL_CONTENT]) or content_block == "nan":
            continue
            
        content_block = content_block.replace("\n", " ").strip()
        for status in ["ABIERTO", "CERRADO", "EN MONITOREO", "STANDBY"]:
            content_block = content_block.replace(f"[{status}]", f"\n[{status}]")
            content_block = content_block.replace(f"[{status.lower()}]", f"\n[{status}]")
        
        lines = content_block.split("\n")
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            match = CASE_PATTERN.match(line)
            if match:
                status_str, code_str, desc_str = match.groups()
                
                status_enum = CaseStatus.ABIERTO
                s_upper = status_str.upper()
                if "CERRADO" in s_upper: status_enum = CaseStatus.CERRADO
                elif "MONITOREO" in s_upper: status_enum = CaseStatus.EN_MONITOREO
                elif "STANDBY" in s_upper: status_enum = CaseStatus.STANDBY
                
                code = code_str.strip()
                desc = desc_str.strip()
                service = code.split(' ')[0] if ' ' in code else "General"
                
                if code in cases_map:
                    existing_case = cases_map[code]
                    
                    if existing_case.sby_responsable != resp:
                        existing_case.sby_responsable = resp
                    
                    if existing_case.estado != status_enum:
                        existing_case.estado = status_enum
                        
                    existing_case.updated_at = date_val
                    
                    obs = Observation(
                        case=existing_case,
                        content=f"**[{date_val.strftime('%Y-%m-%d')}] Actualización Semanal:**\n{desc}",
                        created_by_id=admin_id,
                        created_at=date_val
                    )
                    session.add(obs)
                    session.add(existing_case)
                    count_updated += 1
                    
                else:
                    existing_db = await session.exec(select(Case).where(Case.codigo == code))
                    existing_case_db = existing_db.first()
                    
                    if existing_case_db:
                        cases_map[code] = existing_case_db
                        existing_case_db.estado = status_enum
                        existing_case_db.sby_responsable = resp
                        existing_case_db.updated_at = date_val
                        
                        obs = Observation(
                            case_id=existing_case_db.id,
                            content=f"**[{date_val.strftime('%Y-%m-%d')}] Actualización Semanal:**\n{desc}",
                            created_by_id=admin_id,
                            created_at=date_val
                        )
                        session.add(obs)
                        session.add(existing_case_db)
                        count_updated += 1
                    else:
                        new_case = Case(
                            codigo=code,
                            servicio_o_plataforma=service,
                            prioridad=Priority.MEDIO,
                            estado=status_enum,
                            sby_responsable=resp,
                            motivo=desc,
                            creado_por_id=admin_id,
                            fecha_inicio=date_val,
                            updated_at=date_val
                        )
                        session.add(new_case)
                        cases_map[code] = new_case
                        
                        obs = Observation(
                            case=new_case,
                            content=f"**[{date_val.strftime('%Y-%m-%d')}] Importación Inicial:**\n{desc}",
                            created_by_id=admin_id,
                            created_at=date_val
                        )
                        session.add(obs)
                        count_created += 1

    await session.commit()
    return {"message": f"Legacy Import Processed: {count_created} created, {count_updated} updates."}


# ==========================================
# NUEVO: EXPORTAR CASOS CON OBSERVACIONES
# ==========================================
@router.get("/export-with-observations")
async def export_cases_with_observations(
    format: str = Query("xlsx", pattern="^(xlsx|csv)$"),
    session: AsyncSession = Depends(get_session)
):
    """
    Exporta casos y observaciones en dos archivos separados (en un ZIP) o en hojas separadas de Excel.
    """
    # Obtener todos los casos
    cases_result = await session.exec(select(Case))
    cases = cases_result.all()

    if not cases:
        raise HTTPException(status_code=404, detail="No cases found to export.")

    # Obtener todas las observaciones
    observations_result = await session.exec(select(Observation))
    observations = observations_result.all()

    # Crear DataFrame de casos
    cases_data = []
    for case in cases:
        cases_data.append({
            'codigo': case.codigo,
            'servicio_o_plataforma': case.servicio_o_plataforma,
            'estado': case.estado.value,
            'prioridad': case.prioridad.value,
            'sby_responsable': case.sby_responsable or '',
            'fecha_inicio': case.fecha_inicio,
            'fecha_fin': case.fecha_fin,
            'motivo': case.motivo or '',
            'observaciones': case.observaciones or '',
            'creado_por_id': case.creado_por_id,
            'created_at': case.created_at,
            'updated_at': case.updated_at
        })
    
    df_cases = pd.DataFrame(cases_data)

    # Crear DataFrame de observaciones
    observations_data = []
    obs_counter = {}  # Para numerar observaciones por caso
    
    for obs in observations:
        case_codigo = next((c.codigo for c in cases if c.id == obs.case_id), 'UNKNOWN')
        
        if case_codigo not in obs_counter:
            obs_counter[case_codigo] = 0
        obs_counter[case_codigo] += 1
        
        observations_data.append({
            'id': obs.id,
            'case_codigo': case_codigo,
            'numero_observacion': obs_counter[case_codigo],
            'content': obs.content,
            'created_by_id': obs.created_by_id,
            'created_at': obs.created_at
        })
    
    df_observations = pd.DataFrame(observations_data)

    # Crear archivo Excel con múltiples hojas
    if format == 'xlsx':
        stream = io.BytesIO()
        
        with pd.ExcelWriter(stream, engine='openpyxl') as writer:
            df_cases.to_excel(writer, sheet_name='Casos', index=False)
            if len(df_observations) > 0:
                df_observations.to_excel(writer, sheet_name='Observaciones', index=False)
        
        stream.seek(0)
        
        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=casos_y_observaciones_export.xlsx"}
        )
    else:
        # Para CSV, exportar solo casos (mantener compatibilidad)
        stream = io.BytesIO()
        df_cases.to_csv(stream, index=False, encoding='utf-8')
        stream.seek(0)
        
        return StreamingResponse(
            stream,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=casos_export.csv"}
        )


# ==========================================
# EXPORTACIÓN SIMPLE (MANTENIDO)
# ==========================================
@router.get("/export")
async def export_cases(
    format: str = Query("tsv", pattern="^(tsv|csv|xlsx)$"),
    session: AsyncSession = Depends(get_session)
):
    """
    Exportación simple de casos en un solo archivo.
    Mantiene compatibilidad con el formato anterior.
    """
    statement = select(Case)
    results = await session.exec(statement)
    cases = results.all()

    if not cases:
        raise HTTPException(status_code=404, detail="No cases found to export.")

    # Convert to DataFrame
    data = [case.dict() for case in cases]
    df = pd.DataFrame(data)

    stream = io.BytesIO()

    if format == 'tsv':
        df.to_csv(stream, sep='\t', index=False, encoding='utf-8')
        media_type = "text/tab-separated-values"
        filename = "cases_export.tsv"
    elif format == 'csv':
        df.to_csv(stream, index=False, encoding='utf-8')
        media_type = "text/csv"
        filename = "cases_export.csv"
    else:
        df.to_excel(stream, index=False)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = "cases_export.xlsx"

    stream.seek(0)
    
    return StreamingResponse(
        stream,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# ==========================================
# IMPORTAR EXCEL COMPLETO (CASOS + OBSERVACIONES)
# ==========================================
@router.post("/import-complete-excel", status_code=201)
async def import_complete_excel(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Importa casos y observaciones desde un único archivo Excel con dos hojas:
    - Hoja "Casos": Contiene todos los casos
    - Hoja "Observaciones": Contiene las observaciones (opcional)
    """
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Formato de archivo inválido. Por favor suba un archivo Excel (.xlsx o .xls)")

    contents = await file.read()
    
    try:
        # Leer todas las hojas del Excel
        excel_file = pd.ExcelFile(io.BytesIO(contents))
        
        if 'Casos' not in excel_file.sheet_names:
            raise HTTPException(status_code=400, detail="El archivo Excel debe contener una hoja llamada 'Casos'")
        
        df_casos = pd.read_excel(excel_file, sheet_name='Casos')
        
        # Verificar si existe la hoja de observaciones
        has_observations = 'Observaciones' in excel_file.sheet_names
        df_observaciones = pd.read_excel(excel_file, sheet_name='Observaciones') if has_observations else None
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al parsear el archivo Excel: {str(e)}")

    # Validar columnas requeridas para casos
    required_cols_casos = ['codigo', 'servicio_o_plataforma', 'estado', 'prioridad']
    missing_cols = [col for col in required_cols_casos if col not in df_casos.columns]
    
    if missing_cols:
        raise HTTPException(status_code=400, detail=f"Faltan columnas requeridas en la hoja 'Casos': {', '.join(missing_cols)}")

    # ✅ FIX: Llenar NaN solo en columnas de texto, no en numéricas (evita error con float64)
    for col in df_casos.columns:
        if df_casos[col].dtype == 'object':  # Solo columnas de texto
            df_casos[col].fillna('', inplace=True)

    casos_importados = 0
    casos_actualizados = 0
    errores_casos = []
    casos_map = {}  # Mapeo codigo -> case_id

    print(f"\n📥 Importando {len(df_casos)} casos...")

    for index, row in df_casos.iterrows():
        try:
            # Normalizar enums
            try:
                estado_str = str(row['estado']).upper().replace('CASESTATUS.', '')
                estado = CaseStatus[estado_str]
            except:
                estado = CaseStatus.ABIERTO
            
            try:
                prioridad_str = str(row['prioridad']).upper().replace('PRIORITY.', '')
                prioridad = Priority[prioridad_str]
            except:
                prioridad = Priority.MEDIO

            # Parsear fechas
            fecha_inicio = row.get('fecha_inicio', datetime.utcnow())
            if isinstance(fecha_inicio, str):
                try:
                    fecha_inicio = pd.to_datetime(fecha_inicio)
                except:
                    fecha_inicio = datetime.utcnow()
            
            fecha_fin = row.get('fecha_fin', None)
            if fecha_fin and isinstance(fecha_fin, str) and fecha_fin.strip():
                try:
                    fecha_fin = pd.to_datetime(fecha_fin)
                except:
                    fecha_fin = None
            else:
                fecha_fin = None

            created_at = row.get('created_at', fecha_inicio)
            if isinstance(created_at, str):
                try:
                    created_at = pd.to_datetime(created_at)
                except:
                    created_at = fecha_inicio

            updated_at = row.get('updated_at', datetime.utcnow())
            if isinstance(updated_at, str):
                try:
                    updated_at = pd.to_datetime(updated_at)
                except:
                    updated_at = datetime.utcnow()

            codigo = str(row['codigo']).strip()

            # Verificar si el caso ya existe
            result = await session.exec(select(Case).where(Case.codigo == codigo))
            existing_case = result.first()

            if existing_case:
                # Actualizar caso existente
                existing_case.servicio_o_plataforma = str(row['servicio_o_plataforma'])
                existing_case.prioridad = prioridad
                existing_case.estado = estado
                existing_case.sby_responsable = str(row.get('sby_responsable', ''))
                existing_case.motivo = str(row.get('motivo', ''))
                existing_case.observaciones = str(row.get('observaciones', ''))
                existing_case.fecha_inicio = fecha_inicio
                existing_case.fecha_fin = fecha_fin
                existing_case.updated_at = updated_at
                
                session.add(existing_case)
                casos_map[codigo] = existing_case.id
                casos_actualizados += 1
            else:
                # Crear nuevo caso
                new_case = Case(
                    codigo=codigo,
                    servicio_o_plataforma=str(row['servicio_o_plataforma']),
                    prioridad=prioridad,
                    estado=estado,
                    motivo=str(row.get('motivo', '')),
                    sby_responsable=str(row.get('sby_responsable', '')),
                    observaciones=str(row.get('observaciones', '')),
                    creado_por_id=current_user.id,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    created_at=created_at,
                    updated_at=updated_at
                )
                
                session.add(new_case)
                await session.flush()
                casos_map[codigo] = new_case.id
                casos_importados += 1

        except Exception as e:
            errores_casos.append(f"Fila {index+2}: {str(e)}")

    await session.commit()
    print(f"✅ Casos importados: {casos_importados}, actualizados: {casos_actualizados}")

    # Importar observaciones si existen
    observaciones_importadas = 0
    errores_observaciones = []

    if has_observations and df_observaciones is not None and len(df_observaciones) > 0:
        print(f"\n📝 Importando {len(df_observaciones)} observaciones...")
        
        required_cols_obs = ['case_codigo', 'content', 'created_at']
        missing_cols_obs = [col for col in required_cols_obs if col not in df_observaciones.columns]
        
        if missing_cols_obs:
            raise HTTPException(status_code=400, detail=f"Faltan columnas requeridas en la hoja 'Observaciones': {', '.join(missing_cols_obs)}")

        # ✅ FIX: Llenar NaN solo en columnas de texto
        for col in df_observaciones.columns:
            if df_observaciones[col].dtype == 'object':
                df_observaciones[col].fillna('', inplace=True)

        for index, row in df_observaciones.iterrows():
            try:
                case_codigo = str(row['case_codigo']).strip()
                
                # Buscar el case_id
                if case_codigo not in casos_map:
                    result = await session.exec(select(Case).where(Case.codigo == case_codigo))
                    case = result.first()
                    if not case:
                        errores_observaciones.append(f"Fila {index+2}: Caso '{case_codigo}' no encontrado")
                        continue
                    case_id = case.id
                else:
                    case_id = casos_map[case_codigo]

                created_at_obs = row.get('created_at')
                if isinstance(created_at_obs, str):
                    try:
                        created_at_obs = pd.to_datetime(created_at_obs)
                    except:
                        created_at_obs = datetime.utcnow()

                created_by_id = row.get('created_by_id')
                if pd.isna(created_by_id) or created_by_id == '':
                    created_by_id = current_user.id
                else:
                    created_by_id = int(created_by_id)

                new_observation = Observation(
                    case_id=case_id,
                    content=str(row['content']),
                    created_by_id=created_by_id,
                    created_at=created_at_obs
                )
                
                session.add(new_observation)
                observaciones_importadas += 1

            except Exception as e:
                errores_observaciones.append(f"Fila {index+2}: {str(e)}")

        await session.commit()
        print(f"✅ Observaciones importadas: {observaciones_importadas}")

    # Preparar respuesta
    response_msg = f"Importación completada: {casos_importados} casos creados, {casos_actualizados} casos actualizados"
    if observaciones_importadas > 0:
        response_msg += f", {observaciones_importadas} observaciones importadas"
    
    if errores_casos or errores_observaciones:
        response_msg += f". Errores: {len(errores_casos)} en casos, {len(errores_observaciones)} en observaciones"
    
    return {
        "message": response_msg,
        "casos_importados": casos_importados,
        "casos_actualizados": casos_actualizados,
        "observaciones_importadas": observaciones_importadas,
        "errores": errores_casos + errores_observaciones
    }


# ==========================================
# EXPORTAR USUARIOS
# ==========================================
@router.get("/export-users")
async def export_users(
    format: str = Query("xlsx", pattern="^(xlsx|csv)$"),
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Exporta todos los usuarios del sistema.
    Solo disponible para administradores.
    """
    from app.models import UserRole
    
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden exportar usuarios")
    
    # Obtener todos los usuarios
    users_result = await session.exec(select(User))
    users = users_result.all()

    if not users:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios para exportar")

    # Crear DataFrame de usuarios (sin incluir la contraseña hasheada por seguridad)
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'nombre': user.nombre,
            'email': user.email,
            'rol': user.rol.value,
            'is_active': user.is_active
        })
    
    df_users = pd.DataFrame(users_data)

    stream = io.BytesIO()

    if format == 'xlsx':
        df_users.to_excel(stream, index=False, sheet_name='Usuarios')
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = "usuarios_export.xlsx"
    else:
        df_users.to_csv(stream, index=False, encoding='utf-8')
        media_type = "text/csv"
        filename = "usuarios_export.csv"

    stream.seek(0)
    
    return StreamingResponse(
        stream,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# ==========================================
# IMPORTAR USUARIOS
# ==========================================
@router.post("/import-users", status_code=201)
async def import_users(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """
    Importa usuarios desde un archivo Excel o CSV.
    Solo disponible para administradores.
    
    Columnas requeridas: nombre, email, rol
    Columnas opcionales: password, is_active
    
    Si no se proporciona password, se genera uno aleatorio que se incluye en la respuesta.
    """
    from app.models import UserRole, UserCreate
    from app.auth import get_password_hash
    import secrets
    import string
    
    if current_user.rol != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Solo los administradores pueden importar usuarios")
    
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Formato de archivo inválido. Use Excel (.xlsx, .xls) o CSV (.csv)")

    contents = await file.read()
    
    try:
        if file.filename.endswith('.csv'):
            df_users = pd.read_csv(io.BytesIO(contents))
        else:
            df_users = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al parsear el archivo: {str(e)}")

    # Validar columnas requeridas
    required_cols = ['nombre', 'email', 'rol']
    missing_cols = [col for col in required_cols if col not in df_users.columns]
    
    if missing_cols:
        raise HTTPException(status_code=400, detail=f"Faltan columnas requeridas: {', '.join(missing_cols)}")

    # ✅ FIX: Llenar NaN solo en columnas de texto
    for col in df_users.columns:
        if df_users[col].dtype == 'object':
            df_users[col].fillna('', inplace=True)

    usuarios_importados = 0
    usuarios_actualizados = 0
    errores = []
    passwords_generados = []

    print(f"\n👥 Importando {len(df_users)} usuarios...")

    for index, row in df_users.iterrows():
        try:
            email = str(row['email']).strip().lower()
            nombre = str(row['nombre']).strip()
            
            # Validar email
            if not email or '@' not in email:
                errores.append(f"Fila {index+2}: Email inválido '{email}'")
                continue
            
            # Validar rol
            try:
                rol_str = str(row['rol']).upper()
                rol = UserRole[rol_str]
            except:
                errores.append(f"Fila {index+2}: Rol inválido '{row['rol']}'. Use: CONSULTA, INGRESO o ADMIN")
                continue
            
            # Verificar si el usuario ya existe
            result = await session.exec(select(User).where(User.email == email))
            existing_user = result.first()

            if existing_user:
                # Actualizar usuario existente
                existing_user.nombre = nombre
                existing_user.rol = rol
                
                if 'is_active' in row and str(row['is_active']).lower() in ['false', '0', 'no']:
                    existing_user.is_active = False
                else:
                    existing_user.is_active = True
                
                # Si se proporciona nueva contraseña, actualizarla
                if 'password' in row and str(row['password']).strip():
                    existing_user.hashed_password = get_password_hash(str(row['password']))
                
                session.add(existing_user)
                usuarios_actualizados += 1
            else:
                # Generar o usar contraseña proporcionada
                if 'password' in row and str(row['password']).strip():
                    password = str(row['password']).strip()
                else:
                    # Generar contraseña aleatoria
                    alphabet = string.ascii_letters + string.digits
                    password = ''.join(secrets.choice(alphabet) for _ in range(12))
                    passwords_generados.append({
                        'email': email,
                        'nombre': nombre,
                        'password': password
                    })
                
                is_active = True
                if 'is_active' in row and str(row['is_active']).lower() in ['false', '0', 'no']:
                    is_active = False
                
                # Crear nuevo usuario
                new_user = User(
                    nombre=nombre,
                    email=email,
                    hashed_password=get_password_hash(password),
                    rol=rol,
                    is_active=is_active
                )
                
                session.add(new_user)
                usuarios_importados += 1

        except Exception as e:
            errores.append(f"Fila {index+2}: {str(e)}")

    await session.commit()
    print(f"✅ Usuarios importados: {usuarios_importados}, actualizados: {usuarios_actualizados}")

    # Preparar respuesta
    response_msg = f"Importación completada: {usuarios_importados} usuarios creados, {usuarios_actualizados} usuarios actualizados"
    
    if errores:
        response_msg += f". {len(errores)} errores encontrados"
    
    response_data = {
        "message": response_msg,
        "usuarios_importados": usuarios_importados,
        "usuarios_actualizados": usuarios_actualizados,
        "errores": errores
    }
    
    # Incluir contraseñas generadas si hay alguna
    if passwords_generados:
        response_data["contraseñas_generadas"] = passwords_generados
        response_data["advertencia"] = "IMPORTANTE: Guarde las contraseñas generadas. No se podrán recuperar después."
    
    return response_data