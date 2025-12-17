#!/usr/bin/env python3
"""
分析指定目录中的媒体文件（图片和视频）
"""
import os
import sys
from pathlib import Path
from typing import Dict, List

# 支持的媒体文件扩展名
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'}


def analyze_media_directory(directory: str) -> Dict[str, List[str]]:
    """
    分析目录中的媒体文件
    
    Args:
        directory: 要分析的目录路径
        
    Returns:
        包含images和videos两个列表的字典
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"目录不存在: {directory}")
    
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"不是有效的目录: {directory}")
    
    images = []
    videos = []
    
    # 遍历目录中的所有文件
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        
        # 跳过子目录
        if os.path.isdir(full_path):
            continue
        
        # 检查文件扩展名
        ext = Path(item).suffix.lower()
        
        if ext in IMAGE_EXTENSIONS:
            images.append(os.path.abspath(full_path))
        elif ext in VIDEO_EXTENSIONS:
            videos.append(os.path.abspath(full_path))
    
    # 按文件名排序
    images.sort()
    videos.sort()
    
    return {
        'images': images,
        'videos': videos,
        'total_images': len(images),
        'total_videos': len(videos)
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_media.py <目录路径>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    try:
        result = analyze_media_directory(directory)
        
        print(f"\n📁 目录分析结果: {directory}")
        print(f"{'='*60}")
        print(f"📷 图片文件: {result['total_images']} 个")
        for img in result['images']:
            print(f"   - {img}")
        
        print(f"\n🎬 视频文件: {result['total_videos']} 个")
        for vid in result['videos']:
            print(f"   - {vid}")
        
        print(f"\n{'='*60}")
        print(f"✅ 分析完成")
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
