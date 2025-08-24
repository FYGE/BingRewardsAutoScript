import requests
import json
import time
from typing import List, Dict, Optional


def get_weibo_hot_search() -> List[Dict[str, str]]:
    """
    获取微博热搜榜前50的关键词

    Returns:
        List[Dict]: 包含热搜关键词信息的列表
        每个元素包含: {
            'rank': 排名,
            'keyword': 关键词,
            'hot_degree': 热度,
            'url': 微博搜索链接,
            'category': 分类标签
        }
    """

    # 微博热搜榜API
    url = "https://weibo.com/ajax/side/hotSearch"

    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://weibo.com/',
        'Connection': 'keep-alive',
    }

    try:
        # 发送请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功

        # 解析JSON数据
        data = response.json()
        data = response.json()

        # 提取热搜数据
        hot_search_data = []

        # 处理实时热搜
        if 'data' in data and 'realtime' in data['data']:
            realtime_list = data['data']['realtime']

            for index, item in enumerate(realtime_list[:50]):  # 取前50个
                keyword_info = {
                    'rank': str(index + 1),
                    'keyword': item.get('word', ''),
                    'hot_degree': str(item.get('num', 0)),
                    'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}",
                    'category': item.get('category', '实时热搜')
                }
                hot_search_data.append(keyword_info)

        # 如果实时热搜数据不足，补充热门搜索数据
        if len(hot_search_data) < 50 and 'data' in data and 'hotgov' in data['data']:
            hotgov_list = data['data']['hotgov']

            for item in hotgov_list:
                if len(hot_search_data) >= 50:
                    break

                # 检查是否已存在
                exists = any(hs['keyword'] == item.get('word', '') for hs in hot_search_data)
                if not exists:
                    keyword_info = {
                        'rank': str(len(hot_search_data) + 1),
                        'keyword': item.get('word', ''),
                        'hot_degree': str(item.get('num', 0)),
                        'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}",
                        'category': item.get('category', '热门搜索')
                    }
                    hot_search_data.append(keyword_info)

        return hot_search_data

    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return []
    except Exception as e:
        print(f"获取微博热搜失败: {e}")
        return []


def get_weibo_hot_search_keywords_only() -> List[str]:
    """
    只获取微博热搜榜前50的关键词列表（简化版）

    Returns:
        List[str]: 热搜关键词列表
    """
    hot_search_data = get_weibo_hot_search()
    return [item['keyword'] for item in hot_search_data]


def display_hot_search():
    """
    显示微博热搜榜（格式化输出）
    """
    print("正在获取微博热搜榜...")
    hot_search_data = get_weibo_hot_search()

    if not hot_search_data:
        print("获取热搜榜失败，请稍后重试")
        return

    print(f"\n=== 微博热搜榜 (共{len(hot_search_data)}条) ===")
    print("-" * 80)

    for item in hot_search_data:
        print(f"{item['rank']:>2}. {item['keyword']:<20} 热度: {item['hot_degree']:<10} 分类: {item['category']}")

    print("-" * 80)


def save_hot_search_to_file(filename: str = "weibo_hot_search.txt"):
    """
    将热搜榜保存到文件

    Args:
        filename (str): 保存的文件名
    """
    hot_search_data = get_weibo_hot_search()

    if not hot_search_data:
        print("没有数据可保存")
        return

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"微博热搜榜 - 更新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 100 + "\n")

            for item in hot_search_data:
                f.write(f"{item['rank']}. {item['keyword']}\n")
                f.write(f"   热度: {item['hot_degree']} | 分类: {item['category']}\n")
                f.write(f"   链接: {item['url']}\n\n")

        print(f"热搜榜已保存到 {filename}")

    except Exception as e:
        print(f"保存文件失败: {e}")


# 使用示例
# if __name__ == "__main__":
    # # 方法1: 获取完整的热搜数据
    # print("方法1: 获取完整热搜数据")
    # hot_search_data = get_weibo_hot_search()
    # for i, item in enumerate(hot_search_data[:10], 1):  # 显示前10个
    #     print(f"{i}. {item['keyword']} (热度: {item['hot_degree']})")
    #
    # print("\n" + "=" * 50 + "\n")
    #
    # # 方法2: 只获取关键词列表
    # print("方法2: 只获取关键词列表")
    # keywords = get_weibo_hot_search_keywords_only()
    # print("前10个热搜关键词:", keywords[:10])
    #
    # print("\n" + "=" * 50 + "\n")

    # 方法3: 格式化显示
    # display_hot_search()
    #
    # # 方法4: 保存到文件
    # save_hot_search_to_file()
