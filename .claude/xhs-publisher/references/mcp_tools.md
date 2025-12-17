# Xiaohongshu MCP 工具使用指南

## 前置要求

### 1. MCP服务运行
确保 xiaohongshu-mcp 服务已启动并运行在：
- **地址**：`http://localhost:18060/mcp`
- **启动方法**：运行下载的二进制文件或源码编译版本

### 2. 账号登录
- **首次使用**：必须先运行登录工具完成登录
- **登录工具**：`xiaohongshu-login` 二进制文件
- **重要提示**：登录后不要在其他网页端登录同一账号，否则会被踢下线

## 可用MCP工具

### 1. check_login_status
检查当前小红书登录状态

**参数**：无

**返回**：登录状态信息

**使用场景**：
- 发布前确认登录状态
- 调试MCP连接
- 定期检查会话有效性

### 2. publish_content
发布图文内容到小红书

**参数**：
- `title` (必需): 标题，不超过20字
- `content` (必需): 正文内容
- `images` (必需): 图片列表，支持三种方式：
  1. HTTP/HTTPS 链接
  2. 本地文件绝对路径
  3. 本地目录路径（自动读取所有图片）
- `tags` (可选): 话题标签列表

**图片说明**：
- 支持格式：.jpg, .jpeg, .png, .gif, .webp, .bmp
- 推荐使用本地路径（稳定、快速）
- 可以直接传入目录路径，自动识别所有图片
- 不会递归读取子目录

**示例**：
```json
{
  "title": "秋日穿搭分享",
  "content": "今天分享几套秋季穿搭...",
  "images": [
    "/Users/username/Pictures/outfit1.jpg",
    "/Users/username/Pictures/outfit2.jpg"
  ],
  "tags": ["穿搭", "秋季", "时尚"]
}
```

**目录方式示例**：
```json
{
  "title": "我的旅行相册",
  "content": "上周去的九寨沟...",
  "images": ["/Users/username/Pictures/jiuzhaigou/"],
  "tags": ["旅行", "九寨沟"]
}
```

### 3. publish_with_video
发布视频内容到小红书

**参数**：
- `title` (必需): 标题，不超过20字
- `content` (必需): 正文内容描述
- `video` (必需): 本地视频文件绝对路径
- `tags` (可选): 话题标签列表

**视频说明**：
- 仅支持本地视频文件，不支持HTTP链接
- 视频处理时间较长，需耐心等待
- 建议文件大小不超过 1GB

**示例**：
```json
{
  "title": "美食制作教程",
  "content": "教大家做简单美味的家常菜...",
  "video": "/Users/username/Videos/cooking.mp4",
  "tags": ["美食", "教程", "家常菜"]
}
```

### 4. search_feeds
搜索小红书内容

**参数**：
- `keyword` (必需): 搜索关键词

**返回**：搜索结果列表

**使用场景**：
- 研究同类内容
- 查找热门话题
- 竞品分析

### 5. list_feeds
获取小红书首页推荐列表

**参数**：无

**返回**：推荐内容列表

**使用场景**：
- 了解当前热门内容
- 寻找灵感
- 分析推荐算法

### 6. get_feed_detail
获取帖子详细信息

**参数**：
- `feed_id` (必需): 帖子ID
- `xsec_token` (必需): 安全令牌

**返回**：
- 帖子完整内容
- 用户信息
- 互动数据（点赞、收藏、评论数）
- 评论列表

**注意**：feed_id 和 xsec_token 可从搜索结果或Feed列表中获取

### 7. post_comment_to_feed
发表评论到帖子

**参数**：
- `feed_id` (必需): 帖子ID
- `xsec_token` (必需): 安全令牌
- `content` (必需): 评论内容

**使用场景**：
- 互动增加账号活跃度
- 自动回复管理

### 8. user_profile
获取用户个人主页

**参数**：
- `user_id` (必需): 用户ID
- `xsec_token` (必需): 安全令牌

**返回**：
- 用户基本信息
- 关注/粉丝数据
- 用户发布的笔记列表

## 最佳实践

### 发布流程
1. **检查登录状态**：使用 `check_login_status`
2. **准备内容**：整理标题、正文、媒体文件
3. **选择工具**：
   - 有图片 → `publish_content`
   - 有视频 → `publish_with_video`
4. **发布内容**：调用相应工具
5. **验证结果**：检查返回信息

### 路径使用建议
- ✅ **推荐**：使用绝对路径（如 `/Users/name/Pictures/image.jpg`）
- ✅ **推荐**：使用目录路径批量处理图片
- ⚠️  **避免**：使用相对路径可能导致找不到文件
- ⚠️  **避免**：视频使用HTTP链接（不支持）

### 图片vs视频选择
- **图文内容**：流量通常更好，推荐优先使用
- **视频内容**：处理时间长，但某些类型（教程、vlog）更适合
- **建议**：根据内容性质选择最合适的形式

### 错误处理
- **登录失效**：重新运行登录工具
- **文件未找到**：检查路径是否正确，使用绝对路径
- **标题过长**：确保标题不超过20字
- **网络问题**：检查MCP服务是否运行

## 调试技巧

### 验证MCP连接
```bash
# 使用MCP Inspector
npx @modelcontextprotocol/inspector

# 连接到 http://localhost:18060/mcp
# 测试 Ping Server 和 List Tools
```

### 检查服务状态
- MCP服务应该在 `http://localhost:18060/mcp` 可访问
- 登录状态可通过 `check_login_status` 验证
- 查看服务日志排查问题

### 常见错误
1. **"not logged in"** → 需要先运行登录工具
2. **"file not found"** → 检查文件路径是否正确
3. **"title too long"** → 标题超过20字限制
4. **"connection refused"** → MCP服务未启动
