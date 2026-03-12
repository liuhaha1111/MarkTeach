import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

import App from '../../App';


test('typing markdown refreshes preview pane', async () => {
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ html: '<h1>Demo</h1>', toc: [], diagnostics: [] }),
    })
  );

  render(<App />);
  const editor = screen.getByLabelText(/markdown input/i);
  await userEvent.clear(editor);
  await userEvent.type(editor, '# Demo');

  expect(await screen.findByText('Demo')).toBeInTheDocument();
});
