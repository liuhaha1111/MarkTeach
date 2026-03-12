import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

import App from '../../App';


test('saves provider credentials via settings api', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      if (url.includes('/api/settings/credentials')) {
        return {
          ok: true,
          json: async () => ({ ok: true }),
        } as Response;
      }
      return {
        ok: true,
        json: async () => ({ html: '', toc: [], diagnostics: [] }),
      } as Response;
    })
  );

  render(<App />);

  await userEvent.click(screen.getByRole('button', { name: /settings/i }));
  await userEvent.type(screen.getByLabelText(/api key/i), 'sk-demo');
  await userEvent.type(screen.getByLabelText(/master password/i), 'pass1234');
  await userEvent.click(screen.getByRole('button', { name: /save credentials/i }));

  expect(await screen.findByText(/credentials saved/i)).toBeInTheDocument();
});
