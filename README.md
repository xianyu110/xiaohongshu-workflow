# 小红书智能发布工作流 (Xiaohongshu Smart Publisher)

这是一个基于 Claude Code 的小红书内容智能发布工具，能够自动将文本内容格式化为符合小红书规范的标题和正文，自动识别媒体文件，并通过 MCP 服务发布内容。

## 🌟 主要功能

### 📝 内容智能整理
- 自动将文本格式化为符合小红书规范的标题（≤20字）和正文
- 智能截断标题，确保符合小红书硬性要求
- 建议相关话题标签
- 支持内容优化建议

### 📸 媒体自动识别
- 扫描指定目录，自动识别所有图片和视频文件
- 支持多种图片格式：.jpg, .jpeg, .png, .gif, .webp, .bmp
- 支持多种视频格式：.mp4, .mov, .avi, .mkv等
- 返回所有媒体文件的绝对路径列表

### 🚀 智能发布
- 根据媒体类型自动选择合适的发布方式（图文/视频）
- 无缝对接 xiaohongshu-mcp 工具
- 支持批量处理和发布

## 📁 项目结构

```
xiaohongshu-workflow/
├── .claude/
│   └── xhs-publisher/
│       ├── SKILL.md                    # 技能使用说明
│       ├── scripts/
│       │   ├── format_content.py       # 内容格式化脚本
│       │   └── analyze_media.py        # 媒体分析脚本
│       └── references/
│           ├── content_guidelines.md   # 内容规范参考
│           └── mcp_tools.md           # MCP工具参考
├── claudecode.md                        # Claude Code 教程原文
├── README.md                            # 项目说明文档
├── .gitignore                          # Git忽略文件
├── xiaohongshu-login-darwin-arm64      # 登录工具 (macOS ARM64)
├── xiaohongshu-mcp-darwin-arm64        # MCP服务 (macOS ARM64)
├── xiaohongshu-mcp-darwin-amd64        # MCP服务 (macOS Intel)
└── test-media/                         # 测试媒体文件目录
    ├── breakfast_test.jpg
    └── claude-code-tutorial.jpg
```

## 🚀 快速开始

### 前置要求

1. **xiaohongshu-mcp 服务已启动**
   ```bash
   # 启动 MCP 服务
   ./xiaohongshu-mcp-darwin-arm64

   # 服务地址：http://localhost:18060/mcp
   ```

2. **完成登录**
   ```bash
   # 运行登录工具
   ./xiaohongshu-login-darwin-arm64
   ```

### 基本使用

#### 1. 内容格式化
```bash
# 格式化文本内容
python3 .claude/xhs-publisher/scripts/format_content.py "你的文本内容"
```

#### 2. 媒体文件分析
```bash
# 分析媒体目录
python3 .claude/xhs-publisher/scripts/analyze_media.py "/path/to/media/directory"
```

#### 3. 发布内容
根据媒体类型选择发布方式：
- **有图片无视频**：使用 `publish_content`
- **有视频**：使用 `publish_with_video`

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

## 📊 内容规范

- **标题**：最多20字（硬性限制）
- **图片**：1-9张，推荐3:4或1:1尺寸
- **视频**：推荐9:16竖屏，15秒-5分钟
- **标签**：3-5个相关话题标签
- **发布**：建议黄金时段（早7-9点，午12-14点，晚18-23点）

## 🛠️ 技术栈

- **Python 3.8+**：脚本开发语言
- **MCP (Model Context Protocol)**：与AI模型的通信协议
- **Claude Code**：AI编程助手
- **小红书MCP服务**：小红书API集成

## 📦 依赖项

```bash
# Python依赖（如果需要独立运行脚本）
pip install Pillow  # 用于图片处理
```

## ⚠️ 注意事项

### 账号安全
- 登录后不要在其他网页端登录同一账号
- 避免频繁操作，遵守平台限制（每日最多50篇）

### 内容质量
- 确保内容原创或有授权
- 避免违规内容
- 保持真实性

### 技术限制
- 标题严格限制20字
- 视频仅支持本地文件
- 图片建议1-9张

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
- 小红书平台 - 内容发布目标平台
- MCP协议 - AI模型通信标准

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至项目维护者

---

**让AI帮你轻松管理小红书内容发布！** 🎉