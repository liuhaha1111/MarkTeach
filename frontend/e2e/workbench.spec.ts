import { expect, test } from '@playwright/test';

const ZIP_BYTES = Buffer.from([
  0x50, 0x4b, 0x05, 0x06,
  0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00,
  0x00, 0x00, 0x00, 0x00,
  0x00, 0x00,
]);

test('markdown to ai rewrite to zip export', async ({ page }) => {
  await page.route('**/api/transform/preview', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ html: '<h2>Core Concepts</h2>', toc: [], diagnostics: [] }),
    });
  });

  await page.route('**/api/transform/ai-rewrite', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ jobId: 'job-1' }),
    });
  });

  await page.route('**/api/transform/jobs/job-1', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'done',
        resultMarkdown: '## Core',
        html: '<h2>Core Concepts</h2>',
        error: null,
        traceId: 'job-1',
      }),
    });
  });

  await page.route('**/api/export/zip', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ artifactId: 'artifact-1', downloadUrl: '/api/export/download/artifact-1' }),
    });
  });

  await page.route('**/api/export/download/artifact-1', async (route) => {
    await route.fulfill({
      status: 200,
      headers: {
        'content-type': 'application/zip',
        'content-disposition': 'attachment; filename="lesson.zip"',
      },
      body: ZIP_BYTES,
    });
  });

  await page.goto('/');
  await page.getByLabel('Markdown Input').fill('# Topic');
  await page.getByRole('button', { name: 'AI Rewrite' }).click();
  await expect(page.getByRole('heading', { name: 'Core Concepts' })).toBeVisible();

  const downloadPromise = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export ZIP' }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toContain('.zip');
});
