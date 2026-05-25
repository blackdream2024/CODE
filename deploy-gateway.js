const { execSync } = require('child_process');

const args = [
  'mcporter', 'call', 'cloudbase.manageCloudRun',
  'action=deploy',
  'serverName=mingpan-gateway',
  'targetPath=c:/Users/zhaoboyan/CodeBuddy/Claw/MingPanEngine/backend/services/gateway-service',
  'serverConfig={"OpenAccessTypes":["PUBLIC"],"Cpu":0.5,"Mem":1,"MinNum":1,"MaxNum":5}'
];

try {
  const result = execSync(`npx ${args.join(' ')}`, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
  console.log(result);
} catch (e) {
  console.error(e.stdout || '');
  console.error(e.stderr || '');
  process.exit(1);
}
