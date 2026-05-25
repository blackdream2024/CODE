import { Card, Row, Col, Typography, Tag, Divider, Tooltip } from 'antd';
import type { BaziData } from '../types';

const { Title, Text } = Typography;

interface BaziChartProps {
  data: BaziData;
}

const wuxingColors: Record<string, string> = {
  '金': '#DAA520',
  '木': '#2E8B57',
  '水': '#4169E1',
  '火': '#DC143C',
  '土': '#8B6914',
};

const wuxingBg: Record<string, string> = {
  '金': '#FFF8DC',
  '木': '#F0FFF0',
  '水': '#F0F8FF',
  '火': '#FFF0F5',
  '土': '#FAF0E6',
};

const tianGanWuxing: Record<string, string> = {
  '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
  '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
};

const tianGanYinYang: Record<string, string> = {
  '甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳',
  '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴',
};

const diZhiWuxing: Record<string, string> = {
  '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
  '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水',
};

const diZhiCangGan: Record<string, string[]> = {
  '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'],
  '卯': ['乙'], '辰': ['戊', '乙', '癸'], '巳': ['丙', '庚', '戊'],
  '午': ['丁', '己'], '未': ['己', '丁', '乙'], '申': ['庚', '壬', '戊'],
  '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲'],
};

function BaziChart({ data }: BaziChartProps) {
  const pillars = [
    { label: '年柱', ...data.四柱.年柱, nayin: data.纳音?.年柱 },
    { label: '月柱', ...data.四柱.月柱, nayin: data.纳音?.月柱 },
    { label: '日柱', ...data.四柱.日柱, nayin: data.纳音?.日柱 },
    { label: '时柱', ...data.四柱.时柱, nayin: data.纳音?.时柱 },
  ];

  const shishen = data.十神 || {};
  const shensha = data.神煞 || [];
  const changsheng = data.十二长生 || {};
  const kongwang = data.空亡;

  return (
    <div>
      {/* 四柱八字主体 */}
      <div style={{
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
        borderRadius: 12,
        padding: 24,
        marginBottom: 24,
        boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
      }}>
        <div style={{
          textAlign: 'center',
          marginBottom: 20,
          borderBottom: '2px solid rgba(255,255,255,0.1)',
          paddingBottom: 16,
        }}>
          <Text style={{ color: '#e6a23c', fontSize: 18, fontWeight: 'bold', letterSpacing: 4 }}>
            四 柱 八 字
          </Text>
        </div>

        <Row gutter={0} justify="center">
          {pillars.map((pillar, index) => {
            const tianGanWX = tianGanWuxing[pillar.天干] || '';
            const diZhiWX = diZhiWuxing[pillar.地支] || '';
            const tianGanYY = tianGanYinYang[pillar.天干] || '';
            const shishenKey = index === 2 ? '日主' : `${pillar.天干}${index}`;
            const shishenValue = shishen[shishenKey] || '';
            const cangGan = diZhiCangGan[pillar.地支] || [];
            const changshengInfo = changsheng[pillar.label] || changsheng[['年柱', '月柱', '日柱', '时柱'][index]];
            const isRiZhu = index === 2;
            const shenshaForPillar = shensha.filter((s: any) => s.位置?.includes(pillar.地支) || s.位置?.includes(pillar.label));

            return (
              <Col xs={12} sm={6} key={pillar.label}>
                <div style={{
                  textAlign: 'center',
                  padding: '0 8px',
                  borderRight: index < 3 ? '1px solid rgba(255,255,255,0.1)' : 'none',
                }}>
                  {/* 柱名 */}
                  <div style={{
                    color: '#999',
                    fontSize: 13,
                    marginBottom: 12,
                    letterSpacing: 2,
                  }}>
                    {pillar.label}
                  </div>

                  {/* 十神 */}
                  {shishenValue && (
                    <div style={{ marginBottom: 8 }}>
                      <Tag
                        color={isRiZhu ? '#d4a853' : '#e6a23c'}
                        style={{ fontSize: 12, borderRadius: 4 }}
                      >
                        {shishenValue}
                      </Tag>
                    </div>
                  )}

                  {/* 天干 */}
                  <Tooltip title={`${tianGanYY}${tianGanWX} ${pillar.天干}`}>
                    <div style={{
                      width: 64,
                      height: 64,
                      margin: '0 auto 8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      borderRadius: 8,
                      background: isRiZhu
                        ? `linear-gradient(135deg, ${wuxingColors[tianGanWX]}22, ${wuxingColors[tianGanWX]}44)`
                        : wuxingBg[tianGanWX],
                      border: isRiZhu ? `2px solid ${wuxingColors[tianGanWX]}` : `1px solid ${wuxingColors[tianGanWX]}66`,
                      boxShadow: isRiZhu ? `0 0 12px ${wuxingColors[tianGanWX]}44` : 'none',
                    }}>
                      <span style={{
                        fontSize: 32,
                        fontWeight: 'bold',
                        color: isRiZhu ? wuxingColors[tianGanWX] : wuxingColors[tianGanWX],
                        textShadow: isRiZhu ? `0 0 8px ${wuxingColors[tianGanWX]}66` : 'none',
                      }}>
                        {pillar.天干}
                      </span>
                    </div>
                  </Tooltip>

                  {/* 天干五行标签 */}
                  <div style={{ marginBottom: 12 }}>
                    <Tag
                      color={wuxingColors[tianGanWX]}
                      style={{ fontSize: 11, borderRadius: 4, opacity: 0.8 }}
                    >
                      {tianGanYY}{tianGanWX}
                    </Tag>
                  </div>

                  {/* 地支 */}
                  <Tooltip title={`${diZhiWuxing[pillar.地支]} ${pillar.地支}`}>
                    <div style={{
                      width: 64,
                      height: 64,
                      margin: '0 auto 8px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      borderRadius: 8,
                      background: wuxingBg[diZhiWX],
                      border: `1px solid ${wuxingColors[diZhiWX]}66`,
                    }}>
                      <span style={{
                        fontSize: 32,
                        fontWeight: 'bold',
                        color: wuxingColors[diZhiWX],
                      }}>
                        {pillar.地支}
                      </span>
                    </div>
                  </Tooltip>

                  {/* 地支五行标签 */}
                  <div style={{ marginBottom: 8 }}>
                    <Tag
                      color={wuxingColors[diZhiWX]}
                      style={{ fontSize: 11, borderRadius: 4, opacity: 0.8 }}
                    >
                      {diZhiWX}
                    </Tag>
                  </div>

                  {/* 纳音 */}
                  {pillar.nayin && (
                    <div style={{
                      marginTop: 12,
                      padding: '4px 8px',
                      background: 'rgba(114, 46, 209, 0.15)',
                      borderRadius: 4,
                      border: '1px solid rgba(114, 46, 209, 0.3)',
                    }}>
                      <Text style={{ color: '#b37feb', fontSize: 11 }}>
                        {pillar.nayin.五行}
                      </Text>
                    </div>
                  )}

                  {/* 十二长生 */}
                  {changshengInfo && (
                    <div style={{ marginTop: 8 }}>
                      <Text style={{ color: '#8c8c8c', fontSize: 10 }}>
                        {changshengInfo.阶段}
                      </Text>
                    </div>
                  )}
                </div>
              </Col>
            );
          })}
        </Row>

        {/* 空亡 */}
        {kongwang && (
          <div style={{
            marginTop: 20,
            paddingTop: 16,
            borderTop: '1px solid rgba(255,255,255,0.1)',
            textAlign: 'center',
          }}>
            <Text style={{ color: '#999', fontSize: 12 }}>
              空亡：
              <span style={{ color: '#ff7875', marginLeft: 8 }}>
                {kongwang.空亡?.join(' ')}
              </span>
            </Text>
          </div>
        )}
      </div>

      {/* 日主信息卡片 */}
      <Card
        title="日主信息"
        style={{ marginBottom: 16 }}
        headStyle={{ background: '#1a1a3e', borderBottom: '2px solid #e6a23c' }}
      >
        <Row gutter={[16, 16]}>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Text type="secondary" style={{ fontSize: 12 }}>日主</Text>
              <div style={{
                fontSize: 28,
                fontWeight: 'bold',
                color: wuxingColors[tianGanWuxing[data.日主]],
                marginTop: 4,
              }}>
                {data.日主}
              </div>
              <Tag color={wuxingColors[tianGanWuxing[data.日主]]}>
                {tianGanYinYang[data.日主]}{tianGanWuxing[data.日主]}
              </Tag>
            </div>
          </Col>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Text type="secondary" style={{ fontSize: 12 }}>旺衰</Text>
              <div style={{
                fontSize: 20,
                fontWeight: 'bold',
                color: data.旺衰 === '身旺' ? '#52c41a' : data.旺衰 === '身弱' ? '#ff4d4f' : '#faad14',
                marginTop: 8,
              }}>
                {data.旺衰}
              </div>
            </div>
          </Col>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Text type="secondary" style={{ fontSize: 12 }}>格局</Text>
              <div style={{
                fontSize: 18,
                fontWeight: 'bold',
                color: '#d4a853',
                marginTop: 8,
              }}>
                {data.格局}
              </div>
            </div>
          </Col>
          <Col span={6}>
            <div style={{ textAlign: 'center' }}>
              <Text type="secondary" style={{ fontSize: 12 }}>用神</Text>
              <div style={{
                fontSize: 20,
                fontWeight: 'bold',
                color: wuxingColors[data.用神 || ''],
                marginTop: 8,
              }}>
                {data.用神 || '-'}
              </div>
              {data.忌神 && (
                <Text style={{ color: '#999', fontSize: 11 }}>
                  忌：{data.忌神}
                </Text>
              )}
            </div>
          </Col>
        </Row>
      </Card>

      {/* 地支藏干 */}
      <Card
        title="地支藏干"
        style={{ marginBottom: 16 }}
        headStyle={{ background: '#1a1a3e', borderBottom: '2px solid #d4a853' }}
      >
        <Row gutter={[16, 16]}>
          {Object.entries(data.地支藏干 || {}).map(([zhi, cangGan]) => (
            <Col span={6} key={zhi}>
              <div style={{
                textAlign: 'center',
                padding: 12,
                background: wuxingBg[diZhiWuxing[zhi]],
                borderRadius: 8,
                border: `1px solid ${wuxingColors[diZhiWuxing[zhi]]}44`,
              }}>
                <div style={{
                  fontSize: 20,
                  fontWeight: 'bold',
                  color: wuxingColors[diZhiWuxing[zhi]],
                  marginBottom: 8,
                }}>
                  {zhi}
                </div>
                <div>
                  {Array.isArray(cangGan) ? cangGan.map((gan: string, i: number) => (
                    <Tag
                      key={i}
                      color={wuxingColors[tianGanWuxing[gan]]}
                      style={{ margin: '2px', fontSize: 12 }}
                    >
                      {gan}
                    </Tag>
                  )) : (
                    <Tag color={wuxingColors[tianGanWuxing[cangGan]]}>
                      {cangGan}
                    </Tag>
                  )}
                </div>
              </div>
            </Col>
          ))}
        </Row>
      </Card>

      {/* 神煞 */}
      {shensha.length > 0 && (
        <Card
          title="神煞"
          style={{ marginBottom: 16 }}
          headStyle={{ background: '#1a1a3e', borderBottom: '2px solid #faad14' }}
        >
          <Row gutter={[12, 12]}>
            {shensha.map((item: any, index: number) => (
              <Col span={8} key={index}>
                <div style={{
                  padding: 12,
                  background: '#fffbe6',
                  borderRadius: 8,
                  border: '1px solid #ffe58f',
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                    <Tag color="orange" style={{ fontSize: 13, fontWeight: 'bold' }}>
                      {item.名称}
                    </Tag>
                    <Text type="secondary" style={{ fontSize: 11 }}>
                      {item.位置}
                    </Text>
                  </div>
                  <Text style={{ fontSize: 12, color: '#666' }}>
                    {item.描述}
                  </Text>
                </div>
              </Col>
            ))}
          </Row>
        </Card>
      )}
    </div>
  );
}

export default BaziChart;
