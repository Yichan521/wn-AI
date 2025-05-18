
# 问农AI小程序

## 项目简介
问农AI是一款面向农业生产者的智能助手小程序，旨在通过AI技术为农业生产提供智能化解决方案。

## 主要功能
- 农产品文案智能生成
- 农产品宣传海报生成
- 数字人推广短视频

## 使用说明
### 前端运行
1. Git clone 本仓库
2. 使用[微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/devtools.html)打开本项目
3. 点击"编译"按钮启动小程序

### 后端运行
```bash
python miniprogram/backend/app.py
```

## 项目结构
```
miniprogram/
├── pages/            # 小程序页面
│   ├── index/        # 首页
│   ├── writting/     # 文案写作页
│   ├── poster-making/     # 海报制作页
│   ├── video-making/     # 视频制作页
│   └── user-center/  # 用户中心
├── components/       # 公共组件
├── utils/            # 工具函数
└── app.js            # 小程序入口文件
```

## 开发环境要求
- 微信开发者工具 1.06+
- Node.js 14+
- Python 3.11+ (后端服务)
- 微信小程序开发者账号

## 注意事项
当前版本功能仍在完善中，欢迎贡献代码和提出建议。