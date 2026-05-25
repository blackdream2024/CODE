import { Card, Typography, Row, Col, Tag, Divider, Alert } from 'antd';
import ReactECharts from 'echarts-for-react';

const { Title, Text, Paragraph } = Typography;

interface WuxingRadarProps {
  data: {
    金: number;
    木: number;
    水: number;
    火: number;
    土: number;
  };
  analysis?: {
    五行关系?: string;
    旺衰分析?: string;
    用神忌神?: string;
    五行建议?: string;
  };
}

function WuxingRadar({ data, analysis }: WuxingRadarProps) {
  const option = {
    title: {
      text: '五行力量分布',
      left: 'center',
    },
    tooltip: {},
    radar: {
      indicator: [
        { name: '金', max: 100 },
        { name: '木', max: 100 },
        { name: '水', max: 100 },
        { name: '火', max: 100 },
        { name: '土', max: 100 },
      ],
      shape: 'circle',
      splitNumber: 5,
      axisName: {
        color: '#333',
        fontSize: 14,
      },
      splitLine: {
        lineStyle: {
          color: [
            'rgba(255, 0, 0, 0.1)',
            'rgba(255, 0, 0, 0.2)',
            'rgba(255, 0, 0, 0.3)',
            'rgba(255, 0, 0, 0.4)',
            'rgba(255, 0, 0, 0.5)',
          ],
        },
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(255, 255, 255, 0.5)'],
        },
      },
    },
    series: [
      {
        name: '五行力量',
        type: 'radar',
        data: [
          {
            value: [data.金, data.木, data.水, data.火, data.土],
            name: '五行分布',
            areaStyle: {
              color: 'rgba(114, 46, 209, 0.2)',
            },
            lineStyle: {
              color: '#d4a853',
              width: 2,
            },
            itemStyle: {
              color: '#d4a853',
            },
          },
        ],
      },
    ],
  };

  const total = data.金 + data.木 + data.水 + data.火 + data.土;

  // 五行关系分析
  const wuxingRelations = [
    { name: '相生', description: '金生水、水生木、木生火、火生土、土生金', meaning: '代表促进、帮助、增长的关系' },
    { name: '相克', description: '金克木、木克土、土克水、水克火、火克金', meaning: '代表制约、控制、削弱的关系' },
    { name: '比和', description: '同类五行相遇', meaning: '代表互助、增强、稳定的关系' },
    { name: '泄气', description: '生我者泄气', meaning: '代表消耗、减弱、付出的关系' },
    { name: '耗气', description: '我生者耗气', meaning: '代表消耗、付出、发展中的关系' }
  ];

  // 五行特质详解
  const wuxingDetails = [
    {
      element: '金',
      color: '#FFD700',
      nature: '从革',
      season: '秋季',
      direction: '西方',
      organ: '肺、大肠',
      emotion: '悲、忧',
      virtue: '义气、果断、收敛',
      weakness: '过于刚强、缺乏变通',
      career: '金融、法律、军警、机械',
      advice: '需培养柔性，学会变通'
    },
    {
      element: '木',
      color: '#228B22',
      nature: '曲直',
      season: '春季',
      direction: '东方',
      organ: '肝、胆',
      emotion: '怒',
      virtue: '仁慈、生长、条达',
      weakness: '过于固执、缺乏耐心',
      career: '教育、文化、医疗、环保',
      advice: '需培养耐心，学会坚持'
    },
    {
      element: '水',
      color: '#1E90FF',
      nature: '润下',
      season: '冬季',
      direction: '北方',
      organ: '肾、膀胱',
      emotion: '恐',
      virtue: '智慧、流动、润下',
      weakness: '过于多变、缺乏定性',
      career: '贸易、运输、旅游、传媒',
      advice: '需培养定性，学会专注'
    },
    {
      element: '火',
      color: '#FF4500',
      nature: '炎上',
      season: '夏季',
      direction: '南方',
      organ: '心、小肠',
      emotion: '喜',
      virtue: '礼仪、热情、炎上',
      weakness: '过于急躁、缺乏冷静',
      career: '能源、电子、娱乐、餐饮',
      advice: '需培养冷静，学会思考'
    },
    {
      element: '土',
      color: '#8B4513',
      nature: '稼穑',
      season: '四季末',
      direction: '中央',
      organ: '脾、胃',
      emotion: '思',
      virtue: '诚信、厚重、稼穑',
      weakness: '过于保守、缺乏创新',
      career: '房地产、农业、建筑、会计',
      advice: '需培养创新，学会变通'
    }
  ];

  // 计算五行旺衰
  const getWuxingStatus = (element: string, value: number) => {
    const percentage = (value / total) * 100;
    if (percentage >= 30) return '旺';
    if (percentage >= 20) return '较强';
    if (percentage >= 10) return '中等';
    if (percentage >= 5) return '较弱';
    return '弱';
  };

  // 找出最旺和最弱的五行
  const elements = Object.entries(data);
  const strongest = elements.reduce((a, b) => a[1] > b[1] ? a : b);
  const weakest = elements.reduce((a, b) => a[1] < b[1] ? a : b);

  return (
    <div>
      <Title level={4}>五行分析</Title>

      <Card>
        <ReactECharts option={option} style={{ height: 400 }} />
      </Card>

      <Card title="五行比例与旺衰" style={{ marginTop: 16 }}>
        <Row gutter={[16, 16]}>
          {Object.entries(data).map(([element, value]) => {
            const percentage = ((value / total) * 100).toFixed(1);
            const status = getWuxingStatus(element, value);
            const colors: Record<string, string> = {
              '金': '#FFD700',
              '木': '#228B22',
              '水': '#1E90FF',
              '火': '#FF4500',
              '土': '#8B4513',
            };

            return (
              <Col span={4} key={element} style={{ textAlign: 'center' }}>
                <div
                  style={{
                    fontSize: 24,
                    fontWeight: 'bold',
                    color: colors[element],
                  }}
                >
                  {element}
                </div>
                <div style={{ fontSize: 18 }}>{value}</div>
                <div style={{ color: '#666' }}>{percentage}%</div>
                <Tag color={status === '旺' ? 'red' : status === '弱' ? 'blue' : 'green'}>
                  {status}
                </Tag>
              </Col>
            );
          })}
        </Row>
        
        <Divider />
        
        <Row gutter={16}>
          <Col span={12}>
            <Alert
              message="最旺五行"
              description={`${strongest[0]}（${strongest[1]}）- ${getWuxingStatus(strongest[0], strongest[1])}`}
              type="info"
              showIcon
            />
          </Col>
          <Col span={12}>
            <Alert
              message="最弱五行"
              description={`${weakest[0]}（${weakest[1]}）- ${getWuxingStatus(weakest[0], weakest[1])}`}
              type="warning"
              showIcon
            />
          </Col>
        </Row>
      </Card>

      <Card title="五行关系分析" style={{ marginTop: 16 }}>
        <Paragraph>
          <Text strong>五行相生相克：</Text>五行之间存在相生相克的关系，相生代表促进、帮助，
          相克代表制约、控制。五行平衡则运势平稳，五行偏颇则运势起伏。
        </Paragraph>
        
        <Row gutter={16}>
          {wuxingRelations.map((relation, index) => (
            <Col span={8} key={index}>
              <Card size="small" title={relation.name}>
                <Text>{relation.description}</Text>
                <br />
                <Text type="secondary">{relation.meaning}</Text>
              </Card>
            </Col>
          ))}
        </Row>
        
        {analysis?.五行关系 && (
          <Alert
            message="五行关系分析"
            description={analysis.五行关系}
            type="info"
            showIcon
            style={{ marginTop: 16 }}
          />
        )}
      </Card>

      <Card title="五行特质详解" style={{ marginTop: 16 }}>
        <Row gutter={16}>
          {wuxingDetails.map((detail, index) => (
            <Col span={8} key={index}>
              <Card 
                size="small" 
                title={
                  <span>
                    <span style={{ color: detail.color, fontSize: 18, marginRight: 8 }}>{detail.element}</span>
                    {detail.nature}
                  </span>
                }
              >
                <p><strong>季节：</strong>{detail.season}</p>
                <p><strong>方向：</strong>{detail.direction}</p>
                <p><strong>脏腑：</strong>{detail.organ}</p>
                <p><strong>情志：</strong>{detail.emotion}</p>
                <p><strong>美德：</strong>{detail.virtue}</p>
                <p><strong>弱点：</strong>{detail.weakness}</p>
                <p><strong>适合职业：</strong>{detail.career}</p>
                <p><strong>建议：</strong>{detail.advice}</p>
              </Card>
            </Col>
          ))}
        </Row>
      </Card>

      <Card title="五行解读与建议" style={{ marginTop: 16 }}>
        <Paragraph>
          <Text strong>五行平衡建议：</Text>
          {strongest[0]}过旺，建议通过{weakest[0]}来平衡。具体方法：
        </Paragraph>
        
        <ul>
          <li><strong>饮食调理：</strong>多食用{weakest[0]}属性的食物</li>
          <li><strong>方位调整：</strong>多往{wuxingDetails.find(d => d.element === weakest[0])?.direction}方向发展</li>
          <li><strong>颜色搭配：</strong>多使用{wuxingDetails.find(d => d.element === weakest[0])?.color}颜色</li>
          <li><strong>职业选择：</strong>适合{wuxingDetails.find(d => d.element === weakest[0])?.career}相关行业</li>
        </ul>
        
        {analysis?.旺衰分析 && (
          <Alert
            message="旺衰分析"
            description={analysis.旺衰分析}
            type="info"
            showIcon
            style={{ marginTop: 16 }}
          />
        )}
        
        {analysis?.用神忌神 && (
          <Alert
            message="用神忌神"
            description={analysis.用神忌神}
            type="success"
            showIcon
            style={{ marginTop: 16 }}
          />
        )}
        
        {analysis?.五行建议 && (
          <Alert
            message="五行建议"
            description={analysis.五行建议}
            type="warning"
            showIcon
            style={{ marginTop: 16 }}
          />
        )}
      </Card>
    </div>
  );
}

export default WuxingRadar;
