import { Card, Timeline, Typography, Tag, Row, Col } from 'antd';

const { Title, Text } = Typography;

interface DayunTimelineProps {
  data: Array<{
    天干: string;
    地支: string;
    十神: string;
    起始年龄: number;
    结束年龄: number;
  }>;
}

const shishenColors: Record<string, string> = {
  '比肩': '#d4a853',
  '劫财': '#d4a853',
  '食神': '#52c41a',
  '伤官': '#52c41a',
  '正财': '#faad14',
  '偏财': '#faad14',
  '正官': '#d4a853',
  '七杀': '#d4a853',
  '正印': '#eb2f96',
  '偏印': '#eb2f96',
};

function DayunTimeline({ data }: DayunTimelineProps) {
  if (!data || data.length === 0) {
    return (
      <div>
        <Title level={4}>大运流年</Title>
        <Card>
          <Text type="secondary">暂无大运数据</Text>
        </Card>
      </div>
    );
  }

  // 假设当前年龄30岁
  const currentAge = 30;

  return (
    <div>
      <Title level={4}>大运流年</Title>

      <Card>
        <Timeline
          mode="left"
          items={data.map((dayun) => {
            const isCurrent = currentAge >= dayun.起始年龄 && currentAge <= dayun.结束年龄;
            const color = isCurrent ? '#d4a853' : '#d9d9d9';

            return {
              color,
              label: (
                <div style={{ width: 200 }}>
                  <Text strong={isCurrent}>
                    {dayun.起始年龄}-{dayun.结束年龄}岁
                  </Text>
                  {isCurrent && (
                    <Tag color="purple" style={{ marginLeft: 8 }}>
                      当前
                    </Tag>
                  )}
                </div>
              ),
              children: (
                <Card
                  size="small"
                  style={{
                    borderColor: isCurrent ? '#d4a853' : undefined,
                    borderWidth: isCurrent ? 2 : 1,
                  }}
                >
                  <Row gutter={16}>
                    <Col>
                      <div style={{ fontSize: 24, fontWeight: 'bold' }}>
                        {dayun.天干}{dayun.地支}
                      </div>
                    </Col>
                    <Col>
                      <Tag color={shishenColors[dayun.十神] || '#666'}>
                        {dayun.十神}
                      </Tag>
                    </Col>
                  </Row>

                  <div style={{ marginTop: 8, color: '#666' }}>
                    {getDayunDescription(dayun.十神)}
                  </div>
                </Card>
              ),
            };
          })}
        />
      </Card>

      <Card title="大运说明" style={{ marginTop: 16 }}>
        <ul>
          <li>大运每10年一换，影响人生不同阶段的运势走向</li>
          <li>十神代表该阶段的主要能量特征</li>
          <li>紫色标记为当前所处的大运阶段</li>
          <li>大运与命局的配合决定运势起伏</li>
        </ul>
      </Card>
    </div>
  );
}

function getDayunDescription(shishen: string): string {
  const descriptions: Record<string, string> = {
    '比肩': '竞争与合作并存，适合团队发展',
    '劫财': '财运波动，需谨慎投资',
    '食神': '才华展现，适合创意工作',
    '伤官': '突破创新，但需注意口舌',
    '正财': '稳定收入，适合理财规划',
    '偏财': '意外之财，投资运佳',
    '正官': '事业上升，适合晋升发展',
    '七杀': '压力与机遇并存，需努力突破',
    '正印': '贵人相助，学习运佳',
    '偏印': '灵感涌现，适合研究探索',
  };

  return descriptions[shishen] || '运势平稳';
}

export default DayunTimeline;
