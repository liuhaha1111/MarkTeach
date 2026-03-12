import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

import App from '../../App';


test('ai rewrite replaces preview content after job done', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/api/transform/ai-rewrite')) {
        return {
          ok: true,
          json: async () => ({ jobId: 'job-1' }),
        } as Response;
      }
      if (url.includes('/api/transform/jobs/job-1')) {
        return {
          ok: true,
          json: async () => ({
            status: 'done',
            resultMarkdown: '## Core',
            html: '<h2>Core Concepts</h2>',
            error: null,
            traceId: 'job-1',
          }),
        } as Response;
      }

      return {
        ok: true,
        json: async () => ({ html: '', toc: [], diagnostics: [] }),
      } as Response;
    })
  );

  render(<App />);
  await userEvent.click(screen.getByRole('button', { name: /ai rewrite/i }));

  expect(await screen.findByText('Core Concepts')).toBeInTheDocument();
});
