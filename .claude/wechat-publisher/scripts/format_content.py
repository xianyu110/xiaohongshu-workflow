#!/usr/bin/env python3
"""
将文本内容格式化为符合微信公众号要求的标题和正文
"""
import sys
import json
from typing import Dict


def format_for_wechat(text: str, max_title_length: int = 64) -> Dict[str, str]:
    """
    将文本格式化为微信公众号内容

    Args:
        text: 原始文本内容
        max_title_length: 标题最大长度（默认64字符，约32个汉字）

    Returns:
        包含title和content的字典
    """
    lines = text.strip().split('\n')
    
    # 移除空行
    lines = [line.strip() for line in lines if line.strip()]
    
    if not lines:
        raise ValueError("文本内容为空")
    
    # 第一行作为标题的基础
    title_base = lines[0]
    
    # 截取标题到最大长度
    if len(title_base) > max_title_length:
        # 智能截断：尽量在标点符号处截断
        title = title_base[:max_title_length]
        # 去掉末尾可能的不完整标点
        while title and title[-1] in '，。！？、；：""''':
            title = title[:-1]
        if not title:
            title = title_base[:max_title_length]
    else:
        title = title_base
    
    # 正文内容
    if len(lines) > 1:
        # 如果有多行，第一行之后的都是正文
        content_lines = lines[1:]
        content = '\n\n'.join(content_lines)
    else:
        # 如果只有一行，使用原始内容作为正文
        content = text.strip()
    
    # 添加公众号格式化
    formatted_content = format_wechat_content(content, len(title_base), max_title_length)

    return {
        'title': title,
        'content': formatted_content,
        'original_title_length': len(title_base),
        'title_truncated': len(title_base) > max_title_length,
        'word_count': len(formatted_content)
    }


def format_wechat_content(content: str, title_length: int, max_title_length: int) -> str:
    """
    格式化正文内容以适应公众号要求

    Args:
        content: 原始正文内容
        title_length: 标题长度
        max_title_length: 标题最大长度

    Returns:
        格式化后的正文内容
    """
    lines = content.strip().split('\n')

    # 添加小标题和分隔符，提升阅读体验
    formatted_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 如果行很短且不包含句号，可能是小标题
        if len(line) <= 30 and '。' not in line and '，' not in line:
            # 为小标题添加格式
            formatted_lines.append(f"\n## {line}\n")
        else:
            # 普通段落
            formatted_lines.append(line)

    formatted_content = '\n'.join(formatted_lines)

    # 添加文章尾部
    if len(formatted_content) > 100:  # 只有较长的文章才添加尾部
        formatted_content += "\n\n---\n\n*本文内容仅供参考，欢迎留言讨论*"

    return formatted_content


def suggest_tags(content: str, max_tags: int = 5) -> list:
    """
    基于内容建议话题标签（简单版本）
    
    Args:
        content: 内容文本
        max_tags: 最多返回的标签数量
        
    Returns:
        建议的标签列表
    """
    # 这里提供一个简单的实现
    # 实际使用时可以结合AI模型生成更准确的标签
    
    # 常见话题关键词映射（公众号风格）
    keywords_map = {
        'AI': ['AI编程', '人工智能', '机器学习', '深度学习'],
        '编程': ['编程技术', '代码分享', '软件开发', '编程教程'],
        '科技': ['科技前沿', '数字生活', '智能时代', '科技观察'],
        '教程': ['实用教程', '技能提升', '知识分享', '学习方法'],
        '美食': ['��食探店', '料理分享', '餐厅推荐', '美食文化'],
        '旅游': ['旅行攻略', '景点推荐', '游记分享', '旅行见闻'],
        '时尚': ['穿搭分享', '时尚潮流', '搭配技巧', '时尚观察'],
        '健身': ['运动健身', '健康生活', '瘦身塑形', '运动技巧'],
        '读书': ['读书心得', '好书推荐', '知识管理', '学习方法'],
        '职场': ['职场技能', '工作效率', '职业发展', '管理心得'],
        '生活': ['生活方式', '生活技巧', '情感故事', '人生感悟'],
        '数码': ['数码测评', '科技产品', '设备推荐', '数码资讯'],
    }
    
    suggested = []
    content_lower = content.lower()
    
    for category, tags in keywords_map.items():
        if category in content:
            suggested.extend(tags[:2])
            if len(suggested) >= max_tags:
                break
    
    return suggested[:max_tags]


def main():
    if len(sys.argv) < 2:
        print("用法: python format_content.py <文本内容>")
        print("或者: echo '文本内容' | python format_content.py")
        sys.exit(1)
    
    # 从命令行参数或stdin读取内容
    if sys.argv[1] == '-':
        text = sys.stdin.read()
    else:
        text = ' '.join(sys.argv[1:])
    
    try:
        result = format_for_wechat(text)
        tags = suggest_tags(result['content'])

        print("\n" + "="*60)
        print("📝 微信公众号内容格式化结果")
        print("="*60)
        print(f"\n📌 标题 ({len(result['title'])}字符):")
        print(f"   {result['title']}")

        if result['title_truncated']:
            print(f"   ⚠️  原标题 {result['original_title_length']} 字符，已截断到 {len(result['title'])} 字符")

        print(f"\n📄 正文字数: {result['word_count']} 字")
        print(f"   {result['content'][:300]}{'...' if len(result['content']) > 300 else ''}")

        # 字数建议
        if result['word_count'] < 500:
            print(f"   💡 建议：正文偏短，建议扩展到500-3000字以获得更好阅读体验")
        elif result['word_count'] > 5000:
            print(f"   ⚠️  注意��正文过长，建议控制在5000字以内")

        if tags:
            print(f"\n🏷️  建议标签:")
            print(f"   {' | '.join(tags)}")

        print("\n" + "="*60)
        print(f"📊 内容质量评估:")
        print(f"   ✓ 标题长度: {len(result['title'])}/64 字符")
        print(f"   ✓ 正文字数: {result['word_count']} 字 (建议500-3000字)")

        # 输出JSON格式（供程序调用）
        json_output = {
            'title': result['title'],
            'content': result['content'],
            'suggested_tags': tags,
            'word_count': result['word_count'],
            'title_optimal': 10 <= len(result['title']) <= 64,
            'content_optimal': 500 <= result['word_count'] <= 3000
        }
        print(f"\nJSON输出:\n{json.dumps(json_output, ensure_ascii=False, indent=2)}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
