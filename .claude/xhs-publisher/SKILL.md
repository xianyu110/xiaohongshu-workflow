---
name: xhs-publisher
description: 小红书内容智能发布工具。自动将文本整理成符合小红书格式的标题（≤20字）和正文，自动识别指定目录中的图片和视频文件，并通过xiaohongshu-mcp发布内容。适用于需要发布小红书内容、批量处理媒体文件、或自动化小红书运营的场景。
---

# 小红书智能发布工具

自动化小红书内容发布的完整工作流，包括内容格式化、媒体文件识别和发布。

## 核心功能

1. **内容智能整理**：自动将文本格式化为符合小红书规范的标题和正文
2. **媒体自动识别**：扫描指定目录，自动识别所有图片和视频文件
3. **智能发布**：根据媒体类型自动选择合适的发布方式（图文/视频）
4. **MCP集成**：无缝对接xiaohongshu-mcp工具

## 前置要求

### 必须满足
1. **xiaohongshu-mcp服务已启动**
   - 服务地址：`http://localhost:18060/mcp`
   - 已完成登录（运行过 `xiaohongshu-login` 工具）

2. **MCP连接已配置**
   - Claude Desktop/CLI 已配置 xiaohongshu-mcp
   - 可以调用 xiaohongshu-mcp 的工具

### 验证方法
```bash
# 检查MCP服务是否运行
curl http://localhost:18060/mcp

# 或在Claude中运行
使用 check_login_status 工具验证登录状态
```

## 使用流程

### 基本使用

当用户请求发布小红书内容时，按以下步骤操作：

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
- 自动提取/生成标题（确保≤20字）
- 格式化正文内容
- 建议相关话题标签

**输出示例**：
```json
{
  "title": "秋日穿搭分享",
  "content": "详细的正文内容...",
  "suggested_tags": ["穿搭", "秋季", "时尚"]
}
```

**重要**：标题长度严格限制20字，这是小红书的硬性要求。

#### 步骤3：媒体文件分析（可选）

如果用户提供了媒体目录，使用 `analyze_media.py` 脚本：

```bash
python scripts/analyze_media.py "/path/to/media/directory"
```

**脚本功能**：
- 自动识别图片（.jpg, .jpeg, .png, .gif, .webp, .bmp）
- 自动识别视频（.mp4, .mov, .avi, .mkv等）
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
  "total_videos": 1
}
```

#### 步骤4：选择发布方式

根据媒体类型决定：

**情况A：有图片，无视频 → 使用 `publish_content`**
```
调用MCP工具：publish_content
参数：
- title: 格式化后的标题
- content: 格式化后的正文
- images: 图片路径列表或目录路径
- tags: 建议的标签（可选）
```

**情况B：有视频 → 使用 `publish_with_video`**
```
调用MCP工具：publish_with_video
参数：
- title: 格式化后的标题
- content: 格式化后的正文
- video: 视频文件路径
- tags: 建议的标签（可选）
```

**情况C：仅文本，无媒体**
```
提示用户：小红书需要配图或视频
建议：
1. 提供媒体文件
2. 或使用AI生成配图
3. 或从网络获取合适的图片
```

#### 步骤5：执行发布

调用相应的MCP工具完成发布。

#### 步骤6：反馈结果

向用户报告：
- 发布状态（成功/失败）
- 标题和内容摘要
- 使用的媒体文件数量
- 任何警告或建议

### 高级功能

#### 批量发布
如果目录中有多个视频，可以为每个视频创建单独的帖子。

#### 内容优化建议
基于 `content_guidelines.md` 中的规范，提供内容优化建议：
- 标题是否够吸引人
- 正文是否结构清晰
- 标签是否相关
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
- ❌ 不支持HTTP链接

### 最佳实践
- 优先使用绝对路径，避免相对路径
- 使用目录路径可以批量处理图片
- 确保文件存在且可访问

## 内容规范参考

详细的内容规范请查看：`references/content_guidelines.md`

**关键要点**：
- 标题：最多20字（硬性限制）
- 图片：1-9张，推荐3:4或1:1尺寸
- 视频：推荐9:16竖屏，15秒-5分钟
- 标签：3-5个相关话题标签
- 发布：建议黄金时段（早7-9点，午12-14点，晚18-23点）

## MCP工具参考

详细的MCP工具说明请查看：`references/mcp_tools.md`

**核心工具**：
- `check_login_status`：检查登录状态
- `publish_content`：发布图文
- `publish_with_video`：发布视频

## 常见场景示例

### 场景1：发布图文内容

**用户请求**：
```
帮我把这段文字发布到小红书，配图使用 /Users/me/Pictures/food/ 目录下的图片

"今天在市中心发现了一家宝藏咖啡店，环境超级棒，咖啡也很好喝。店里的装修是简约北欧风格，采光特别好。我点了一杯拿铁和一块提拉米苏，味道都很不错。人均消费大概80元左右，性价比很高。推荐给喜欢喝咖啡的朋友们！"
```

**执行步骤**：

1. **格式化内容**
```bash
python scripts/format_content.py "今天在市中心发现了一家宝藏咖啡店..."
```

得到：
- 标题："市中心宝藏咖啡店推荐"（10字）
- 正文：原文
- 标签：["美食", "咖啡", "探店"]

2. **分析媒体**
```bash
python scripts/analyze_media.py "/Users/me/Pictures/food/"
```

得到：
- 3张图片

3. **发布内容**
```
使用 publish_content 工具：
- title: "市中心宝藏咖啡店推荐"
- content: [正文内容]
- images: ["/Users/me/Pictures/food/"]
- tags: ["美食", "咖啡", "探店"]
```

### 场景2：发布视频内容

**用户请求**：
```
把这个视频发布到小红书：/Users/me/Videos/workout.mp4
标题："10分钟居家健身教程"
```

**执行步骤**：

1. **验证视频存在**
2. **准备内容**
   - 标题：10分钟居家健身教程（10字，符合要求）
   - 生成正文描述
   - 建议标签：["健身", "运动", "教程"]

3. **发布**
```
使用 publish_with_video 工具：
- title: "10分钟居家健身教程"
- content: [视频描述]
- video: "/Users/me/Videos/workout.mp4"
- tags: ["健身", "运动", "教程"]
```

### 场景3：自动分析并发布

**用户请求**：
```
自动分析 /Users/me/Documents/travel/ 目录，生成并发布小红书内容
```

**执行步骤**：

1. **分析目录**
```bash
python scripts/analyze_media.py "/Users/me/Documents/travel/"
```

2. **根据内容生成描述**
   - 查看图片内容（如果可能）
   - 生成相关的旅行描述

3. **格式化并发布**
   - 如果有图片：使用 publish_content
   - 如果有视频：使用 publish_with_video

## 错误处理

### 常见问题

**问题1：登录失败**
- 错误：`not logged in`
- 解决：运行 `xiaohongshu-login` 工具重新登录

**问题2：文件未找到**
- 错误：`file not found`
- 解决：检查路径是否正确，使用绝对路径

**问题3：标题过长**
- 错误：`title too long`
- 解决：使用脚本自动截断到20字

**问题4：MCP连接失败**
- 错误：`connection refused`
- 解决：确保 xiaohongshu-mcp 服务正在运行

### 调试建议

1. **验证MCP连接**：先调用 `check_login_status`
2. **测试脚本**：单独运行脚本确认功能正常
3. **检查路径**：使用绝对路径，避免路径错误
4. **查看日志**：检查 xiaohongshu-mcp 服务日志

## 注意事项

1. **账号安全**
   - 登录后不要在其他网页端登录同一账号
   - 避免频繁操作，遵守平台限制（每日最多50篇）

2. **内容质量**
   - 确保内容原创或有授权
   - 避免违规内容
   - 保持真实性

3. **技术限制**
   - 标题严格限制20字
   - 视频仅支持本地文件
   - 图片建议1-9张

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
选择发布方式（图文/视频）
    ↓
调用MCP工具发布
    ↓
反馈结果给用户
```

通过这个skill，用户只需提供原始内容和媒体文件位置，即可自动完成小红书内容的整理和发布。
