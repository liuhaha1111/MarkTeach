export type PreviewResponse = {
  html: string;
  toc: Array<{ id: string; text: string; level: number }>;
  diagnostics: string[];
};

export type AiRewriteRequest = {
  rawMarkdown: string;
  audienceLevel: string;
  style: string;
  length: string;
  themeId: string;
  provider: string;
  model: string;
};

export type AiJobResponse = {
  status: 'pending' | 'running' | 'done' | 'failed';
  resultMarkdown: string;
  html: string;
  error: string | null;
  traceId: string;
};

export async function requestPreview(rawMarkdown: string): Promise<PreviewResponse> {
  const response = await fetch('/api/transform/preview', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      rawMarkdown,
      themeId: 'classic',
      previewOptions: { toc: true },
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to load preview.');
  }

  return (await response.json()) as PreviewResponse;
}

export async function saveCredentials(payload: {
  provider: string;
  apiKey: string;
  masterPassword: string;
}) {
  const response = await fetch('/api/settings/credentials', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error('Failed to save credentials.');
  }

  return response.json();
}

export async function startAiRewrite(payload: AiRewriteRequest): Promise<{ jobId: string }> {
  const response = await fetch('/api/transform/ai-rewrite', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error('Failed to start AI rewrite.');
  }

  return (await response.json()) as { jobId: string };
}

export async function readAiJob(jobId: string): Promise<AiJobResponse> {
  const response = await fetch(`/api/transform/jobs/${jobId}`);
  if (!response.ok) {
    throw new Error('Failed to query AI job.');
  }
  return (await response.json()) as AiJobResponse;
}

export async function createExport(finalMarkdown: string): Promise<{ artifactId: string; downloadUrl: string }> {
  const response = await fetch('/api/export/zip', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      finalMarkdown,
      themeId: 'classic',
      previewOptions: { toc: true },
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to export ZIP.');
  }

  return (await response.json()) as { artifactId: string; downloadUrl: string };
}
