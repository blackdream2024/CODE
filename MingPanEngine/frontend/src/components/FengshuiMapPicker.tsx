import { useState } from 'react';
import { Card, Input, Button, Row, Col, Typography, Space, message } from 'antd';
import { EnvironmentOutlined, SearchOutlined, AimOutlined } from '@ant-design/icons';

const { Text } = Typography;

interface FengshuiMapPickerProps {
  onLocationSelect: (location: {
    address: string;
    latitude: number;
    longitude: number;
    building_name?: string;
  }) => void;
  initialAddress?: string;
  initialLat?: number;
  initialLng?: number;
}

function FengshuiMapPicker({ onLocationSelect, initialAddress, initialLat, initialLng }: FengshuiMapPickerProps) {
  const [address, setAddress] = useState(initialAddress || '');
  const [latitude, setLatitude] = useState<number | undefined>(initialLat);
  const [longitude, setLongitude] = useState<number | undefined>(initialLng);
  const [buildingName, setBuildingName] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  // 模拟搜索地址
  const handleSearch = async () => {
    if (!address.trim()) {
      message.warning('请输入地址');
      return;
    }

    setIsSearching(true);
    try {
      // 模拟API调用延迟
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // 根据地址生成模拟坐标（北京为中心）
      const mockLat = 39.9042 + (Math.random() - 0.5) * 0.1;
      const mockLng = 116.4074 + (Math.random() - 0.5) * 0.1;
      
      setLatitude(mockLat);
      setLongitude(mockLng);
      
      message.success('地址搜索成功');
    } catch (error) {
      message.error('地址搜索失败');
    } finally {
      setIsSearching(false);
    }
  };

  // 获取当前位置
  const handleGetCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude: lat, longitude: lng } = position.coords;
          setLatitude(lat);
          setLongitude(lng);
          message.success('已获取当前位置');
        },
        (error) => {
          console.error('获取位置失败:', error);
          message.error('无法获取当前位置，请手动输入坐标');
        }
      );
    } else {
      message.error('浏览器不支持地理位置功能');
    }
  };

  // 确认选择
  const handleConfirm = () => {
    if (!latitude || !longitude) {
      message.warning('请先搜索地址或获取位置');
      return;
    }

    onLocationSelect({
      address: address || '未命名位置',
      latitude,
      longitude,
      building_name: buildingName || undefined
    });

    message.success('位置信息已保存');
  };

  return (
    <Card
      title={
        <span>
          <EnvironmentOutlined style={{ marginRight: 8, color: '#d4a853' }} />
          房屋位置信息
        </span>
      }
      style={{ marginBottom: 16 }}
    >
      <Space direction="vertical" style={{ width: '100%' }}>
        {/* 地址输入 */}
        <div>
          <Text strong>详细地址：</Text>
          <Input.Search
            placeholder="输入详细地址，如：北京市朝阳区建国路88号"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            onSearch={handleSearch}
            enterButton={<><SearchOutlined /> 搜索</>}
            loading={isSearching}
            style={{ marginTop: 8 }}
          />
        </div>

        {/* 建筑名称 */}
        <div>
          <Text strong>建筑名称（可选）：</Text>
          <Input
            placeholder="如：某某小区3号楼"
            value={buildingName}
            onChange={(e) => setBuildingName(e.target.value)}
            style={{ marginTop: 8 }}
          />
        </div>

        {/* 坐标输入 */}
        <Row gutter={16}>
          <Col span={12}>
            <Text strong>纬度：</Text>
            <Input
              placeholder="如：39.9042"
              value={latitude?.toString() || ''}
              onChange={(e) => setLatitude(parseFloat(e.target.value) || undefined)}
              style={{ marginTop: 8 }}
            />
          </Col>
          <Col span={12}>
            <Text strong>经度：</Text>
            <Input
              placeholder="如：116.4074"
              value={longitude?.toString() || ''}
              onChange={(e) => setLongitude(parseFloat(e.target.value) || undefined)}
              style={{ marginTop: 8 }}
            />
          </Col>
        </Row>

        {/* 获取当前位置按钮 */}
        <Button
          icon={<AimOutlined />}
          onClick={handleGetCurrentLocation}
          block
          style={{ marginTop: 8 }}
        >
          获取当前位置
        </Button>

        {/* 地图预览（模拟） */}
        {latitude && longitude && (
          <div style={{ 
            marginTop: 16, 
            padding: 16, 
            backgroundColor: 'rgba(212, 168, 83, 0.1)', 
            borderRadius: 8,
            border: '1px dashed #d4a853'
          }}>
            <div style={{ textAlign: 'center', marginBottom: 8 }}>
              <EnvironmentOutlined style={{ fontSize: 24, color: '#d4a853' }} />
            </div>
            <div style={{ textAlign: 'center' }}>
              <Text strong>已选择位置</Text>
            </div>
            <div style={{ textAlign: 'center', marginTop: 4 }}>
              <Text type="secondary">
                北纬 {latitude.toFixed(4)}°，东经 {longitude.toFixed(4)}°
              </Text>
            </div>
            {address && (
              <div style={{ textAlign: 'center', marginTop: 4 }}>
                <Text type="secondary">{address}</Text>
              </div>
            )}
            <div style={{ textAlign: 'center', marginTop: 8 }}>
              <Text type="secondary" style={{ fontSize: 12 }}>
                提示：实际项目中可集成腾讯地图API实现地图选点
              </Text>
            </div>
          </div>
        )}

        {/* 确认按钮 */}
        <Button
          type="primary"
          icon={<EnvironmentOutlined />}
          onClick={handleConfirm}
          block
          disabled={!latitude || !longitude}
          style={{ marginTop: 16 }}
        >
          确认位置信息
        </Button>
      </Space>
    </Card>
  );
}

export default FengshuiMapPicker;