import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import Dashboard from '../Dashboard'

const renderWithProviders = (ui: React.ReactElement) => {
  return render(
    <ConfigProvider>
      <BrowserRouter>
        {ui}
      </BrowserRouter>
    </ConfigProvider>
  )
}

describe('Dashboard', () => {
  it('renders welcome message', () => {
    renderWithProviders(<Dashboard />)
    
    expect(screen.getByText('欢迎使用命盘推演仿真系统')).toBeInTheDocument()
  })

  it('renders quick start guide', () => {
    renderWithProviders(<Dashboard />)
    
    expect(screen.getByText('快速开始')).toBeInTheDocument()
    expect(screen.getByText('第一步：')).toBeInTheDocument()
    expect(screen.getByText('第二步：')).toBeInTheDocument()
    expect(screen.getByText('第三步：')).toBeInTheDocument()
    expect(screen.getByText('第四步：')).toBeInTheDocument()
  })

  it('renders system features', () => {
    renderWithProviders(<Dashboard />)
    
    expect(screen.getByText('系统特点')).toBeInTheDocument()
    expect(screen.getByText(/多模型交叉验证/)).toBeInTheDocument()
    expect(screen.getByText(/人际关系网络仿真/)).toBeInTheDocument()
    expect(screen.getByText(/环境风水因子/)).toBeInTheDocument()
    expect(screen.getByText(/OASIS动态推演/)).toBeInTheDocument()
  })

  it('renders scenario cards', () => {
    renderWithProviders(<Dashboard />)
    
    expect(screen.getByText('可用场景')).toBeInTheDocument()
    expect(screen.getByText('事业推演')).toBeInTheDocument()
    expect(screen.getByText('婚姻推演')).toBeInTheDocument()
    expect(screen.getByText('合作推演')).toBeInTheDocument()
    expect(screen.getByText('搬迁推演')).toBeInTheDocument()
  })

  it('renders start button', () => {
    renderWithProviders(<Dashboard />)
    
    expect(screen.getByText('开始录入命盘')).toBeInTheDocument()
  })
})