type ExportPanelProps = {
  onExport: () => Promise<void>;
};

export default function ExportPanel({ onExport }: ExportPanelProps) {
  return (
    <section style={{ marginBottom: '12px' }}>
      <button type="button" onClick={() => void onExport()}>
        Export ZIP
      </button>
    </section>
  );
}
