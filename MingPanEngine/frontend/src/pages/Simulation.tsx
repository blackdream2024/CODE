import { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Button,
  Select,
  InputNumber,
  Form,
  message,
  Spin,
  Space,
  Tag,
  Divider,
  Timeline,
  Input,
} from 'antd';
import {
  ExperimentOutlined,
  PlayCircleOutlined,
  StarOutlined,
  ThunderboltOutlined,
  BookOutlined,
  AimOutlined,
  BulbOutlined,
  CheckCircleOutlined,
  CalendarOutlined,
  TeamOutlined,
  CalculatorOutlined,
} from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { useChartStore } from '../stores/chartStore';
import { oasisApi } from '../services/api';
import type { ScenarioType } from '../types';
import CalculationProcess from '../components/CalculationProcess';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

const scenarioDescriptions: Record<ScenarioType, { name: string; desc: string }> = {
  career: { name: '事业推演', desc: '分析事业发展前景，适合创业、跳槽、升职等决策' },
  marriage: { name: '婚姻推演', desc: '分析感情婚姻走势，适合结婚、恋爱、相亲等场景' },
  cooperation: { name: '合作推演', desc: '分析合作关系发展，适合合伙、签约、团队协作' },
  relocation: { name: '搬迁推演', desc: '分析搬迁时机，适合搬家、换城市、出国等决策' },
  investment: { name: '投资推演', desc: '分析投资理财前景，适合股票、基金、房产等投资决策' },
  health: { name: '健康推演', desc: '分析健康运势，适合养生、医疗、运动等决策' },
  learning: { name: '学习推演', desc: '分析学习考试运势，适合升学、考证、培训等决策' },
};

function Simulation() {
  const { charts, selectedScenario, setSelectedScenario, simulationResult, setSimulationResult, isSimulating, setIsSimulating } = useChartStore();
  const [form] = Form.useForm();
  const [steps, setSteps] = useState(12);
  const [samples, setSamples] = useState(50);
  // 时间范围状态
  const [startYear, setStartYear] = useState(2026);
  const [startMonth, setStartMonth] = useState(1);
  // 额外Agent输入
  const [extraAgents, setExtraAgents] = useState<Array<{name: string; birth_date: string; birth_time: string; gender: string}>>([]);

  const handleSimulate = async () => {
    if (charts.length === 0 && extraAgents.length === 0) {
      message.warning('请先录入命盘数据或添加参与者');
      return;
    }

    setIsSimulating(true);
    try {
      // 合并已选命盘和额外Agent
      const agents = [
        ...charts.map((chart) => ({
          name: chart.name,
          birth_date: chart.birth_date,
          birth_time: chart.birth_time,
          gender: chart.gender,
        })),
        ...extraAgents,
      ];

      const result = await oasisApi.simulate({
        agents,
        scenario: selectedScenario,
        steps,
        samples,
        start_year: startYear,
        start_month: startMonth,
      });

      setSimulationResult(result);
      message.success('推演完成！');
    } catch (error) {
      console.error('推演失败:', error);
      message.error('推演失败，请稍后重试');
    } finally {
      setIsSimulating(false);
    }
  };

  const addExtraAgent = () => {
    setExtraAgents([...extraAgents, { name: '', birth_date: '', birth_time: '12:00', gender: 'male' }]);
  };

  const removeExtraAgent = (index: number) => {
    setExtraAgents(extraAgents.filter((_, i) => i !== index));
  };

  const updateExtraAgent = (index: number, field: string, value: string) => {
    const updated = [...extraAgents];
    (updated[index] as any)[field] = value;
    setExtraAgents(updated);
  };

  const getHeatmapOption = () => {
    if (!simulationResult) return {};

    const months = simulationResult.monthly_heatmap.map((h) => `${h.year}年${h.month}月`);
    const agentIds = Object.keys(simulationResult.monthly_heatmap[0]?.agents || {});
    const agentNames = agentIds.map((id) => {
      const chart = charts.find((c) => c.id === id);
      return chart?.name || id;
    });

    const data: any[] = [];
    simulationResult.monthly_heatmap.forEach((h, monthIdx) => {
      agentIds.forEach((agentId, agentIdx) => {
        const agentData = h.agents[agentId];
        if (agentData) {
          data.push([monthIdx, agentIdx, agentData.fortune]);
        }
      });
    });

    return {
      title: {
        text: '运势热力图',
        left: 'center',
      },
      tooltip: {
        position: 'top',
        formatter: (params: any) => {
          const [monthIdx, agentIdx, value] = params.data;
          const agentId = agentIds[agentIdx];
          const heatData = simulationResult.monthly_heatmap[monthIdx]?.agents[agentId];
          const explanation = heatData?.explanation || '';
          const classicalRef = heatData?.classical_reference || '';
          let tooltip = `<strong>${months[monthIdx]} - ${agentNames[agentIdx]}</strong><br/>运势指数: ${value.toFixed(3)}`;
          if (explanation) tooltip += `<br/><em>${explanation}</em>`;
          if (classicalRef) tooltip += `<br/><span style="color:#d4a853;font-size:11px;">📚 ${classicalRef}</span>`;
          return tooltip;
        },
      },
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%',
        top: '15%',
      },
      xAxis: {
        type: 'category',
        data: months,
        splitArea: { show: true },
      },
      yAxis: {
        type: 'category',
        data: agentNames,
        splitArea: { show: true },
      },
      visualMap: {
        min: 0,
        max: 1,
        calculable: true,
        orient: 'horizontal',
        left: 'center',
        bottom: '0%',
        inRange: {
          color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#fee090', '#fdae61', '#f46d43', '#d73027'],
        },
      },
      series: [
        {
          type: 'heatmap',
          data,
          label: {
            show: true,
            formatter: (params: any) => params.data[2].toFixed(2),
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
        },
      ],
    };
  };

  const getCloudOption = () => {
    if (!simulationResult) return {};

    const agentIds = Object.keys(simulationResult.probability_cloud);
    const agentNames = agentIds.map((id) => {
      const chart = charts.find((c) => c.id === id);
      return chart?.name || id;
    });

    // 使用第一个agent的维度信息
    const firstAgentId = agentIds[0];
    const cloudData = simulationResult.probability_cloud[firstAgentId];
    const dimensionNames = cloudData?.dimension_explanations 
      ? cloudData.dimensions.map((dim, idx) => {
          const explanation = cloudData.dimension_explanations?.[idx] || dim;
          return { name: explanation.split('：')[0] || dim, max: 1 };
        })
      : cloudData?.dimensions.map(dim => ({ name: dim, max: 1 })) || [];

    return {
      title: {
        text: '概率云分布',
        left: 'center',
      },
      tooltip: {
        formatter: (params: any) => {
          const data = params.data;
          if (!data) return '';
          let tooltip = `<strong>${data.name}</strong><br/>`;
          if (cloudData?.dimension_explanations) {
            cloudData.dimension_explanations.forEach((exp, idx) => {
              tooltip += `${exp}: ${(data.value[idx] * 100).toFixed(0)}%<br/>`;
            });
          } else {
            data.value.forEach((v: number, idx: number) => {
              tooltip += `${dimensionNames[idx]?.name || `维度${idx+1}`}: ${(v * 100).toFixed(0)}%<br/>`;
            });
          }
          return tooltip;
        }
      },
      radar: {
        indicator: dimensionNames,
      },
      series: [
        {
          type: 'radar',
          data: agentIds.map((agentId, index) => {
            const cloud = simulationResult.probability_cloud[agentId];
            return {
              value: cloud.mean,
              name: agentNames[index],
              areaStyle: { opacity: 0.2 },
            };
          }),
        },
      ],
    };
  };

  return (
    <div className="gf-cloud-pattern" style={{ minHeight: '100vh', padding: 'clamp(12px, 3vw, 24px)' }}>
      {/* 顶部标题区域 */}
      <div style={{ 
        textAlign: 'center', 
        marginBottom: 'clamp(24px, 5vw, 48px)',
        position: 'relative',
        zIndex: 1,
      }}>
        <div className="gf-bagua-border" style={{ marginBottom: 24 }}>
          <Title level={2} className="gf-title-gold" style={{ 
            margin: 0,
            fontSize: 'clamp(20px, 5vw, 32px)',
            fontWeight: 700,
            letterSpacing: 'clamp(2px, 1vw, 6px)',
          }}>
            推演仿真
          </Title>
        </div>
        <Paragraph style={{ 
          color: '#b8b8d0', 
          fontSize: 16,
          maxWidth: 600,
          margin: '0 auto',
          lineHeight: 1.8,
        }}>
          基于OASIS多智能体社会仿真，输出概率云而非固定结论
        </Paragraph>
        <div className="gf-huiwen-divider" style={{ width: 200, margin: '24px auto' }} />
      </div>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={8}>
          <div className="gf-card" style={{ padding: 'clamp(16px, 3vw, 32px)', height: '100%' }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              marginBottom: 24,
              gap: 12,
            }}>
              <StarOutlined style={{ color: '#d4a853', fontSize: 24 }} />
              <Title level={4} className="gf-title" style={{ margin: 0 }}>
                推演配置
              </Title>
            </div>
            <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
            
            <Form form={form} layout="vertical">
              <Form.Item label="推演场景">
                <Select
                  value={selectedScenario}
                  onChange={setSelectedScenario}
                  style={{ width: '100%' }}
                >
                  {Object.entries(scenarioDescriptions).map(([key, value]) => (
                    <Option key={key} value={key}>
                      {value.name}
                    </Option>
                  ))}
                </Select>
              </Form.Item>

              <Form.Item label={<><CalendarOutlined style={{ marginRight: 8 }} />起始时间</>}>
                <Row gutter={8}>
                  <Col xs={12} sm={12}>
                    <InputNumber
                      min={1900}
                      max={2100}
                      value={startYear}
                      onChange={(v) => setStartYear(v || 2026)}
                      placeholder="年份"
                      style={{ width: '100%' }}
                      addonAfter="年"
                    />
                  </Col>
                  <Col xs={12} sm={12}>
                    <InputNumber
                      min={1}
                      max={12}
                      value={startMonth}
                      onChange={(v) => setStartMonth(v || 1)}
                      placeholder="月份"
                      style={{ width: '100%' }}
                      addonAfter="月"
                    />
                  </Col>
                </Row>
              </Form.Item>

              <Form.Item label="仿真步数（月）">
                <InputNumber
                  min={3}
                  max={24}
                  value={steps}
                  onChange={(v) => setSteps(v || 12)}
                  style={{ width: '100%' }}
                />
              </Form.Item>

              <Form.Item label="采样次数">
                <InputNumber
                  min={10}
                  max={200}
                  value={samples}
                  onChange={(v) => setSamples(v || 50)}
                  style={{ width: '100%' }}
                />
              </Form.Item>

              <Form.Item>
                <Button
                  type="primary"
                  className="gf-btn-primary"
                  icon={<PlayCircleOutlined />}
                  onClick={handleSimulate}
                  loading={isSimulating}
                  block
                  disabled={charts.length === 0 && extraAgents.length === 0}
                >
                  开始推演
                </Button>
              </Form.Item>
            </Form>

            <Divider className="gf-divider" style={{ margin: '24px 0' }} />

            <div>
              <Text strong style={{ color: '#ffffff' }}>已选命盘：</Text>
              {charts.length === 0 ? (
                <Text style={{ color: '#b8b8d0' }}>暂无</Text>
              ) : (
                <Space wrap style={{ marginTop: 8 }}>
                  {charts.map((chart) => (
                    <Tag key={chart.id} className="gf-tag">
                      {chart.name}
                    </Tag>
                  ))}
                </Space>
              )}
            </div>

            <Divider className="gf-divider" style={{ margin: '16px 0' }} />

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                <Text strong style={{ color: '#ffffff' }}>
                  <TeamOutlined style={{ marginRight: 8 }} />额外参与者
                </Text>
                <Button 
                  size="small" 
                  type="dashed" 
                  onClick={addExtraAgent}
                  style={{ borderColor: '#d4a853', color: '#d4a853' }}
                >
                  + 添加
                </Button>
              </div>
              
              {extraAgents.length === 0 ? (
                <Text style={{ color: '#b8b8d0', fontSize: 12 }}>点击"添加"输入更多参与者信息</Text>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {extraAgents.map((agent, index) => (
                    <div key={index} style={{ 
                      padding: '8px', 
                      background: 'rgba(212,168,83,0.05)', 
                      borderRadius: 4,
                      border: '1px solid rgba(212,168,83,0.15)'
                    }}>
                      <Row gutter={4}>
                        <Col xs={8} sm={8}>
                          <Input
                            size="small"
                            placeholder="姓名"
                            value={agent.name}
                            onChange={(e) => updateExtraAgent(index, 'name', e.target.value)}
                          />
                        </Col>
                        <Col xs={8} sm={8}>
                          <Input
                            size="small"
                            placeholder="出生日期"
                            value={agent.birth_date}
                            onChange={(e) => updateExtraAgent(index, 'birth_date', e.target.value)}
                          />
                        </Col>
                        <Col xs={6} sm={6}>
                          <Select
                            size="small"
                            value={agent.gender}
                            onChange={(v) => updateExtraAgent(index, 'gender', v)}
                            style={{ width: '100%' }}
                          >
                            <Option value="male">男</Option>
                            <Option value="female">女</Option>
                          </Select>
                        </Col>
                        <Col xs={2} sm={2}>
                          <Button 
                            size="small" 
                            danger 
                            onClick={() => removeExtraAgent(index)}
                            style={{ padding: '0 4px' }}
                          >
                            X
                          </Button>
                        </Col>
                      </Row>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div style={{ marginTop: 16 }}>
              <Text style={{ color: '#b8b8d0' }}>
                {scenarioDescriptions[selectedScenario].desc}
              </Text>
            </div>
          </div>
        </Col>

        <Col xs={24} lg={16}>
          {isSimulating ? (
            <div className="gf-card" style={{ padding: '32px' }}>
              <div style={{ textAlign: 'center', padding: 40 }}>
                <Spin size="large" />
                <div style={{ marginTop: 16 }}>
                  <Text style={{ color: '#b8b8d0' }}>正在运行推演仿真...</Text>
                </div>
              </div>
            </div>
          ) : simulationResult ? (
            <>
              <div className="gf-card" style={{ padding: '32px', marginBottom: 24 }}>
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  marginBottom: 24,
                  gap: 12,
                }}>
                  <ThunderboltOutlined style={{ color: '#d4a853', fontSize: 24 }} />
                  <Title level={4} className="gf-title" style={{ margin: 0 }}>
                    推演结果
                  </Title>
                </div>
                <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
                
                <Row gutter={[24, 24]}>
                  <Col xs={12} sm={6}>
                    <div className="gf-card" style={{ padding: 'clamp(12px, 2vw, 24px)', textAlign: 'center' }}>
                      <div className="gf-statistic">
                        <div className="gf-statistic-value">{simulationResult.steps}</div>
                        <div className="gf-statistic-label">仿真月数</div>
                      </div>
                    </div>
                  </Col>
                  <Col xs={12} sm={6}>
                    <div className="gf-card" style={{ padding: 'clamp(12px, 2vw, 24px)', textAlign: 'center' }}>
                      <div className="gf-statistic">
                        <div className="gf-statistic-value">{simulationResult.key_decisions.length}</div>
                        <div className="gf-statistic-label">关键决策点</div>
                      </div>
                    </div>
                  </Col>
                  <Col xs={12} sm={6}>
                    <div className="gf-card" style={{ padding: 'clamp(12px, 2vw, 24px)', textAlign: 'center' }}>
                      <div className="gf-statistic">
                        <div className="gf-statistic-value">{Object.keys(simulationResult.probability_cloud).length}</div>
                        <div className="gf-statistic-label">Agent数量</div>
                      </div>
                    </div>
                  </Col>
                  <Col xs={12} sm={6}>
                    <div className="gf-card" style={{ padding: 'clamp(12px, 2vw, 24px)', textAlign: 'center' }}>
                      <div className="gf-statistic">
                        <div className="gf-statistic-value">{simulationResult.risk_analysis?.risk_level || '未知'}</div>
                        <div className="gf-statistic-label">风险等级</div>
                      </div>
                    </div>
                  </Col>
                </Row>
              </div>

              <Card title="风险分析" style={{ marginBottom: 16 }}>
                <Row gutter={[16, 16]}>
                  <Col xs={12} sm={6}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>风险等级</Text>
                        <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>
                          {simulationResult.risk_analysis?.risk_level || '未知'}
                        </div>
                      </div>
                    </Card>
                  </Col>
                  <Col xs={12} sm={6}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>风险指数</Text>
                        <div style={{ fontSize: 18, fontWeight: 'bold', color: '#e85d3a' }}>
                          {simulationResult.risk_analysis?.overall_risk_score
                            ? (simulationResult.risk_analysis.overall_risk_score * 100).toFixed(0) + '%'
                            : 'N/A'}
                        </div>
                      </div>
                    </Card>
                  </Col>
                  <Col xs={12} sm={6}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>波动性</Text>
                        <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>
                          {simulationResult.risk_analysis?.volatility || 0}
                        </div>
                      </div>
                    </Card>
                  </Col>
                  <Col xs={12} sm={6}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>风险因素</Text>
                        <div style={{ fontSize: 14, color: '#b8b8d0' }}>
                          {simulationResult.risk_analysis?.risk_factors?.length || 0}个
                        </div>
                      </div>
                    </Card>
                  </Col>
                </Row>

                {/* 详细风险因素 */}
                {simulationResult.risk_analysis?.risk_factors_detail && simulationResult.risk_analysis.risk_factors_detail.length > 0 && (
                  <>
                    <Divider />
                    <Title level={5}>详细风险因素</Title>
                    <Row gutter={[8, 8]}>
                      {simulationResult.risk_analysis.risk_factors_detail.map((factor, index) => {
                        const levelColorMap: Record<string, string> = {
                          '高': '#ff4d4f',
                          '中': '#faad14',
                          '低': '#d4a853',
                        };
                        const color = levelColorMap[factor.level] || '#d9d9d9';
                        return (
                          <Col xs={24} sm={12} key={index}>
                            <Card size="small" style={{ borderLeft: `4px solid ${color}` }}>
                              <div>
                                <Text strong>{factor.factor}</Text>
                                <Tag color={color} style={{ marginLeft: 8 }}>{factor.level}风险</Tag>
                              </div>
                              <Paragraph style={{ margin: '8px 0 4px', fontSize: 13 }}>
                                {factor.detail}
                              </Paragraph>
                              
                              {/* 古籍引用 */}
                              {factor.classical_reference && (
                                <div style={{ 
                                  background: 'rgba(212,168,83,0.05)', 
                                  padding: '8px 12px', 
                                  borderRadius: 4, 
                                  marginTop: 8,
                                  borderLeft: '3px solid #d4a853',
                                  fontStyle: 'italic'
                                }}>
                                  <Text type="secondary" style={{ fontSize: 12 }}>
                                    📚 {factor.classical_reference}
                                  </Text>
                                </div>
                              )}
                              
                              {/* 化解建议 */}
                              <div style={{ background:'rgba(212,168,83,0.08)', padding: '8px 12px', borderRadius: 4, marginTop: 8 }}>
                                <Text strong style={{ fontSize: 12, color: '#d4a853' }}>💡 化解建议:</Text>
                                <Paragraph style={{ margin: '4px 0 0', fontSize: 13 }}>
                                  {factor.mitigation}
                                </Paragraph>
                              </div>
                              
                              {/* 具体行动步骤 */}
                              {factor.actionable_steps && factor.actionable_steps.length > 0 && (
                                <div style={{ marginTop: 8 }}>
                                  <Text strong style={{ fontSize: 12, color: '#d4a853' }}>🎯 具体行动:</Text>
                                  <ul style={{ margin: '4px 0 0', paddingLeft: 16 }}>
                                    {factor.actionable_steps.map((step, stepIdx) => (
                                      <li key={stepIdx} style={{ fontSize: 12, marginBottom: 2 }}>
                                        <Text>{step}</Text>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}
                            </Card>
                          </Col>
                        );
                      })}
                    </Row>
                  </>
                )}

                {/* 传统风险因素 */}
                {simulationResult.risk_analysis?.risk_factors && simulationResult.risk_analysis.risk_factors.length > 0 && (
                  <>
                    <Divider />
                    <Title level={5}>风险因素</Title>
                    <ul>
                      {simulationResult.risk_analysis.risk_factors.map((factor: string, index: number) => (
                        <li key={index}>
                          <Paragraph>{factor}</Paragraph>
                        </li>
                      ))}
                    </ul>
                  </>
                )}

                {simulationResult.risk_analysis?.risk_advice && (
                  <>
                    <Divider />
                    <Card size="small" style={{ background:'rgba(212,168,83,0.08)', borderColor:'rgba(212,168,83,0.2)' }}>
                      <Text strong style={{ color: '#faad14' }}>⚠️ 风险建议：</Text>
                      <Paragraph style={{ margin: '8px 0 0' }}>
                        {simulationResult.risk_analysis.risk_advice}
                      </Paragraph>
                    </Card>
                  </>
                )}

                {simulationResult.risk_analysis?.classical_risk_analysis && (
                  <>
                    <Divider />
                    <div style={{ 
                      padding: '12px 16px', 
                      background: 'rgba(212,168,83,0.05)', 
                      borderRadius: 8,
                      borderLeft: '3px solid #d4a853',
                      fontStyle: 'italic'
                    }}>
                      <Text strong style={{ color: '#d4a853', fontSize: 14 }}>📚 古籍风险分析</Text>
                      <Paragraph style={{ margin: '8px 0 0', fontSize: 13, color: '#b8b8d0' }}>
                        {simulationResult.risk_analysis.classical_risk_analysis}
                      </Paragraph>
                    </div>
                  </>
                )}

                {simulationResult.risk_analysis?.mitigation_suggestions && simulationResult.risk_analysis.mitigation_suggestions.length > 0 && (
                  <>
                    <Title level={5} style={{ marginTop: 16 }}>风险缓解建议</Title>
                    <ul>
                      {simulationResult.risk_analysis.mitigation_suggestions.map((suggestion: string, index: number) => (
                        <li key={index}>
                          <Paragraph>{suggestion}</Paragraph>
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </Card>

              <Card title="运势热力图" style={{ marginBottom: 16 }}>
                <ReactECharts option={getHeatmapOption()} style={{ height: 300 }} />
                <div style={{ 
                  marginTop: 16, 
                  padding: '12px 16px', 
                  background: 'rgba(212,168,83,0.05)', 
                  borderRadius: 8,
                  borderLeft: '3px solid #d4a853'
                }}>
                  <Text strong style={{ color: '#d4a853', fontSize: 14 }}>📊 热力图解读</Text>
                  <Paragraph style={{ margin: '8px 0 0', fontSize: 13, color: '#b8b8d0' }}>
                    热力图展示未来12个月的运势变化趋势。颜色越深红，运势越旺盛；颜色越深蓝，运势越低迷。
                    每个月的运势受流年干支、十神旺衰、五行力量等因素影响。
                  </Paragraph>
                </div>
              </Card>

              <Card title="概率云分布" style={{ marginBottom: 16 }}>
                <ReactECharts option={getCloudOption()} style={{ height: 300 }} />
                <div style={{ 
                  marginTop: 16, 
                  padding: '12px 16px', 
                  background: 'rgba(212,168,83,0.05)', 
                  borderRadius: 8,
                  borderLeft: '3px solid #d4a853'
                }}>
                  <Text strong style={{ color: '#d4a853', fontSize: 14 }}>☁️ 概率云解读</Text>
                  <Paragraph style={{ margin: '8px 0 0', fontSize: 13, color: '#b8b8d0' }}>
                    概率云展示各维度运势的综合评估。数值越高，该维度运势越佳。
                    {simulationResult.probability_cloud && Object.values(simulationResult.probability_cloud)[0]?.classical_basis && (
                      <>
                        <br/>
                        <Text style={{ color: '#d4a853', fontSize: 12 }}>
                          📚 {Object.values(simulationResult.probability_cloud)[0].classical_basis}
                        </Text>
                      </>
                    )}
                  </Paragraph>
                </div>
              </Card>

              <Card title="轨迹预测" style={{ marginBottom: 16 }}>
                <Row gutter={[16, 16]}>
                  <Col xs={24} sm={8}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>趋势</Text>
                        <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>
                          {simulationResult.trajectory_prediction?.trend === 'upward' ? '上升' : 
                           simulationResult.trajectory_prediction?.trend === 'downward' ? '下降' : '平稳'}
                        </div>
                      </div>
                    </Card>
                  </Col>
                  <Col xs={24} sm={8}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>斜率</Text>
                        <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>
                          {simulationResult.trajectory_prediction?.slope || 0}
                        </div>
                      </div>
                    </Card>
                  </Col>
                  <Col xs={24} sm={8}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>预测点数</Text>
                        <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>
                          {simulationResult.trajectory_prediction?.predictions?.length || 0}
                        </div>
                      </div>
                    </Card>
                  </Col>
                </Row>
                
                {/* 趋势解读 */}
                {simulationResult.trajectory_prediction?.trend_explanation && (
                  <div style={{ 
                    marginTop: 16, 
                    padding: '12px 16px', 
                    background: 'rgba(212,168,83,0.05)', 
                    borderRadius: 8,
                    borderLeft: '3px solid #d4a853'
                  }}>
                    <Text strong style={{ color: '#d4a853', fontSize: 14 }}>📈 趋势解读</Text>
                    <Paragraph style={{ margin: '8px 0 0', fontSize: 13, color: '#b8b8d0' }}>
                      {simulationResult.trajectory_prediction.trend_explanation}
                    </Paragraph>
                    {simulationResult.trajectory_prediction.classical_trajectory_basis && (
                      <div style={{ marginTop: 8, fontStyle: 'italic' }}>
                        <Text style={{ color: '#d4a853', fontSize: 12 }}>
                          📚 {simulationResult.trajectory_prediction.classical_trajectory_basis}
                        </Text>
                      </div>
                    )}
                  </div>
                )}
                
                {simulationResult.trajectory_prediction?.predictions && (
                  <>
                    <Divider />
                    <Title level={5}>未来预测</Title>
                    <Row gutter={[8, 8]}>
                      {simulationResult.trajectory_prediction.predictions.map((prediction: any, index: number) => (
                        <Col xs={12} sm={8} key={index}>
                          <Card size="small" style={{ textAlign: 'center' }}>
                            <Text strong>{prediction.year}年{prediction.month}月</Text>
                            <div style={{ fontSize: 16, fontWeight: 'bold', color: '#d4a853' }}>
                              {prediction.value.toFixed(2)}
                            </div>
                            <div>
                              <Text type="secondary">置信度: {(prediction.confidence * 100).toFixed(0)}%</Text>
                            </div>
                            {prediction.explanation && (
                              <div style={{ marginTop: 4, fontSize: 12, color: '#b8b8d0' }}>
                                {prediction.explanation}
                              </div>
                            )}
                            {prediction.classical_basis && (
                              <div style={{ marginTop: 4, fontSize: 11, color: '#d4a853', fontStyle: 'italic' }}>
                                📚 {prediction.classical_basis}
                              </div>
                            )}
                          </Card>
                        </Col>
                      ))}
                    </Row>
                  </>
                )}
              </Card>

              <Card title="推演总结">
                <div style={{ whiteSpace: 'pre-wrap' }}>
                  {simulationResult.summary}
                </div>
              </Card>

              <Card title="关键决策点" style={{ marginTop: 16 }}>
                {simulationResult.key_decisions.length === 0 ? (
                  <Text type="secondary">未发现关键决策点</Text>
                ) : (
                  <Timeline
                    items={simulationResult.key_decisions.map((decision) => ({
                      color: decision.type === 'peak' ? 'green' : 'red',
                      children: (
                        <div>
                          <Text strong>{decision.description}</Text>
                          <div>
                            <Tag color={decision.type === 'peak' ? 'green' : 'red'}>
                              {decision.type === 'peak' ? '高峰' : '低谷'}
                            </Tag>
                            <Text type="secondary">{decision.year}年{decision.month}月</Text>
                          </div>
                          {decision.classical_basis && (
                            <div style={{ 
                              marginTop: 8, 
                              padding: '8px 12px', 
                              background: 'rgba(212,168,83,0.05)', 
                              borderRadius: 4,
                              fontStyle: 'italic',
                              fontSize: 12
                            }}>
                              <Text style={{ color: '#d4a853' }}>
                                📚 {decision.classical_basis}
                              </Text>
                            </div>
                          )}
                          {decision.actionable_advice && (
                            <div style={{ 
                              marginTop: 8, 
                              padding: '8px 12px', 
                              background: 'rgba(212,168,83,0.08)', 
                              borderRadius: 4,
                              fontSize: 12
                            }}>
                              <Text strong style={{ color: '#d4a853' }}>🎯 行动建议: </Text>
                              <Text style={{ color: '#b8b8d0' }}>{decision.actionable_advice}</Text>
                            </div>
                          )}
                        </div>
                      ),
                    }))}
                  />
                )}
              </Card>

              <Card title="季节效应" style={{ marginTop: 16 }}>
                {simulationResult.seasonal_effects ? (
                  <Row gutter={[16, 16]}>
                    {Object.entries(simulationResult.seasonal_effects).map(([agentId, effects]: [string, any]) => (
                      <Col span={24} key={agentId}>
                        <Card size="small">
                          <Title level={5}>{agentId}</Title>
                          <Row gutter={[8, 8]}>
                            <Col xs={12} sm={6}>
                              <Card size="small" style={{ textAlign: 'center' }}>
                                <Text strong>春</Text>
                                <div style={{ fontSize: 16, fontWeight: 'bold', color: '#d4a853' }}>
                                  {effects.spring?.toFixed(2) || 'N/A'}
                                </div>
                              </Card>
                            </Col>
                            <Col xs={12} sm={6}>
                              <Card size="small" style={{ textAlign: 'center' }}>
                                <Text strong>夏</Text>
                                <div style={{ fontSize: 16, fontWeight: 'bold', color: '#ff4d4f' }}>
                                  {effects.summer?.toFixed(2) || 'N/A'}
                                </div>
                              </Card>
                            </Col>
                            <Col xs={12} sm={6}>
                              <Card size="small" style={{ textAlign: 'center' }}>
                                <Text strong>秋</Text>
                                <div style={{ fontSize: 16, fontWeight: 'bold', color: '#fa8c16' }}>
                                  {effects.autumn?.toFixed(2) || 'N/A'}
                                </div>
                              </Card>
                            </Col>
                            <Col xs={12} sm={6}>
                              <Card size="small" style={{ textAlign: 'center' }}>
                                <Text strong>冬</Text>
                                <div style={{ fontSize: 16, fontWeight: 'bold', color: '#d4a853' }}>
                                  {effects.winter?.toFixed(2) || 'N/A'}
                                </div>
                              </Card>
                            </Col>
                          </Row>
                          {effects.explanation && (
                            <div style={{ 
                              marginTop: 12, 
                              padding: '8px 12px', 
                              background: 'rgba(212,168,83,0.05)', 
                              borderRadius: 4,
                              fontSize: 13
                            }}>
                              <Text style={{ color: '#b8b8d0' }}>
                                {effects.explanation}
                              </Text>
                            </div>
                          )}
                          {effects.classical_basis && (
                            <div style={{ 
                              marginTop: 8, 
                              padding: '8px 12px', 
                              background: 'rgba(212,168,83,0.05)', 
                              borderRadius: 4,
                              fontStyle: 'italic',
                              fontSize: 12
                            }}>
                              <Text style={{ color: '#d4a853' }}>
                                📚 {effects.classical_basis}
                              </Text>
                            </div>
                          )}
                        </Card>
                      </Col>
                    ))}
                  </Row>
                ) : (
                  <Text type="secondary">暂无季节效应数据</Text>
                )}
              </Card>

              <Card title="专业建议" style={{ marginTop: 16 }}>
                {simulationResult.recommendations && simulationResult.recommendations.length > 0 ? (
                  <ul>
                    {simulationResult.recommendations.map((recommendation: string, index: number) => (
                      <li key={index} style={{ marginBottom: 8 }}>
                        <Paragraph style={{ margin: 0 }}>{recommendation}</Paragraph>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <Text type="secondary">暂无专业建议</Text>
                )}
              </Card>

              {/* 古籍引用 */}
              {simulationResult.classical_references && simulationResult.classical_references.length > 0 && (
                <Card title="古籍引用" style={{ marginTop: 16 }}>
                  <div style={{ 
                    background: 'rgba(212,168,83,0.05)', 
                    padding: '16px', 
                    borderRadius: 8,
                    borderLeft: '4px solid #d4a853'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: 12 }}>
                      <BookOutlined style={{ color: '#d4a853', marginRight: 8 }} />
                      <Text strong style={{ color: '#d4a853', fontSize: 16 }}>古籍参考</Text>
                    </div>
                    <Paragraph style={{ margin: '0 0 16px', color: '#b8b8d0', fontSize: 13 }}>
                      以下古籍文献为本次推演提供理论依据，帮助您理解分析结论的来源。
                    </Paragraph>
                    
                    {simulationResult.classical_references.map((ref, index) => (
                      <div key={index} style={{ 
                        marginBottom: 16, 
                        padding: '12px 16px', 
                        background: 'rgba(0,0,0,0.2)', 
                        borderRadius: 6,
                        borderLeft: '3px solid rgba(212,168,83,0.5)'
                      }}>
                        <div style={{ marginBottom: 8 }}>
                          <Text strong style={{ color: '#d4a853', fontSize: 14 }}>
                            "{ref.text}"
                          </Text>
                          <Text style={{ color: '#8888a8', fontSize: 12, marginLeft: 8 }}>
                            —— {ref.source}
                          </Text>
                        </div>
                        <div style={{ marginBottom: 4 }}>
                          <Text style={{ color: '#b8b8d0', fontSize: 13 }}>
                            <Text strong style={{ color: '#d4a853' }}>释义：</Text>
                            {ref.explanation}
                          </Text>
                        </div>
                        <div>
                          <Text style={{ color: '#b8b8d0', fontSize: 13 }}>
                            <Text strong style={{ color: '#d4a853' }}>关联：</Text>
                            {ref.relevance}
                          </Text>
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              )}

              {/* 场景分析 */}
              {simulationResult.scenario_analysis && (
                <Card title="场景分析" style={{ marginTop: 16 }}>
                  <div style={{ 
                    background: 'rgba(212,168,83,0.05)', 
                    padding: '16px', 
                    borderRadius: 8,
                    borderLeft: '4px solid #d4a853'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: 12 }}>
                      <AimOutlined style={{ color: '#d4a853', marginRight: 8 }} />
                      <Text strong style={{ color: '#d4a853', fontSize: 16 }}>
                        {simulationResult.scenario_analysis.scenario_name}
                      </Text>
                    </div>
                    <Paragraph style={{ margin: '0 0 16px', color: '#b8b8d0', fontSize: 13 }}>
                      {simulationResult.scenario_analysis.scenario_description}
                    </Paragraph>
                    
                    <Row gutter={[16, 16]}>
                      <Col xs={24} sm={12}>
                        <div style={{ padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: 6 }}>
                          <Text strong style={{ color: '#d4a853', fontSize: 14 }}>
                            <StarOutlined style={{ marginRight: 8 }} />
                            关键因素
                          </Text>
                          <ul style={{ margin: '8px 0 0', paddingLeft: 16 }}>
                            {simulationResult.scenario_analysis.key_factors.map((factor, idx) => (
                              <li key={idx} style={{ marginBottom: 4, fontSize: 13, color: '#b8b8d0' }}>
                                {factor}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </Col>
                      <Col xs={24} sm={12}>
                        <div style={{ padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: 6 }}>
                          <Text strong style={{ color: '#d4a853', fontSize: 14 }}>
                            <BulbOutlined style={{ marginRight: 8 }} />
                            机遇
                          </Text>
                          <ul style={{ margin: '8px 0 0', paddingLeft: 16 }}>
                            {simulationResult.scenario_analysis.opportunities.map((opp, idx) => (
                              <li key={idx} style={{ marginBottom: 4, fontSize: 13, color: '#95de64' }}>
                                {opp}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </Col>
                    </Row>
                    
                    <div style={{ marginTop: 16, padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: 6 }}>
                      <Text strong style={{ color: '#faad14', fontSize: 14 }}>
                        ⚠️ 挑战
                      </Text>
                      <ul style={{ margin: '8px 0 0', paddingLeft: 16 }}>
                        {simulationResult.scenario_analysis.challenges.map((challenge, idx) => (
                          <li key={idx} style={{ marginBottom: 4, fontSize: 13, color: '#ff7875' }}>
                            {challenge}
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div style={{ marginTop: 16, padding: '12px', background: 'rgba(0,0,0,0.2)', borderRadius: 6 }}>
                      <Text strong style={{ color: '#d4a853', fontSize: 14 }}>
                        <CheckCircleOutlined style={{ marginRight: 8 }} />
                        行动指南
                      </Text>
                      <ul style={{ margin: '8px 0 0', paddingLeft: 16 }}>
                        {simulationResult.scenario_analysis.actionable_guidance.map((guidance, idx) => (
                          <li key={idx} style={{ marginBottom: 8, fontSize: 13, color: '#b8b8d0' }}>
                            {guidance}
                          </li>
                        ))}
                      </ul>
                    </div>
                    
                    <div style={{ 
                      marginTop: 16, 
                      padding: '12px 16px', 
                      background: 'rgba(212,168,83,0.1)', 
                      borderRadius: 6,
                      fontStyle: 'italic'
                    }}>
                      <Text style={{ color: '#d4a853', fontSize: 12 }}>
                        📚 {simulationResult.scenario_analysis.classical_basis}
                      </Text>
                    </div>
                  </div>
                </Card>
              )}

              {/* 吉凶时段分析 */}
              {simulationResult.fortune_periods && (
                <Card title="吉凶时段分析" style={{ marginTop: 16 }}>
                  <Row gutter={[16, 16]}>
                    <Col xs={24} sm={12}>
                      <Card size="small" style={{ background:'rgba(212,168,83,0.08)', borderColor:'rgba(212,168,83,0.2)' }}>
                        <div style={{ textAlign: 'center' }}>
                          <Text strong style={{ color: '#d4a853' }}>最佳月份</Text>
                          <div style={{ fontSize: 20, fontWeight: 'bold', color: '#d4a853', marginTop: 8 }}>
                            {simulationResult.fortune_periods.peak_month.year}年{simulationResult.fortune_periods.peak_month.month}月
                          </div>
                          <div>
                            <Tag color="green">{simulationResult.fortune_periods.peak_month.level}</Tag>
                          </div>
                          <div style={{ marginTop: 4 }}>
                            <Text type="secondary">
                              运势指数: {simulationResult.fortune_periods.peak_month.score.toFixed(3)}
                            </Text>
                          </div>
                        </div>
                      </Card>
                    </Col>
                    <Col xs={24} sm={12}>
                      <Card size="small" style={{ background: '#fff2e8', borderColor: '#ffbb96' }}>
                        <div style={{ textAlign: 'center' }}>
                          <Text strong style={{ color: '#e85d3a' }}>需注意月份</Text>
                          <div style={{ fontSize: 20, fontWeight: 'bold', color: '#e85d3a', marginTop: 8 }}>
                            {simulationResult.fortune_periods.low_month.year}年{simulationResult.fortune_periods.low_month.month}月
                          </div>
                          <div>
                            <Tag color="red">{simulationResult.fortune_periods.low_month.level}</Tag>
                          </div>
                          <div style={{ marginTop: 4 }}>
                            <Text type="secondary">
                              运势指数: {simulationResult.fortune_periods.low_month.score.toFixed(3)}
                            </Text>
                          </div>
                        </div>
                      </Card>
                    </Col>
                  </Row>

                  <Divider />

                  <Title level={5}>月度运势趋势</Title>
                  <div style={{ overflowX: 'auto' }}>
                    <Row gutter={[4, 4]} style={{ minWidth: 600 }}>
                      {simulationResult.fortune_periods.monthly_fortune.map((month, index) => {
                        const colorMap: Record<string, string> = {
                          'high': '#95de64',
                          'medium': '#d4a853',
                          'low': '#ff7875',
                        };
                        const bgColor = colorMap[month.level] || '#d9d9d9';
                        return (
                          <Col xs={4} sm={2} key={index}>
                            <div
                              style={{
                                textAlign: 'center',
                                padding: '8px 4px',
                                background: bgColor + '30',
                                borderRadius: 4,
                                border: `1px solid ${bgColor}`,
                              }}
                            >
                              <div style={{ fontSize: 11, fontWeight: 'bold' }}>{month.year}年</div>
                              <div style={{ fontSize: 12, fontWeight: 'bold' }}>{month.month}月</div>
                              <div style={{ fontSize: 14, fontWeight: 'bold', color: bgColor }}>
                                {month.score}
                              </div>
                              <Tag color={bgColor} style={{ fontSize: 10, marginTop: 2 }}>
                                {month.level}
                              </Tag>
                              {month.explanation && (
                                <div style={{ fontSize: 9, marginTop: 4, color: '#b8b8d0' }}>
                                  {month.explanation}
                                </div>
                              )}
                            </div>
                          </Col>
                        );
                      })}
                    </Row>
                  </div>

                  <Divider />

                  <Paragraph>
                    <Text strong>分析总结：</Text>
                    {simulationResult.fortune_periods.analysis}
                  </Paragraph>

                  {simulationResult.fortune_periods.classical_analysis && (
                    <div style={{ 
                      marginTop: 8, 
                      padding: '12px 16px', 
                      background: 'rgba(212,168,83,0.05)', 
                      borderRadius: 8,
                      borderLeft: '3px solid #d4a853',
                      fontStyle: 'italic'
                    }}>
                      <Text style={{ color: '#d4a853', fontSize: 12 }}>
                        📚 {simulationResult.fortune_periods.classical_analysis}
                      </Text>
                    </div>
                  )}

                  {simulationResult.fortune_periods.auspicious_months.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      <Text strong>吉月：</Text>
                      {simulationResult.fortune_periods.auspicious_months.map((month, idx) => (
                        <Tag key={idx} color="green" style={{ margin: '2px' }}>{month}</Tag>
                      ))}
                    </div>
                  )}

                  {simulationResult.fortune_periods.inauspicious_months.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      <Text strong>凶月：</Text>
                      {simulationResult.fortune_periods.inauspicious_months.map((month, idx) => (
                        <Tag key={idx} color="red" style={{ margin: '2px' }}>{month}</Tag>
                      ))}
                    </div>
                  )}
                </Card>
              )}

              {/* 规则应用详情 */}
              {simulationResult.applied_rules && simulationResult.applied_rules.length > 0 && (
                <Card title="规则应用详情" style={{ marginTop: 16 }}>
                  <Row gutter={[8, 8]}>
                    {simulationResult.applied_rules.map((rule, index) => (
                      <Col xs={12} sm={8} key={index}>
                        <Card size="small" style={{ height: '100%' }}>
                          <div>
                            <Text strong>{rule.description}</Text>
                          </div>
                          <div style={{ marginTop: 4 }}>
                            <Tag color="blue">优先级: {rule.priority}</Tag>
                            {rule.interaction_boost !== 1.0 && (
                              <Tag color={rule.interaction_boost > 1 ? 'green' : 'red'}>
                                交互加成: {((rule.interaction_boost - 1) * 100).toFixed(0)}%
                              </Tag>
                            )}
                          </div>
                          {Object.keys(rule.changes).length > 0 && (
                            <div style={{ marginTop: 8 }}>
                              <Text type="secondary" style={{ fontSize: 12 }}>状态变化：</Text>
                              {Object.entries(rule.changes).map(([key, value]) => (
                                <div key={key} style={{ fontSize: 12 }}>
                                  <Text type="secondary">{key}: </Text>
                                  <Text style={{ color: value > 0 ? '#d4a853' : '#ff4d4f' }}>
                                    {value > 0 ? '+' : ''}{(value * 100).toFixed(1)}%
                                  </Text>
                                </div>
                              ))}
                            </div>
                          )}
                          {rule.classical_basis && (
                            <div style={{ 
                              marginTop: 8, 
                              padding: '8px 12px', 
                              background: 'rgba(212,168,83,0.05)', 
                              borderRadius: 4,
                              fontStyle: 'italic',
                              fontSize: 11
                            }}>
                              <Text style={{ color: '#d4a853' }}>
                                📚 {rule.classical_basis}
                              </Text>
                            </div>
                          )}
                        </Card>
                      </Col>
                    ))}
                  </Row>
                </Card>
              )}

              {/* 真实计算过程 */}
              {simulationResult.real_calculation_process && (
                <Card title={<><CalculatorOutlined style={{ marginRight: 8 }} />真实计算过程</>} style={{ marginTop: 16 }}>
                  {/* 八字分析 */}
                  {simulationResult.real_calculation_process.bazi_analysis && (
                    <>
                      <Title level={5} style={{ color: '#d4a853' }}>八字排盘分析</Title>
                      <Timeline
                        items={simulationResult.real_calculation_process.bazi_analysis.map((step) => ({
                          color: 'blue',
                          children: (
                            <div>
                              <Text strong style={{ color: '#d4a853' }}>{step.step}</Text>
                              <div style={{ marginTop: 4 }}>
                                <Text style={{ color: '#b8b8d0', fontSize: 13 }}>{step.description}</Text>
                              </div>
                              <div style={{ 
                                marginTop: 8, 
                                padding: '8px 12px', 
                                background: 'rgba(0,0,0,0.2)', 
                                borderRadius: 4,
                                fontFamily: 'monospace'
                              }}>
                                <Text style={{ color: '#95de64', fontSize: 12 }}>{step.calculation}</Text>
                              </div>
                              <div style={{ marginTop: 4 }}>
                                <Tag color="blue">{step.result}</Tag>
                              </div>
                              {step.classical_basis && (
                                <div style={{ 
                                  marginTop: 8, 
                                  padding: '6px 10px', 
                                  background: 'rgba(212,168,83,0.05)', 
                                  borderRadius: 4,
                                  fontStyle: 'italic',
                                  fontSize: 11
                                }}>
                                  <Text style={{ color: '#d4a853' }}>📚 {step.classical_basis}</Text>
                                </div>
                              )}
                            </div>
                          ),
                        }))}
                      />
                      <Divider />
                    </>
                  )}

                  {/* 五行分析 */}
                  {simulationResult.real_calculation_process.wuxing_analysis && (
                    <>
                      <Title level={5} style={{ color: '#d4a853' }}>五行力量分析</Title>
                      <Row gutter={[8, 8]}>
                        {simulationResult.real_calculation_process.wuxing_analysis.map((wuxing, index) => {
                          const elementColors: Record<string, string> = {
                            '金': '#d4a853',
                            '木': '#95de64',
                            '水': '#597ef7',
                            '火': '#ff4d4f',
                            '土': '#d9d9d9',
                          };
                          const color = elementColors[wuxing.element] || '#d4a853';
                          const count = simulationResult.real_calculation_process!.wuxing_analysis.length;
                          // 在移动设备上每行最多2个，桌面端根据数量自适应
                          const xsSpan = count <= 2 ? 12 : Math.floor(24 / Math.min(count, 2));
                          const smSpan = Math.floor(24 / Math.min(count, 4));
                          return (
                            <Col xs={xsSpan} sm={smSpan} key={index}>
                              <Card size="small" style={{ textAlign: 'center', borderColor: color }}>
                                <div style={{ fontSize: 24, fontWeight: 'bold', color }}>{wuxing.element}</div>
                                <div style={{ fontSize: 18, fontWeight: 'bold', color, marginTop: 4 }}>
                                  {(wuxing.strength * 100).toFixed(0)}%
                                </div>
                                <div style={{ fontSize: 11, marginTop: 4, color: '#b8b8d0' }}>
                                  {wuxing.calculation}
                                </div>
                                <Divider style={{ margin: '8px 0' }} />
                                <div style={{ fontSize: 11, color: '#b8b8d0' }}>
                                  {wuxing.impact}
                                </div>
                              </Card>
                            </Col>
                          );
                        })}
                      </Row>
                      <Divider />
                    </>
                  )}

                  {/* 大运分析 */}
                  {simulationResult.real_calculation_process.dayun_analysis && (
                    <>
                      <Title level={5} style={{ color: '#d4a853' }}>大运分析</Title>
                      <Row gutter={[8, 8]}>
                        {simulationResult.real_calculation_process.dayun_analysis.map((dayun, index) => (
                          <Col xs={12} sm={6} key={index}>
                            <Card size="small" style={{ height: '100%' }}>
                              <Text strong style={{ color: '#d4a853' }}>{dayun.period}</Text>
                              <div style={{ fontSize: 12, color: '#b8b8d0', marginTop: 4 }}>
                                {dayun.start_year}-{dayun.end_year}
                              </div>
                              <div style={{ 
                                marginTop: 8, 
                                padding: '6px', 
                                background: 'rgba(0,0,0,0.2)', 
                                borderRadius: 4,
                                fontFamily: 'monospace',
                                fontSize: 11
                              }}>
                                {dayun.calculation}
                              </div>
                              <div style={{ marginTop: 8, fontSize: 12 }}>
                                {dayun.impact}
                              </div>
                            </Card>
                          </Col>
                        ))}
                      </Row>
                      <Divider />
                    </>
                  )}

                  {/* 流年分析 */}
                  {simulationResult.real_calculation_process.liunian_analysis && (
                    <>
                      <Title level={5} style={{ color: '#d4a853' }}>流年分析</Title>
                      <Row gutter={[8, 8]}>
                        {simulationResult.real_calculation_process.liunian_analysis.map((liunian, index) => (
                          <Col xs={12} sm={8} key={index}>
                            <Card size="small">
                              <Text strong style={{ color: '#d4a853', fontSize: 16 }}>{liunian.year}</Text>
                              <Tag color="blue" style={{ marginLeft: 8 }}>{liunian.gan_zhi}</Tag>
                              <div style={{ 
                                marginTop: 8, 
                                padding: '6px', 
                                background: 'rgba(0,0,0,0.2)', 
                                borderRadius: 4,
                                fontFamily: 'monospace',
                                fontSize: 11
                              }}>
                                {liunian.calculation}
                              </div>
                              <div style={{ marginTop: 8, fontSize: 12, color: '#b8b8d0' }}>
                                {liunian.impact}
                              </div>
                            </Card>
                          </Col>
                        ))}
                      </Row>
                      <Divider />
                    </>
                  )}

                  {/* 互动分析 */}
                  {simulationResult.real_calculation_process.interaction_analysis && (
                    <>
                      <Title level={5} style={{ color: '#d4a853' }}>互动分析</Title>
                      {simulationResult.real_calculation_process.interaction_analysis.map((interaction, index) => (
                        <Card size="small" key={index} style={{ marginBottom: 8 }}>
                          <Row gutter={16} align="middle">
                            <Col xs={24} sm={4}>
                              <Text strong style={{ color: '#d4a853', display: 'block', marginBottom: 8 }}>
                                {interaction.agent1_id} ↔ {interaction.agent2_id}
                              </Text>
                            </Col>
                            <Col xs={12} sm={4}>
                              <div style={{ textAlign: 'center' }}>
                                <div style={{ fontSize: 24, fontWeight: 'bold', color: '#d4a853' }}>
                                  {interaction.compatibility}
                                </div>
                                <Text style={{ fontSize: 12, color: '#b8b8d0' }}>契合度</Text>
                              </div>
                            </Col>
                            <Col xs={12} sm={16}>
                              <div style={{ 
                                padding: '6px', 
                                background: 'rgba(0,0,0,0.2)', 
                                borderRadius: 4,
                                fontFamily: 'monospace',
                                fontSize: 11
                              }}>
                                {interaction.calculation}
                              </div>
                              <div style={{ marginTop: 4 }}>
                                {interaction.factors.map((factor, idx) => (
                                  <Tag key={idx} color="blue" style={{ margin: '2px' }}>{factor}</Tag>
                                ))}
                              </div>
                            </Col>
                          </Row>
                        </Card>
                      ))}
                    </>
                  )}
                </Card>
              )}

              {/* 推理过程日志 */}
              {simulationResult.reasoning_report && (
                <Card title="推理过程日志" style={{ marginTop: 16 }}>
                  <div
                    style={{
                      background: '#1e1e1e',
                      color: '#d4d4d4',
                      padding: 16,
                      borderRadius: 8,
                      fontFamily: 'Consolas, Monaco, monospace',
                      fontSize: 13,
                      maxHeight: 400,
                      overflowY: 'auto',
                      whiteSpace: 'pre-wrap',
                      lineHeight: 1.6,
                    }}
                  >
                    {simulationResult.reasoning_report.split('\n').map((line, index) => {
                      let color = '#d4d4d4';
                      if (line.startsWith('✓')) color = '#6a9955';
                      else if (line.startsWith('✗')) color = '#f44747';
                      else if (line.startsWith('⚠')) color = '#cca700';
                      else if (line.startsWith('  ↕')) color = '#569cd6';
                      else if (line.startsWith('=')) color = '#4ec9b0';
                      else if (line.startsWith('📊')) color = '#4ec9b0';
                      else if (line.startsWith('🎯')) color = '#c586c0';
                      return (
                        <div key={index} style={{ color }}>
                          {line}
                        </div>
                      );
                    })}
                  </div>
                </Card>
              )}

              <Card title="推演计算过程" style={{ marginTop: 16 }}>
                {simulationResult.calculation_process ? (
                  <CalculationProcess data={simulationResult.calculation_process} title="OASIS推演计算过程" />
                ) : (
                  <Text type="secondary">暂无计算过程数据</Text>
                )}
              </Card>
            </>
          ) : (
            <Card>
              <div style={{ textAlign: 'center', padding: 40 }}>
                <ExperimentOutlined style={{ fontSize: 48, color: '#d9d9d9' }} />
                <div style={{ marginTop: 16 }}>
                  <Text type="secondary">请先录入命盘，然后选择场景开始推演</Text>
                </div>
              </div>
            </Card>
          )}
        </Col>
      </Row>
    </div>
  );
}

export default Simulation;
