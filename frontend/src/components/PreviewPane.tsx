type PreviewPaneProps = {
  html: string;
  loading: boolean;
  error: string | null;
};

const SCRIPT_TAG_PATTERN = /<script[\s\S]*?>[\s\S]*?<\/script>/gi;
const EVENT_HANDLER_PATTERN = /\son[a-z]+="[^"]*"/gi;

export default function PreviewPane({ html, loading, error }: PreviewPaneProps) {
  const safeHtml = html.replace(SCRIPT_TAG_PATTERN, '').replace(EVENT_HANDLER_PATTERN, '');

  return (
    <section>
      <h2>Preview</h2>
      {loading ? <p>Loading preview...</p> : null}
      {error ? <p role="alert">{error}</p> : null}
      <article dangerouslySetInnerHTML={{ __html: safeHtml }} />
    </section>
  );
}
