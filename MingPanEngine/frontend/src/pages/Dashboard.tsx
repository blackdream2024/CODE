import { Row, Col, Card, Statistic, Typography, Space, Button, Tag, Divider } from 'antd';
import {
  UserOutlined,
  ExperimentOutlined,
  TeamOutlined,
  CompassOutlined,
  StarOutlined,
  ThunderboltOutlined,
  SafetyOutlined,
  RocketOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useChartStore } from '../stores/chartStore';

const { Title, Paragraph, Text } = Typography;

function Dashboard() {
  const navigate = useNavigate();
  const { charts, simulationResult } = useChartStore();

  return (
    <div className="gf-cloud-pattern" style={{ minHeight: '100vh', padding: '24px' }}>
      {/* 顶部标题区域 */}
      <div style={{ 
        textAlign: 'center', 
        marginBottom: 48,
        position: 'relative',
        zIndex: 1,
      }}>
        <div className="gf-bagua-border" style={{ marginBottom: 24 }}>
          <Title level={2} className="gf-title-gold" style={{ 
            margin: 0,
            fontSize: 32,
            fontWeight: 700,
            letterSpacing: 6,
          }}>
            命盘推演仿真系统
          </Title>
        </div>
        <Paragraph style={{ 
          color: '#b8b8d0', 
          fontSize: 16,
          maxWidth: 600,
          margin: '0 auto',
          lineHeight: 1.8,
        }}>
          融合传统智慧与现代科技，基于八字、紫微斗数、风水等多维度命理分析，
          结合AI技术实现动态情境推演
        </Paragraph>
        <div className="gf-huiwen-divider" style={{ width: 200, margin: '24px auto' }} />
      </div>

      {/* 统计卡片区域 */}
      <Row gutter={[24, 24]} style={{ marginBottom: 48 }}>
        <Col xs={24} sm={12} lg={6}>
          <div className="gf-card gf-gold-glow" style={{ 
            padding: '32px 24px',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
          }} onClick={() => navigate('/chart-input')}>
            <div className="gf-icon" style={{ marginBottom: 16 }}>
              <UserOutlined style={{ fontSize: 32 }} />
            </div>
            <div className="gf-statistic">
              <div className="gf-statistic-value">{charts.length}</div>
              <div className="gf-statistic-label">已录入命盘</div>
            </div>
            <Tag className="gf-tag" style={{ marginTop: 16 }}>点击查看</Tag>
          </div>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <div className="gf-card" style={{ 
            padding: '32px 24px',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
          }} onClick={() => navigate('/simulation')}>
            <div style={{ color: '#c41e3a', marginBottom: 16 }}>
              <ExperimentOutlined style={{ fontSize: 32 }} />
            </div>
            <div className="gf-statistic">
              <div className="gf-statistic-value">{simulationResult ? 1 : 0}</div>
              <div className="gf-statistic-label">推演次数</div>
            </div>
            <Tag className="gf-tag" style={{ marginTop: 16 }}>开始推演</Tag>
          </div>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <div className="gf-card" style={{ 
            padding: '32px 24px',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
          }} onClick={() => navigate('/relation')}>
            <div style={{ color: '#7b2d8e', marginBottom: 16 }}>
              <TeamOutlined style={{ fontSize: 32 }} />
            </div>
            <div className="gf-statistic">
              <div className="gf-statistic-value">0</div>
              <div className="gf-statistic-label">关系分析</div>
            </div>
            <Tag className="gf-tag" style={{ marginTop: 16 }}>分析关系</Tag>
          </div>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <div className="gf-card" style={{ 
            padding: '32px 24px',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
          }} onClick={() => navigate('/chart-view')}>
            <div style={{ color: '#d4a853', marginBottom: 16 }}>
              <CompassOutlined style={{ fontSize: 32 }} />
            </div>
            <div className="gf-statistic">
              <div className="gf-statistic-value">{charts.length}</div>
              <div className="gf-statistic-label">命盘查看</div>
            </div>
            <Tag className="gf-tag" style={{ marginTop: 16 }}>查看详情</Tag>
          </div>
        </Col>
      </Row>

      {/* 功能介绍区域 */}
      <Row gutter={[24, 24]} style={{ marginBottom: 48 }}>
        <Col xs={24} lg={12}>
          <div className="gf-card" style={{ padding: '32px', height: '100%' }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              marginBottom: 24,
              gap: 12,
            }}>
              <StarOutlined style={{ color: '#d4a853', fontSize: 24 }} />
              <Title level={4} className="gf-title" style={{ margin: 0 }}>
                快速开始
              </Title>
            </div>
            <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                <div style={{ 
                  width: 24, 
                  height: 24, 
                  borderRadius: '50%', 
                  background: 'rgba(212, 168, 83, 0.2)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                  marginTop: 2,
                }}>
                  <Text style={{ color: '#d4a853', fontSize: 12, fontWeight: 600 }}>1</Text>
                </div>
                <div>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: 4 }}>
                    录入命盘数据
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    输入出生日期、时间、性别等基本信息
                  </Text>
                </div>
              </div>
              <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                <div style={{ 
                  width: 24, 
                  height: 24, 
                  borderRadius: '50%', 
                  background: 'rgba(212, 168, 83, 0.2)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                  marginTop: 2,
                }}>
                  <Text style={{ color: '#d4a853', fontSize: 12, fontWeight: 600 }}>2</Text>
                </div>
                <div>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: 4 }}>
                    查看排盘结果
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    八字排盘和紫微命盘分析结果
                  </Text>
                </div>
              </div>
              <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                <div style={{ 
                  width: 24, 
                  height: 24, 
                  borderRadius: '50%', 
                  background: 'rgba(212, 168, 83, 0.2)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                  marginTop: 2,
                }}>
                  <Text style={{ color: '#d4a853', fontSize: 12, fontWeight: 600 }}>3</Text>
                </div>
                <div>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: 4 }}>
                    选择推演场景
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    事业、婚姻、合作、搬迁等多种场景
                  </Text>
                </div>
              </div>
              <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                <div style={{ 
                  width: 24, 
                  height: 24, 
                  borderRadius: '50%', 
                  background: 'rgba(212, 168, 83, 0.2)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                  marginTop: 2,
                }}>
                  <Text style={{ color: '#d4a853', fontSize: 12, fontWeight: 600 }}>4</Text>
                </div>
                <div>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: 4 }}>
                    查看推演结果
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    概率云、热力图等可视化分析
                  </Text>
                </div>
              </div>
            </Space>
            <Button 
              type="primary" 
              className="gf-btn-primary"
              style={{ marginTop: 32 }}
              onClick={() => navigate('/chart-input')}
            >
              开始录入命盘
            </Button>
          </div>
        </Col>
        <Col xs={24} lg={12}>
          <div className="gf-card" style={{ padding: '32px', height: '100%' }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              marginBottom: 24,
              gap: 12,
            }}>
              <ThunderboltOutlined style={{ color: '#d4a853', fontSize: 24 }} />
              <Title level={4} className="gf-title" style={{ margin: 0 }}>
                系统特点
              </Title>
            </div>
            <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <div style={{ 
                display: 'flex', 
                gap: 16, 
                alignItems: 'flex-start',
                padding: '16px',
                background: 'rgba(212, 168, 83, 0.05)',
                borderRadius: 8,
                border: '1px solid rgba(212, 168, 83, 0.1)',
              }}>
                <SafetyOutlined style={{ color: '#d4a853', fontSize: 20, marginTop: 4 }} />
                <div>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: 4 }}>
                    多模型交叉验证
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    八字、紫微、梅花易数三大体系互相印证，提高分析准确性
                  </Text>
                </div>
              </div>
              <div style={{ 
                display: 'flex', 
                gap: 16, 
                alignItems: 'flex-start',
                padding: '16px',
                background: 'rgba(196, 30, 58, 0.05)',
                borderRadius: 8,
                border: '1px solid rgba(196, 30, 58, 0.1)',
              }}>
                <TeamOutlined style={{ color: '#c41e3a', fontSize: 20, marginTop: 4 }} />
                <div>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: 4 }}>
                    人际关系网络仿真
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    多人命盘耦合，推演合作、婚姻、竞争等动态关系
                  </Text>
                </div>
              </div>
              <div style={{ 
                display: 'flex', 
                gap: 16, 
                alignItems: 'flex-start',
                padding: '16px',
                background: 'rgba(123, 45, 142, 0.05)',
                borderRadius: 8,
                border: '1px solid rgba(123, 45, 142, 0.1)',
              }}>
                <CompassOutlined style={{ color: '#7b2d8e', fontSize: 20, marginTop: 4 }} />
                <div>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: 4 }}>
                    环境风水因子
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    GPS定位 + 八宅/玄空风水计算，环境能量分析
                  </Text>
                </div>
              </div>
              <div style={{ 
                display: 'flex', 
                gap: 16, 
                alignItems: 'flex-start',
                padding: '16px',
                background: 'rgba(212, 168, 83, 0.05)',
                borderRadius: 8,
                border: '1px solid rgba(212, 168, 83, 0.1)',
              }}>
                <RocketOutlined style={{ color: '#d4a853', fontSize: 20, marginTop: 4 }} />
                <div>
                  <Text strong style={{ color: '#ffffff', display: 'block', marginBottom: 4 }}>
                    OASIS动态推演
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    多智能体社会仿真，输出概率云而非固定结论
                  </Text>
                </div>
              </div>
            </Space>
          </div>
        </Col>
      </Row>

      {/* 可用场景区域 */}
      <div className="gf-card" style={{ padding: '32px' }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          marginBottom: 24,
          gap: 12,
        }}>
          <ExperimentOutlined style={{ color: '#d4a853', fontSize: 24 }} />
          <Title level={4} className="gf-title" style={{ margin: 0 }}>
            可用场景
          </Title>
        </div>
        <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
        <Row gutter={[24, 24]}>
          {[
            { 
              type: 'career', 
              name: '事业推演', 
              desc: '分析事业发展前景，适合创业、跳槽、升职等决策',
              icon: <RocketOutlined />,
              color: '#d4a853',
            },
            { 
              type: 'marriage', 
              name: '婚姻推演', 
              desc: '分析感情婚姻走势，适合结婚、恋爱、相亲等场景',
              icon: <TeamOutlined />,
              color: '#c41e3a',
            },
            { 
              type: 'cooperation', 
              name: '合作推演', 
              desc: '分析合作关系发展，适合合伙、签约、团队协作',
              icon: <SafetyOutlined />,
              color: '#7b2d8e',
            },
            { 
              type: 'relocation', 
              name: '搬迁推演', 
              desc: '分析搬迁时机，适合搬家、换城市、出国等决策',
              icon: <CompassOutlined />,
              color: '#d4a853',
            },
          ].map((scenario) => (
            <Col xs={24} sm={12} key={scenario.type}>
              <div 
                className="gf-card" 
                style={{ 
                  padding: '24px',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                }}
                onClick={() => navigate('/simulation')}
              >
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: 16,
                  marginBottom: 16,
                }}>
                  <div style={{ 
                    color: scenario.color,
                    fontSize: 24,
                    width: 48,
                    height: 48,
                    borderRadius: '50%',
                    background: `${scenario.color}15`,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    {scenario.icon}
                  </div>
                  <div>
                    <Text strong style={{ color: '#ffffff', fontSize: 18, display: 'block' }}>
                      {scenario.name}
                    </Text>
                    <Text style={{ color: '#b8b8d0', fontSize: 14 }}>
                      {scenario.desc}
                    </Text>
                  </div>
                </div>
                <div style={{ 
                  display: 'flex', 
                  justifyContent: 'flex-end',
                }}>
                  <Tag className="gf-tag">立即推演</Tag>
                </div>
              </div>
            </Col>
          ))}
        </Row>
      </div>

      {/* 底部装饰 */}
      <div style={{ 
        textAlign: 'center', 
        marginTop: 48,
        padding: '24px',
        position: 'relative',
        zIndex: 1,
      }}>
        <div className="gf-huiwen-divider" style={{ width: 100, margin: '0 auto 16px' }} />
        <Text style={{ color: '#6a6a8a', fontSize: 12, letterSpacing: 2 }}>
          命盘推演仿真系统 v1.0.0
        </Text>
      </div>
    </div>
  );
}

export default Dashboard;
