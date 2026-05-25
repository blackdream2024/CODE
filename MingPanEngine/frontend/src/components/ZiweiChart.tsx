import { useRef, useEffect } from 'react';
import { Card, Row, Col, Typography, Tag, Space, Divider, Tooltip } from 'antd';
import type { ZiweiData } from '../types';

const { Title, Text } = Typography;

interface ZiweiChartProps {
  data: ZiweiData;
}

const starColors: Record<string, string> = {
  main: '#d4a853',
  auxiliary: '#d4a853',
  malefic: '#ff4d4f',
};

const huaColors: Record<string, string> = {
  '禄': '#52c41a',
  '权': '#faad14',
  '科': '#d4a853',
  '忌': '#ff4d4f',
};

function ZiweiChart({ data }: ZiweiChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const size = 640;
    canvas.width = size;
    canvas.height = size;

    // 绘制深色背景
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, size, size);

    // 绘制外边框
    ctx.strokeStyle = '#e6a23c';
    ctx.lineWidth = 3;
    ctx.strokeRect(4, 4, size - 8, size - 8);
    ctx.strokeStyle = '#e6a23c88';
    ctx.lineWidth = 1;
    ctx.strokeRect(8, 8, size - 16, size - 16);

    const cellWidth = (size - 20) / 4;
    const cellHeight = (size - 20) / 3;
    const offsetX = 10;
    const offsetY = 10;

    const palacePositions = [
      { row: 0, col: 0 }, // 命宫
      { row: 0, col: 1 }, // 兄弟宫
      { row: 0, col: 2 }, // 夫妻宫
      { row: 0, col: 3 }, // 子女宫
      { row: 1, col: 3 }, // 财帛宫
      { row: 2, col: 3 }, // 疾厄宫
      { row: 2, col: 2 }, // 迁移宫
      { row: 2, col: 1 }, // 交友宫
      { row: 2, col: 0 }, // 事业宫
      { row: 1, col: 0 }, // 田宅宫
      { row: 1, col: 1 }, // 福德宫
      { row: 1, col: 2 }, // 父母宫
    ];

    data.palaces.forEach((palace, index) => {
      if (index >= 12) return;

      const pos = palacePositions[index];
      const x = offsetX + pos.col * cellWidth;
      const y = offsetY + pos.row * cellHeight;

      // 宫位背景
      ctx.fillStyle = palace.is_ming_palace ? '#2d1b69' : '#16213e';
      ctx.fillRect(x + 2, y + 2, cellWidth - 4, cellHeight - 4);

      // 命宫高亮边框
      if (palace.is_ming_palace) {
        ctx.strokeStyle = '#e6a23c';
        ctx.lineWidth = 2;
        ctx.strokeRect(x + 2, y + 2, cellWidth - 4, cellHeight - 4);
      } else {
        ctx.strokeStyle = '#ffffff22';
        ctx.lineWidth = 1;
        ctx.strokeRect(x + 2, y + 2, cellWidth - 4, cellHeight - 4);
      }

      // 宫位名称
      ctx.fillStyle = palace.is_ming_palace ? '#e6a23c' : '#ffffffcc';
      ctx.font = 'bold 13px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(palace.name, x + cellWidth / 2, y + 18);

      // 天干地支
      ctx.fillStyle = '#999';
      ctx.font = '11px sans-serif';
      ctx.fillText(`${palace.tian_gan}${palace.zhi}`, x + cellWidth / 2, y + 34);

      // 分隔线
      ctx.strokeStyle = '#ffffff15';
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      ctx.moveTo(x + 8, y + 40);
      ctx.lineTo(x + cellWidth - 8, y + 40);
      ctx.stroke();

      // 星曜
      let starY = y + 55;
      palace.stars.forEach((star) => {
        // 主星用金色，辅星用蓝色，煞星用红色
        if (star.category === 'main') {
          ctx.fillStyle = '#e6a23c';
          ctx.font = 'bold 12px sans-serif';
        } else if (star.category === 'auxiliary') {
          ctx.fillStyle = '#69c0ff';
          ctx.font = '11px sans-serif';
        } else {
          ctx.fillStyle = '#ff7875';
          ctx.font = '11px sans-serif';
        }
        ctx.textAlign = 'left';

        // 星曜名称
        ctx.fillText(star.name, x + 10, starY);

        // 四化标记
        if (star.hua && star.hua.length > 0) {
          star.hua.forEach((hua, huaIndex) => {
            const huaColor = huaColors[hua] || '#ff4d4f';
            ctx.fillStyle = huaColor;
            ctx.font = 'bold 10px sans-serif';
            // 圆形背景
            const huaX = x + 55 + huaIndex * 18;
            const huaY = starY - 5;
            ctx.beginPath();
            ctx.arc(huaX, huaY, 7, 0, Math.PI * 2);
            ctx.fillStyle = huaColor + '33';
            ctx.fill();
            ctx.fillStyle = huaColor;
            ctx.textAlign = 'center';
            ctx.fillText(hua, huaX, starY);
          });
        }

        starY += 18;
      });
    });

    // 中心区域 - 深色圆形
    const centerX = size / 2;
    const centerY = size / 2;
    const radius = 45;

    // 绘制圆形背景
    ctx.fillStyle = '#0f3460';
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#e6a23c';
    ctx.lineWidth = 2;
    ctx.stroke();

    // 五行局
    ctx.fillStyle = '#e6a23c';
    ctx.font = 'bold 16px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(data.wu_xing_ju, centerX, centerY - 8);

    // 农历
    ctx.fillStyle = '#ffffffaa';
    ctx.font = '10px sans-serif';
    ctx.fillText(`${data.lunar_date.year}年`, centerX, centerY + 12);
    ctx.fillText(`${data.lunar_date.month}月${data.lunar_date.day}日`, centerX, centerY + 26);

  }, [data]);

  return (
    <div>
      <Title level={4} style={{ marginBottom: 16 }}>紫微命盘</Title>

      <Row gutter={16}>
        <Col xs={24} lg={16}>
          <Card
            style={{
              background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
              borderRadius: 12,
            }}
            bodyStyle={{ padding: 12 }}
          >
            <canvas
              ref={canvasRef}
              style={{
                width: '100%',
                maxWidth: 640,
                height: 'auto',
                borderRadius: 8,
              }}
            />
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          {/* 命盘信息 */}
          <Card
            title="命盘信息"
            style={{ marginBottom: 16 }}
            headStyle={{ background: '#1a1a3e', borderBottom: '2px solid #d4a853' }}
          >
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <div style={{
                textAlign: 'center',
                padding: 12,
                background: '#f0e6ff',
                borderRadius: 8,
              }}>
                <Text type="secondary" style={{ fontSize: 12 }}>五行局</Text>
                <div style={{ fontSize: 22, fontWeight: 'bold', color: '#d4a853', marginTop: 4 }}>
                  {data.wu_xing_ju}
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <Text type="secondary" style={{ fontSize: 11 }}>农历</Text>
                  <div style={{ fontSize: 14, fontWeight: 'bold' }}>
                    {data.lunar_date.year}年
                    {data.lunar_date.is_leap ? '闰' : ''}
                    {data.lunar_date.month}月
                    {data.lunar_date.day}日
                  </div>
                </div>
                <div>
                  <Text type="secondary" style={{ fontSize: 11 }}>年柱</Text>
                  <div style={{ fontSize: 14, fontWeight: 'bold' }}>
                    {data.lunar_date.year_gan}{data.lunar_date.year_zhi}
                  </div>
                </div>
              </div>
            </Space>
          </Card>

          {/* 四化飞星 */}
          <Card
            title="四化飞星"
            style={{ marginBottom: 16 }}
            headStyle={{ background: '#1a1a3e', borderBottom: '2px solid #faad14' }}
          >
            <Row gutter={[8, 8]}>
              {Object.entries(data.sihua || {}).map(([hua, star]) => (
                <Col span={12} key={hua}>
                  <div style={{
                    padding: '8px 12px',
                    background: huaColors[hua] + '15',
                    borderRadius: 6,
                    border: `1px solid ${huaColors[hua]}44`,
                    textAlign: 'center',
                  }}>
                    <div style={{
                      fontSize: 18,
                      fontWeight: 'bold',
                      color: huaColors[hua],
                    }}>
                      {hua}
                    </div>
                    <div style={{ fontSize: 13, color: '#666', marginTop: 4 }}>
                      {star}
                    </div>
                  </div>
                </Col>
              ))}
            </Row>
          </Card>

          {/* 主星分布 */}
          <Card
            title="主星分布"
            headStyle={{ background: '#1a1a3e', borderBottom: '2px solid #d4a853' }}
          >
            <Space direction="vertical" style={{ width: '100%' }} size={8}>
              {Object.entries(data.main_stars || {}).map(([name, info]) => {
                const palace = data.palaces[info.palace_index];
                const hasHua = palace?.stars?.find(s => s.name === name)?.hua;
                return (
                  <div key={name} style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '4px 8px',
                    background: hasHua ? '#fff7e6' : '#1a1a3e',
                    borderRadius: 4,
                    border: hasHua ? '1px solid #ffe58f' : '1px solid #f0f0f0',
                  }}>
                    <div>
                      <Tag color={starColors.main} style={{ fontWeight: 'bold' }}>
                        {name}
                      </Tag>
                      {hasHua && hasHua.map((h: string) => (
                        <Tag key={h} color={huaColors[h]} style={{ fontSize: 10 }}>
                          {h}
                        </Tag>
                      ))}
                    </div>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {palace?.name || `宫位${info.palace_index + 1}`}
                    </Text>
                  </div>
                );
              })}
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default ZiweiChart;
