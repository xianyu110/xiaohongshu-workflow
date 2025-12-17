---
name: wechat-publisher
description: 微信公众号内容智能发布工具。自动将文本整理成符合公众号格式的标题（≤64字）和正文，自动识别指定目录中的图片和视频文件，并通过第三方API工具发布内容。适用于需要发布公众号内容、批量处理媒体文件、或自动化公众号运营的场景。
---

# 微信公众号智能发布工具

自动化微信公众号内容发布的完整工作流，包括内容格式化、媒体文件识别和发布。

## 核心功能

1. **内容智能整理**：自动将文本格式化为符合公众号规范的标题和正文
2. **媒体自动识别**：扫描指定目录，自动识别所有图片和视频文件
3. **智能发布**：根据媒体类型自动选择合适的发布方式（图文/视频）
4. **第三方API集成**：支持Wechaty、Offiaccount等开源工具

## 前置要求

### 推荐工具选择

根据搜索结果，推荐以下开源工具：

#### 方案一：Wechaty（推荐）
- **项目地址**：https://github.com/wechaty/wechaty
- **语言支持**：JavaScript, TypeScript, Python, Go, Java, C#
- **特点**：成熟的对话AI SDK，社区活跃，2025年持续更新

#### 方案二：Offiaccount
- **项目地址**：https://github.com/wechaty/offiaccount
- **语言**：Node.js
- **NPM包**：`offiaccount`
- **特点**：专为公众号API设计，轻量级

### 安装准备

#### Wechaty安装
```bash
# 使用npm安装
npm install wechaty

# 使用Python安装
pip install wechaty
```

#### Offiaccount安装
```bash
npm install offiaccount
```

### 必须满足
1. **公众号开发者权限**
   - 已认证的微信公众号（服务号或订阅号）
   - 开发者ID和开发者密钥
   - API调用权限已开启

2. **服务器配置**
   - 服务器URL已配置
   - Token验证已通过
   - 消息加解密密钥已设置

## 使用流程

### 基本使用

当用户请求发布公众号内容时，按以下步骤操作：

#### 步骤1：理解用户需求
- 获取原始文本内容
- 获取媒体文件目录路径（如果有）
- 确认发布偏好（标签、风格等）

#### 步骤2：内容格式化

使用 `format_content.py` 脚本整理内容：

```bash
python scripts/format_content.py "原始文本内容"
```

**脚本功能**：
- 自动提取/生成标题（确保≤64字）
- 格式化正文内容，支持公众号富文本格式
- 建议相关话题标签
- 添加适当的分隔符和排版

**输出示例**：
```json
{
  "title": "Claude Code 15分钟入门教程：零基础也能做出第一个AI作品",
  "content": "详细的正文内容，包含小标题、段落分隔等...",
  "suggested_tags": ["AI编程", "ClaudeCode", "零基础学编程", "技术分享"],
  "word_count": 1856
}
```

**重要**：标题长度严格限制64个字符（约32个汉字），这是公众号的建议上限。

#### 步骤3：媒体文件分析（可选）

如果用户提供了媒体目录，使用 `analyze_media.py` 脚本：

```bash
python scripts/analyze_media.py "/path/to/media/directory"
```

**脚本功能**：
- 自动识别图片（.jpg, .jpeg, .png, .gif, .webp, .bmp）
- 自动识别视频（.mp4, .mov, .avi, .mkv等）
- 检查文件大小（图片≤2MB）
- 返回所有媒体文件的绝对路径列表

**输出示例**：
```json
{
  "images": [
    "/path/to/image1.jpg",
    "/path/to/image2.png"
  ],
  "videos": [
    "/path/to/video.mp4"
  ],
  "total_images": 2,
  "total_videos": 1,
  "valid_sizes": true
}
```

#### 步骤4：选择发布方式

根据媒体类型决定：

**情况A：有图片，无视频 → 使用图文发布**
```
调用API：素材管理 + 图文消息创建
参数：
- title: 格式化后的标题
- content: 格式化后的正文
- thumb_media_id: 封面图片媒体ID
- content_source_url: 原文链接（可选）
- digest: 摘要（可选）
```

**情况B：有视频 → 使用视频发布**
```
调用API：素材上传 + 视频消息创建
参数：
- title: 视频标题
- introduction: 视频介绍
- media_id: 视频媒体ID
- thumb_media_id: 视频封面媒体ID
```

**情况C：仅文本，无媒体**
```
调用API：纯文本消息发布
参数：
- content: 格式化后的正文
```

#### 步骤5：执行发布

使用选择的第三方工具调用相应的API完成发布。

**Wechaty示例**：
```python
from wechaty import Wechaty
import asyncio

async def publish_article():
    bot = Wechaty()
    await bot.start()

    # 发布公众号文章
    await bot.publish_article(
        title="标题",
        content="正文内容",
        media_ids=["图片媒体ID"]
    )
```

**Offiaccount示例**：
```javascript
const Offiaccount = require('offiaccount');

const api = new Offiaccount({
  appId: 'your_app_id',
  appSecret: 'your_app_secret'
});

// 发布图文消息
api.uploadNewsMaterial({
  articles: [{
    title: "标题",
    content: "正文内容",
    thumb_media_id: "封面图片ID"
  }]
});
```

#### 步骤6：反馈结果

向用户报告：
- 发布状态（成功/失败）
- 标题和内容摘要
- 使用的媒体文件数量
- 文章链接（如果发布成功）
- 任何警告或建议

### 高级功能

#### 批量发布
如果目录中有多个内容文件，可以批量创建和发布多篇公众号文章。

#### 内容优化建议
基于公众号内容规范，提供内容优化建议：
- 标题是否够吸引人且符合长度要求
- 正文是否结构清晰，有适当的段落分隔
- 图片尺寸和质量是否合适
- 字数是否在推荐范围内（1000-3000字）
- 发布时间建议

## 路径处理规则

### 图片路径
支持三种方式：
1. **HTTP/HTTPS链接**：`["https://example.com/image.jpg"]`
2. **本地文件绝对路径**：`["/Users/name/Pictures/img.jpg"]`（推荐）
3. **本地目录路径**：`["/Users/name/Pictures/album/"]`（推荐，自动识别）

### 视频路径
仅支持本地文件绝对路径：
- ✅ `/Users/name/Videos/video.mp4`
- ✅ 支持常见视频格式（mp4, mov, avi等）
- ❌ 建议视频文件大小≤100MB

### 最佳实践
- 优先使用绝对路径，避免相对路径
- 使用目录路径可以批量处理图片
- 确保文件存在且可访问
- 图片宽度建议900px，高度自适应
- 视频时长建议30秒-10分钟

## 内容规范参考

### 标题规范
- **长度**：建议20-64个字符（10-32个汉字）
- **最长限制**：不超过64个字符
- **建议**：避免过短或过长，包含关键词

### 正文规范
- **字数建议**：1000-3000字（最佳阅读体验）
- **最大字数**：5000字以内
- **格式支持**：
  - 富文本编辑（文字、图片、音频、视频）
  - Markdown格式和基础HTML标签
  - 图文混排
  - 超链接和公众号名片
  - 小程序卡片

### 媒体要求
- **图片大小**：不超过2MB，建议宽度900px
- **视频大小**：建议≤100MB
- **发布频率**：每日最多8篇文章

## 常见场景示例

### 场景1：发布技术教程文章

**用户请求**：
```
帮我把这个Claude Code教程发布到公众号，配图使用 /Users/me/Pictures/tutorial/ 目录下的图片

"Claude Code 15分钟入门教程：零基础也能做出第一个AI作品

还在觉得编程很难？2025年的AI工具让编程变得超级简单！
本教程将带你从零开始安装Claude Code，做出第一个待办清单应用..."
```

**执行步骤**：

1. **格式化内容**
```bash
python scripts/format_content.py "Claude Code 15分钟入门教程..."
```

得到：
- 标题："Claude Code 15分钟入门教程：零基础也能做出第一个AI作品"（25字）
- 正文：格式化后的教程内容
- 标签：["AI编程", "ClaudeCode", "零基础学编程", "技术分享"]

2. **分析媒体**
```bash
python scripts/analyze_media.py "/Users/me/Pictures/tutorial/"
```

得到：
- 8张图片，全部符合尺寸要求

3. **发布内容**
```
使用 Wechaty API：
- title: "Claude Code 15分钟入门教程：零基础也能做出第一个AI作品"
- content: [格式化后的正文内容]
- images: [图片路径列表]
```

### 场景2：发布产品介绍视频

**用户请求**：
```
把这个产品介绍视频发布到公众号：/Users/me/Videos/product_demo.mp4
标题："新品发布：智能助手Pro功能介绍"
```

**执行步骤**：

1. **验证视频存在**
2. **准备内容**
   - 标题：新品发布：智能助手Pro功能介绍（15字，符合要求）
   - 生成视频描述和相关介绍
   - 准备视频封面

3. **发布**
```
使用 Offiaccount API：
- title: "新品发布：智能助手Pro功能介绍"
- media_id: 上传视频获得的媒体ID
- thumb_media_id: 视频封面媒体ID
```

## 错误处理

### 常见问题

**问题1：API调用失败**
- 错误：`access_token invalid`
- 解决：重新获取access_token，检查AppID和AppSecret

**问题2：媒体文件上传失败**
- 错误：`media file too large`
- 解决：压缩图片或视频，确保文件大小在限制内

**问题3：标题过长**
- 错误：`title too long`
- 解决：使用脚本自动截断到64字

**问题4：内容审核失败**
- 错误：`content not approved`
- 解决：检查内容是否包含违规词汇，确保内容合规

### 调试建议

1. **验证API权限**：先调用基础API测试连接
2. **测试脚本**：单独运行脚本确认功能正常
3. **检查路径**：使用绝对路径，避免路径错误
4. **查看日志**：检查第三方工具的运行日志

## 注意事项

1. **账号安全**
   - 妥善保管AppID和AppSecret
   - 定期更换access_token
   - 遵守平台API调用频率限制

2. **内容质量**
   - 确保内容原创或有授权
   - 避免违规内容和敏感词汇
   - 保持内容的真实性和准确性

3. **技术限制**
   - 标题严格限制64个字符
   - 图片大小≤2MB
   - 视频大小建议≤100MB
   - 每日最多发布8篇文章

## 工作流总结

```
用户请求
    ↓
理解需求（文本+媒体路径）
    ↓
内容格式化（format_content.py）
    ↓
媒体分析（analyze_media.py，如需要）
    ↓
选择发布方式（图文/视频/纯文本）
    ↓
调用第三方API发布（Wechaty/Offiaccount）
    ↓
反馈结果给用户
```

通过这个skill，用户只需提供原始内容和媒体文件位置，即可自动完成公众号内容的整理和发布。支持多种第三方工具，提供了灵活的集成方案。