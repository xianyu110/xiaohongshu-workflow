#!/usr/bin/env python3
"""
将文本内容格式化为符合小红书要求的标题和正文
"""
import sys
import json
from typing import Dict


def format_for_xiaohongshu(text: str, max_title_length: int = 20) -> Dict[str, str]:
    """
    将文本格式化为小红书内容
    
    Args:
        text: 原始文本内容
        max_title_length: 标题最大长度（默认20字）
        
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
    
    return {
        'title': title,
        'content': content,
        'original_title_length': len(title_base),
        'title_truncated': len(title_base) > max_title_length
    }


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
    
    # 常见话题关键词映射
    keywords_map = {
        '美食': ['美食', '美食推荐', '探店'],
        '旅游': ['旅游', '旅行', '旅行攻略'],
        '穿搭': ['穿搭', '时尚', '搭配'],
        '护肤': ['护肤', '美妆', '护肤品'],
        '健身': ['健身', '运动', '减肥'],
        '学习': ['学习', '读书', '效率'],
        '生活': ['生活', '日常', 'vlog'],
        '数码': ['数码', '科技', '测评'],
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
        result = format_for_xiaohongshu(text)
        tags = suggest_tags(result['content'])
        
        print("\n" + "="*60)
        print("📝 小红书内容格式化结果")
        print("="*60)
        print(f"\n📌 标题 ({len(result['title'])}字):")
        print(f"   {result['title']}")
        
        if result['title_truncated']:
            print(f"   ⚠️  原标题 {result['original_title_length']} 字，已截断到 {len(result['title'])} 字")
        
        print(f"\n📄 正文:")
        print(f"   {result['content'][:200]}{'...' if len(result['content']) > 200 else ''}")
        
        if tags:
            print(f"\n🏷️  建议标签:")
            print(f"   {' '.join(['#' + tag for tag in tags])}")
        
        print("\n" + "="*60)
        
        # 输出JSON格式（供程序调用）
        json_output = {
            'title': result['title'],
            'content': result['content'],
            'suggested_tags': tags
        }
        print(f"\nJSON输出:\n{json.dumps(json_output, ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
