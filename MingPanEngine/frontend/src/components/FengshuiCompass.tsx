import { useRef, useEffect, useState } from 'react';
import { Card, Typography, Tag, Row, Col, Space, Slider, InputNumber, Button, message } from 'antd';
import { CompassOutlined, EnvironmentOutlined } from '@ant-design/icons';

const { Text, Paragraph } = Typography;

interface FengshuiCompassProps {
  onDirectionChange?: (direction: number) => void;
  initialDirection?: number;
}

const directionNames: Record<string, string> = {
  'N': '北',
  'NE': '东北',
  'E': '东',
  'SE': '东南',
  'S': '南',
  'SW': '西南',
  'W': '西',
  'NW': '西北',
};

const directionColors: Record<string, string> = {
  'N': '#1E90FF',
  'NE': '#8B4513',
  'E': '#228B22',
  'SE': '#FFD700',
  'S': '#FF4500',
  'SW': '#8B4513',
  'W': '#FFD700',
  'NW': '#228B22',
};

function FengshuiCompass({ onDirectionChange, initialDirection = 0 }: FengshuiCompassProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [direction, setDirection] = useState(initialDirection);
  const [selectedDirection, setSelectedDirection] = useState<string>('');

  const getDirectionLabel = (angle: number): string => {
    const normalized = ((angle % 360) + 360) % 360;
    if (normalized >= 337.5 || normalized < 22.5) return 'N';
    if (normalized >= 22.5 && normalized < 67.5) return 'NE';
    if (normalized >= 67.5 && normalized < 112.5) return 'E';
    if (normalized >= 112.5 && normalized < 157.5) return 'SE';
    if (normalized >= 157.5 && normalized < 202.5) return 'S';
    if (normalized >= 202.5 && normalized < 247.5) return 'SW';
    if (normalized >= 247.5 && normalized < 292.5) return 'W';
    return 'NW';
  };

  const drawCompass = (ctx: CanvasRenderingContext2D, size: number) => {
    const centerX = size / 2;
    const centerY = size / 2;
    const radius = size * 0.4;

    // 清空画布
    ctx.clearRect(0, 0, size, size);

    // 绘制外圆
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.strokeStyle = '#d9d9d9';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 绘制内圆
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 0.8, 0, Math.PI * 2);
    ctx.strokeStyle = '#d9d9d9';
    ctx.lineWidth = 1;
    ctx.stroke();

    // 绘制中心点
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#d4a853';
    ctx.fill();

    // 绘制方向线和文字
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const directionAngles = [0, 45, 90, 135, 180, 225, 270, 315];

    directions.forEach((dir, index) => {
      const angle = (directionAngles[index] * Math.PI) / 180;
      const x1 = centerX + Math.cos(angle - Math.PI / 2) * radius * 0.9;
      const y1 = centerY + Math.sin(angle - Math.PI / 2) * radius * 0.9;
      const x2 = centerX + Math.cos(angle - Math.PI / 2) * radius;
      const y2 = centerY + Math.sin(angle - Math.PI / 2) * radius;

      // 绘制方向线
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = directionColors[dir];
      ctx.lineWidth = dir === 'N' ? 3 : 1;
      ctx.stroke();

      // 绘制方向文字
      const textX = centerX + Math.cos(angle - Math.PI / 2) * radius * 1.15;
      const textY = centerY + Math.sin(angle - Math.PI / 2) * radius * 1.15;

      ctx.fillStyle = dir === selectedDirection ? '#d4a853' : '#333';
      ctx.font = dir === selectedDirection ? 'bold 14px sans-serif' : '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(directionNames[dir], textX, textY);
    });

    // 绘制指针（当前方向）
    const pointerAngle = ((direction - 90) * Math.PI) / 180;
    const pointerLength = radius * 0.7;

    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.lineTo(
      centerX + Math.cos(pointerAngle) * pointerLength,
      centerY + Math.sin(pointerAngle) * pointerLength
    );
    ctx.strokeStyle = '#ff4d4f';
    ctx.lineWidth = 3;
    ctx.stroke();

    // 绘制指针头部
    const arrowSize = 10;
    const arrowX = centerX + Math.cos(pointerAngle) * pointerLength;
    const arrowY = centerY + Math.sin(pointerAngle) * pointerLength;

    ctx.beginPath();
    ctx.moveTo(arrowX, arrowY);
    ctx.lineTo(
      arrowX + Math.cos(pointerAngle + 2.5) * arrowSize,
      arrowY + Math.sin(pointerAngle + 2.5) * arrowSize
    );
    ctx.lineTo(
      arrowX + Math.cos(pointerAngle - 2.5) * arrowSize,
      arrowY + Math.sin(pointerAngle - 2.5) * arrowSize
    );
    ctx.closePath();
    ctx.fillStyle = '#ff4d4f';
    ctx.fill();
  };

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const size = 300;
    canvas.width = size;
    canvas.height = size;

    drawCompass(ctx, size);
  }, [direction, selectedDirection]);

  const handleDirectionChange = (value: number) => {
    setDirection(value);
    setSelectedDirection(getDirectionLabel(value));
    onDirectionChange?.(value);
  };

  const handleQuickDirection = (dir: string) => {
    const angles: Record<string, number> = {
      'N': 0,
      'NE': 45,
      'E': 90,
      'SE': 135,
      'S': 180,
      'SW': 225,
      'W': 270,
      'NW': 315,
    };

    const angle = angles[dir] || 0;
    setDirection(angle);
    setSelectedDirection(dir);
    onDirectionChange?.(angle);
    message.success(`已设置朝向：${directionNames[dir]}`);
  };

  return (
    <Card title="风水罗盘" extra={<CompassOutlined />}>
      <Row gutter={16}>
        <Col xs={24} md={12}>
          <div style={{ textAlign: 'center' }}>
            <canvas
              ref={canvasRef}
              style={{
                width: '100%',
                maxWidth: 300,
                height: 'auto',
                border: '1px solid #d9d9d9',
                borderRadius: '50%',
              }}
            />
          </div>
        </Col>

        <Col xs={24} md={12}>
          <Space direction="vertical" style={{ width: '100%' }}>
            <div>
              <Text strong>当前朝向：</Text>
              <Tag color="purple" style={{ marginLeft: 8 }}>
                {directionNames[selectedDirection] || '未设置'} ({direction}°)
              </Tag>
            </div>

            <div>
              <Text strong>调节角度：</Text>
              <Slider
                min={0}
                max={359}
                value={direction}
                onChange={handleDirectionChange}
                marks={{
                  0: '北',
                  45: '东北',
                  90: '东',
                  135: '东南',
                  180: '南',
                  225: '西南',
                  270: '西',
                  315: '西北',
                }}
              />
            </div>

            <div>
              <Text strong>快速选择：</Text>
              <div style={{ marginTop: 8 }}>
                <Space wrap>
                  {Object.entries(directionNames).map(([key, name]) => (
                    <Button
                      key={key}
                      size="small"
                      type={selectedDirection === key ? 'primary' : 'default'}
                      onClick={() => handleQuickDirection(key)}
                      style={{
                        borderColor: directionColors[key],
                        color: selectedDirection === key ? '#fff' : directionColors[key],
                        backgroundColor: selectedDirection === key ? directionColors[key] : undefined,
                      }}
                    >
                      {name}
                    </Button>
                  ))}
                </Space>
              </div>
            </div>

            <div>
              <Text strong>精确输入：</Text>
              <Space style={{ marginTop: 8 }}>
                <InputNumber
                  min={0}
                  max={359}
                  value={direction}
                  onChange={(v) => handleDirectionChange(v || 0)}
                  addonAfter="°"
                />
              </Space>
            </div>
          </Space>
        </Col>
      </Row>

      <Card title="风水说明" style={{ marginTop: 16 }}>
        <Paragraph>
          <EnvironmentOutlined /> 罗盘用于确定建筑朝向，是风水分析的基础工具。
        </Paragraph>
        <ul>
          <li>北方（N）：坎卦，属水，代表事业运</li>
          <li>南方（S）：离卦，属火，代表名声运</li>
          <li>东方（E）：震卦，属木，代表健康运</li>
          <li>西方（W）：兑卦，属金，代表子孙运</li>
          <li>东北（NE）：艮卦，属土，代表学业运</li>
          <li>东南（SE）：巽卦，属木，代表财运</li>
          <li>西南（SW）：坤卦，属土，代表婚姻运</li>
          <li>西北（NW）：乾卦，属金，代表贵人运</li>
        </ul>
      </Card>
    </Card>
  );
}

export default FengshuiCompass;
