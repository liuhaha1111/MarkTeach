import { useEffect, useState } from 'react';

import ExportPanel from './components/ExportPanel';
import MarkdownEditor from './components/MarkdownEditor';
import ModelControls from './components/ModelControls';
import PreviewPane from './components/PreviewPane';
import SettingsDrawer from './components/SettingsDrawer';
import {
  createExport,
  readAiJob,
  requestPreview,
  saveCredentials,
  startAiRewrite,
} from './lib/api';
import { useWorkbenchStore } from './state/useWorkbenchStore';

export default function App() {
  const {
    markdown,
    setMarkdown,
    previewHtml,
    setPreviewHtml,
    loading,
    setLoading,
    error,
    setError,
  } = useWorkbenchStore();

  const [settingsOpen, setSettingsOpen] = useState(false);
  const [provider, setProvider] = useState('openai');
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  useEffect(() => {
    const timer = setTimeout(async () => {
      try {
        setLoading(true);
        setError(null);
        const preview = await requestPreview(markdown);
        setPreviewHtml(preview.html);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown preview error');
      } finally {
        setLoading(false);
      }
    }, 120);

    return () => clearTimeout(timer);
  }, [markdown, setError, setLoading, setPreviewHtml]);

  const handleSaveCredentials = async (payload: {
    provider: string;
    apiKey: string;
    masterPassword: string;
  }) => {
    await saveCredentials(payload);
    setSaveMessage('Credentials saved');
  };

  const handleRewrite = async () => {
    const created = await startAiRewrite({
      rawMarkdown: markdown,
      audienceLevel: 'beginner',
      style: 'teaching',
      length: 'medium',
      themeId: 'classic',
      provider,
      model: provider === 'deepseek' ? 'deepseek-chat' : 'gpt-4o-mini',
    });

    const status = await readAiJob(created.jobId);
    if (status.status === 'done') {
      setPreviewHtml(status.html);
      setMarkdown(status.resultMarkdown);
    }
  };

  const handleExport = async () => {
    const artifact = await createExport(markdown);
    if (typeof window !== 'undefined') {
      window.location.assign(artifact.downloadUrl);
    }
  };

  return (
    <main
      style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '20px',
        padding: '20px',
      }}
    >
      <section>
        <button type="button" onClick={() => setSettingsOpen((prev) => !prev)}>
          Settings
        </button>
        <SettingsDrawer
          provider={provider}
          open={settingsOpen}
          saveMessage={saveMessage}
          onProviderChange={setProvider}
          onSave={handleSaveCredentials}
        />
        <ModelControls onRewrite={handleRewrite} />
        <ExportPanel onExport={handleExport} />
        <MarkdownEditor value={markdown} onChange={setMarkdown} />
      </section>
      <PreviewPane html={previewHtml} loading={loading} error={error} />
    </main>
  );
}

