import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import ChartInput from '../ChartInput'

const renderWithProviders = (ui: React.ReactElement) => {
  return render(
    <ConfigProvider>
      <BrowserRouter>
        {ui}
      </BrowserRouter>
    </ConfigProvider>
  )
}

describe('ChartInput', () => {
  it('renders page title', () => {
    renderWithProviders(<ChartInput />)
    
    expect(screen.getByText('命盘录入')).toBeInTheDocument()
  })

  it('renders steps', () => {
    renderWithProviders(<ChartInput />)
    
    expect(screen.getByText('基本信息')).toBeInTheDocument()
    expect(screen.getByText('出生信息')).toBeInTheDocument()
  })

  it('renders first step form', () => {
    renderWithProviders(<ChartInput />)
    
    expect(screen.getByLabelText('命盘名称')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('例如：我的命盘')).toBeInTheDocument()
  })

  it('renders instructions card', () => {
    renderWithProviders(<ChartInput />)
    
    expect(screen.getByText('输入说明')).toBeInTheDocument()
    expect(screen.getByText(/出生日期/)).toBeInTheDocument()
    expect(screen.getByText(/出生时间/)).toBeInTheDocument()
    expect(screen.getByText(/性别/)).toBeInTheDocument()
  })

  it('renders next button', () => {
    renderWithProviders(<ChartInput />)
    
    expect(screen.getByText('下一步')).toBeInTheDocument()
  })
})