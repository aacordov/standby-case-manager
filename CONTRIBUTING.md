# 🤝 Guía de Contribución - Standby Case Manager

¡Gracias por tu interés en contribuir a Standby Case Manager! Esta guía te ayudará a empezar.

---

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Development](#proceso-de-development)
- [Proceso de Review](#proceso-de-review)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Features](#sugerir-features)

---

## 📜 Código de Conducta

Al participar en este proyecto, te comprometes a mantener un ambiente respetuoso y colaborativo. Esperamos que todos los contribuyentes:

- Sean respetuosos y considerados
- Acepten críticas constructivas
- Se enfoquen en lo mejor para la comunidad
- Muestren empatía hacia otros miembros

---

## 🚀 Cómo Contribuir

### 1. Fork el Proyecto

```bash
# Fork desde GitHub UI, luego clona tu fork
git clone git@github.com:TU-USUARIO/standby-case-manager.git
cd standby-case-manager
```

### 2. Configura el Upstream

```bash
git remote add upstream git@github.com:rortiz-09/standby-case-manager.git
git fetch upstream
```

### 3. Crea una Rama

```bash
# Para nuevas features
git checkout -b feature/nombre-descriptivo

# Para corrección de bugs
git checkout -b fix/descripcion-del-bug

# Para mejoras de documentación
git checkout -b docs/descripcion-cambio
```

### 4. Realiza tus Cambios

- Escribe código limpio y bien documentado
- Sigue los estándares de código establecidos
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario

### 5. Commit tus Cambios

Usamos Conventional Commits para mensajes claros:

```bash
# Features
git commit -m "feat: agregar filtro por fecha en casos"

# Fixes
git commit -m "fix: corregir error de autenticación en login"

# Documentación
git commit -m "docs: actualizar guía de instalación"

# Refactoring
git commit -m "refactor: optimizar consultas de base de datos"

# Tests
git commit -m "test: agregar tests para módulo de usuarios"

# Chores
git commit -m "chore: actualizar dependencias"
```

### 6. Push a tu Fork

```bash
git push origin feature/nombre-descriptivo
```

### 7. Abre un Pull Request

1. Ve a tu fork en GitHub
2. Click en "Pull Request"
3. Asegúrate de seleccionar la rama correcta
4. Completa la plantilla de PR con:
   - Descripción de los cambios
   - Issue relacionado (si aplica)
   - Screenshots (si es UI)
   - Checklist completado

---

## 📏 Estándares de Código

### Python (Backend)

#### Style Guide

Seguimos [PEP 8](https://pep8.org/) con algunas excepciones:

- **Línea máxima**: 100 caracteres (no 79)
- **Imports**: Agrupados y ordenados alfabéticamente
- **Docstrings**: Google Style para todas las funciones públicas

#### Formato

```python
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Case
from app.schemas import CaseCreate, CaseUpdate


def get_cases(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> List[Case]:
    """
    Obtiene una lista de casos con filtros opcionales.
    
    Args:
        session: Sesión de base de datos
        skip: Número de registros a saltar
        limit: Número máximo de registros a devolver
        status: Filtro opcional por estado
        
    Returns:
        Lista de casos que cumplen los criterios
        
    Raises:
        HTTPException: Si hay un error en la consulta
    """
    query = select(Case)
    
    if status:
        query = query.where(Case.status == status)
    
    query = query.offset(skip).limit(limit)
    cases = session.exec(query).all()
    
    return cases
```

#### Herramientas

```bash
# Instalar herramientas de formato
pip install black isort flake8 mypy

# Formatear código
black backend/
isort backend/

# Linting
flake8 backend/

# Type checking
mypy backend/
```

### TypeScript/React (Frontend)

#### Style Guide

Seguimos las guías de [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript):

- **Indentación**: 2 espacios
- **Quotes**: Single quotes para strings
- **Semicolons**: Siempre
- **Nombres**: camelCase para variables/funciones, PascalCase para componentes

#### Formato

```typescript
import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from '@/api/axios';

interface Case {
  id: number;
  title: string;
  status: string;
}

interface CaseListProps {
  userId?: number;
  onSelectCase?: (caseId: number) => void;
}

export const CaseList: React.FC<CaseListProps> = ({ 
  userId, 
  onSelectCase 
}) => {
  const [selectedId, setSelectedId] = useState<number | null>(null);
  
  const { data: cases, isLoading } = useQuery({
    queryKey: ['cases', userId],
    queryFn: async () => {
      const response = await axios.get<Case[]>('/cases', {
        params: { user_id: userId }
      });
      return response.data;
    }
  });
  
  const handleClick = (id: number) => {
    setSelectedId(id);
    onSelectCase?.(id);
  };
  
  if (isLoading) {
    return <div>Cargando...</div>;
  }
  
  return (
    <ul className="space-y-2">
      {cases?.map((case) => (
        <li 
          key={case.id}
          onClick={() => handleClick(case.id)}
          className={cn(
            'p-4 cursor-pointer rounded-lg',
            selectedId === case.id && 'bg-blue-50'
          )}
        >
          {case.title}
        </li>
      ))}
    </ul>
  );
};
```

#### Herramientas

```bash
# Instalar herramientas
npm install -D eslint prettier

# Formatear código
npm run format

# Linting
npm run lint

# Fix automático
npm run lint:fix
```

### SQL

- Usa nombres en snake_case para tablas y columnas
- Prefiere TIMESTAMP sobre DATE cuando sea posible
- Siempre define índices para foreign keys
- Usa constraints apropiadas (NOT NULL, UNIQUE, etc.)

---

## 🔄 Proceso de Development

### 1. Mantén tu Fork Actualizado

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 2. Sincroniza tu Rama

```bash
git checkout feature/tu-feature
git rebase main
```

### 3. Ejecuta Tests

**Backend:**
```bash
cd backend
source .venv/bin/activate
pytest
pytest --cov=app
```

**Frontend:**
```bash
cd frontend
npm run test
npm run test:coverage
```

### 4. Verifica Linting

```bash
# Backend
black --check backend/
flake8 backend/

# Frontend
npm run lint
```

---

## ✅ Proceso de Review

### Requisitos para Merge

- [ ] Todos los tests pasan
- [ ] Cobertura de código se mantiene >80%
- [ ] No hay conflictos con main
- [ ] Al menos 1 aprobación de reviewer
- [ ] Linting pasa sin errores
- [ ] Documentación actualizada (si aplica)
- [ ] CHANGELOG.md actualizado (para features)

### Tiempos de Review

- **Features pequeños**: 1-2 días
- **Features grandes**: 3-5 días
- **Hotfixes**: Mismo día (si es crítico)

### Qué Esperamos en un PR

1. **Descripción clara**: Explica qué y por qué
2. **Tests**: Incluye tests para nueva funcionalidad
3. **Screenshots**: Si hay cambios visuales
4. **Breaking changes**: Documéntalos claramente
5. **Performance**: Considera el impacto en rendimiento

---

## 🐛 Reportar Bugs

### Antes de Reportar

1. Busca en [Issues existentes](https://github.com/rortiz-09/standby-case-manager/issues)
2. Verifica que estás usando la última versión
3. Revisa la documentación

### Cómo Reportar

Usa la plantilla de Bug Report en GitHub Issues e incluye:

```markdown
**Descripción del Bug**
Descripción clara y concisa del problema.

**Para Reproducir**
Pasos para reproducir el comportamiento:
1. Ve a '...'
2. Click en '...'
3. Scroll hasta '...'
4. Ver error

**Comportamiento Esperado**
Qué esperabas que sucediera.

**Screenshots**
Si aplica, agrega screenshots.

**Ambiente:**
 - OS: [e.g. Ubuntu 22.04]
 - Navegador: [e.g. Chrome 120]
 - Versión: [e.g. 2.2.3]

**Contexto Adicional**
Cualquier información relevante.
```

---

## 💡 Sugerir Features

### Antes de Sugerir

1. Revisa el roadmap del proyecto
2. Busca en Issues existentes
3. Considera si es una feature general o específica a tu caso

### Cómo Sugerir

Usa la plantilla de Feature Request e incluye:

```markdown
**¿Tu feature request está relacionada a un problema?**
Descripción clara del problema.

**Describe la solución que te gustaría**
Descripción clara de lo que quieres que pase.

**Describe alternativas que has considerado**
Otras soluciones o features que has considerado.

**Contexto adicional**
Screenshots, mockups, ejemplos de otros sistemas.
```

---

## 📚 Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

---

## 📞 Contacto del Equipo

Para preguntas sobre contribuciones:

- **Allan Córdova**: [aacordov@gmail.com](mailto:aacordov@gmail.com)
- **José Briones**: [josmbrio@gmail.com](mailto:josmbrio@gmail.com)
- **Larry Sánchez**: [lajasanc@gmail.com](mailto:lajasanc@gmail.com)
- **Ronny Ortiz**: [ronny.ortiz.54@hotmail.com](mailto:ronny.ortiz.54@hotmail.com)

---

**¡Gracias por contribuir a Standby Case Manager! 🚀**
