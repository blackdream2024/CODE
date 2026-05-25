import { useRef, useEffect, useCallback } from 'react';
import * as d3 from 'd3';
import { Card, Typography, Tag, Space } from 'antd';

const { Text } = Typography;

interface NetworkNode {
  id: string;
  name: string;
  type: 'person' | 'element' | 'star';
  group: number;
  value?: number;
  color?: string;
}

interface NetworkLink {
  source: string;
  target: string;
  type: 'harmony' | 'conflict' | 'support' | 'control';
  value: number;
  label?: string;
}

interface RelationNetworkProps {
  chart1Name: string;
  chart2Name: string;
  wuxing1: Record<string, number>;
  wuxing2: Record<string, number>;
  compatibility: {
    score: number;
    details?: Array<{
      type: string;
      description: string;
    }>;
  };
}

const wuxingColors: Record<string, string> = {
  '金': '#FFD700',
  '木': '#228B22',
  '水': '#1E90FF',
  '火': '#FF4500',
  '土': '#8B4513',
};

const wuxingRelations: Record<string, Record<string, string>> = {
  '金': { '金': 'harmony', '木': 'control', '水': 'support', '火': 'conflict', '土': 'support' },
  '木': { '金': 'conflict', '木': 'harmony', '水': 'support', '火': 'support', '土': 'control' },
  '水': { '金': 'support', '木': 'support', '水': 'harmony', '火': 'control', '土': 'conflict' },
  '火': { '金': 'control', '木': 'support', '水': 'conflict', '火': 'harmony', '土': 'support' },
  '土': { '金': 'support', '木': 'conflict', '水': 'support', '火': 'support', '土': 'harmony' },
};

const linkColors: Record<string, string> = {
  'harmony': '#52c41a',
  'conflict': '#ff4d4f',
  'support': '#d4a853',
  'control': '#faad14',
};

function RelationNetwork({
  chart1Name,
  chart2Name,
  wuxing1,
  wuxing2,
  compatibility,
}: RelationNetworkProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  const buildNetworkData = useCallback(() => {
    const nodes: NetworkNode[] = [];
    const links: NetworkLink[] = [];

    // 添加两个命盘节点
    nodes.push({
      id: 'chart1',
      name: chart1Name,
      type: 'person',
      group: 1,
      value: compatibility.score,
    });

    nodes.push({
      id: 'chart2',
      name: chart2Name,
      type: 'person',
      group: 2,
      value: compatibility.score,
    });

    // 添加五行节点
    const elements = ['金', '木', '水', '火', '土'];
    elements.forEach((el) => {
      const val1 = wuxing1[el] || 0;
      const val2 = wuxing2[el] || 0;

      // 命盘1的五行
      if (val1 > 0) {
        nodes.push({
          id: `chart1_${el}`,
          name: `${el} (${(val1 * 100).toFixed(0)}%)`,
          type: 'element',
          group: 1,
          value: val1,
          color: wuxingColors[el],
        });

        links.push({
          source: 'chart1',
          target: `chart1_${el}`,
          type: 'support',
          value: val1,
        });
      }

      // 命盘2的五行
      if (val2 > 0) {
        nodes.push({
          id: `chart2_${el}`,
          name: `${el} (${(val2 * 100).toFixed(0)}%)`,
          type: 'element',
          group: 2,
          value: val2,
          color: wuxingColors[el],
        });

        links.push({
          source: 'chart2',
          target: `chart2_${el}`,
          type: 'support',
          value: val2,
        });
      }

      // 五行之间的关系
      if (val1 > 0 && val2 > 0) {
        const relation = wuxingRelations[el][el];
        links.push({
          source: `chart1_${el}`,
          target: `chart2_${el}`,
          type: relation as any,
          value: Math.min(val1, val2),
          label: relation === 'harmony' ? '比和' : relation === 'support' ? '相生' : relation === 'control' ? '相克' : '相冲',
        });
      }
    });

    return { nodes, links };
  }, [chart1Name, chart2Name, wuxing1, wuxing2, compatibility.score]);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = 500;
    const height = 400;

    svg.selectAll('*').remove();

    const { nodes, links } = buildNetworkData();

    const simulation = d3
      .forceSimulation(nodes as any)
      .force(
        'link',
        d3
          .forceLink(links as any)
          .id((d: any) => d.id)
          .distance(80)
      )
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(30));

    const g = svg.append('g');

    // 添加缩放
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 2])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    // 绘制连线
    const link = g
      .append('g')
      .selectAll('line')
      .data(links)
      .enter()
      .append('line')
      .attr('stroke', (d) => linkColors[d.type] || '#999')
      .attr('stroke-width', (d) => Math.max(1, d.value * 3))
      .attr('stroke-opacity', 0.6);

    // 绘制连线标签
    const linkLabel = g
      .append('g')
      .selectAll('text')
      .data(links.filter((d) => d.label))
      .enter()
      .append('text')
      .attr('font-size', 10)
      .attr('fill', '#666')
      .attr('text-anchor', 'middle')
      .text((d) => d.label || '');

    // 绘制节点
    const node = g
      .append('g')
      .selectAll('circle')
      .data(nodes)
      .enter()
      .append('circle')
      .attr('r', (d) => (d.type === 'person' ? 25 : 15))
      .attr('fill', (d) => {
        if (d.color) return d.color;
        return d.group === 1 ? '#d4a853' : '#d4a853';
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .call(
        d3
          .drag<SVGCircleElement, NetworkNode>()
          .on('start', (event, d: any) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on('drag', (event, d: any) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on('end', (event, d: any) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    // 节点标签
    const nodeLabel = g
      .append('g')
      .selectAll('text')
      .data(nodes)
      .enter()
      .append('text')
      .attr('font-size', (d) => (d.type === 'person' ? 12 : 10))
      .attr('font-weight', (d) => (d.type === 'person' ? 'bold' : 'normal'))
      .attr('text-anchor', 'middle')
      .attr('dy', (d) => (d.type === 'person' ? 35 : 25))
      .attr('fill', '#333')
      .text((d) => d.name);

    // 更新位置
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      linkLabel
        .attr('x', (d: any) => (d.source.x + d.target.x) / 2)
        .attr('y', (d: any) => (d.source.y + d.target.y) / 2);

      node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);

      nodeLabel.attr('x', (d: any) => d.x).attr('y', (d: any) => d.y);
    });

    return () => {
      simulation.stop();
    };
  }, [buildNetworkData]);

  return (
    <Card title="关系网络图">
      <div style={{ textAlign: 'center', marginBottom: 16 }}>
        <Space>
          <Tag color="#d4a853">{chart1Name}</Tag>
          <Text type="secondary">与</Text>
          <Tag color="#d4a853">{chart2Name}</Tag>
        </Space>
      </div>

      <svg
        ref={svgRef}
        width="100%"
        height={400}
        style={{
          border: '1px solid #d9d9d9',
          borderRadius: 8,
          background: '#1a1a3e',
        }}
      />

      <div style={{ marginTop: 16 }}>
        <Space wrap>
          <Tag color="#52c41a">比和</Tag>
          <Tag color="#d4a853">相生</Tag>
          <Tag color="#faad14">相克</Tag>
          <Tag color="#ff4d4f">相冲</Tag>
        </Space>
        <Text type="secondary" style={{ marginLeft: 8 }}>
          拖拽节点可调整布局，滚轮缩放
        </Text>
      </div>
    </Card>
  );
}

export default RelationNetwork;
