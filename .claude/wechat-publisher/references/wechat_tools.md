# 微信公众号开发工具参考

## 推荐的开源工具

### 1. Wechaty（强烈推荐）

**GitHub**: https://github.com/wechaty/wechaty

**特点**:
- 支持多种编程语言：JavaScript, TypeScript, Python, Go, Java, C#
- 成熟的对话AI SDK，社区活跃
- 2025年持续更新和维护
- 丰富的API接口和插件生态

**安装**:
```bash
# Python
pip install wechaty

# JavaScript/Node.js
npm install wechaty
```

**基本使用示例**:
```python
# Python示例
from wechaty import Wechaty
import asyncio

class MyBot(Wechaty):
    async def on_message(self, msg):
        # 处理消息
        print(f"收到消息: {msg.text()}")

async def main():
    bot = MyBot()
    await bot.start()

asyncio.run(main())
```

```javascript
// JavaScript示例
const { Wechaty } = require('wechaty')

const bot = new Wechaty({
  name: 'my-bot',
})

bot.on('message', async msg => {
  console.log(`收到消息: ${msg.text()}`)
})

bot.start()
```

### 2. Offiaccount

**GitHub**: https://github.com/wechaty/offiaccount

**NPM**: https://www.npmjs.com/package/offiaccount

**特点**:
- 专为微信公众号API设计
- Node.js环境
- 轻量级，专注于公众号功能

**安装**:
```bash
npm install offiaccount
```

**基本使用示例**:
```javascript
const Offiaccount = require('offiaccount');

// 初始化
const api = new Offiaccount({
  appId: 'your_app_id',
  appSecret: 'your_app_secret'
});

// 获取access_token
async function getToken() {
  try {
    const token = await api.getAccessToken();
    console.log('Access Token:', token);
    return token;
  } catch (error) {
    console.error('获取Token失败:', error);
  }
}

// 上传素材
async function uploadMedia() {
  try {
    const result = await api.uploadMedia({
      type: 'image',
      media_path: '/path/to/image.jpg'
    });
    console.log('上传结果:', result);
    return result.media_id;
  } catch (error) {
    console.error('上传失败:', error);
  }
}

// 创建图文消息
async function createNews() {
  try {
    const newsData = {
      articles: [{
        title: "文章标题",
        content: "文章内容",
        thumb_media_id: "封面图片media_id",
        author: "作者",
        digest: "摘要",
        show_cover_pic: 1,
        content_source_url: "原文链接"
      }]
    };

    const result = await api.uploadNewsMaterial(newsData);
    console.log('创建图文消息成功:', result);
    return result.media_id;
  } catch (error) {
    console.error('创建图文消息失败:', error);
  }
}
```

## 公众号API核心功能

### 1. 素材管理

**上传临时素材**:
```javascript
// 上传图片（3天有效期）
const result = await api.uploadMedia({
  type: 'image',
  media_path: '/path/to/image.jpg'
});

// 上传视频
const videoResult = await api.uploadMedia({
  type: 'video',
  media_path: '/path/to/video.mp4',
  title: '视频标题',
  introduction: '视频介绍'
});
```

**上传永久素材**:
```javascript
// 上传永久图片
const result = await api.addMaterial({
  type: 'image',
  media_path: '/path/to/image.jpg'
});

// 上传永久视频
const videoResult = await api.addMaterial({
  type: 'video',
  media_path: '/path/to/video.mp4',
  title: '视频标题',
  introduction: '视频介绍'
});
```

### 2. 图文消息管理

**创建图文消息**:
```javascript
const newsData = {
  articles: [{
    title: "文章标题",
    author: "作者名称",
    digest: "文章摘要",
    content: "文章HTML内容",
    content_source_url: "原文链接",
    thumb_media_id: "封面图片media_id",
    show_cover_pic: 1,
    need_open_comment: 1,
    only_fans_can_comment: 0
  }]
};

const result = await api.uploadNewsMaterial(newsData);
```

**更新图文消息**:
```javascript
const updateData = {
  media_id: "要更新的图文消息media_id",
  index: 0, // 要更新的文章索引（从0开始）
  articles: {
    title: "新标题",
    content: "新内容",
    // ... 其他字段
  }
};

const result = await api.updateNews(updateData);
```

### 3. 群发消息

**群发图文消息**:
```javascript
// 预览群发
const previewData = {
  touser: "用户的openid",
  mpnews: {
    media_id: "图文消息media_id"
  }
};

const previewResult = await api.massPreview(previewData);

// 群发给所有用户
const massData = {
  mpnews: {
    media_id: "图文消息media_id"
  },
  send_ignore_reprint: 0,
  clientmsgid: "自定义消息ID"
};

const massResult = await api.massSendAll(massData);
```

**按标签群发**:
```javascript
// 先获取标签列表
const tags = await api.getTagList();

// 按标签群发
const tagMassData = {
  filter: {
    is_to_all: false,
    tag_id: tags[0].id // 使用第一个标签
  },
  mpnews: {
    media_id: "图文消息media_id"
  }
};

const tagResult = await api.massSend(tagMassData);
```

### 4. 用户��理

**获取用户列表**:
```javascript
// 获取用户列表
const userList = await api.getUserList({
  next_openid: null // 从第一个用户开始
});

// 获取用户详细信息
const userInfo = await api.getUserInfo({
  openid: "用户的openid"
});
```

**标签管理**:
```javascript
// 创建标签
const tagResult = await api.createTag({
  name: "新标签名称"
});

// 为用户打标签
const tagUser = await api.tagging({
  tagid: tagResult.tag.id,
  openid_list: ["openid1", "openid2"]
});
```

## 常用API端点

### 基础信息获取

```javascript
// 获取access_token
POST https://api.weixin.qq.com/cgi-bin/token
参数: grant_type=client_credential&appid=APPID&secret=APPSECRET

// 获取服务器IP地址
GET https://api.weixin.qq.com/cgi-bin/getcallbackip
```

### 素材管理

```javascript
// 上传临时素材
POST https://api.weixin.qq.com/cgi-bin/media/upload
参数: access_token=ACCESS_TOKEN&type=TYPE

// 上传永久素材
POST https://api.weixin.qq.com/cgi-bin/material/add_material
参数: access_token=ACCESS_TOKEN&type=TYPE

// 获取素材列表
POST https://api.weixin.qq.com/cgi-bin/material/batchget_material
参数: access_token=ACCESS_TOKEN&type=TYPE&offset=OFFSET&count=COUNT
```

### 图文消息

```javascript
// 新增图文消息
POST https://api.weixin.qq.com/cgi-bin/draft/add
参数: access_token=ACCESS_TOKEN

// 获取图文消息列表
GET https://api.weixin.qq.com/cgi-bin/draft/batchget
参数: access_token=ACCESS_TOKEN&offset=OFFSET&count=COUNT&no_content=NO_CONTENT
```

## 错误处理

### 常见错误码

- `40001`: access_token过期
- `40002`: 不合法的凭证类型
- `40003`: 不合法的openid
- `40004`: 不合法的媒体文件类型
- `40005`: 不合法的文件大小
- `40006`: 不合法的媒体文件ID
- `41001`: 缺少access_token参数
- `41002`: 缺少appid参数
- `42001`: access_token超时
- `42002`: refresh_token超时
- `43001`: 需要GET请求
- `44002`: POST内容为空
- `44003`: 图文消息内容为空
- `45001`: 多媒体文件大小超过限制
- `45002`: 消息内容超过限制
- `45003`: 标题字段超过限制
- `45004**: 描述字段超过限制
- `45005**: 链接字段超过限制
- `45006**: 图片链接字段超过限制
- `45007**: 语音播放时间超过限制
- `45008**: 图文消息超过限制

### 错误处理示例

```javascript
async function handleApiCall(apiFunction, ...args) {
  try {
    const result = await apiFunction(...args);
    return { success: true, data: result };
  } catch (error) {
    console.error('API调用失败:', error);

    // 处理特定错误
    if (error.code === 40001 || error.code === 42001) {
      // access_token过期，重新获取
      await refreshAccessToken();
      // 重试调用
      return await handleApiCall(apiFunction, ...args);
    }

    return {
      success: false,
      error: error.message,
      code: error.code
    };
  }
}
```

## 安全注意事项

### 1. 凭证管理
- 妥善保管AppID和AppSecret
- 定期更换access_token
- 使用HTTPS协议进行API调用

### 2. 频率限制
- 遵守API调用频率限制
- 实现合理的重试机制
- 缓存常用数据，减少API调用

### 3. 数据安全
- 敏感数据加密传输
- 用户隐私保护
- 定期备份重要数据

## 开发建议

### 1. 环境配置
```javascript
const config = {
  development: {
    app_id: 'dev_app_id',
    app_secret: 'dev_app_secret',
    token: 'dev_token'
  },
  production: {
    app_id: 'prod_app_id',
    app_secret: 'prod_app_secret',
    token: 'prod_token'
  }
};
```

### 2. 日志记录
```javascript
function logApiCall(method, url, params, result, duration) {
  console.log({
    timestamp: new Date().toISOString(),
    method,
    url,
    params,
    success: result.success,
    duration: `${duration}ms`
  });
}
```

### 3. 缓存策略
```javascript
const cache = new Map();

async function getCachedAccessToken() {
  const cached = cache.get('access_token');
  if (cached && cached.expiry > Date.now()) {
    return cached.token;
  }

  const token = await getNewAccessToken();
  cache.set('access_token', {
    token: token,
    expiry: Date.now() + (token.expires_in - 60) * 1000
  });

  return token;
}
```

通过以上工具和API参考，可以快速搭建微信公众号的自动化发布系统。建议根据具体需求选择合适的工具（Wechaty功能更全面，Offiaccount更轻量），并遵循最佳实践进行开发。