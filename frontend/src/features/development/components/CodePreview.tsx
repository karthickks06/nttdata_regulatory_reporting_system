import { useState } from 'react';

interface CodePreviewProps {
  code: string;
  language: 'sql' | 'python' | 'javascript';
  title?: string;
}

export function CodePreview({ code, language, title }: CodePreviewProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="flex justify-between items-center px-4 py-3 border-b bg-gray-50">
        <div>
          {title && <h3 className="font-semibold">{title}</h3>}
          <span className="text-xs text-gray-500 uppercase">{language}</span>
        </div>
        <button
          onClick={handleCopy}
          className="px-3 py-1 text-sm bg-primary text-white rounded hover:bg-primary/90"
        >
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>
      <div className="p-4 overflow-x-auto">
        <pre className="text-sm font-mono">
          <code>{code}</code>
        </pre>
      </div>
    </div>
  );
}
