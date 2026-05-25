import { Card, Row, Col, Typography, Tag, Timeline, Collapse } from 'antd';

const { Text, Paragraph } = Typography;
const { Panel } = Collapse;

interface CalculationStep {
  step_number: number;
  title: string;
  description: string;
  input_data: Record<string, any>;
  calculation_formula: string;
  calculation_process: string[];
  output_result: any;
  explanation: string;
  references: string[];
}

interface CalculationProcessData {
  engine_name: string;
  calculation_type: string;
  start_time: string;
  end_time: string;
  steps: CalculationStep[];
  final_result: any;
  summary: string;
}

interface CalculationProcessProps {
  data: CalculationProcessData;
  title?: string;
}

function CalculationProcess({ data, title = '计算过程详解' }: CalculationProcessProps) {
  if (!data || !data.steps || data.steps.length === 0) {
    return (
      <Card title={title}>
        <Text type="secondary">暂无计算过程数据</Text>
      </Card>
    );
  }

  const formatValue = (value: any): string => {
    if (value === null || value === undefined) return '无';
    if (typeof value === 'object') return JSON.stringify(value, null, 2);
    return String(value);
  };

  return (
    <Card title={title}>
      {/* 引擎信息 */}
      <Card size="small" style={{ marginBottom: 16, background: '#f5f5f5' }}>
        <Row gutter={16}>
          <Col span={8}>
            <Text strong>引擎名称：</Text>
            <Text>{data.engine_name}</Text>
          </Col>
          <Col span={8}>
            <Text strong>计算类型：</Text>
            <Text>{data.calculation_type}</Text>
          </Col>
          <Col span={8}>
            <Text strong>计算时间：</Text>
            <Text>{data.start_time ? new Date(data.start_time).toLocaleString() : '未知'}</Text>
          </Col>
        </Row>
      </Card>

      {/* 计算步骤 */}
      <Collapse defaultActiveKey={['0']} style={{ marginBottom: 16 }}>
        {data.steps.map((step, index) => (
          <Panel
            header={
              <div>
                <Tag color="blue">步骤 {step.step_number}</Tag>
                <Text strong>{step.title}</Text>
              </div>
            }
            key={index}
          >
            <div style={{ padding: '8px 0' }}>
              {/* 步骤描述 */}
              <Paragraph>
                <Text strong>描述：</Text> {step.description}
              </Paragraph>

              {/* 输入数据 */}
              {step.input_data && Object.keys(step.input_data).length > 0 && (
                <div style={{ marginBottom: 16 }}>
                  <Text strong>输入数据：</Text>
                  <div style={{ background: '#f6f8fa', padding: 8, borderRadius: 4, marginTop: 8 }}>
                    {Object.entries(step.input_data).map(([key, value]) => (
                      <div key={key}>
                        <Text type="secondary">{key}：</Text>
                        <Text>{formatValue(value)}</Text>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* 计算公式 */}
              {step.calculation_formula && (
                <div style={{ marginBottom: 16 }}>
                  <Text strong>计算公式：</Text>
                  <div style={{ background: '#f6f8fa', padding: 8, borderRadius: 4, marginTop: 8 }}>
                    <Text code>{step.calculation_formula}</Text>
                  </div>
                </div>
              )}

              {/* 计算过程 */}
              {step.calculation_process && step.calculation_process.length > 0 && (
                <div style={{ marginBottom: 16 }}>
                  <Text strong>计算过程：</Text>
                  <Timeline
                    style={{ marginTop: 8 }}
                    items={step.calculation_process.map((process) => ({
                      children: <Text>{process}</Text>,
                    }))}
                  />
                </div>
              )}

              {/* 输出结果 */}
              {step.output_result !== null && step.output_result !== undefined && (
                <div style={{ marginBottom: 16 }}>
                  <Text strong>输出结果：</Text>
                  <div style={{ background: '#f6f8fa', padding: 8, borderRadius: 4, marginTop: 8 }}>
                    <Text>{formatValue(step.output_result)}</Text>
                  </div>
                </div>
              )}

              {/* 解释说明 */}
              {step.explanation && (
                <div style={{ marginBottom: 16 }}>
                  <Text strong>解释说明：</Text>
                  <Paragraph style={{ marginTop: 8, background: '#fffbe6', padding: 8, borderRadius: 4 }}>
                    {step.explanation}
                  </Paragraph>
                </div>
              )}

              {/* 参考典籍 */}
              {step.references && step.references.length > 0 && (
                <div>
                  <Text strong>参考典籍：</Text>
                  <div style={{ marginTop: 8 }}>
                    {step.references.map((ref, i) => (
                      <Tag key={i} color="orange" style={{ marginBottom: 4 }}>
                        {ref}
                      </Tag>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </Panel>
        ))}
      </Collapse>

      {/* 计算总结 */}
      {data.summary && (
        <Card size="small" title="计算总结" style={{ background: '#f6ffed' }}>
          <Paragraph>{data.summary}</Paragraph>
        </Card>
      )}

      {/* 最终结果 */}
      {data.final_result !== null && data.final_result !== undefined && (
        <Card size="small" title="最终结果" style={{ marginTop: 16, background: '#f0f5ff' }}>
          <Text>{formatValue(data.final_result)}</Text>
        </Card>
      )}
    </Card>
  );
}

export default CalculationProcess;