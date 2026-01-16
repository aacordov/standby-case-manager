import { describe, it, expect } from 'vitest';
import { screen } from '@testing-library/react';
import { render } from '../../test/test-utils';
import NotFound from '../NotFound';

describe('NotFound Page', () => {
  it('should render 404 message', () => {
    render(<NotFound />);
    
    expect(screen.getByText(/404/i)).toBeInTheDocument();
    expect(screen.getByText(/página no encontrada/i)).toBeInTheDocument();
  });

  it('should have a link to go back home', () => {
    render(<NotFound />);
    
    const homeLink = screen.getByRole('link', { name: /volver al inicio/i });
    expect(homeLink).toBeInTheDocument();
    expect(homeLink).toHaveAttribute('href', '/');
  });
});
