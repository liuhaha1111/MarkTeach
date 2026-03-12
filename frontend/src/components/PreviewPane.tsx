type PreviewPaneProps = {
  html: string;
  loading: boolean;
  error: string | null;
};

export default function PreviewPane({ html, loading, error }: PreviewPaneProps) {
  return (
    <section>
      <h2>Preview</h2>
      {loading ? <p>Loading preview...</p> : null}
      {error ? <p role="alert">{error}</p> : null}
      <article dangerouslySetInnerHTML={{ __html: html }} />
    </section>
  );
}
