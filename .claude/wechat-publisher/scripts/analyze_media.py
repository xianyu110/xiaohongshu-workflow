#!/usr/bin/env python3
"""
分析指定目录中的媒体文件（图片和视频）- 微信公众号专用
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

# 公众号媒体文件限制
MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB (建议值)

# 支持的媒体文件扩展名
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'}


def analyze_media_directory(directory: str) -> Dict[str, List[Tuple[str, bool]]]:
    """
    分析目录中的媒体文件

    Args:
        directory: 要分析的目录路径

    Returns:
        包含images和videos两个列表的字典，每个元素为(文件路径, 大小是否合规)的元组
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
        abs_path = os.path.abspath(full_path)

        if ext in IMAGE_EXTENSIONS:
            # 检查图片文件大小
            file_size = os.path.getsize(full_path)
            size_valid = file_size <= MAX_IMAGE_SIZE
            images.append((abs_path, size_valid))
        elif ext in VIDEO_EXTENSIONS:
            # 检查视频文件大小
            file_size = os.path.getsize(full_path)
            size_valid = file_size <= MAX_VIDEO_SIZE
            videos.append((abs_path, size_valid))

    # 按文件名排序
    images.sort()
    videos.sort()

    return {
        'images': images,
        'videos': videos,
        'total_images': len(images),
        'total_videos': len(videos),
        'all_sizes_valid': all(size_valid for _, size_valid in images + videos)
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_media.py <目录路径>")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    try:
        result = analyze_media_directory(directory)

        print(f"\n📁 微信公众号媒体文件分析: {directory}")
        print(f"{'='*60}")
        print(f"📷 图片文件: {result['total_images']} 个 (限制: ≤2MB)")
        valid_images = 0
        for img_path, size_valid in result['images']:
            file_size = os.path.getsize(img_path) / (1024*1024)  # MB
            status = "✅" if size_valid else "❌"
            print(f"   {status} {img_path} ({file_size:.1f}MB)")
            if size_valid:
                valid_images += 1

        print(f"\n🎬 视频文件: {result['total_videos']} 个 (建议: ≤100MB)")
        valid_videos = 0
        for vid_path, size_valid in result['videos']:
            file_size = os.path.getsize(vid_path) / (1024*1024)  # MB
            status = "✅" if size_valid else "❌"
            print(f"   {status} {vid_path} ({file_size:.1f}MB)")
            if size_valid:
                valid_videos += 1

        print(f"\n{'='*60}")
        print(f"📊 合规性检查:")
        print(f"   图片合规: {valid_images}/{result['total_images']}")
        print(f"   视频合规: {valid_videos}/{result['total_videos']}")

        if result['all_sizes_valid']:
            print(f"   ✅ 所有文件大小都符合公众号要求")
        else:
            print(f"   ⚠️  部分文件大小超出限制，请压缩后重试")

        # 输出JSON格式（供程序调用）
        json_output = {
            'images': [{'path': path, 'size_valid': valid} for path, valid in result['images']],
            'videos': [{'path': path, 'size_valid': valid} for path, valid in result['videos']],
            'total_images': result['total_images'],
            'total_videos': result['total_videos'],
            'all_sizes_valid': result['all_sizes_valid'],
            'valid_image_count': valid_images,
            'valid_video_count': valid_videos
        }
        print(f"\nJSON输出:\n{json.dumps(json_output, ensure_ascii=False, indent=2)}")

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
