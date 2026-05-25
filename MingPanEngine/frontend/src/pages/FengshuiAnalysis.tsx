import { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Select,
  Button,
  message,
  InputNumber,
  Space,
  Tag,
  Divider,
  Empty,
  Tabs,
  Alert,
} from 'antd';
import { EnvironmentOutlined, BookOutlined, StarOutlined, CompassOutlined } from '@ant-design/icons';
import { useChartStore } from '../stores/chartStore';
import { fengshuiApi } from '../services/api';
import FengshuiCompass from '../components/FengshuiCompass';
import CalculationProcess from '../components/CalculationProcess';
import FengshuiMapPicker from '../components/FengshuiMapPicker';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

function FengshuiAnalysis() {
  const { charts } = useChartStore();
  const [chartId, setChartId] = useState<string>('');
  const [buildingYear, setBuildingYear] = useState<number>(2000);
  const [direction, setDirection] = useState<number>(0);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  
  // 新增位置信息状态
  const [address, setAddress] = useState<string>('');
  const [latitude, setLatitude] = useState<number | undefined>();
  const [longitude, setLongitude] = useState<number | undefined>();
  const [buildingName, setBuildingName] = useState<string>('');
  const [floor, setFloor] = useState<number>(1);
  const [totalFloors, setTotalFloors] = useState<number>(6);
  const [buildingType, setBuildingType] = useState<string>('apartment');
  const [nearbyWater, setNearbyWater] = useState<boolean>(false);
  const [waterDirection, setWaterDirection] = useState<string>('south');
  const [nearbyMountain, setNearbyMountain] = useState<boolean>(false);
  const [mountainDirection, setMountainDirection] = useState<string>('north');

  const handleAnalyze = async () => {
    if (!chartId) {
      message.warning('请选择命盘');
      return;
    }

    const chart = charts.find((c) => c.id === chartId);
    if (!chart) {
      message.error('命盘数据不存在');
      return;
    }

    setLoading(true);
    try {
      const response = await fengshuiApi.analyze({
        birth_year: new Date(chart.birth_date).getFullYear(),
        gender: chart.gender,
        building_direction: direction,
        building_year: buildingYear,
        // 位置信息
        address,
        latitude,
        longitude,
        building_name: buildingName,
        floor,
        total_floors: totalFloors,
        building_type: buildingType as any,
        // 环境信息
        nearby_water: nearbyWater,
        water_direction: waterDirection as any,
        nearby_mountain: nearbyMountain,
        mountain_direction: mountainDirection as any,
      });

      setResult(response.data);
      message.success('风水分析完成！');
    } catch (error) {
      console.error('风水分析失败:', error);
      message.error('分析失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  // 处理地图位置选择
  const handleLocationSelect = (location: {
    address: string;
    latitude: number;
    longitude: number;
    building_name?: string;
  }) => {
    setAddress(location.address);
    setLatitude(location.latitude);
    setLongitude(location.longitude);
    if (location.building_name) {
      setBuildingName(location.building_name);
    }
  };

  return (
    <div className="gf-cloud-pattern">
      <div className="gf-bagua-border">
        <Title level={2} className="gf-title-gold" style={{ fontSize: 'clamp(20px, 5vw, 32px)', fontWeight: 700, letterSpacing: 'clamp(2px, 1vw, 6px)' }}>风水分析</Title>
      </div>
      <div className="gf-huiwen-divider" />

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={10}>
          <div className="gf-card">
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
              <StarOutlined style={{ color: '#d4a853', marginRight: 8 }} />
              <Title level={4} style={{ margin: 0, color: '#d4a853' }}>风水配置</Title>
            </div>
            <Space direction="vertical" style={{ width: '100%' }}>
              <div>
                <Text strong>选择命盘：</Text>
                <Select
                  style={{ width: '100%', marginTop: 8 }}
                  placeholder="选择命盘"
                  value={chartId || undefined}
                  onChange={setChartId}
                >
                  {charts.map((chart) => (
                    <Option key={chart.id} value={chart.id}>
                      {chart.name} ({chart.gender === 'male' ? '男' : '女'})
                    </Option>
                  ))}
                </Select>
              </div>

              <div>
                <Text strong>建筑年份：</Text>
                <InputNumber
                  style={{ width: '100%', marginTop: 8 }}
                  min={1900}
                  max={2030}
                  value={buildingYear}
                  onChange={(v) => setBuildingYear(v || 2000)}
                  placeholder="输入建筑年份"
                />
              </div>

              <Divider />

              <FengshuiCompass
                initialDirection={direction}
                onDirectionChange={setDirection}
              />

              {/* 地图选择器 */}
              <FengshuiMapPicker
                onLocationSelect={handleLocationSelect}
                initialAddress={address}
                initialLat={latitude}
                initialLng={longitude}
              />

              {/* 楼层信息 */}
              <Divider />
              <div>
                <Text strong>楼层信息：</Text>
                <Row gutter={16} style={{ marginTop: 8 }}>
                  <Col xs={12} sm={12}>
                    <div>
                      <Text type="secondary">当前楼层：</Text>
                      <InputNumber
                        style={{ width: '100%', marginTop: 4 }}
                        min={1}
                        max={100}
                        value={floor}
                        onChange={(v) => setFloor(v || 1)}
                        placeholder="当前楼层"
                      />
                    </div>
                  </Col>
                  <Col xs={12} sm={12}>
                    <div>
                      <Text type="secondary">总楼层：</Text>
                      <InputNumber
                        style={{ width: '100%', marginTop: 4 }}
                        min={1}
                        max={100}
                        value={totalFloors}
                        onChange={(v) => setTotalFloors(v || 6)}
                        placeholder="总楼层"
                      />
                    </div>
                  </Col>
                </Row>
              </div>

              {/* 建筑类型 */}
              <div style={{ marginTop: 16 }}>
                <Text strong>建筑类型：</Text>
                <Select
                  style={{ width: '100%', marginTop: 8 }}
                  value={buildingType}
                  onChange={setBuildingType}
                >
                  <Option value="apartment">公寓住宅</Option>
                  <Option value="house">别墅独栋</Option>
                  <Option value="office">办公写字楼</Option>
                  <Option value="shop">商铺店面</Option>
                  <Option value="other">其他类型</Option>
                </Select>
              </div>

              {/* 环境信息 */}
              <Divider />
              <div>
                <Text strong>环境信息：</Text>
                <Row gutter={16} style={{ marginTop: 8 }}>
                  <Col xs={24} sm={12}>
                    <div>
                      <Text type="secondary">附近有水：</Text>
                      <Select
                        style={{ width: '100%', marginTop: 4 }}
                        value={nearbyWater}
                        onChange={setNearbyWater}
                      >
                        <Option value={false}>无</Option>
                        <Option value={true}>有</Option>
                      </Select>
                    </div>
                    {nearbyWater && (
                      <div style={{ marginTop: 8 }}>
                        <Text type="secondary">水在何方：</Text>
                        <Select
                          style={{ width: '100%', marginTop: 4 }}
                          value={waterDirection}
                          onChange={setWaterDirection}
                        >
                          <Option value="north">北方</Option>
                          <Option value="south">南方</Option>
                          <Option value="east">东方</Option>
                          <Option value="west">西方</Option>
                          <Option value="northeast">东北</Option>
                          <Option value="northwest">西北</Option>
                          <Option value="southeast">东南</Option>
                          <Option value="southwest">西南</Option>
                        </Select>
                      </div>
                    )}
                  </Col>
                  <Col xs={24} sm={12}>
                    <div>
                      <Text type="secondary">附近有山：</Text>
                      <Select
                        style={{ width: '100%', marginTop: 4 }}
                        value={nearbyMountain}
                        onChange={setNearbyMountain}
                      >
                        <Option value={false}>无</Option>
                        <Option value={true}>有</Option>
                      </Select>
                    </div>
                    {nearbyMountain && (
                      <div style={{ marginTop: 8 }}>
                        <Text type="secondary">山在何方：</Text>
                        <Select
                          style={{ width: '100%', marginTop: 4 }}
                          value={mountainDirection}
                          onChange={setMountainDirection}
                        >
                          <Option value="north">北方</Option>
                          <Option value="south">南方</Option>
                          <Option value="east">东方</Option>
                          <Option value="west">西方</Option>
                          <Option value="northeast">东北</Option>
                          <Option value="northwest">西北</Option>
                          <Option value="southeast">东南</Option>
                          <Option value="southwest">西南</Option>
                        </Select>
                      </div>
                    )}
                  </Col>
                </Row>
              </div>

              <Button
                className="gf-btn-primary"
                icon={<EnvironmentOutlined />}
                onClick={handleAnalyze}
                loading={loading}
                block
                disabled={!chartId}
              >
                开始分析
              </Button>
            </Space>
          </div>
        </Col>

        <Col xs={24} lg={14}>
          {result ? (
            <Tabs
              className="gf-tabs"
              defaultActiveKey="professional"
              items={[
                {
                  key: 'basic',
                  label: '基础分析',
                  children: (
                    <>
                      <Card title="风水综合评分" style={{ marginBottom: 16 }}>
                        <Row gutter={[16, 16]}>
                          <Col xs={24} sm={8}>
                            <Card size="small">
                              <div style={{ textAlign: 'center' }}>
                                <Text strong>综合评分</Text>
                                <div style={{ fontSize: 'clamp(20px, 4vw, 24px)', fontWeight: 'bold', color: '#d4a853' }}>
                                  {result.overall_score?.score || 0}
                                </div>
                              </div>
                            </Card>
                          </Col>
                          <Col xs={24} sm={8}>
                            <Card size="small">
                              <div style={{ textAlign: 'center' }}>
                                <Text strong>吉凶等级</Text>
                                <div style={{ fontSize: 'clamp(20px, 4vw, 24px)', fontWeight: 'bold', color: '#d4a853' }}>
                                  {result.overall_score?.grade || '未知'}
                                </div>
                              </div>
                            </Card>
                          </Col>
                          <Col xs={24} sm={8}>
                            <Card size="small">
                              <div style={{ textAlign: 'center' }}>
                                <Text strong>评价</Text>
                                <div style={{ fontSize: 14, color: '#b8b8d0' }}>
                                  {result.overall_score?.comment || '暂无评价'}
                                </div>
                              </div>
                            </Card>
                          </Col>
                        </Row>
                        {/* 评分明细 */}
                        {result.overall_score?.factors && result.overall_score.factors.length > 0 && (
                          <div style={{ marginTop: 16 }}>
                            <Text strong style={{ color: '#d4a853' }}>评分明细：</Text>
                            <div style={{ marginTop: 8 }}>
                              {result.overall_score.factors.map((factor: string, index: number) => (
                                <Tag key={index} color="gold" style={{ marginBottom: 8, fontSize: 12 }}>
                                  {factor}
                                </Tag>
                              ))}
                            </div>
                          </div>
                        )}
                      </Card>

                      <Card title="八宅分析" style={{ marginBottom: 16 }}>
                        <Row gutter={[16, 16]}>
                          <Col xs={24} sm={12}>
                            <Card size="small">
                              <div style={{ textAlign: 'center' }}>
                                <Text strong>命卦</Text>
                                <div style={{ fontSize: 'clamp(20px, 4vw, 24px)', fontWeight: 'bold', color: '#d4a853' }}>
                                  {result.bazhai_analysis?.ming_gua || '未知'}
                                </div>
                              </div>
                            </Card>
                          </Col>
                          <Col xs={24} sm={12}>
                            <Card size="small">
                              <div style={{ textAlign: 'center' }}>
                                <Text strong>东四命/西四命</Text>
                                <div style={{ fontSize: 'clamp(20px, 4vw, 24px)', fontWeight: 'bold', color: '#1890ff' }}>
                                  {result.bazhai_analysis?.dong_xi || '未知'}
                                </div>
                              </div>
                            </Card>
                          </Col>
                        </Row>
                        <Divider />
                        <Title level={5}>八方吉凶</Title>
                        <Row gutter={[8, 8]}>
                          {Object.entries(result.bazhai_analysis?.directions || {}).map(([dir, info]: [string, any]) => (
                            <Col xs={12} sm={8} md={6} key={dir}>
                              <Card size="small" style={{ textAlign: 'center' }}>
                                <Tag color={info.type === '吉' ? 'green' : 'red'}>{dir}</Tag>
                                <div style={{ marginTop: 4 }}>
                                  <Text strong>{info.star}</Text>
                                </div>
                                <div>
                                  <Text type="secondary">{info.type}</Text>
                                </div>
                              </Card>
                            </Col>
                          ))}
                        </Row>
                      </Card>

                      <Card title="玄空飞星" style={{ marginBottom: 16 }}>
                        <Paragraph>
                          {result.xuankong_analysis?.description || '暂无玄空分析数据'}
                        </Paragraph>
                        {result.xuankong_analysis?.yun_info && (
                          <>
                            <Title level={5}>三元九运</Title>
                            <Row gutter={[16, 16]}>
                              <Col xs={24} sm={8}>
                                <Card size="small">
                                  <div style={{ textAlign: 'center' }}>
                                    <Text strong>当前元运</Text>
                                    <div style={{ fontSize: 'clamp(16px, 3vw, 18px)', fontWeight: 'bold', color: '#d4a853' }}>
                                      {result.xuankong_analysis.yun_info.yun}运
                                    </div>
                                  </div>
                                </Card>
                              </Col>
                              <Col xs={24} sm={8}>
                                <Card size="small">
                                  <div style={{ textAlign: 'center' }}>
                                    <Text strong>年份范围</Text>
                                    <div style={{ fontSize: 14 }}>
                                      {result.xuankong_analysis.yun_info.start_year}-{result.xuankong_analysis.yun_info.end_year}
                                    </div>
                                  </div>
                                </Card>
                              </Col>
                              <Col xs={24} sm={8}>
                                <Card size="small">
                                  <div style={{ textAlign: 'center' }}>
                                    <Text strong>描述</Text>
                                    <div style={{ fontSize: 14 }}>
                                      {result.xuankong_analysis.yun_info.描述}
                                    </div>
                                  </div>
                                </Card>
                              </Col>
                            </Row>
                          </>
                        )}
                        {result.xuankong_analysis?.yearly_stars && (
                          <>
                            <Title level={5}>流年飞星</Title>
                            <Row gutter={[8, 8]}>
                              {Object.entries(result.xuankong_analysis.yearly_stars).map(([dir, star]: [string, any]) => (
                                <Col xs={12} sm={8} md={6} key={dir}>
                                  <Card size="small" style={{ textAlign: 'center' }}>
                                    <Tag color="blue">{dir}</Tag>
                                    <div style={{ marginTop: 4 }}>
                                      <Text strong>{star}</Text>
                                    </div>
                                  </Card>
                                </Col>
                              ))}
                            </Row>
                          </>
                        )}
                        {result.xuankong_analysis?.zibai_combinations && (
                          <>
                            <Title level={5}>紫白飞星组合</Title>
                            <Row gutter={[8, 8]}>
                              {result.xuankong_analysis.zibai_combinations.map((combination: string, index: number) => (
                                <Col xs={12} sm={8} md={6} key={index}>
                                  <Card size="small" style={{ textAlign: 'center' }}>
                                    <Tag color="purple">{combination}</Tag>
                                  </Card>
                                </Col>
                              ))}
                            </Row>
                          </>
                        )}
                        {result.xuankong_analysis?.fengshui_advice && (
                          <>
                            <Title level={5}>玄空风水建议</Title>
                            <ul>
                              {result.xuankong_analysis.fengshui_advice.map((advice: string, index: number) => (
                                <li key={index}>
                                  <Paragraph>{advice}</Paragraph>
                                </li>
                              ))}
                            </ul>
                          </>
                        )}
                      </Card>

                      <Card title="风水建议">
                        <ul>
                          {(result.suggestions || []).map((suggestion: string, index: number) => (
                            <li key={index}>
                              <Paragraph>{suggestion}</Paragraph>
                            </li>
                          ))}
                        </ul>
                        {result.xuankong_analysis?.liu_nian_detail && (
                          <>
                            <Divider />
                            <Title level={5}>流年太岁详情</Title>
                            <Row gutter={[16, 16]}>
                              <Col xs={24} sm={8}>
                                <Card size="small">
                                  <div style={{ textAlign: 'center' }}>
                                    <Text strong>流年干支</Text>
                                    <div style={{ fontSize: 'clamp(16px, 3vw, 18px)', fontWeight: 'bold', color: '#d4a853' }}>
                                      {result.xuankong_analysis.liu_nian_detail.干支}
                                    </div>
                                  </div>
                                </Card>
                              </Col>
                              <Col xs={24} sm={8}>
                                <Card size="small">
                                  <div style={{ textAlign: 'center' }}>
                                    <Text strong>九星</Text>
                                    <div style={{ fontSize: 14 }}>
                                      {result.xuankong_analysis.liu_nian_detail.九星}
                                    </div>
                                  </div>
                                </Card>
                              </Col>
                              <Col xs={24} sm={8}>
                                <Card size="small">
                                  <div style={{ textAlign: 'center' }}>
                                    <Text strong>描述</Text>
                                    <div style={{ fontSize: 14 }}>
                                      {result.xuankong_analysis.liu_nian_detail.描述}
                                    </div>
                                  </div>
                                </Card>
                              </Col>
                            </Row>
                          </>
                        )}
                      </Card>

                      <Card title="风水计算过程" style={{ marginTop: 16 }}>
                        {result.calculation_process ? (
                          <CalculationProcess data={result.calculation_process} title="风水分析计算过程" />
                        ) : (
                          <Text type="secondary">暂无计算过程数据</Text>
                        )}
                      </Card>
                    </>
                  ),
                },
                {
                  key: 'professional',
                  label: '专业分析',
                  children: (
                    <>
                      {/* 风水格局总评 */}
                      {result.风水格局总评 && (
                        <Card title="风水格局总评" style={{ marginBottom: 16 }}>
                          <Row gutter={[16, 16]}>
                            <Col span={24}>
                              <Card size="small" style={{ backgroundColor: 'rgba(212, 168, 83, 0.1)', borderColor: 'rgba(212, 168, 83, 0.3)' }}>
                                <div style={{ textAlign: 'center' }}>
                                  <Text strong style={{ fontSize: 16 }}>综合评级</Text>
                                  <div style={{ fontSize: 28, fontWeight: 'bold', color: '#d4a853', marginTop: 8 }}>
                                    {result.风水格局总评.综合评级}
                                  </div>
                                </div>
                              </Card>
                            </Col>
                          </Row>
                          {/* 评分因素明细 */}
                          {result.风水格局总评.评分因素 && result.风水格局总评.评分因素.length > 0 && (
                            <div style={{ marginTop: 16 }}>
                              <Text strong style={{ color: '#d4a853' }}>评分因素：</Text>
                              <div style={{ marginTop: 8 }}>
                                {result.风水格局总评.评分因素.map((factor: string, index: number) => (
                                  <Tag key={index} color="gold" style={{ marginBottom: 8, fontSize: 12 }}>
                                    {factor}
                                  </Tag>
                                ))}
                              </div>
                            </div>
                          )}
                          <Divider />
                          <Row gutter={[16, 16]}>
                            <Col xs={24} sm={12}>
                              <Card size="small" title="财运格局">
                                <Paragraph>{result.风水格局总评.财运格局}</Paragraph>
                              </Card>
                            </Col>
                            <Col xs={24} sm={12}>
                              <Card size="small" title="健康格局">
                                <Paragraph>{result.风水格局总评.健康格局}</Paragraph>
                              </Card>
                            </Col>
                          </Row>
                          <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
                            <Col xs={24} sm={12}>
                              <Card size="small" title="事业格局">
                                <Paragraph>{result.风水格局总评.事业格局}</Paragraph>
                              </Card>
                            </Col>
                            <Col xs={24} sm={12}>
                              <Card size="small" title="感情格局">
                                <Paragraph>{result.风水格局总评.感情格局}</Paragraph>
                              </Card>
                            </Col>
                          </Row>
                          {result.风水格局总评.古籍总论 && (
                            <Alert
                              message="古籍总论"
                              description={result.风水格局总评.古籍总论}
                              type="success"
                              showIcon
                              icon={<BookOutlined />}
                              style={{ marginTop: 16 }}
                            />
                          )}
                        </Card>
                      )}

                      {/* 古籍风水批断 */}
                      {result.古籍风水批断 && (
                        <Card
                          title={
                            <span>
                              <BookOutlined style={{ marginRight: 8 }} />
                              古籍风水批断
                            </span>
                          }
                          style={{ marginBottom: 16 }}
                        >
                          {result.古籍风水批断.沈氏玄空学 && (
                            <Card
                              size="small"
                              title="《沈氏玄空学》论玄空飞星"
                              style={{ marginBottom: 12, borderLeft: '4px solid #d4a853' }}
                            >
                              <Paragraph style={{ fontStyle: 'italic', color: '#b8b8d0' }}>
                                {result.古籍风水批断.沈氏玄空学}
                              </Paragraph>
                            </Card>
                          )}
                          {result.古籍风水批断.八宅明镜 && (
                            <Card
                              size="small"
                              title="《八宅明镜》论八宅风水"
                              style={{ marginBottom: 12, borderLeft: '4px solid #d4a853' }}
                            >
                              <Paragraph style={{ fontStyle: 'italic', color: '#b8b8d0' }}>
                                {result.古籍风水批断.八宅明镜}
                              </Paragraph>
                            </Card>
                          )}
                          {result.古籍风水批断.阳宅三要 && (
                            <Card
                              size="small"
                              title="《阳宅三要》论门主灶"
                              style={{ marginBottom: 12, borderLeft: '4px solid #d4a853' }}
                            >
                              <Paragraph style={{ fontStyle: 'italic', color: '#b8b8d0' }}>
                                {result.古籍风水批断.阳宅三要}
                              </Paragraph>
                            </Card>
                          )}
                          {result.古籍风水批断.风水总评 && (
                            <Alert
                              message="风水综合总评"
                              description={result.古籍风水批断.风水总评}
                              type="warning"
                              showIcon
                              icon={<BookOutlined />}
                              style={{ marginTop: 12 }}
                            />
                          )}
                        </Card>
                      )}

                      {/* 八宅详解 */}
                      {result.八宅详解 && (
                        <Card title="八宅详解" style={{ marginBottom: 16 }}>
                          <Row gutter={[16, 16]}>
                            <Col xs={24} sm={8}>
                              <Card size="small" title="命卦分析">
                                <Paragraph>{result.八宅详解.命卦分析}</Paragraph>
                              </Card>
                            </Col>
                            <Col xs={24} sm={8}>
                              <Card size="small" title="宅卦分析">
                                <Paragraph>{result.八宅详解.宅卦分析}</Paragraph>
                              </Card>
                            </Col>
                            <Col xs={24} sm={8}>
                              <Card size="small" title="命宅配合" style={{ backgroundColor: 'rgba(212, 168, 83, 0.1)' }}>
                                <Paragraph>{result.八宅详解.命宅配合}</Paragraph>
                              </Card>
                            </Col>
                          </Row>
                          {result.八宅详解.吉凶方位详解 && (
                            <>
                              <Divider />
                              <Title level={5}>吉凶方位详解</Title>
                              <Row gutter={[12, 12]}>
                                {result.八宅详解.吉凶方位详解.map((item: any, index: number) => (
                                  <Col xs={24} sm={12} key={index}>
                                    <Card
                                      size="small"
                                      style={{
                                        borderLeft: `4px solid ${item.吉凶 === '最吉' || item.吉凶 === '次吉' || item.吉凶 === '三吉' || item.吉凶 === '小吉' ? '#52c41a' : '#ff4d4f'}`,
                                      }}
                                    >
                                      <div style={{ marginBottom: 8 }}>
                                        <Tag color={item.吉凶 === '最吉' || item.吉凶 === '次吉' || item.吉凶 === '三吉' || item.吉凶 === '小吉' ? 'green' : 'red'}>
                                          {item.吉凶}
                                        </Tag>
                                        <Text strong style={{ marginLeft: 8 }}>{item.方位}</Text>
                                      </div>
                                      <div>
                                        <Text type="secondary">星名：</Text>
                                        <Text>{item.星名}</Text>
                                      </div>
                                      <div>
                                        <Text type="secondary">应用：</Text>
                                        <Text>{item.应用}</Text>
                                      </div>
                                      {item.古籍论述 && (
                                        <Alert
                                          message={item.古籍论述}
                                          type="info"
                                          style={{ marginTop: 8, fontSize: 12 }}
                                        />
                                      )}
                                    </Card>
                                  </Col>
                                ))}
                              </Row>
                            </>
                          )}
                        </Card>
                      )}

                      {/* 玄空详解 */}
                      {result.玄空详解 && (
                        <Card title="玄空详解" style={{ marginBottom: 16 }}>
                          <Row gutter={[16, 16]}>
                            <Col xs={24} sm={12}>
                              <Card size="small" title="当运分析">
                                <Paragraph>{result.玄空详解.当运分析}</Paragraph>
                              </Card>
                            </Col>
                            <Col xs={24} sm={12}>
                              <Card size="small" title="山星向星">
                                <Paragraph>{result.玄空详解.山星向星}</Paragraph>
                              </Card>
                            </Col>
                          </Row>

                          {result.玄空详解.飞星组合详解 && (
                            <>
                              <Divider />
                              <Title level={5}>飞星组合详解</Title>
                              <Row gutter={[12, 12]}>
                                {result.玄空详解.飞星组合详解.map((item: any, index: number) => (
                                  <Col xs={24} sm={12} key={index}>
                                    <Card size="small" style={{ borderLeft: `4px solid ${item.吉凶 === '吉' ? '#52c41a' : '#ff4d4f'}` }}>
                                      <div style={{ marginBottom: 8 }}>
                                        <Tag color={item.吉凶 === '吉' ? 'green' : 'red'}>{item.吉凶}</Tag>
                                        <Text strong style={{ marginLeft: 8 }}>{item.组合}</Text>
                                      </div>
                                      <div>
                                        <Text type="secondary">应用：</Text>
                                        <Text>{item.应用}</Text>
                                      </div>
                                      {item.古籍论述 && (
                                        <Alert
                                          message={item.古籍论述}
                                          type="info"
                                          style={{ marginTop: 8, fontSize: 12 }}
                                        />
                                      )}
                                    </Card>
                                  </Col>
                                ))}
                              </Row>
                            </>
                          )}

                          {result.玄空详解.流年飞星详解 && (
                            <>
                              <Divider />
                              <Title level={5}>流年飞星详解</Title>
                              <Alert
                                message="2026年流年飞星"
                                description={result.玄空详解.流年飞星详解}
                                type="warning"
                                showIcon
                              />
                            </>
                          )}

                          {result.玄空详解.化煞建议 && (
                            <>
                              <Divider />
                              <Title level={5}>化煞建议</Title>
                              <ul>
                                {result.玄空详解.化煞建议.map((advice: string, index: number) => (
                                  <li key={index}>
                                    <Paragraph>{advice}</Paragraph>
                                  </li>
                                ))}
                              </ul>
                            </>
                          )}
                        </Card>
                      )}
                    </>
                  ),
                },
              ]}
            />
          ) : (
            <div className="gf-card">
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: 16 }}>
                <CompassOutlined style={{ color: '#d4a853', marginRight: 8 }} />
                <Title level={4} style={{ margin: 0, color: '#d4a853' }}>风水分析</Title>
              </div>
              <Empty
                description="请选择命盘并设置建筑信息进行风水分析"
                image={Empty.PRESENTED_IMAGE_SIMPLE}
              />
            </div>
          )}
        </Col>
      </Row>
      <div className="gf-huiwen-divider" />
      <div style={{ textAlign: 'center', marginTop: 16, color: '#b8b8d0', fontSize: 12 }}>
        命盘推演系统 · 融合传统智慧与现代科技
      </div>
    </div>
  );
}

export default FengshuiAnalysis;
