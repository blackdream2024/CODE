import { Suspense, lazy, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Layout, Menu, ConfigProvider, theme, Spin } from 'antd';
import {
  DashboardOutlined,
  UserOutlined,
  ExperimentOutlined,
  CompassOutlined,
  TeamOutlined,
  EnvironmentOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

import Dashboard from './pages/Dashboard';
import './styles/guofeng.css';

// 懒加载页面组件 - 代码分割
const ChartInput = lazy(() => import('./pages/ChartInput'));
const ChartView = lazy(() => import('./pages/ChartView'));
const Simulation = lazy(() => import('./pages/Simulation'));
const RelationAnalysis = lazy(() => import('./pages/RelationAnalysis'));
const FengshuiAnalysis = lazy(() => import('./pages/FengshuiAnalysis'));

const { Header, Content, Sider } = Layout;

type MenuItem = Required<MenuProps>['items'][number];

function getItem(
  label: React.ReactNode,
  key: string,
  icon?: React.ReactNode,
  children?: MenuItem[]
): MenuItem {
  return {
    key,
    icon,
    children,
    label: <Link to={key}>{label}</Link>,
  } as MenuItem;
}

const menuItems: MenuItem[] = [
  getItem('总览', '/', <DashboardOutlined />),
  getItem('命盘录入', '/chart-input', <UserOutlined />),
  getItem('命盘查看', '/chart-view', <CompassOutlined />),
  getItem('推演仿真', '/simulation', <ExperimentOutlined />),
  getItem('关系分析', '/relation', <TeamOutlined />),
  getItem('风水分析', '/fengshui', <EnvironmentOutlined />),
];

function AppLayout() {
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  const getSelectedKey = () => {
    const path = location.pathname;
    if (path === '/') return '/';
    if (path.startsWith('/chart-input')) return '/chart-input';
    if (path.startsWith('/chart-view')) return '/chart-view';
    if (path.startsWith('/simulation')) return '/simulation';
    if (path.startsWith('/relation')) return '/relation';
    if (path.startsWith('/fengshui')) return '/fengshui';
    return '/';
  };

  const siderWidth = collapsed ? 80 : 200;

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider
        breakpoint="lg"
        collapsedWidth="80"
        collapsed={collapsed}
        onBreakpoint={(broken) => {
          setIsMobile(broken);
          setCollapsed(broken);
        }}
        onCollapse={(value) => setCollapsed(value)}
        className="gf-sider"
        style={{
          overflow: 'auto',
          height: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
          zIndex: 100,
        }}
      >
        {/* Logo 区域 */}
        <div
          style={{
            height: collapsed ? 64 : 80,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            borderBottom: '1px solid rgba(212, 168, 83, 0.2)',
            position: 'relative',
            zIndex: 1,
            transition: 'height 0.2s',
          }}
        >
          {/* 八卦符号 */}
          <div style={{
            width: collapsed ? 36 : 40,
            height: collapsed ? 36 : 40,
            borderRadius: '50%',
            border: '2px solid #d4a853',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: collapsed ? 0 : 8,
            background: 'radial-gradient(circle, rgba(212, 168, 83, 0.1) 0%, transparent 70%)',
            boxShadow: '0 0 20px rgba(212, 168, 83, 0.2)',
            transition: 'all 0.2s',
          }}>
            <span style={{ 
              color: '#d4a853', 
              fontSize: collapsed ? 18 : 20, 
              fontWeight: 'bold',
              fontFamily: 'serif',
            }}>
              ☰
            </span>
          </div>
          {!collapsed && (
            <>
              <div style={{
                color: '#d4a853',
                fontSize: 16,
                fontWeight: 700,
                letterSpacing: 4,
                fontFamily: 'serif',
                textShadow: '0 0 10px rgba(212, 168, 83, 0.3)',
              }}>
                命盘推演
              </div>
              <div style={{
                color: '#b8b8d0',
                fontSize: 10,
                letterSpacing: 2,
                marginTop: 2,
              }}>
                MINGPAN ENGINE
              </div>
            </>
          )}
        </div>
        
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[getSelectedKey()]}
          items={menuItems}
          className="gf-menu"
          inlineCollapsed={collapsed}
          style={{ 
            background: 'transparent',
            borderRight: 'none',
            marginTop: 8,
          }}
        />
        
        {/* 底部装饰 */}
        {!collapsed && (
          <div style={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            padding: '16px',
            textAlign: 'center',
            borderTop: '1px solid rgba(212, 168, 83, 0.1)',
          }}>
            <div style={{
              color: '#6a6a8a',
              fontSize: 11,
              letterSpacing: 1,
            }}>
              v1.0.0
            </div>
          </div>
        )}
      </Sider>
      
      <Layout style={{ marginLeft: siderWidth, transition: 'margin-left 0.2s' }}>
        <Header
          className="gf-header"
          style={{
            padding: isMobile ? '0 16px' : '0 32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            height: 64,
            position: 'sticky',
            top: 0,
            zIndex: 99,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: isMobile ? 8 : 16 }}>
            {isMobile && (
              <div
                onClick={() => setCollapsed(!collapsed)}
                style={{ 
                  cursor: 'pointer', 
                  color: '#d4a853', 
                  fontSize: 20,
                  padding: '4px 8px',
                }}
              >
                {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              </div>
            )}
            <h1 style={{ 
              margin: 0, 
              fontSize: isMobile ? 16 : 20, 
              color: '#ffffff',
              fontWeight: 600,
              letterSpacing: isMobile ? 1 : 2,
              whiteSpace: 'nowrap',
            }}>
              {isMobile ? '命盘推演' : '命盘推演仿真系统'}
            </h1>
            {!isMobile && (
              <div style={{
                padding: '2px 12px',
                background: 'rgba(212, 168, 83, 0.1)',
                border: '1px solid rgba(212, 168, 83, 0.3)',
                borderRadius: 4,
                color: '#d4a853',
                fontSize: 12,
                letterSpacing: 1,
              }}>
                专业版
              </div>
            )}
          </div>
          {!isMobile && (
            <div style={{ 
              display: 'flex',
              alignItems: 'center',
              gap: 24,
            }}>
              <div style={{ 
                color: '#b8b8d0', 
                fontSize: 13,
                letterSpacing: 1,
              }}>
                融合传统智慧与现代科技
              </div>
              <div style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: '#52c41a',
                boxShadow: '0 0 10px rgba(82, 196, 26, 0.5)',
              }} />
            </div>
          )}
        </Header>
        
        <Content className="gf-content" style={{ margin: isMobile ? 12 : 24 }}>
          <div style={{ position: 'relative', zIndex: 1 }}>
            <Suspense fallback={
              <div className="gf-loading" style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                minHeight: '60vh' 
              }}>
                <Spin size="large" tip="加载中..." />
              </div>
            }>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/chart-input" element={<ChartInput />} />
                <Route path="/chart-view" element={<ChartView />} />
                <Route path="/simulation" element={<Simulation />} />
                <Route path="/relation" element={<RelationAnalysis />} />
                <Route path="/fengshui" element={<FengshuiAnalysis />} />
              </Routes>
            </Suspense>
          </div>
        </Content>
      </Layout>
    </Layout>
  );
}

function App() {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorPrimary: '#d4a853',
          colorBgContainer: '#141430',
          colorBgElevated: '#1a1a3e',
          colorBgLayout: '#0a0a1a',
          colorText: '#ffffff',
          colorTextSecondary: '#b8b8d0',
          colorBorder: 'rgba(212, 168, 83, 0.2)',
          colorBorderSecondary: 'rgba(255, 255, 255, 0.05)',
          borderRadius: 8,
          fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
        },
        components: {
          Menu: {
            darkItemBg: 'transparent',
            darkSubMenuItemBg: 'transparent',
            darkItemSelectedBg: 'rgba(212, 168, 83, 0.15)',
            darkItemHoverBg: 'rgba(212, 168, 83, 0.1)',
            darkItemSelectedColor: '#d4a853',
            darkItemColor: '#b8b8d0',
          },
          Card: {
            colorBgContainer: '#141430',
            colorBorderSecondary: 'rgba(212, 168, 83, 0.2)',
          },
          Table: {
            colorBgContainer: '#141430',
            headerBg: 'rgba(212, 168, 83, 0.05)',
            headerColor: '#d4a853',
            rowHoverBg: 'rgba(212, 168, 83, 0.05)',
          },
          Input: {
            colorBgContainer: 'rgba(255, 255, 255, 0.05)',
            colorBorder: 'rgba(212, 168, 83, 0.2)',
            colorText: '#ffffff',
            colorTextPlaceholder: '#6a6a8a',
          },
          Select: {
            colorBgContainer: 'rgba(255, 255, 255, 0.05)',
            colorBorder: 'rgba(212, 168, 83, 0.2)',
            colorText: '#ffffff',
            colorTextPlaceholder: '#6a6a8a',
          },
          Button: {
            primaryShadow: '0 4px 15px rgba(212, 168, 83, 0.3)',
          },
          Tabs: {
            inkBarColor: '#d4a853',
            itemActiveColor: '#d4a853',
            itemHoverColor: '#e6c07a',
            itemSelectedColor: '#d4a853',
            itemColor: '#b8b8d0',
          },
        },
      }}
    >
      <Router>
        <AppLayout />
      </Router>
    </ConfigProvider>
  );
}

export default App;
