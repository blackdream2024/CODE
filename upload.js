const ci = require('miniprogram-ci');
const path = require('path');

// 配置信息
const config = {
  appid: 'wx58451cb0f5d8a78c',
  projectPath: path.join(__dirname, 'miniprogram'),
  privateKeyPath: 'C:/Users/zhaoboyan/Desktop/private.wx58451cb0f5d8a78c.key',
  version: '1.0.2',
  desc: '命理星河 v1.0.2 - 迁移到CloudBase云函数，无需本地后端'
};

async function upload() {
  console.log('开始上传小程序...');
  console.log('配置信息:', {
    appid: config.appid,
    projectPath: config.projectPath,
    version: config.version,
    desc: config.desc
  });

  try {
    const project = new ci.Project({
      appid: config.appid,
      type: 'miniProgram',
      projectPath: config.projectPath,
      privateKeyPath: config.privateKeyPath,
      ignores: ['node_modules/**/*', '.git/**/*', '*.md', '*.key']
    });

    const uploadResult = await ci.upload({
      project,
      version: config.version,
      desc: config.desc,
      setting: {
        es6: true,
        minify: true,
        autoPrefixWXSS: true
      }
    });

    console.log('上传成功！');
    console.log('上传结果:', uploadResult);
    console.log('');
    console.log('下一步操作：');
    console.log('1. 登录微信公众平台: https://mp.weixin.qq.com');
    console.log('2. 进入"版本管理"页面');
    console.log('3. 在"开发版本"中找到刚上传的版本');
    console.log('4. 点击"提交审核"');
    console.log('5. 审核通过后点击"发布"');
  } catch (error) {
    console.error('上传失败:', error);
    process.exit(1);
  }
}

upload();
