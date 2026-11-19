// Public entry point for the Lexora database module.
//
// Application code should import from '@/db' instead of reaching into the
// internal modules directly.
export { closePool, db, pool } from './client';
