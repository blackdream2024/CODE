import { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Select,
  Button,
  Tag,
  Space,
  Divider,
  message,
  Empty,
  Tabs,
  InputNumber,
} from 'antd';
import { TeamOutlined, StarOutlined, HeartOutlined, PlusOutlined, DeleteOutlined } from '@ant-design/icons';
import { useChartStore } from '../stores/chartStore';
import { relationApi } from '../services/api';
import RelationNetwork from '../components/RelationNetwork';
import CalculationProcess from '../components/CalculationProcess';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

function RelationAnalysis() {
  const { charts } = useChartStore();
  // 支持多人分析
  const [selectedChartIds, setSelectedChartIds] = useState<string[]>([]);
  const [relationType, setRelationType] = useState('spouse');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  // 时间范围
  const [startYear, setStartYear] = useState(2026);
  const [startMonth, setStartMonth] = useState(1);

  const addChartSelect = () => {
    if (selectedChartIds.length < 6) {
      setSelectedChartIds([...selectedChartIds, '']);
    }
  };

  const removeChartSelect = (index: number) => {
    setSelectedChartIds(selectedChartIds.filter((_, i) => i !== index));
  };

  const updateChartSelect = (index: number, value: string) => {
    const updated = [...selectedChartIds];
    updated[index] = value;
    setSelectedChartIds(updated);
  };

  const handleAnalyze = async () => {
    const validIds = selectedChartIds.filter(id => id !== '');
    if (validIds.length < 2) {
      message.warning('请至少选择两个命盘');
      return;
    }

    // 检查是否有重复
    const uniqueIds = new Set(validIds);
    if (uniqueIds.size !== validIds.length) {
      message.warning('请选择不同的命盘');
      return;
    }

    const selectedCharts = validIds.map(id => charts.find(c => c.id === id)).filter(Boolean);
    if (selectedCharts.length !== validIds.length) {
      message.error('命盘数据不存在');
      return;
    }

    setLoading(true);
    try {
      // 对于多人分析，计算所有两两组合
      const pairs: Array<{chart1: any; chart2: any}> = [];
      for (let i = 0; i < selectedCharts.length; i++) {
        for (let j = i + 1; j < selectedCharts.length; j++) {
          pairs.push({
            chart1: selectedCharts[i]!.bazi_data,
            chart2: selectedCharts[j]!.bazi_data,
          });
        }
      }

      // 调用分析API（取第一对作为主要结果）
      const response = await relationApi.analyze({
        chart1: pairs[0].chart1,
        chart2: pairs[0].chart2,
        relationship_type: relationType,
      });

      // 将多人信息附加到结果中
      setResult({
        ...response.data,
        multi_person: selectedCharts.length > 2,
        agents: selectedCharts.map(c => ({ id: c!.id, name: c!.name })),
        pairs_count: pairs.length,
      });
      message.success(`分析完成！共分析${pairs.length}对关系`);
    } catch (error) {
      console.error('关系分析失败:', error);
      message.error('分析失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  const relationTypes = [
    { value: 'spouse', label: '配偶关系', desc: '分析两人婚姻配对情况' },
    { value: 'partner', label: '合作伙伴', desc: '分析事业合作契合度' },
    { value: 'friend', label: '朋友关系', desc: '分析友情相处模式' },
    { value: 'colleague', label: '同事关系', desc: '分析工作配合度' },
  ];

  // 根据关系类型获取古籍引用和分析方法
  const getRelationClassicalTexts = (type: string) => {
    const texts: Record<string, Array<{source: string; title: string; content: string}>> = {
      spouse: [
        { source: '《渊海子平》', title: '论合婚', content: '合婚之法，先看男女双方日主五行是否相生相合。相生者，情投意合；相克者，需有通关之神。日主相合者，如甲己合、乙庚合、丙辛合、丁壬合、戊癸合，主夫妻恩爱，白头偕老。' },
        { source: '《三命通会》', title: '论婚姻', content: '合婚之道，贵在五行互补。男命火旺，宜配水旺之女；女命木旺，宜配金旺之男。阴阳相济，刚柔并济，方为美满姻缘。若双方日主相冲相克，需看大运流年是否有化解之机。' },
        { source: '《滴天髓》', title: '论妻财', content: '何知其人偕老，妻星有理会。男命以财星为妻，女命以官星为夫。财官有力，配合得当，主夫妻和睦，白头偕老。若财官无力，或被冲克，主婚姻多波折。' },
        { source: '《子平真诠》', title: '论日柱合婚', content: '合婚之法，先看日柱干支是否相合。日干相合者，如甲己合土、乙庚合金，主夫妻同心。日支相合者，如子丑合、寅亥合，主夫妻和谐。若日柱天克地冲，主婚姻多口舌是非。' },
        { source: '《穷通宝鉴》', title: '论调候', content: '婚姻之道，贵在调候。男命火旺燥烈，需水润之；女命水旺寒湿，需火暖之。阴阳调和，方为美满。调候得宜，夫妻感情自然和谐。' },
      ],
      partner: [
        { source: '《三命通会》', title: '论合作', content: '合作之道，贵在五行相生相助。日主相生者，主合作顺利；日主相克者，需有通关之神。财官相配者，主事业有成。比肩帮身者，主有助力但需防争财。' },
        { source: '《渊海子平》', title: '论财官配合', content: '财为养命之源，官为立身之本。合作求财，须看财星是否有力。食神生财者，主合作生财有道；伤官见官者，主合作多口舌是非。财官得配，事业亨通。' },
        { source: '《滴天髓》', title: '论比劫争财', content: '比肩争财，兄弟不和。合作之人，日主不宜太过相同。太过相同者，主有争财之象。宜一刚一柔，一主一辅，方为长久之道。' },
        { source: '《子平真诠》', title: '论格局配合', content: '格局相合者，主合作顺利。食神格配正财格，主生财有道；正官格配正印格，主事业有成。格局相冲者，主合作多波折。' },
        { source: '《神峰通考》', title: '论贵人相助', content: '天乙贵人、文昌贵人入命者，主一生多得贵人相助。合作之人，若双方互为贵人，主合作顺利，事业有成。' },
      ],
      friend: [
        { source: '《渊海子平》', title: '论比劫', content: '比肩帮身，主有兄弟朋友之助。比肩太旺者，主有争竞之象。劫财帮身，主有朋友之助，但需防劫财破财。交友之道，贵在五行相助。' },
        { source: '《三命通会》', title: '论交友', content: '交友之道，贵在日主相生。日主相生者，主友情深厚；日主相克者，主有口舌是非。食神格人善交际，正印格人重情义。' },
        { source: '《滴天髓》', title: '论贵人', content: '天乙贵人入命者，主一生多得贵人相助。朋友之中，若互为贵人者，主友情长久，互相扶持。贵人者，逢凶化吉之神也。' },
        { source: '《子平真诠》', title: '论桃花与人缘', content: '桃花入命者，主异性缘佳，人缘好。子午卯酉为桃花，寅午戌见卯为桃花。朋友之中，桃花旺者，主交际广泛，人缘极佳。' },
        { source: '《穷通宝鉴》', title: '论五行与性格', content: '金主义，木主仁，水主智，火主礼，土主信。交友之道，贵在五行互补。金旺者配木旺者，刚柔并济；水旺者配火旺者，阴阳调和。' },
      ],
      colleague: [
        { source: '《三命通会》', title: '论官杀', content: '正官为立身之本，主上司器重；七杀为权威之星，主有领导才能。同事之间，官杀得配者，主工作配合默契。官杀混杂者，主有争斗之象。' },
        { source: '《渊海子平》', title: '论事业', content: '食神制杀，英雄独压万人。同事之间，食神格人有才华，正官格人守规矩。食神配正官，主工作配合得当，事业有成。' },
        { source: '《滴天髓》', title: '论印星', content: '印星有力，主有学问，善于学习。同事之间，正印格人善于指导，偏印格人善于创新。印星配食伤，主有教学相长之象。' },
        { source: '《子平真诠》', title: '论财官', content: '财为养命之源，官为立身之本。同事之间，财官得配者，主工作顺利，事业有成。财星有力者，主有财运；官星有力者，主有官运。' },
        { source: '《神峰通考》', title: '论驿马', content: '驿马入命者，主奔波劳碌，适合外出发展。同事之间，驿马旺者，主工作繁忙，出差机会多。驿马配食神，主有出差生财之象。' },
      ],
    };
    return texts[type] || texts.spouse;
  };

  // 根据关系类型获取分析维度
  const getRelationDimensions = (type: string) => {
    const dimensions: Record<string, Array<{title: string; description: string}>> = {
      spouse: [
        { title: '日主相合', description: '日柱天干是否相合，如甲己合、乙庚合等，主夫妻同心' },
        { title: '地支六合', description: '日支是否六合，如子丑合、寅亥合等，主夫妻和谐' },
        { title: '五行互补', description: '双方五行是否互补，如一方火旺配一方水旺' },
        { title: '财官配合', description: '男命财星为妻，女命官星为夫，财官是否有力' },
        { title: '大运同步', description: '双方大运是否同步，吉凶是否相应' },
      ],
      partner: [
        { title: '日主相生', description: '日柱天干是否相生，主合作顺利' },
        { title: '财星助力', description: '双方财星是否有力，主合作生财' },
        { title: '格局配合', description: '双方格局是否相合，如食神配正财' },
        { title: '贵人互引', description: '双方是否互为贵人，主合作有助力' },
        { title: '比劫平衡', description: '比劫不宜太旺，否则主争财' },
      ],
      friend: [
        { title: '日主相生', description: '日柱天干是否相生，主友情深厚' },
        { title: '桃花人缘', description: '桃花是否入命，主交际广泛' },
        { title: '贵人相助', description: '是否互为贵人，主友情长久' },
        { title: '五行性格', description: '五行是否互补，性格是否相投' },
        { title: '比劫适度', description: '比劫适度主有助力，太旺主争竞' },
      ],
      colleague: [
        { title: '官杀配合', description: '正官七杀是否配合得当，主工作默契' },
        { title: '食伤才华', description: '食伤是否有力，主有才华配合' },
        { title: '印星学习', description: '印星是否有力，主学习互助' },
        { title: '财官得配', description: '财官是否得配，主事业顺利' },
        { title: '驿马配合', description: '驿马是否配合，主工作协调' },
      ],
    };
    return dimensions[type] || dimensions.spouse;
  };

  const selectedCharts = selectedChartIds.filter(id => id !== '').map(id => charts.find(c => c.id === id)).filter(Boolean);
  const chart1 = selectedCharts[0];
  const chart2 = selectedCharts[1];

  const tabItems = result
    ? [
        {
          key: 'detail',
          label: '详细分析',
          children: (
            <>
              {/* 多人关系概览 */}
              {result.multi_person && result.agents && (
                <Card title="多人关系网络" style={{ marginBottom: 16 }}>
                  <div style={{ textAlign: 'center', marginBottom: 16 }}>
                    <Text style={{ color: '#d4a853' }}>
                      共{result.agents.length}人参与分析，{result.pairs_count}对关系
                    </Text>
                  </div>
                  <Row gutter={[8, 8]} justify="center">
                    {result.agents.map((agent: any, index: number) => (
                      <Col key={index}>
                        <Tag color="blue" style={{ padding: '4px 12px', fontSize: 14 }}>
                          {agent.name}
                        </Tag>
                      </Col>
                    ))}
                  </Row>
                </Card>
              )}

              <Card title="综合评分" style={{ marginBottom: 16 }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 48, fontWeight: 'bold', color: '#d4a853' }}>
                    {result.score || 0}
                  </div>
                  <div>分</div>
                  <Tag color={result.score > 70 ? 'green' : result.score > 50 ? 'orange' : 'red'}>
                    {result.score > 70 ? '良好' : result.score > 50 ? '一般' : '需谨慎'}
                  </Tag>
                </div>
              </Card>

              <Card title={relationType === 'spouse' ? '八字合婚' : '八字配合'} style={{ marginBottom: 16 }}>
                <Paragraph>{result.bazi_compatibility || '暂无详细分析'}</Paragraph>
              </Card>

              <Card title="五行配合" style={{ marginBottom: 16 }}>
                <Paragraph>{result.wuxing_compatibility || '暂无详细分析'}</Paragraph>
              </Card>

              <Card title={`${relationTypes.find(t => t.value === relationType)?.label || ''}建议`}>
                <Paragraph>{result.suggestions || '暂无建议'}</Paragraph>
              </Card>
            </>
          ),
        },
        {
          key: 'professional',
          label: '专业分析',
          children: (() => {
            const classicalTexts = getRelationClassicalTexts(relationType);
            const dimensions = getRelationDimensions(relationType);
            const typeLabel = relationTypes.find(t => t.value === relationType)?.label || '配偶关系';
            return (
            <>
              {/* 古籍分析依据 */}
              <Card title={`古籍${typeLabel}分析依据`} style={{ marginBottom: 16 }}>
                <div>
                  {classicalTexts.map((text, index) => (
                    <Card size="small" title={`${text.source}${text.title}`} style={{ marginBottom: 8 }} key={index}>
                      <Paragraph style={{ fontStyle: 'italic', color: '#d4a853' }}>
                        {text.content}
                      </Paragraph>
                    </Card>
                  ))}
                </div>
              </Card>

              {/* 分析维度 */}
              <Card title={`${typeLabel}分析维度`} style={{ marginBottom: 16 }}>
                <Row gutter={[16, 16]}>
                  {dimensions.map((dim, index) => (
                    <Col xs={24} sm={8} key={index}>
                      <Card size="small" style={{ height: '100%' }}>
                        <div style={{ textAlign: 'center' }}>
                          <Tag color="gold" style={{ fontSize: 14, padding: '4px 12px' }}>{dim.title}</Tag>
                          <div style={{ fontSize: 12, color: '#b8b8d0', marginTop: 8 }}>{dim.description}</div>
                        </div>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </Card>

              <Card title={relationType === 'spouse' ? '大运合婚分析' : '大运配合分析'} style={{ marginBottom: 16 }}>
                {result.dayun_analysis && result.dayun_analysis.length > 0 ? (
                  <Row gutter={[16, 16]}>
                    {result.dayun_analysis.map((dayun: any, index: number) => (
                      <Col xs={24} sm={8} key={index}>
                        <Card size="small">
                          <div style={{ textAlign: 'center' }}>
                            <Text strong>{dayun.period}</Text>
                            <div style={{ fontSize: 14, color: '#b8b8d0' }}>
                              {dayun.age_range}
                            </div>
                            <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>
                              {dayun.compatibility}分
                            </div>
                            <div style={{ fontSize: 12, color: '#8888a8' }}>
                              {dayun.description}
                            </div>
                          </div>
                        </Card>
                      </Col>
                    ))}
                  </Row>
                ) : (
                  <Text type="secondary">暂无大运分析数据</Text>
                )}
              </Card>

              <Card title="流年桃花分析" style={{ marginBottom: 16 }}>
                {result.liunian_analysis && result.liunian_analysis.length > 0 ? (
                  <Row gutter={[16, 16]}>
                    {result.liunian_analysis.map((liunian: any, index: number) => (
                      <Col xs={24} sm={8} key={index}>
                        <Card size="small">
                          <div style={{ textAlign: 'center' }}>
                            <Text strong>{liunian.year}年</Text>
                            <div style={{ fontSize: 18, fontWeight: 'bold', color: liunian.taohua ? '#ff4d4f' : '#d4a853' }}>
                              {liunian.taohua ? '桃花运' : '无桃花'}
                            </div>
                            <div style={{ fontSize: 12, color: '#8888a8' }}>
                              {liunian.description}
                            </div>
                          </div>
                        </Card>
                      </Col>
                    ))}
                  </Row>
                ) : (
                  <Text type="secondary">暂无流年桃花分析数据</Text>
                )}
              </Card>

              <Card title="关系特征" style={{ marginBottom: 16 }}>
                {result.relationship_features && result.relationship_features.length > 0 ? (
                  <Row gutter={[8, 8]}>
                    {result.relationship_features.map((feature: string, index: number) => (
                      <Col xs={12} sm={8} md={6} key={index}>
                        <Tag color="blue">{feature}</Tag>
                      </Col>
                    ))}
                  </Row>
                ) : (
                  <Text type="secondary">暂无关系特征数据</Text>
                )}
              </Card>

              <Card title="风险因素" style={{ marginBottom: 16 }}>
                {result.risk_factors && result.risk_factors.length > 0 ? (
                  <ul>
                    {result.risk_factors.map((factor: string, index: number) => (
                      <li key={index}>
                        <Paragraph>{factor}</Paragraph>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <Text type="secondary">暂无风险因素数据</Text>
                )}
              </Card>

              <Card title="改善建议" style={{ marginBottom: 16 }}>
                {result.improvement_suggestions && result.improvement_suggestions.length > 0 ? (
                  <ul>
                    {result.improvement_suggestions.map((suggestion: string, index: number) => (
                      <li key={index}>
                        <Paragraph>{suggestion}</Paragraph>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <Text type="secondary">暂无改善建议数据</Text>
                )}
              </Card>
            </>
            );
          })(),
        },
        {
          key: 'network',
          label: '关系网络图',
          children:
            chart1 && chart2 ? (
              <RelationNetwork
                chart1Name={chart1.name}
                chart2Name={chart2.name}
                wuxing1={chart1.bazi_data.五行力量}
                wuxing2={chart2.bazi_data.五行力量}
                compatibility={{
                  score: result.score || 0,
                  details: result.details,
                }}
              />
            ) : (
              <Card>
                <Empty description="请至少选择两个命盘" />
              </Card>
            ),
        },
        {
          key: 'calculation_process',
          label: '计算过程',
          children: result?.calculation_process ? (
            <CalculationProcess data={result.calculation_process} title="关系分析计算过程" />
          ) : (
            <Empty description="暂无计算过程数据" />
          ),
        },
      ]
    : [];

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
            关系分析
          </Title>
        </div>
        <Paragraph style={{ 
          color: '#b8b8d0', 
          fontSize: 16,
          maxWidth: 600,
          margin: '0 auto',
          lineHeight: 1.8,
        }}>
          基于八字命理，分析两人之间的关系契合度
        </Paragraph>
        <div className="gf-huiwen-divider" style={{ width: 200, margin: '24px auto' }} />
      </div>

      <Row gutter={[24, 24]}>
        <Col xs={24} lg={8}>
          <div className="gf-card" style={{ padding: '32px', height: '100%' }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              marginBottom: 24,
              gap: 12,
            }}>
              <StarOutlined style={{ color: '#d4a853', fontSize: 24 }} />
              <Title level={4} className="gf-title" style={{ margin: 0 }}>
                选择命盘
              </Title>
            </div>
            <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
            
            <Space direction="vertical" style={{ width: '100%' }} size="large">
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                  <Text strong style={{ color: '#ffffff' }}>选择参与者：</Text>
                  <Button 
                    size="small" 
                    type="dashed" 
                    onClick={addChartSelect}
                    icon={<PlusOutlined />}
                    disabled={selectedChartIds.length >= 6}
                    style={{ borderColor: '#d4a853', color: '#d4a853' }}
                  >
                    添加
                  </Button>
                </div>
                
                {selectedChartIds.length === 0 ? (
                  <div style={{ 
                    padding: '16px', 
                    background: 'rgba(212,168,83,0.05)', 
                    borderRadius: 4, 
                    textAlign: 'center',
                    border: '1px dashed rgba(212,168,83,0.3)'
                  }}>
                    <Text style={{ color: '#b8b8d0' }}>点击"添加"选择参与者</Text>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {selectedChartIds.map((chartId, index) => (
                      <div key={index} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                        <Text style={{ color: '#d4a853', minWidth: 24 }}>{index + 1}.</Text>
                        <Select
                          style={{ flex: 1 }}
                          placeholder={`选择参与者${index + 1}`}
                          value={chartId || undefined}
                          onChange={(v) => updateChartSelect(index, v)}
                        >
                          {charts.map((chart) => (
                            <Option key={chart.id} value={chart.id}>
                              {chart.name} ({chart.gender === 'male' ? '男' : '女'})
                            </Option>
                          ))}
                        </Select>
                        <Button 
                          size="small" 
                          danger 
                          icon={<DeleteOutlined />}
                          onClick={() => removeChartSelect(index)}
                        />
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <Divider className="gf-divider" />

              <div>
                <Text strong style={{ color: '#ffffff' }}>起始时间：</Text>
                <Row gutter={8} style={{ marginTop: 8 }}>
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
              </div>

              <Divider className="gf-divider" />

              <div>
                <Text strong style={{ color: '#ffffff' }}>关系类型：</Text>
                <Select
                  style={{ width: '100%', marginTop: 8 }}
                  value={relationType}
                  onChange={setRelationType}
                >
                  {relationTypes.map((type) => (
                    <Option key={type.value} value={type.value}>
                      {type.label}
                    </Option>
                  ))}
                </Select>
                <div style={{ marginTop: 8, color: '#b8b8d0' }}>
                  {relationTypes.find((t) => t.value === relationType)?.desc}
                </div>
              </div>

              <Button
                type="primary"
                className="gf-btn-primary"
                icon={<TeamOutlined />}
                onClick={handleAnalyze}
                loading={loading}
                block
                disabled={selectedChartIds.filter(id => id !== '').length < 2}
              >
                开始分析
              </Button>
            </Space>
          </div>
        </Col>

        <Col xs={24} lg={16}>
          {result ? (
            <div className="gf-card" style={{ padding: '32px' }}>
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                marginBottom: 24,
                gap: 12,
              }}>
                <HeartOutlined style={{ color: '#d4a853', fontSize: 24 }} />
                <Title level={4} className="gf-title" style={{ margin: 0 }}>
                  分析结果
                </Title>
              </div>
              <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
              
              <Tabs items={tabItems} className="gf-tabs" />
            </div>
          ) : (
            <div className="gf-card" style={{ padding: '32px' }}>
              <div style={{ textAlign: 'center', padding: 40 }}>
                <TeamOutlined style={{ fontSize: 48, color: '#d4a853' }} />
                <div style={{ marginTop: 16 }}>
                  <Text style={{ color: '#b8b8d0' }}>请选择至少两个命盘进行关系分析</Text>
                  <div style={{ marginTop: 8, color: '#8888a8', fontSize: 12 }}>
                    支持2-6人的多人关系分析
                  </div>
                </div>
              </div>
            </div>
          )}
        </Col>
      </Row>

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

export default RelationAnalysis;
