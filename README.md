# 微信公众号智能发布工作流 (WeChat Official Account Publisher)

这是一个基于 Claude Code 的微信公众号内容智能发布工具，能够自动将文本内容格式化为符合公众号规范的标题和正文，自动识别媒体文件，并通过第三方API工具发布内容。

## 🌟 主要功能

### 📝 内容智能整理
- 自动将文本格式化为符合公众号规范的标题（≤64字）和正文
- 智能截断标题，确保符合公众号建议长度
- 建议相关话题标签
- 支持内容优化建议和字数统计

### 📸 媒体自动识别
- 扫描指定目录，自动识别所有图片和视频文件
- 支持多种图片格式：.jpg, .jpeg, .png, .gif, .webp, .bmp
- 支持多种视频格式：.mp4, .mov, .avi, .mkv等
- 检查文件大小，确保符合公众号限制（图片≤2MB）

### 🚀 智能发布
- 根据媒体类型自动选择合适的发布方式（图文/视频/纯文本）
- 支持 Wechaty、Offiaccount 等开源工具
- 灵活的API集成方案
- 支持批量处理和发布

## 📁 项目结构

```
wechat-workflow/
├── .claude/
│   ├── xhs-publisher/                  # 小红书技能（已弃用）
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── format_content.py
│   │   │   └── analyze_media.py
│   │   └── references/
│   │       ├── content_guidelines.md
│   │       └── mcp_tools.md
│   └── wechat-publisher/               # 微信公众号技能
│       ├── SKILL.md                    # 技能使用说明
│       ├── scripts/
│       │   ├── format_content.py       # 内容格式化脚本
│       │   └── analyze_media.py        # 媒体分析脚本
│       └── references/
│           ├── wechat_guidelines.md    # 公众号内容规范
│           └── wechat_tools.md         # API工具参考
├── claudecode.md                        # Claude Code 教程原文
├── README.md                            # 项目说明文档
├── .gitignore                          # Git忽略文件
├── xiaohongshu-login-darwin-arm64      # 旧版登录工具（保留）
├── xiaohongshu-mcp-darwin-arm64        # 旧版MCP服��（保留）
├── xiaohongshu-mcp-darwin-amd64        # 旧版MCP服务（保留）
└── test-media/                         # 测试媒体文件目录
    ├── breakfast_test.jpg
    └── claude-code-tutorial.jpg
```

## 🚀 快速开始

### 前置要求

#### 1. 选择开发工具

**推荐方案一：Wechaty（功能全面）**
```bash
# 安装Wechaty
pip install wechaty  # Python版本
# 或者
npm install wechaty  # Node.js版本
```

**推荐方案二：Offiaccount（轻量级）**
```bash
# 安装Offiaccount
npm install offiaccount
```

#### 2. 公众号配置
- 已认证的微信公众号（服务号或订阅号）
- 获取开发者ID（AppID）和开发者密钥（AppSecret）
- 配置服务器URL、Token和消息加解密密钥

### 基本使用

#### 1. 内容格式化
```bash
# 格式化文本内容（支持公众号规范）
python3 .claude/wechat-publisher/scripts/format_content.py "你的文本内容"
```

#### 2. 媒体文件分析
```bash
# 分析媒体目录（检查文件大小是否符合要求）
python3 .claude/wechat-publisher/scripts/analyze_media.py "/path/to/media/directory"
```

#### 3. 发布内容

**使用Wechaty示例**：
```python
from wechaty import Wechaty
import asyncio

async def publish_article():
    bot = Wechaty()
    await bot.start()

    # 发布公众号文章
    await bot.publish_article(
        title="文章标题",
        content="文章内容",
        media_ids=["图片媒体ID"]
    )
```

**使用Offiaccount示例**：
```javascript
const Offiaccount = require('offiaccount');
const api = new Offiaccount({
  appId: 'your_app_id',
  appSecret: 'your_app_secret'
});

// 上传并发布图文消息
api.uploadNewsMaterial({
  articles: [{
    title: "文章标题",
    content: "文章内容",
    thumb_media_id: "封面图片ID"
  }]
});
```

## 📋 使用示例

### 示例1：发布图文内容
```bash
# 1. 格式化内容
python3 .claude/xhs-publisher/scripts/format_content.py "今天在市中心发现了一家宝藏咖啡店..."

# 2. 分析媒体文件
python3 .claude/xhs-publisher/scripts/analyze_media.py "/path/to/images"

# 3. 发布（通过MCP工具）
publish_content --title "市中心宝藏咖啡店推荐" --content "..." --images "/path/to/images/"
```

### 示例2：发布视频内容
```bash
# 分析包含视频的目录
python3 .claude/xhs-publisher/scripts/analyze_media.py "/path/to/videos"

# 发布视频
publish_with_video --title "10分钟居家健身教程" --content "..." --video "/path/to/video.mp4"
```

## 📊 公众号内容规范

### 标题规范
- **建议长度**：20-64个字符（约10-32个汉字）
- **最长限制**：64个字符（硬性限制）
- **最佳实践**：简洁明了，包含关键词

### 正文规范
- **建议字数**：1000-3000字（最佳阅读体验）
- **最短要求**：500字以上
- **最长限制**：5000字以内
- **格式支持**：富文本编辑，支持小标题、段落分隔

### 媒体要求
- **图片**：文件大小≤2MB，推荐宽度900px
- **视频**：文件大小建议≤100MB，时长30秒-10分钟
- **格式**：图片支持JPG/PNG/GIF，视频支持MP4/MOV/AVI
- **数量**：每日最多发布8篇文章

### 发布策略
- **黄金时段**：早7-9点、午12-14点、晚18-23点
- **内容类型**：教程、分析、故事、资讯等
- **质量要求**：原创内容，符合平台规范

## 🛠️ 技术栈

- **Python 3.8+**：脚本开发语言
- **Node.js**：微信公众号API开发（可选）
- **Claude Code**：AI编程助手
- **Wechaty**：微信公众号SDK（推荐）
- **Offiaccount**：轻量级公众号API工具
- **微信公众号API**：官方API集成

## 📦 依赖项

```bash
# Python依赖（如果需要独立运行脚本）
pip install Pillow  # 用于图片处理
```

## ⚠️ 注意事项

### 账号安全
- 妥善保管AppID和AppSecret
- 定期更换access_token
- 遵守平台API调用频率限制

### 内容质量
- 确保内容原创或有明确授权
- 避免违规内容和敏感词汇
- 保持内容的真实性和准确性
- 遵守微信公众平台运营规范

### 技术限制
- 标题严格限制64个字符
- 图片文件大小≤2MB
- 视频文件建议≤100MB
- 每日最多发布8篇文章
- API调用有频率限制

### 开发建议
- 使用HTTPS协议进行API调用
- 实现合理的错误处理和重试机制
- 缓存常用数据，减少API调用
- 定期备份重要数据

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Claude Code](https://claude.ai/code) - AI编程助手
- [Wechaty](https://github.com/wechaty/wechaty) - 微信开发SDK
- [Offiaccount](https://github.com/wechaty/offiaccount) - 公众号API工具
- 微信公众号平台 - 内容发布目标平台
- 开源社区 - 提供了丰富的开发工具和资源

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至项目维护者

---

**让AI帮你轻松管理微信公众号内容发布！** 🎉