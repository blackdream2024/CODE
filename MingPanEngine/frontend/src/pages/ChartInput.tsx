import { useState } from 'react';
import { Card, Form, Input, DatePicker, TimePicker, Select, Button, message, Steps, Typography, Divider, Row, Col } from 'antd';
import { UserOutlined, StarOutlined, CompassOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';
import { useChartStore } from '../stores/chartStore';
import { baziApi, ziweiApi } from '../services/api';
import type { ChartData, BaziData, ZiweiData } from '../types';

const { Title, Text, Paragraph } = Typography;
const { Option } = Select;

function ChartInput() {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { addChart, setCurrentChart } = useChartStore();
  const [loading, setLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  const handleSubmit = async (values: any) => {
    setLoading(true);
    try {
      const birthDate = values.birth_date.format('YYYY-MM-DD');
      const birthTime = values.birth_time.format('HH:mm:ss');

      // 调用八字API
      const baziResult = await baziApi.calculate({
        birth_date: birthDate,
        birth_time: birthTime,
        gender: values.gender,
      });

      // 调用紫微API
      let ziweiResult = null;
      try {
        ziweiResult = await ziweiApi.calculate({
          birth_date: birthDate,
          birth_time: birthTime,
          gender: values.gender,
        });
      } catch (error) {
        console.warn('紫微排盘失败，仅使用八字数据:', error);
      }

      // 创建命盘数据
      const chartData: ChartData = {
        id: `chart_${Date.now()}`,
        name: values.name,
        birth_date: birthDate,
        birth_time: birthTime,
        gender: values.gender,
        bazi_data: baziResult.data as BaziData,
        ziwei_data: ziweiResult?.data as ZiweiData | undefined,
      };

      // 保存到store
      addChart(chartData);
      setCurrentChart(chartData);

      message.success('命盘录入成功！');
      setCurrentStep(2);

      // 延迟跳转到查看页面
      setTimeout(() => {
        navigate('/chart-view');
      }, 1500);
    } catch (error) {
      console.error('命盘计算失败:', error);
      message.error('命盘计算失败，请检查输入信息');
    } finally {
      setLoading(false);
    }
  };

  const steps = [
    {
      title: '基本信息',
      content: (
        <Form.Item
          name="name"
          label="命盘名称"
          rules={[{ required: true, message: '请输入命盘名称' }]}
        >
          <Input prefix={<UserOutlined />} placeholder="例如：我的命盘" />
        </Form.Item>
      ),
    },
    {
      title: '出生信息',
      content: (
        <>
          <Form.Item
            name="birth_date"
            label="出生日期"
            rules={[{ required: true, message: '请选择出生日期' }]}
          >
            <DatePicker
              style={{ width: '100%' }}
              placeholder="选择日期"
              disabledDate={(current) => current && current > dayjs().endOf('day')}
            />
          </Form.Item>
          <Form.Item
            name="birth_time"
            label="出生时间"
            rules={[{ required: true, message: '请选择出生时间' }]}
          >
            <TimePicker
              style={{ width: '100%' }}
              format="HH:mm"
              placeholder="选择时间"
            />
          </Form.Item>
          <Form.Item
            name="gender"
            label="性别"
            rules={[{ required: true, message: '请选择性别' }]}
          >
            <Select placeholder="选择性别">
              <Option value="male">男</Option>
              <Option value="female">女</Option>
            </Select>
          </Form.Item>
        </>
      ),
    },
  ];

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
            命盘录入
          </Title>
        </div>
        <Paragraph style={{ 
          color: '#b8b8d0', 
          fontSize: 16,
          maxWidth: 600,
          margin: '0 auto',
          lineHeight: 1.8,
        }}>
          录入您的出生信息，系统将自动计算八字排盘和紫微命盘
        </Paragraph>
        <div className="gf-huiwen-divider" style={{ width: 200, margin: '24px auto' }} />
      </div>

      {/* 主要内容区域 */}
      <Row gutter={[24, 24]}>
        <Col xs={24} lg={16}>
          <div className="gf-card" style={{ padding: '32px' }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              marginBottom: 24,
              gap: 12,
            }}>
              <StarOutlined style={{ color: '#d4a853', fontSize: 24 }} />
              <Title level={4} className="gf-title" style={{ margin: 0 }}>
                录入步骤
              </Title>
            </div>
            <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
            
            <Steps 
              current={currentStep} 
              items={steps.map((s) => ({ title: s.title }))}
              style={{ marginBottom: 32 }}
            />

            <Form
              form={form}
              layout="vertical"
              onFinish={handleSubmit}
            >
              {steps[currentStep]?.content}

              <Form.Item style={{ marginTop: 32 }}>
                {currentStep > 0 && (
                  <Button
                    style={{ marginRight: 16 }}
                    onClick={() => setCurrentStep(currentStep - 1)}
                  >
                    上一步
                  </Button>
                )}
                {currentStep < steps.length - 1 && (
                  <Button type="primary" className="gf-btn-primary" onClick={() => setCurrentStep(currentStep + 1)}>
                    下一步
                  </Button>
                )}
                {currentStep === steps.length - 1 && (
                  <Button type="primary" className="gf-btn-primary" htmlType="submit" loading={loading}>
                    开始排盘
                  </Button>
                )}
              </Form.Item>
            </Form>
          </div>
        </Col>

        <Col xs={24} lg={8}>
          <div className="gf-card" style={{ padding: '32px', height: '100%' }}>
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              marginBottom: 24,
              gap: 12,
            }}>
              <CompassOutlined style={{ color: '#d4a853', fontSize: 24 }} />
              <Title level={4} className="gf-title" style={{ margin: 0 }}>
                输入说明
              </Title>
            </div>
            <Divider className="gf-divider" style={{ margin: '16px 0 24px' }} />
            
            <div style={{ 
              display: 'flex', 
              flexDirection: 'column', 
              gap: 16,
            }}>
              <div style={{ 
                display: 'flex', 
                gap: 12, 
                alignItems: 'flex-start',
                padding: '16px',
                background: 'rgba(212, 168, 83, 0.05)',
                borderRadius: 8,
                border: '1px solid rgba(212, 168, 83, 0.1)',
              }}>
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
                    出生日期
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    请填写阳历生日
                  </Text>
                </div>
              </div>
              <div style={{ 
                display: 'flex', 
                gap: 12, 
                alignItems: 'flex-start',
                padding: '16px',
                background: 'rgba(212, 168, 83, 0.05)',
                borderRadius: 8,
                border: '1px solid rgba(212, 168, 83, 0.1)',
              }}>
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
                    出生时间
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    尽量精确到分钟，不确定可填写大概时间
                  </Text>
                </div>
              </div>
              <div style={{ 
                display: 'flex', 
                gap: 12, 
                alignItems: 'flex-start',
                padding: '16px',
                background: 'rgba(212, 168, 83, 0.05)',
                borderRadius: 8,
                border: '1px solid rgba(212, 168, 83, 0.1)',
              }}>
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
                    性别
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    影响大运排列方向
                  </Text>
                </div>
              </div>
              <div style={{ 
                display: 'flex', 
                gap: 12, 
                alignItems: 'flex-start',
                padding: '16px',
                background: 'rgba(212, 168, 83, 0.05)',
                borderRadius: 8,
                border: '1px solid rgba(212, 168, 83, 0.1)',
              }}>
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
                    自动计算
                  </Text>
                  <Text style={{ color: '#b8b8d0' }}>
                    系统会自动转换农历并计算八字和紫微命盘
                  </Text>
                </div>
              </div>
            </div>
          </div>
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

export default ChartInput;
