/**
 * Application Version Configuration
 * 
 * Actualizar este archivo cuando se lance una nueva versión.
 * La versión sigue Semantic Versioning (semver.org):
 * - MAJOR.MINOR.PATCH (e.g., 2.3.0)
 * - MAJOR: Cambios incompatibles
 * - MINOR: Nueva funcionalidad compatible
 * - PATCH: Correcciones de bugs
 */

export const APP_VERSION =
  import.meta.env.VITE_APP_VERSION || "dev";

export const VERSION_INFO = {
  version: APP_VERSION,
  releaseDate: import.meta.env.VITE_APP_BUILD_DATE || "unknown",
};

export default APP_VERSION;

