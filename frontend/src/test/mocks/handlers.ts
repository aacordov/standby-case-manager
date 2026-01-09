import { http, HttpResponse } from 'msw';

const baseURL = 'http://localhost:8000';

export const handlers = [
  // Auth endpoints
  http.post(`${baseURL}/auth/login`, async ({ request }) => {
    const formData = await request.formData();
    const username = formData.get('username');
    const password = formData.get('password');

    if (username === 'admin@example.com' && password === 'admin123') {
      return HttpResponse.json({
        access_token: 'mock-jwt-token',
        token_type: 'bearer',
      });
    }

    return HttpResponse.json(
      { detail: 'Incorrect username or password' },
      { status: 401 }
    );
  }),

  http.get(`${baseURL}/auth/me`, () => {
    return HttpResponse.json({
      id: 1,
      nombre: 'Admin User',
      email: 'admin@example.com',
      rol: 'ADMIN',
      is_active: true,
    });
  }),

  // Cases endpoints
  http.get(`${baseURL}/cases/`, () => {
    return HttpResponse.json([
      {
        id: 1,
        codigo: 'CASE-001',
        servicio_o_plataforma: 'Plataforma Test',
        prioridad: 'ALTO',
        estado: 'ABIERTO',
        fecha_inicio: '2024-01-01T00:00:00',
        novedades_y_comentarios: 'Test case',
        created_at: '2024-01-01T00:00:00',
        updated_at: '2024-01-01T00:00:00',
      },
    ]);
  }),

  http.post(`${baseURL}/cases/`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      id: 2,
      ...body,
      estado: 'ABIERTO',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }),

  http.get(`${baseURL}/cases/:id`, ({ params }) => {
    return HttpResponse.json({
      id: Number(params.id),
      codigo: `CASE-${params.id}`,
      servicio_o_plataforma: 'Plataforma Test',
      prioridad: 'ALTO',
      estado: 'ABIERTO',
      fecha_inicio: '2024-01-01T00:00:00',
      novedades_y_comentarios: 'Test case',
      observaciones_list: [],
      created_at: '2024-01-01T00:00:00',
      updated_at: '2024-01-01T00:00:00',
    });
  }),

  http.patch(`${baseURL}/cases/:id`, async ({ params, request }) => {
    const body = await request.json();
    return HttpResponse.json({
      id: Number(params.id),
      codigo: `CASE-${params.id}`,
      ...body,
      updated_at: new Date().toISOString(),
    });
  }),

  // Users endpoints
  http.get(`${baseURL}/users/`, () => {
    return HttpResponse.json([
      {
        id: 1,
        nombre: 'Admin User',
        email: 'admin@example.com',
        rol: 'ADMIN',
        is_active: true,
      },
      {
        id: 2,
        nombre: 'Regular User',
        email: 'user@example.com',
        rol: 'INGRESO',
        is_active: true,
      },
    ]);
  }),

  // Stats endpoint
  http.get(`${baseURL}/cases/stats`, () => {
    return HttpResponse.json({
      total: 10,
      abiertos: 3,
      standby: 2,
      en_monitoreo: 3,
      cerrados: 2,
      criticos: 1,
      altos: 3,
      medios: 4,
      bajos: 2,
    });
  }),
];
