import React, { useState, useEffect, useRef } from 'react';
import { Input, Button, Radio, Card, Spin, message } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TextArea } = Input;

interface QueryResponse {
  answer: string;
  references?: string[];
}

const QueryInterface: React.FC = () => {
  const [queryType, setQueryType] = useState<'case_search' | 'legal_consultation'>('legal_consultation');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  // 清理函数，用于关闭EventSource连接
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const handleSubmit = async () => {
    if (!query.trim()) {
      message.warning('请输入查询内容');
      console.warn('Empty query submitted');
      return;
    }

    // 关闭之前的连接
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    setLoading(true);
    setResponse(''); // 清空之前的响应
    console.log(`Submitting query: ${query} (type: ${queryType})`);

    try {
      // 构建查询参数
      const params = new URLSearchParams();
      params.append('text', query);
      params.append('case_type', queryType === 'legal_consultation' ? '法律咨询' : '案例查询');

      // 创建EventSource连接
      const url = `http://localhost:8000/api/query?${params.toString()}`;
      const eventSource = new EventSource(url);
      eventSourceRef.current = eventSource;

      // 处理消息事件
      eventSource.onmessage = (event) => {
        const newData = event.data;
        setResponse(prev => prev + ' ' + newData);
      };

      // 处理错误
      eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        message.error('连接中断，请重试');
        eventSource.close();
        setLoading(false);
      };

      // 处理特定事件
      eventSource.addEventListener('error', (event) => {
        console.error('Legal engine error:', event.data);
        message.error(event.data || '法律引擎异常');
        eventSource.close();
        setLoading(false);
      });

      // 处理连接关闭
      eventSource.addEventListener('done', () => {
        console.log('SSE connection closed');
        eventSource.close();
        setLoading(false);
      });
    } catch (error) {
      console.error('Query failed:', error);
      message.error('查询失败，请稍后重试');
      setLoading(false);
    }
  };

  return (
    <div className="query-interface">
      <div className="query-type-selector">
        <Radio.Group
          value={queryType}
          onChange={(e) => setQueryType(e.target.value)}
          buttonStyle="solid"
        >
          <Radio.Button value="legal_consultation">法律咨询</Radio.Button>
          <Radio.Button value="case_search">案例查询</Radio.Button>
        </Radio.Group>
      </div>

      <TextArea
        rows={4}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={queryType === 'case_search' ? 
          '请输入您想查询的案例关键词或描述...' : 
          '请描述您的法律问题...'}
        style={{ marginBottom: 16 }}
      />

      <Button
        type="primary"
        icon={<SendOutlined />}
        onClick={handleSubmit}
        loading={loading}
      >
        提交查询
      </Button>

      {loading && (
        <div className="loading-container">
          <Spin tip="正在分析您的问题..." />
        </div>
      )}

      {response && (
        <Card className="response-container" title="回复">
          <div className="response-content">
            {response}
          </div>
        </Card>
      )}
    </div>
  );
};

export default QueryInterface;