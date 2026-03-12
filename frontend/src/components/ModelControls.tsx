type ModelControlsProps = {
  onRewrite: () => Promise<void>;
};

export default function ModelControls({ onRewrite }: ModelControlsProps) {
  return (
    <section style={{ marginBottom: '12px' }}>
      <button type="button" onClick={() => void onRewrite()}>
        AI Rewrite
      </button>
    </section>
  );
}
