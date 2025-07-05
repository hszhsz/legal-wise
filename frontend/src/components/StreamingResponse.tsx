import { useState, useEffect } from 'react';

export default function StreamingResponse({ query }: { query: string }) {
  const [response, setResponse] = useState<string[]>([]);

  useEffect(() => {
    const eventSource = new EventSource(`http://localhost:8000/api/legal/consult?text=${encodeURIComponent(query)}`);

    eventSource.onerror = () => {
      eventSource.close();
      setResponse(prev => [...prev, '连接异常，请重试']);
    };

    eventSource.onmessage = (e) => {
      setResponse(prev => [...prev, e.data]);
    };

    return () => eventSource.close();
  }, [query]);

  return (
    <div className="space-y-2">
      {response.map((text, i) => (
        <p key={i} className="text-gray-700 animate-fade-in">{text}</p>
      ))}
    </div>
  );
}