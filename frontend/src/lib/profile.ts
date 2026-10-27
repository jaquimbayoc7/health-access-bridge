// Colores de los perfiles de barreras (0, 1 y 2) con texto blanco y contraste de al menos 4,5:1 (WCAG 1.4.3).
// Antes cada pantalla tenia su propia tabla (y el panel usaba umbrales de 1 a 10 que no corresponden a los perfiles 0, 1 y 2).
const PROFILE_BADGE: Record<number, string> = {
  0: 'bg-gray-600 text-white',
  1: 'bg-green-700 text-white',
  2: 'bg-blue-700 text-white',
};

export const profileBadgeClass = (profile: number | null | undefined): string =>
  (profile !== null && profile !== undefined && PROFILE_BADGE[profile]) || 'bg-gray-600 text-white';
