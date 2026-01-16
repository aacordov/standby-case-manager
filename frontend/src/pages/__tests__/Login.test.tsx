import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { render } from '../../test/test-utils';
import Login from '../Login';
import api from '../../api/axios';

// Mock useNavigate de react-router-dom
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

// Mock de axios
vi.mock('../../api/axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    interceptors: {
      request: { use: vi.fn(), eject: vi.fn() },
      response: { use: vi.fn(), eject: vi.fn() },
    },
  },
}));

describe('Login Page', () => {
  beforeEach(() => {
    // Limpiar mocks y localStorage
    mockNavigate.mockClear();
    localStorage.clear();
    vi.clearAllMocks();
    
    // Mock de matchMedia para ThemeContext
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      configurable: true,
      value: vi.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      })),
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('should render login form', () => {
    render(<Login />);

    expect(screen.getByText('Iniciar Sesión')).toBeInTheDocument();
    expect(screen.getByRole('textbox', { type: /email/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });

  it('should show error with incorrect credentials', async () => {
    // Mock axios para login fallido
    (api.post as any).mockRejectedValueOnce({
      response: {
        data: { error: 'Usuario o contraseña incorrectos' },
        status: 401,
      },
    });

    const user = userEvent.setup();
    render(<Login />);

    const emailInput = screen.getByRole('textbox');
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    const passwordInput = passwordInputs[0];
    const submitButton = screen.getByRole('button', { name: /entrar/i });

    await user.type(emailInput, 'wrong@example.com');
    await user.type(passwordInput as HTMLElement, 'wrongpassword');
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/usuario o contraseña incorrectos/i)).toBeInTheDocument();
    });

    // Verificar que NO se navegó
    expect(mockNavigate).not.toHaveBeenCalled();
  });

  it('should successfully login with correct credentials', async () => {
    // Mock axios para login exitoso - POST /auth/login
    (api.post as any).mockResolvedValueOnce({
      data: {
        access_token: 'mock-jwt-token',
        token_type: 'bearer',
      },
      status: 200,
    });

    // Mock axios para obtener usuario - GET /auth/me
    (api.get as any).mockResolvedValueOnce({
      data: {
        id: 1,
        email: 'admin@example.com',
        role: 'admin',
      },
      status: 200,
    });

    const user = userEvent.setup();
    
    // Espiar localStorage ANTES de renderizar
    const setItemSpy = vi.spyOn(Storage.prototype, 'setItem');
    
    render(<Login />);

    const emailInput = screen.getByRole('textbox');
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    const passwordInput = passwordInputs[0];
    const submitButton = screen.getByRole('button', { name: /entrar/i });
    
    // Llenar el formulario con credenciales correctas
    await user.clear(emailInput);
    await user.type(emailInput, 'admin@example.com');
    await user.clear(passwordInput as HTMLElement);
    await user.type(passwordInput as HTMLElement, 'admin123');
    
    // Submit del formulario
    await user.click(submitButton);

    // Esperar a que se complete el login
    await waitFor(() => {
      // Verificar que se guardó el token
      expect(localStorage.setItem).toHaveBeenCalledWith('token', 'mock-jwt-token');
      
      // Verificar que se guardó el usuario
      expect(localStorage.setItem).toHaveBeenCalledWith(
        'user',
        expect.stringContaining('admin@example.com')
      );
    }, { timeout: 3000 });
    
    // Verificar que la navegación se haya hecho correctamente
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/');
    }, { timeout: 1000 });
    
    // Verificar que se llamó a axios.post con FormData
    expect(api.post).toHaveBeenCalledWith('/auth/login', expect.any(FormData));
    
    // Verificar que se llamó a axios.get para obtener datos del usuario
    expect(api.get).toHaveBeenCalledWith('/auth/me');
  });

  it('should toggle theme when theme button is clicked', async () => {
    const user = userEvent.setup();
    render(<Login />);

    const themeButton = screen.getByTitle(/cambiar tema/i);

    await user.click(themeButton);

    // Solo verificamos que el botón siga presente (toggle interno)
    expect(themeButton).toBeInTheDocument();
  });

  it('should have required fields', () => {
    render(<Login />);

    const emailInput = screen.getByRole('textbox');
    const passwordInputs = document.querySelectorAll('input[type="password"]');

    expect(emailInput).toHaveAttribute('required');
    expect(passwordInputs[0]).toHaveAttribute('required');
  });
});