import { useState } from 'react';

export function useWorkbenchStore() {
  const [markdown, setMarkdown] = useState('');
  const [previewHtml, setPreviewHtml] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return {
    markdown,
    setMarkdown,
    previewHtml,
    setPreviewHtml,
    loading,
    setLoading,
    error,
    setError,
  };
}
