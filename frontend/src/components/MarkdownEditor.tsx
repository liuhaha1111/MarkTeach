import { ChangeEvent } from 'react';

type MarkdownEditorProps = {
  value: string;
  onChange: (next: string) => void;
};

export default function MarkdownEditor({ value, onChange }: MarkdownEditorProps) {
  const handleChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    onChange(event.target.value);
  };

  return (
    <section>
      <label htmlFor="markdown-input">Markdown Input</label>
      <textarea
        id="markdown-input"
        aria-label="Markdown Input"
        value={value}
        onChange={handleChange}
        rows={20}
        style={{ width: '100%', marginTop: '8px' }}
      />
    </section>
  );
}
