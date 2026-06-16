import { useEffect, useRef } from 'react';
import { toast } from 'sonner';

function getJWTExpiry(token: string): number | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    const payload = JSON.parse(atob(parts[1]));
    return payload.exp ? payload.exp * 1000 : null;
  } catch {
    return null;
  }
}

export function useJWTExpiry(logout: () => void) {
  const warningShownRef = useRef(false);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (!token) return;

    const expiry = getJWTExpiry(token);
    if (!expiry) return;

    const now = Date.now();
    const logoutDelay = expiry - now;
    const warningDelay = logoutDelay - 5 * 60 * 1000;

    if (logoutDelay <= 0) {
      logout();
      return;
    }

    let warningTimer: ReturnType<typeof setTimeout> | undefined;
    let logoutTimer: ReturnType<typeof setTimeout> | undefined;

    if (warningDelay > 0 && !warningShownRef.current) {
      warningTimer = setTimeout(() => {
        warningShownRef.current = true;
        toast.warning(
          'Su sesión expirará en 5 minutos. Guarde su trabajo antes de que se cierre automáticamente.',
          { duration: 10000, id: 'jwt-expiry-warning' }
        );
      }, warningDelay);
    }

    logoutTimer = setTimeout(() => {
      toast.error('Sesión expirada. Por favor, inicie sesión nuevamente.', {
        id: 'jwt-expired',
      });
      logout();
    }, logoutDelay);

    return () => {
      clearTimeout(warningTimer);
      clearTimeout(logoutTimer);
    };
  }, [logout]);
}
