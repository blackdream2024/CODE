import { useState } from 'react';
import { Card, Row, Col, Typography, Tabs, Empty, Select, Tag, Divider, Alert, Collapse } from 'antd';
import { StarOutlined, CompassOutlined } from '@ant-design/icons';
import { useChartStore } from '../stores/chartStore';
import BaziChart from '../components/BaziChart';
import ZiweiChart from '../components/ZiweiChart';
import WuxingRadar from '../components/WuxingRadar';
import DayunTimeline from '../components/DayunTimeline';
import CalculationProcess from '../components/CalculationProcess';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;
const { Panel } = Collapse;

function ChartView() {
  const { charts, currentChart, setCurrentChart } = useChartStore();
  const [activeTab, setActiveTab] = useState('bazi');

  if (charts.length === 0) {
    return (
      <div>
        <Title level={2}>命盘查看</Title>
        <Card>
          <Empty
            description="暂无命盘数据，请先录入命盘"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        </Card>
      </div>
    );
  }

  const selectedChart = currentChart || charts[0];

  const tabItems = [
    {
      key: 'bazi',
      label: '八字排盘',
      children: <BaziChart data={selectedChart.bazi_data} />,
    },
    {
      key: 'ziwei',
      label: '紫微斗数',
      children: selectedChart.ziwei_data ? (
        <ZiweiChart data={selectedChart.ziwei_data} />
      ) : (
        <Empty description="无紫微数据" />
      ),
    },
    {
      key: 'wuxing',
      label: '五行分析',
      children: <WuxingRadar data={selectedChart.bazi_data.五行力量} analysis={selectedChart.bazi_data.五行分析} />,
    },
    {
      key: 'dayun',
      label: '大运流年',
      children: <DayunTimeline data={selectedChart.bazi_data.大运} />,
    },
    {
      key: 'ziwei_professional',
      label: '紫微专业分析',
      children: selectedChart.ziwei_data ? (
        <div>
          <Card title="命局分析" style={{ marginBottom: 16 }}>
            {selectedChart.ziwei_data.ming_ju_analysis ? (
              <div>
                <Row gutter={[16, 16]}>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="命宫星曜">
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {selectedChart.ziwei_data.ming_ju_analysis['命宫星曜']?.map((star: string, index: number) => (
                          <Tag key={index} color="blue">{star}</Tag>
                        ))}
                      </div>
                    </Card>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="格局判断">
                      <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>
                        {selectedChart.ziwei_data.ming_ju_analysis['格局判断']}
                      </div>
                      {selectedChart.ziwei_data.ming_ju_analysis['格局详解']?.古籍批断 && (
                        <Paragraph type="secondary" style={{ marginTop: 8 }}>
                          {selectedChart.ziwei_data.ming_ju_analysis['格局详解'].古籍批断}
                        </Paragraph>
                      )}
                    </Card>
                  </Col>
                </Row>
                
                <Divider />
                
                <Card title="命宫星曜详解" style={{ marginBottom: 16 }}>
                  <Collapse>
                    {selectedChart.ziwei_data.ming_ju_analysis['命宫星曜详解']?.map((star: any, index: number) => (
                      <Panel 
                        header={
                          <span>
                            <Tag color="blue">{star.星曜}</Tag>
                            <Text type="secondary">（{star.五行}）</Text>
                            {star.亮度 && <Tag color={star.亮度 === '庙' ? 'green' : star.亮度 === '旺' ? 'blue' : 'orange'}>{star.亮度}</Tag>}
                          </span>
                        } 
                        key={index}
                      >
                        <Paragraph><strong>特质：</strong>{star.特质}</Paragraph>
                        {star.入命宫批断 && <Paragraph><strong>入命宫批断：</strong>{star.入命宫批断}</Paragraph>}
                        {star.古籍批断 && <Paragraph type="secondary"><strong>古籍批断：</strong>{star.古籍批断}</Paragraph>}
                        {star.四化 && star.四化.length > 0 && (
                          <div>
                            <Text strong>四化：</Text>
                            {star.四化.map((hua: string, i: number) => (
                              <Tag key={i} color="purple">{hua}</Tag>
                            ))}
                          </div>
                        )}
                      </Panel>
                    ))}
                  </Collapse>
                </Card>
                
                <Card title="命局特点" style={{ marginBottom: 16 }}>
                  <Row gutter={[8, 8]}>
                    {selectedChart.ziwei_data.ming_ju_analysis['命局特点']?.map((feature: string, index: number) => (
                      <Col xs={12} sm={8} key={index}>
                        <Tag color="green">{feature}</Tag>
                      </Col>
                    ))}
                  </Row>
                </Card>
                
                <Card title="注意事项" style={{ marginBottom: 16 }}>
                  <ul>
                    {selectedChart.ziwei_data.ming_ju_analysis['注意事项']?.map((note: string, index: number) => (
                      <li key={index}>{note}</li>
                    ))}
                  </ul>
                </Card>
                
                {selectedChart.ziwei_data.ming_ju_analysis['古籍参考批断'] && (
                  <Card title="古籍参考批断" style={{ marginBottom: 16 }}>
                    <ul>
                      {selectedChart.ziwei_data.ming_ju_analysis['古籍参考批断'].map((comment: string, index: number) => (
                        <li key={index}>{comment}</li>
                      ))}
                    </ul>
                  </Card>
                )}
              </div>
            ) : (
              <Text type="secondary">暂无命局分析数据</Text>
            )}
          </Card>
          
          <Card title="三方四正分析" style={{ marginBottom: 16 }}>
            {selectedChart.ziwei_data.san_fang_si_zheng ? (
              <div>
                <Row gutter={[16, 16]}>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="三方宫位">
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {selectedChart.ziwei_data.san_fang_si_zheng['三方地支']?.map((zhi: string, index: number) => (
                          <Tag key={index} color="blue">{zhi}</Tag>
                        ))}
                      </div>
                      <Divider />
                      <Text strong>三方星曜：</Text>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 8 }}>
                        {selectedChart.ziwei_data.san_fang_si_zheng['三方星曜']?.map((star: any, index: number) => (
                          <Tag key={index} color={star.category === 'main' ? 'blue' : star.category === 'auxiliary' ? 'green' : 'red'}>
                            {star.star}
                          </Tag>
                        ))}
                      </div>
                    </Card>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="四正宫位">
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {selectedChart.ziwei_data.san_fang_si_zheng['四正地支']?.map((zhi: string, index: number) => (
                          <Tag key={index} color="purple">{zhi}</Tag>
                        ))}
                      </div>
                      <Divider />
                      <Text strong>四正星曜：</Text>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 8 }}>
                        {selectedChart.ziwei_data.san_fang_si_zheng['四正星曜']?.map((star: any, index: number) => (
                          <Tag key={index} color={star.category === 'main' ? 'blue' : star.category === 'auxiliary' ? 'green' : 'red'}>
                            {star.star}
                          </Tag>
                        ))}
                      </div>
                    </Card>
                  </Col>
                </Row>
                
                {selectedChart.ziwei_data.san_fang_si_zheng['三方四正综合分析'] && (
                  <Alert
                    message="三方四正综合分析"
                    description={selectedChart.ziwei_data.san_fang_si_zheng['三方四正综合分析']}
                    type="info"
                    showIcon
                    style={{ marginTop: 16 }}
                  />
                )}
              </div>
            ) : (
              <Text type="secondary">暂无三方四正数据</Text>
            )}
          </Card>
          
          <Card title="飞宫四化分析" style={{ marginBottom: 16 }}>
            {selectedChart.ziwei_data.fei_gong_sihua && selectedChart.ziwei_data.fei_gong_sihua.length > 0 ? (
              <div>
                <Collapse>
                  {selectedChart.ziwei_data.fei_gong_sihua.map((fei_gong: any, index: number) => (
                    <Panel 
                      header={
                        <span>
                          <Tag color="blue">{fei_gong['宫位']}</Tag>
                          <Text type="secondary">（{fei_gong['天干']}）</Text>
                        </span>
                      } 
                      key={index}
                    >
                      <Row gutter={16}>
                        <Col xs={12} sm={6}>
                          <Text strong>化禄：</Text>
                          <Tag color="green">{fei_gong['化禄']}</Tag>
                        </Col>
                        <Col xs={12} sm={6}>
                          <Text strong>化权：</Text>
                          <Tag color="blue">{fei_gong['化权']}</Tag>
                        </Col>
                        <Col xs={12} sm={6}>
                          <Text strong>化科：</Text>
                          <Tag color="purple">{fei_gong['化科']}</Tag>
                        </Col>
                        <Col xs={12} sm={6}>
                          <Text strong>化忌：</Text>
                          <Tag color="red">{fei_gong['化忌']}</Tag>
                        </Col>
                      </Row>
                      
                      {fei_gong['飞入宫位'] && fei_gong['飞入宫位'].length > 0 && (
                        <>
                          <Divider />
                          <Text strong>飞入宫位：</Text>
                          <ul>
                            {fei_gong['飞入宫位'].map((item: any, i: number) => (
                              <li key={i}>
                                {item.四化} {item.星曜} 飞入 {item.飞入宫位}（{item.飞入地支}）
                              </li>
                            ))}
                          </ul>
                        </>
                      )}
                    </Panel>
                  ))}
                </Collapse>
              </div>
            ) : (
              <Text type="secondary">暂无飞宫四化数据</Text>
            )}
          </Card>
          
          <Card title="自化分析" style={{ marginBottom: 16 }}>
            {selectedChart.ziwei_data.zi_hua && selectedChart.ziwei_data.zi_hua.length > 0 ? (
              <div>
                {selectedChart.ziwei_data.zi_hua.map((zi_hua: any, index: number) => (
                  <Alert
                    key={index}
                    message={`${zi_hua['宫位']} - ${zi_hua['自化']}`}
                    description={
                      <div>
                        <p><strong>类型：</strong>{zi_hua['类型']}</p>
                        <p><strong>影响：</strong>{zi_hua['影响']}</p>
                        <p><strong>建议：</strong>{zi_hua['建议']}</p>
                      </div>
                    }
                    type={zi_hua['自化'] === '化禄' ? 'success' : zi_hua['自化'] === '化忌' ? 'error' : 'info'}
                    showIcon
                    style={{ marginBottom: 16 }}
                  />
                ))}
              </div>
            ) : (
              <Text type="secondary">暂无自化数据</Text>
            )}
          </Card>

          {/* 推演分析与结论 */}
          {selectedChart.ziwei_data.analysis_report && (
            <>
              <Card title="推演分析" style={{ marginBottom: 16 }}>
                {selectedChart.ziwei_data.analysis_report.推演分析.map((step: any, index: number) => (
                  <Card size="small" key={index} style={{ marginBottom: 8 }}>
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                        <Tag color="blue">{step.步骤}</Tag>
                      </div>
                      <Paragraph><strong>分析内容：</strong>{step.分析内容}</Paragraph>
                      <Paragraph type="secondary"><strong>依据：</strong>{step.依据}</Paragraph>
                      {step.古籍引用 && (
                        <Paragraph style={{ fontStyle: 'italic', color: '#d4a853' }}><strong>古籍引用：</strong>{step.古籍引用}</Paragraph>
                      )}
                    </div>
                  </Card>
                ))}
              </Card>

              <Card title="推断结论" style={{ marginBottom: 16 }}>
                <Row gutter={[16, 16]}>
                  {selectedChart.ziwei_data.analysis_report.推断结论.map((conclusion: any, index: number) => (
                    <Col xs={24} sm={12} key={index}>
                      <Card size="small" style={{ height: '100%' }}>
                        <div style={{ textAlign: 'center', marginBottom: 8 }}>
                          <Tag color="gold" style={{ fontSize: 14, padding: '4px 16px' }}>{conclusion.方面}</Tag>
                        </div>
                        <Paragraph><strong>推断：</strong>{conclusion.推断}</Paragraph>
                        <Paragraph type="secondary"><strong>依据：</strong>{conclusion.依据}</Paragraph>
                        {conclusion.古籍引用 && (
                          <Paragraph style={{ fontStyle: 'italic', color: '#d4a853', fontSize: 12 }}><strong>古籍：</strong>{conclusion.古籍引用}</Paragraph>
                        )}
                      </Card>
                    </Col>
                  ))}
                </Row>
              </Card>

              <Card title="综合结论" style={{ marginBottom: 16 }}>
                <Alert
                  message={<span style={{ fontSize: 16, fontWeight: 'bold' }}>命局总评</span>}
                  description={selectedChart.ziwei_data.analysis_report.综合结论}
                  type="success"
                  showIcon
                  style={{ marginBottom: 16 }}
                />
                {selectedChart.ziwei_data.analysis_report.古籍总论 && (
                  <Card size="small" title="古籍总论" style={{ background: 'rgba(212,168,83,0.08)', borderColor: 'rgba(212,168,83,0.2)' }}>
                    <Paragraph style={{ fontStyle: 'italic', color: '#d4a853', lineHeight: 1.8 }}>
                      {selectedChart.ziwei_data.analysis_report.古籍总论}
                    </Paragraph>
                  </Card>
                )}
              </Card>
            </>
          )}
        </div>
      ) : (
        <Empty description="无紫微数据" />
      ),
    },
    {
      key: 'professional',
      label: '专业分析',
      children: (
        <div>
          {/* 命局总评 */}
          <Card title="命局总评" style={{ marginBottom: 16 }}>
            {selectedChart.bazi_data.命局总评 ? (
              <div>
                <Row gutter={[16, 16]}>
                  <Col span={24}>
                    <Alert
                      message={<span style={{ fontSize: 18, fontWeight: 'bold' }}>综合评级：{selectedChart.bazi_data.命局总评.综合评级}</span>}
                      type="success"
                      showIcon
                    />
                  </Col>
                </Row>
                <Divider />
                <Row gutter={[16, 16]}>
                  <Col xs={24} sm={8}>
                    <Card size="small" title="事业">
                      <Paragraph>{selectedChart.bazi_data.命局总评.事业}</Paragraph>
                    </Card>
                  </Col>
                  <Col xs={24} sm={8}>
                    <Card size="small" title="财运">
                      <Paragraph>{selectedChart.bazi_data.命局总评.财运}</Paragraph>
                    </Card>
                  </Col>
                  <Col xs={24} sm={8}>
                    <Card size="small" title="感情">
                      <Paragraph>{selectedChart.bazi_data.命局总评.感情}</Paragraph>
                    </Card>
                  </Col>
                </Row>
                <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="健康">
                      <Paragraph>{selectedChart.bazi_data.命局总评.健康}</Paragraph>
                    </Card>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="性格">
                      <Paragraph>{selectedChart.bazi_data.命局总评.性格}</Paragraph>
                    </Card>
                  </Col>
                </Row>
                {selectedChart.bazi_data.命局总评.古籍总论 && (
                  <Alert
                    message="古籍总论"
                    description={selectedChart.bazi_data.命局总评.古籍总论}
                    type="info"
                    showIcon
                    style={{ marginTop: 16 }}
                  />
                )}
              </div>
            ) : (
              <Text type="secondary">暂无命局总评数据</Text>
            )}
          </Card>

          {/* 古籍命理批断 */}
          <Card title="古籍命理批断" style={{ marginBottom: 16 }}>
            {selectedChart.bazi_data.古籍批断 ? (
              <div>
                {selectedChart.bazi_data.古籍批断.渊海子平 && (
                  <Card size="small" title="《渊海子平》批断" style={{ marginBottom: 8 }}>
                    <Paragraph style={{ fontStyle: 'italic', color: '#d4a853' }}>
                      {selectedChart.bazi_data.古籍批断.渊海子平}
                    </Paragraph>
                  </Card>
                )}
                {selectedChart.bazi_data.古籍批断.三命通会 && (
                  <Card size="small" title="《三命通会》批断" style={{ marginBottom: 8 }}>
                    <Paragraph style={{ fontStyle: 'italic', color: '#d4a853' }}>
                      {selectedChart.bazi_data.古籍批断.三命通会}
                    </Paragraph>
                  </Card>
                )}
                {selectedChart.bazi_data.古籍批断.滴天髓 && (
                  <Card size="small" title="《滴天髓》批断" style={{ marginBottom: 8 }}>
                    <Paragraph style={{ fontStyle: 'italic', color: '#d4a853' }}>
                      {selectedChart.bazi_data.古籍批断.滴天髓}
                    </Paragraph>
                  </Card>
                )}
                {selectedChart.bazi_data.古籍批断.子平真诠 && (
                  <Card size="small" title="《子平真诠》批断" style={{ marginBottom: 8 }}>
                    <Paragraph style={{ fontStyle: 'italic', color: '#d4a853' }}>
                      {selectedChart.bazi_data.古籍批断.子平真诠}
                    </Paragraph>
                  </Card>
                )}
                {selectedChart.bazi_data.古籍批断.命理总评 && (
                  <Alert
                    message="综合命理总评"
                    description={selectedChart.bazi_data.古籍批断.命理总评}
                    type="warning"
                    showIcon
                    style={{ marginTop: 8 }}
                  />
                )}
              </div>
            ) : (
              <Text type="secondary">暂无古籍批断数据</Text>
            )}
          </Card>

          {/* 格局精论 */}
          <Card title="格局精论" style={{ marginBottom: 16 }}>
            {selectedChart.bazi_data.格局详解 ? (
              <div>
                <Row gutter={[16, 16]}>
                  <Col xs={12} sm={6}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>格局</Text>
                        <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>
                          {selectedChart.bazi_data.格局详解.格局}
                        </div>
                      </div>
                    </Card>
                  </Col>
                  <Col xs={12} sm={6}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>格局类型</Text>
                        <div style={{ fontSize: 16, fontWeight: 'bold', color: '#d4a853' }}>
                          {selectedChart.bazi_data.格局详解.格局类型 || '正格'}
                        </div>
                      </div>
                    </Card>
                  </Col>
                  <Col xs={12} sm={6}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>格局层次</Text>
                        <div style={{ fontSize: 16, fontWeight: 'bold', color: '#d4a853' }}>
                          {selectedChart.bazi_data.格局详解.格局层次 || '中等'}
                        </div>
                      </div>
                    </Card>
                  </Col>
                  <Col xs={12} sm={6}>
                    <Card size="small">
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>格局条件</Text>
                        <div style={{ fontSize: 14, color: '#b8b8d0' }}>
                          {selectedChart.bazi_data.格局详解.格局条件 || '月令透干'}
                        </div>
                      </div>
                    </Card>
                  </Col>
                </Row>
                <Divider />
                <Paragraph>{selectedChart.bazi_data.格局详解.描述}</Paragraph>
                {selectedChart.bazi_data.格局详解.喜忌分析 && (
                  <Alert
                    message="喜忌分析"
                    description={selectedChart.bazi_data.格局详解.喜忌分析}
                    type="warning"
                    showIcon
                    style={{ marginTop: 16 }}
                  />
                )}
                {selectedChart.bazi_data.格局详解.特点 && (
                  <>
                    <Divider />
                    <Title level={5}>命局特点</Title>
                    <Row gutter={[8, 8]}>
                      {selectedChart.bazi_data.格局详解.特点.map((feature: string, index: number) => (
                        <Col xs={12} sm={8} md={6} key={index}>
                          <Tag color="blue">{feature}</Tag>
                        </Col>
                      ))}
                    </Row>
                  </>
                )}
                {selectedChart.bazi_data.格局详解.古籍引文 && selectedChart.bazi_data.格局详解.古籍引文.length > 0 && (
                  <>
                    <Divider />
                    <Title level={5}>古籍引文</Title>
                    {selectedChart.bazi_data.格局详解.古籍引文.map((quote: string, index: number) => (
                      <Alert
                        key={index}
                        message={quote}
                        type="info"
                        showIcon
                        style={{ marginBottom: 8 }}
                      />
                    ))}
                  </>
                )}
              </div>
            ) : (
              <Text type="secondary">暂无格局详解数据</Text>
            )}
          </Card>

          {/* 用神详解 */}
          <Card title="用神详解" style={{ marginBottom: 16 }}>
            <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
              <Col xs={24} sm={8}>
                <Card size="small" style={{ background:'rgba(212,168,83,0.08)', borderColor:'rgba(212,168,83,0.2)' }}>
                  <div style={{ textAlign: 'center' }}>
                    <Text strong style={{ color: '#d4a853' }}>用神</Text>
                    <div style={{ fontSize: 'clamp(18px, 4vw, 24px)', fontWeight: 'bold', color: '#d4a853' }}>
                      {selectedChart.bazi_data.用神 || '未知'}
                    </div>
                  </div>
                </Card>
              </Col>
              <Col xs={24} sm={8}>
                <Card size="small" style={{ background:'rgba(196,30,58,0.08)', borderColor:'rgba(196,30,58,0.2)' }}>
                  <div style={{ textAlign: 'center' }}>
                    <Text strong style={{ color: '#ff4d4f' }}>忌神</Text>
                    <div style={{ fontSize: 'clamp(18px, 4vw, 24px)', fontWeight: 'bold', color: '#ff4d4f' }}>
                      {selectedChart.bazi_data.忌神 || '未知'}
                    </div>
                  </div>
                </Card>
              </Col>
              <Col xs={24} sm={8}>
                <Card size="small" style={{ background:'rgba(212,168,83,0.08)', borderColor:'rgba(212,168,83,0.2)' }}>
                  <div style={{ textAlign: 'center' }}>
                    <Text strong style={{ color: '#d4a853' }}>喜神</Text>
                    <div style={{ fontSize: 'clamp(18px, 4vw, 24px)', fontWeight: 'bold', color: '#d4a853' }}>
                      {selectedChart.bazi_data.喜神 || '未知'}
                    </div>
                  </div>
                </Card>
              </Col>
            </Row>
            {selectedChart.bazi_data.用神详解 && (
              <div>
                <Divider />
                <Row gutter={[16, 16]}>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="用神层次">
                      <Paragraph>{selectedChart.bazi_data.用神详解.用神层次}</Paragraph>
                    </Card>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="用神作用">
                      <Paragraph>{selectedChart.bazi_data.用神详解.用神作用}</Paragraph>
                    </Card>
                  </Col>
                </Row>
                <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="忌神化解">
                      <Paragraph>{selectedChart.bazi_data.用神详解.忌神化解}</Paragraph>
                    </Card>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Card size="small" title="喜神助力">
                      <Paragraph>{selectedChart.bazi_data.用神详解.喜神助力}</Paragraph>
                    </Card>
                  </Col>
                </Row>
              </div>
            )}
          </Card>

          {/* 纳音五行 */}
          <Card title="纳音五行" style={{ marginBottom: 16 }}>
            {selectedChart.bazi_data.纳音 ? (
              <Row gutter={[16, 16]}>
                {Object.entries(selectedChart.bazi_data.纳音).map(([pillar, nayin]: [string, any]) => (
                  <Col xs={12} sm={6} key={pillar}>
                    <Card size="small" style={{ background:'rgba(123,45,142,0.08)', borderColor:'rgba(123,45,142,0.2)' }}>
                      <div style={{ textAlign: 'center' }}>
                        <Text strong>{pillar}</Text>
                        <div style={{ fontSize: 'clamp(14px, 3vw, 18px)', fontWeight: 'bold', color: '#d4a853' }}>
                          {nayin.五行}
                        </div>
                        <div style={{ fontSize: 13, color: '#b8b8d0', marginTop: 8 }}>
                          {nayin.描述}
                        </div>
                      </div>
                    </Card>
                  </Col>
                ))}
              </Row>
            ) : (
              <Text type="secondary">暂无纳音数据</Text>
            )}
          </Card>

          {/* 神煞 */}
          <Card title="神煞" style={{ marginBottom: 16 }}>
            {selectedChart.bazi_data.神煞 && selectedChart.bazi_data.神煞.length > 0 ? (
              <Row gutter={[16, 16]}>
                {selectedChart.bazi_data.神煞.map((shensha: any, index: number) => (
                  <Col xs={12} sm={8} key={index}>
                    <Card size="small" style={{ background:'rgba(212,168,83,0.08)', borderColor:'rgba(212,168,83,0.2)' }}>
                      <div style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: 16, fontWeight: 'bold', color: '#faad14' }}>
                          {shensha.名称}
                        </div>
                        <Tag color="blue" style={{ marginTop: 8 }}>{shensha.位置}</Tag>
                        <div style={{ fontSize: 13, color: '#b8b8d0', marginTop: 8 }}>
                          {shensha.描述}
                        </div>
                      </div>
                    </Card>
                  </Col>
                ))}
              </Row>
            ) : (
              <Text type="secondary">暂无神煞数据</Text>
            )}
          </Card>

          {/* 十二长生与空亡 */}
          <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
            <Col xs={24} sm={12}>
              <Card title="十二长生" style={{ height: '100%' }}>
                {selectedChart.bazi_data.十二长生 ? (
                  <div>
                    {Object.entries(selectedChart.bazi_data.十二长生).map(([pillar, changsheng]: [string, any]) => (
                      <div key={pillar} style={{ marginBottom: 12, padding: '8px', background:'rgba(255,255,255,0.04)', borderRadius: 4 }}>
                        <Text strong>{pillar}</Text>
                        <Tag color="purple" style={{ marginLeft: 8 }}>{changsheng.阶段}</Tag>
                        <div style={{ fontSize: 13, color: '#b8b8d0', marginTop: 4 }}>
                          {changsheng.描述}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <Text type="secondary">暂无十二长生数据</Text>
                )}
              </Card>
            </Col>
            <Col xs={24} sm={12}>
              <Card title="空亡" style={{ height: '100%' }}>
                {selectedChart.bazi_data.空亡 ? (
                  <div>
                    <div style={{ textAlign: 'center', marginBottom: 16 }}>
                      <Text strong>空亡地支</Text>
                      <div style={{ fontSize: 24, fontWeight: 'bold', color: '#d4a853', marginTop: 8 }}>
                        {selectedChart.bazi_data.空亡.空亡.join('、')}
                      </div>
                    </div>
                    <Divider />
                    <Paragraph>{selectedChart.bazi_data.空亡.描述}</Paragraph>
                  </div>
                ) : (
                  <Text type="secondary">暂无空亡数据</Text>
                )}
              </Card>
            </Col>
          </Row>

          {/* 命局特征 */}
          <Card title="命局特征" style={{ marginBottom: 16 }}>
            {selectedChart.bazi_data.命局特征 && selectedChart.bazi_data.命局特征.length > 0 ? (
              <Row gutter={[8, 8]}>
                {selectedChart.bazi_data.命局特征.map((feature: string, index: number) => (
                  <Col xs={12} sm={8} md={6} lg={4} key={index}>
                    <Tag color="purple" style={{ fontSize: 14, padding: '4px 12px' }}>{feature}</Tag>
                  </Col>
                ))}
              </Row>
            ) : (
              <Text type="secondary">暂无命局特征数据</Text>
            )}
          </Card>
        </div>
      ),
    },
    {
      key: 'calculation_process',
      label: '计算过程',
      children: (
        <div>
          {/* 八字计算过程 */}
          <Card title="八字排盘计算过程" style={{ marginBottom: 16 }}>
            {selectedChart.bazi_data ? (
              <div>
                <Collapse defaultActiveKey={['sz', 'wux', 'geju', 'dayun']}>
                  <Panel header="步骤一：排四柱" key="sz">
                    <Paragraph>
                      <Text strong>输入数据：</Text>出生时间 {selectedChart.birth_date} {selectedChart.birth_time}
                    </Paragraph>
                    <div style={{ background: 'rgba(255,255,255,0.04)', padding: 12, borderRadius: 4, marginBottom: 8 }}>
                      <Text code>年柱：{selectedChart.bazi_data.四柱.年柱.天干}{selectedChart.bazi_data.四柱.年柱.地支}</Text><br/>
                      <Text code>月柱：{selectedChart.bazi_data.四柱.月柱.天干}{selectedChart.bazi_data.四柱.月柱.地支}</Text><br/>
                      <Text code>日柱：{selectedChart.bazi_data.四柱.日柱.天干}{selectedChart.bazi_data.四柱.日柱.地支}</Text><br/>
                      <Text code>时柱：{selectedChart.bazi_data.四柱.时柱.天干}{selectedChart.bazi_data.四柱.时柱.地支}</Text>
                    </div>
                    <Alert message="排四柱以年为根，月为苗，日为花，时为果。" type="info" showIcon />
                  </Panel>
                  <Panel header="步骤二：定日主与十神" key="rzs">
                    <Paragraph><Text strong>日主：</Text>{selectedChart.bazi_data.日主}</Paragraph>
                    <Paragraph><Text strong>旺衰：</Text>{selectedChart.bazi_data.旺衰}</Paragraph>
                    <div style={{ background: 'rgba(255,255,255,0.04)', padding: 12, borderRadius: 4, marginBottom: 8 }}>
                      {Object.entries(selectedChart.bazi_data.十神).map(([key, value]) => (
                        <Tag key={key} color="blue" style={{ margin: 4 }}>{key}：{String(value)}</Tag>
                      ))}
                    </div>
                    <Alert message="以日干为主，配合年月时支，论生克制化。" type="info" showIcon />
                  </Panel>
                  <Panel header="步骤三：五行力量分析" key="wux">
                    <Row gutter={[8, 8]}>
                      {Object.entries(selectedChart.bazi_data.五行力量).map(([element, strength]) => (
                        <Col xs={12} sm={8} key={element}>
                          <Card size="small">
                            <div style={{ textAlign: 'center' }}>
                              <Tag color={element === '金' ? 'gold' : element === '木' ? 'green' : element === '水' ? 'blue' : element === '火' ? 'red' : 'orange'}>{element}</Tag>
                              <div style={{ fontSize: 18, fontWeight: 'bold', color: '#d4a853' }}>{((strength as number) * 100).toFixed(0)}%</div>
                            </div>
                          </Card>
                        </Col>
                      ))}
                    </Row>
                    <div style={{ marginTop: 8 }}>
                      {selectedChart.bazi_data.五行分析 && (
                        <Alert message={selectedChart.bazi_data.五行分析.五行关系} type="info" showIcon />
                      )}
                    </div>
                  </Panel>
                  <Panel header="步骤四：定格局" key="geju">
                    <Paragraph><Text strong>格局：</Text><span style={{ color: '#d4a853', fontWeight: 'bold' }}>{selectedChart.bazi_data.格局}</span></Paragraph>
                    {selectedChart.bazi_data.格局详解 && (
                      <>
                        <Paragraph><Text strong>格局类型：</Text>{selectedChart.bazi_data.格局详解.格局类型 || '正格'}</Paragraph>
                        <Paragraph><Text strong>格局条件：</Text>{selectedChart.bazi_data.格局详解.格局条件 || '月令透干'}</Paragraph>
                        <Paragraph>{selectedChart.bazi_data.格局详解.描述}</Paragraph>
                      </>
                    )}
                    <div style={{ marginTop: 8 }}>
                      <Row gutter={8}>
                        <Col xs={24} sm={8}>
                          <Tag color="gold" style={{ padding: '4px 12px' }}>用神：{selectedChart.bazi_data.用神 || '未知'}</Tag>
                        </Col>
                        <Col xs={24} sm={8}>
                          <Tag color="red" style={{ padding: '4px 12px' }}>忌神：{selectedChart.bazi_data.忌神 || '未知'}</Tag>
                        </Col>
                        <Col xs={24} sm={8}>
                          <Tag color="blue" style={{ padding: '4px 12px' }}>喜神：{selectedChart.bazi_data.喜神 || '未知'}</Tag>
                        </Col>
                      </Row>
                    </div>
                    {selectedChart.bazi_data.格局详解?.古籍引文 && (
                      <div style={{ marginTop: 8 }}>
                        {selectedChart.bazi_data.格局详解.古籍引文.map((quote: string, i: number) => (
                          <Alert key={i} message={quote} type="info" showIcon style={{ marginBottom: 4 }} />
                        ))}
                      </div>
                    )}
                  </Panel>
                  <Panel header="步骤五：排大运" key="dayun">
                    <Row gutter={[8, 8]}>
                      {selectedChart.bazi_data.大运.map((dy: any, index: number) => (
                        <Col xs={12} sm={6} key={index}>
                          <Card size="small">
                            <div style={{ textAlign: 'center' }}>
                              <Text strong>{dy.天干}{dy.地支 || dy.干支?.slice(1)}</Text>
                              <div style={{ fontSize: 12, color: '#b8b8d0' }}>{dy.起始年龄}-{dy.结束年龄}岁</div>
                              <Tag color="purple" style={{ marginTop: 4 }}>{dy.十神 || ''}</Tag>
                            </div>
                          </Card>
                        </Col>
                      ))}
                    </Row>
                    {selectedChart.bazi_data.大运详解 && (
                      <div style={{ marginTop: 8 }}>
                        {selectedChart.bazi_data.大运详解.slice(0, 2).map((dy: any, i: number) => (
                          <Alert key={i} message={`${dy.干支}（${dy.十神}）：${dy.描述}`} description={dy.古籍批断} type="info" showIcon style={{ marginBottom: 4 }} />
                        ))}
                      </div>
                    )}
                  </Panel>
                </Collapse>
              </div>
            ) : (
              <Text type="secondary">暂无八字数据</Text>
            )}
          </Card>

          {/* 紫微计算过程 */}
          {selectedChart.ziwei_data && (
            <Card title="紫微斗数排盘与推演过程">
              {selectedChart.ziwei_data.calculation_process ? (
                <CalculationProcess data={selectedChart.ziwei_data.calculation_process} title="紫微斗数排盘过程" />
              ) : (
                <div>
                  <Collapse defaultActiveKey={['mgsj', 'jumg', 'ssfw', 'sihua', 'yanjiu']}>
                    <Panel header="步骤一：定命宫" key="mgsj">
                      <Paragraph>
                        <Text strong>输入数据：</Text>农历 {selectedChart.ziwei_data.lunar_date.year}年{selectedChart.ziwei_data.lunar_date.month}月{selectedChart.ziwei_data.lunar_date.day}日
                      </Paragraph>
                      <div style={{ background: 'rgba(255,255,255,0.04)', padding: 12, borderRadius: 4, marginBottom: 8 }}>
                        <Text code>命宫在{selectedChart.ziwei_data.palaces.find(p => p.is_ming_palace)?.zhi}宫，天干{selectedChart.ziwei_data.palaces.find(p => p.is_ming_palace)?.tian_gan}</Text>
                      </div>
                      <Alert message="命宫是紫微斗数的核心宫位，代表命主的先天性格和命运基调。" type="info" showIcon />
                    </Panel>
                    <Panel header="步骤二：安主星" key="jumg">
                      <Paragraph><Text strong>五行局：</Text>{selectedChart.ziwei_data.wu_xing_ju}</Paragraph>
                      <Row gutter={[8, 8]} style={{ marginTop: 8 }}>
                        {Object.entries(selectedChart.ziwei_data.main_stars).map(([star, info]: [string, any]) => (
                          <Col xs={12} sm={6} key={star}>
                            <Tag color="blue">{star} → {info.palace || selectedChart.ziwei_data.palaces[info.palace_index]?.name || '未知'}</Tag>
                          </Col>
                        ))}
                      </Row>
                      <Alert message="紫微星系和天府星系是紫微斗数的核心主星体系。" type="info" showIcon />
                    </Panel>
                    <Panel header="步骤三：审三方四正" key="ssfw">
                      {selectedChart.ziwei_data.san_fang_si_zheng ? (
                        <div>
                          <Paragraph><Text strong>三方地支：</Text>{selectedChart.ziwei_data.san_fang_si_zheng['三方地支'].join('、')}</Paragraph>
                          <Paragraph><Text strong>四正地支：</Text>{selectedChart.ziwei_data.san_fang_si_zheng['四正地支'].join('、')}</Paragraph>
                          {selectedChart.ziwei_data.san_fang_si_zheng['三方四正综合分析'] && (
                            <Alert message={selectedChart.ziwei_data.san_fang_si_zheng['三方四正综合分析']} type="info" showIcon />
                          )}
                        </div>
                      ) : (
                        <Text type="secondary">三方四正数据暂缺</Text>
                      )}
                    </Panel>
                    <Panel header="步骤四：安四化飞星" key="sihua">
                      <Row gutter={[8, 8]}>
                        {Object.entries(selectedChart.ziwei_data.sihua).map(([hua, star]) => (
                          <Col xs={12} sm={6} key={hua}>
                            <Card size="small">
                              <div style={{ textAlign: 'center' }}>
                                <Tag color={hua === '禄' ? 'green' : hua === '权' ? 'blue' : hua === '科' ? 'purple' : 'red'}>{hua}</Tag>
                                <div style={{ marginTop: 4 }}><Text strong>{star as string}</Text></div>
                              </div>
                            </Card>
                          </Col>
                        ))}
                      </Row>
                      <Alert message="四化飞星是紫微斗数推演的核心，化禄主财、化权主贵、化科主名、化忌主忌。" type="info" showIcon />
                    </Panel>
                    <Panel header="步骤五：推演命局" key="yanjiu">
                      {selectedChart.ziwei_data.analysis_report ? (
                        <div>
                          {selectedChart.ziwei_data.analysis_report.推演分析.map((step: any, i: number) => (
                            <Alert key={i} message={step.步骤} description={<div><p>{step.分析内容}</p><p style={{color:'#b8b8d0',fontSize:12}}>{step.依据}</p>{step.古籍引用 && <p style={{color:'#d4a853',fontStyle:'italic'}}>{step.古籍引用}</p>}</div>} type="info" showIcon style={{ marginBottom: 8 }} />
                          ))}
                        </div>
                      ) : (
                        <Text type="secondary">推演分析数据暂缺</Text>
                      )}
                    </Panel>
                  </Collapse>
                </div>
              )}
            </Card>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="gf-cloud-pattern" style={{ minHeight: '100vh', padding: 'clamp(12px, 3vw, 24px)' }}>
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
            fontSize: 'clamp(20px, 5vw, 32px)',
            fontWeight: 700,
            letterSpacing: 'clamp(2px, 1vw, 6px)',
          }}>
            命盘查看
          </Title>
        </div>
        <Paragraph style={{ 
          color: '#b8b8d0', 
          fontSize: 16,
          maxWidth: 600,
          margin: '0 auto',
          lineHeight: 1.8,
        }}>
          查看八字排盘、紫微斗数、五行分析等详细信息
        </Paragraph>
        <div className="gf-huiwen-divider" style={{ width: 200, margin: '24px auto' }} />
      </div>

      {/* 命盘选择区域 */}
      <div className="gf-card" style={{ padding: 'clamp(16px, 3vw, 32px)', marginBottom: 24 }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          marginBottom: 24,
          gap: 12,
        }}>
          <StarOutlined style={{ color: '#d4a853', fontSize: 24 }} />
          <Title level={4} className="gf-title" style={{ margin: 0 }}>
            命盘选择
          </Title>
        </div>
        <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
        
        <Row gutter={[16, 16]} align="middle">
          <Col xs={24} sm="auto">
            <Text strong style={{ color: '#ffffff' }}>选择命盘：</Text>
          </Col>
          <Col xs={24} sm={8}>
            <Select
              style={{ width: '100%' }}
              value={selectedChart.id}
              onChange={(value) => {
                const chart = charts.find((c) => c.id === value);
                if (chart) setCurrentChart(chart);
              }}
            >
              {charts.map((chart) => (
                <Option key={chart.id} value={chart.id}>
                  {chart.name}
                </Option>
              ))}
            </Select>
          </Col>
          <Col xs={12} sm="auto">
            <Tag className="gf-tag">{selectedChart.gender === 'male' ? '男' : '女'}</Tag>
          </Col>
          <Col xs={12} sm="auto">
            <Text style={{ color: '#b8b8d0' }}>
              {selectedChart.birth_date} {selectedChart.birth_time}
            </Text>
          </Col>
        </Row>
      </div>

      {/* 命盘内容区域 */}
      <div className="gf-card" style={{ padding: '32px' }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          marginBottom: 24,
          gap: 12,
        }}>
          <CompassOutlined style={{ color: '#d4a853', fontSize: 24 }} />
          <Title level={4} className="gf-title" style={{ margin: 0 }}>
            命盘详情
          </Title>
        </div>
        <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
        
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={tabItems}
          className="gf-tabs"
        />
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

export default ChartView;
