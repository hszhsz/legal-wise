import React from 'react';
import { Layout, Typography } from 'antd';
import QueryInterface from './components/QueryInterface.tsx';
import './App.css';

const { Header, Content, Footer } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  return (
    <Layout className="layout">
      <Header className="header">
        <Title level={3} style={{ color: 'white', margin: '16px 0' }}>
          Legal Wise - 智能法律咨询系统
        </Title>
      </Header>
      <Content style={{ padding: '0 50px', marginTop: 40 }}>
        <div className="site-layout-content">
          <QueryInterface />
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        Legal Wise ©{new Date().getFullYear()} Created by AI Team
      </Footer>
    </Layout>
  );
};

export default App;