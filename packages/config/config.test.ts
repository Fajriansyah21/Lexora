import { describe, it, expect } from 'vitest';
import { workspaceName } from './index';

describe('Lexora Monorepo Foundation', () => {
  it('should export correct workspace name from config package', () => {
    expect(workspaceName).toBe('lexora');
  });

  it('should run a basic truthiness check', () => {
    expect(true).toBe(true);
  });
});
