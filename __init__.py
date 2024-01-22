from .SuperTrendNode import SuperTrendNode  # 引入新的节点类

NODE_CLASS_MAPPINGS = {
    "SuperTrendNode": SuperTrendNode,  # 添加新节点的映射
    # 如果有其他节点，继续在这里添加
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SuperTrendNode": "📈 Super Trend",
    # 如果有其他节点，继续在这里添加
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']