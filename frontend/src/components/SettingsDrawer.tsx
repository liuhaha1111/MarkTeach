import { FormEvent, useState } from 'react';

type SettingsDrawerProps = {
  provider: string;
  open: boolean;
  saveMessage: string | null;
  onProviderChange: (provider: string) => void;
  onSave: (payload: { provider: string; apiKey: string; masterPassword: string }) => Promise<void>;
};

export default function SettingsDrawer({
  provider,
  open,
  saveMessage,
  onProviderChange,
  onSave,
}: SettingsDrawerProps) {
  const [apiKey, setApiKey] = useState('');
  const [masterPassword, setMasterPassword] = useState('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await onSave({ provider, apiKey, masterPassword });
  };

  if (!open) {
    return null;
  }

  return (
    <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '8px', marginBottom: '12px' }}>
      <label htmlFor="provider">Provider</label>
      <select
        id="provider"
        aria-label="Provider"
        value={provider}
        onChange={(event) => onProviderChange(event.target.value)}
      >
        <option value="openai">OpenAI</option>
        <option value="deepseek">DeepSeek</option>
      </select>

      <label htmlFor="api-key">API Key</label>
      <input
        id="api-key"
        aria-label="API Key"
        type="password"
        value={apiKey}
        onChange={(event) => setApiKey(event.target.value)}
      />

      <label htmlFor="master-password">Master Password</label>
      <input
        id="master-password"
        aria-label="Master Password"
        type="password"
        value={masterPassword}
        onChange={(event) => setMasterPassword(event.target.value)}
      />

      <button type="submit">Save Credentials</button>
      {saveMessage ? <p>{saveMessage}</p> : null}
    </form>
  );
}
