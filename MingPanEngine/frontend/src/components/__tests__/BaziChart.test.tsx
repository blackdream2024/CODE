import { render, screen } from '@testing-library/react'
import { ConfigProvider } from 'antd'
import BaziChart from '../BaziChart'

const renderWithProviders = (ui: React.ReactElement) => {
  return render(
    <ConfigProvider>
      {ui}
    </ConfigProvider>
  )
}

const mockBaziData = {
  四柱: {
    年柱: { 天干: '甲', 地支: '子' },
    月柱: { 天干: '丙', 地支: '寅' },
    日柱: { 天干: '戊', 地支: '午' },
    时柱: { 天干: '庚', 地支: '申' },
  },
  日主: '戊',
  十神: {
    '甲0': '七杀',
    '丙1': '偏印',
    '戊2': '日主',
    '庚3': '食神',
  },
  地支藏干: {
    '子': ['癸'],
    '寅': ['甲', '丙', '戊'],
    '午': ['丁', '己'],
    '申': ['庚', '壬', '戊'],
  },
  五行力量: {
    金: 0.2,
    木: 0.15,
    水: 0.1,
    火: 0.3,
    土: 0.25,
  },
  旺衰: '身旺',
  格局: '偏印格',
  大运: [],
}

describe('BaziChart', () => {
  it('renders title', () => {
    renderWithProviders(<BaziChart data={mockBaziData} />)
    
    expect(screen.getByText('四柱八字')).toBeInTheDocument()
  })

  it('renders pillar labels', () => {
    renderWithProviders(<BaziChart data={mockBaziData} />)
    
    expect(screen.getByText('年柱')).toBeInTheDocument()
    expect(screen.getByText('月柱')).toBeInTheDocument()
    expect(screen.getByText('日柱')).toBeInTheDocument()
    expect(screen.getByText('时柱')).toBeInTheDocument()
  })

  it('renders heavenly stems', () => {
    renderWithProviders(<BaziChart data={mockBaziData} />)
    
    expect(screen.getByText('甲')).toBeInTheDocument()
    expect(screen.getByText('丙')).toBeInTheDocument()
    expect(screen.getAllByText('戊').length).toBeGreaterThanOrEqual(1)
    expect(screen.getByText('庚')).toBeInTheDocument()
  })

  it('renders earthly branches', () => {
    renderWithProviders(<BaziChart data={mockBaziData} />)
    
    expect(screen.getByText('子')).toBeInTheDocument()
    expect(screen.getByText('寅')).toBeInTheDocument()
    expect(screen.getByText('午')).toBeInTheDocument()
    expect(screen.getByText('申')).toBeInTheDocument()
  })

  it('renders day master info', () => {
    renderWithProviders(<BaziChart data={mockBaziData} />)
    
    expect(screen.getByText('日主信息')).toBeInTheDocument()
    expect(screen.getByText('身旺')).toBeInTheDocument()
    expect(screen.getByText('偏印格')).toBeInTheDocument()
  })

  it('renders hidden stems', () => {
    renderWithProviders(<BaziChart data={mockBaziData} />)
    
    expect(screen.getByText('地支藏干')).toBeInTheDocument()
  })
})