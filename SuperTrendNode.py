import pandas as pd
import pandas_ta as ta
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from PIL import Image
import io
from torchvision import transforms

"""
@author: Jerlin
@title: SuperTrend
@nickname: 📈 Super Trend
@description: A super trend indicator for US stocks.
"""

class SuperTrendNode:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "stock_symbol": ("STRING", {
                    "default": "MSFT",
                    "multiline": False,
                }),
                "start_date": ("STRING", {
                    "default": "20230601",
                    "multiline": False,
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "Financial Analysis"
    FUNCTION = "generate_supertrend_plot"

    def generate_supertrend_plot(self, stock_symbol, start_date):
        # Convert start date from 'YYYYMMDD' to 'YYYY-MM-DD'
        start_date = pd.to_datetime(start_date, format='%Y%m%d').strftime('%Y-%m-%d')
        df = yf.download(stock_symbol, start=start_date)
        df.ta.supertrend(high=df["High"], low=df["Low"], close=df["Close"], length=14, multiplier=2, append=True)
        df['SUPERTd_14_2.0_shifted'] = df['SUPERTd_14_2.0'].shift(1)
        b_positions = df[(df['SUPERTd_14_2.0'] == 1) & (df['SUPERTd_14_2.0_shifted'] != 1)].index
        s_positions = df[(df['SUPERTd_14_2.0'] == -1) & (df['SUPERTd_14_2.0_shifted'] != -1)].index
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.8, 0.2])
        fig.add_trace(go.Candlestick(x=df.index, increasing_line_color= 'red', decreasing_line_color= 'green',
                                     open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                     name=stock_symbol,legendgroup='1', legendrank=1),row=1, col=1)
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='交易量', marker_color='#0CAEE6'), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['SUPERTs_14_2.0'], mode='lines', name='上轨', line=dict(color='green', shape='spline', dash='dot')),row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['SUPERTl_14_2.0'], mode='lines', name='下轨', line=dict(color='orangered',shape='spline', dash='dot')),row=1, col=1)
        df['MA10'] = df['Close'].rolling(window=10).mean()
        ma10_colors = ['green' if trend == -1 else 'red' for trend in df['SUPERTd_14_2.0']]
        for idx in range(len(df) - 1):
            fig.add_trace(go.Scatter(
                x=[df.index[idx], df.index[idx+1]], 
                y=[df['MA10'].iloc[idx], df['MA10'].iloc[idx+1]],
                mode='lines', line=dict(color=ma10_colors[idx], width=1, shape='spline'),
                showlegend=False
            ), row=1, col=1)
            fig.add_trace(go.Scatter(
                x=[df.index[idx], df.index[idx+1]], 
                y=[df['MA10'].iloc[idx], df['MA10'].iloc[idx+1]],
                mode='markers', marker=dict(color=ma10_colors[idx], size=1),
                showlegend=False
            ), row=1, col=1)
        df['Trend_Change'] = df['SUPERTd_14_2.0'].diff()
        trend_sections = df['Trend_Change'].abs().cumsum().fillna(0)
        for section in trend_sections.unique():
            section_df = df[trend_sections == section]
            if not section_df.empty and section_df['SUPERTd_14_2.0'].iloc[0] == 1:
                fig.add_trace(go.Scatter(
                    x=section_df.index, y=section_df['Close'],
                    mode='lines', line=dict(width=0), showlegend=False
                ), row=1, col=1)
                fig.add_trace(go.Scatter(
                    x=section_df.index, y=section_df['SUPERTl_14_2.0'],
                    mode='lines', fill='tonexty', line=dict(width=0), fillcolor='rgba(255,0,0,0.1)', showlegend=False
                ), row=1, col=1)
            elif not section_df.empty and section_df['SUPERTd_14_2.0'].iloc[0] == -1:
                fig.add_trace(go.Scatter(
                    x=section_df.index, y=section_df['Close'],
                    mode='lines', line=dict(width=0), showlegend=False
                ), row=1, col=1)
                fig.add_trace(go.Scatter(
                    x=section_df.index, y=section_df['SUPERTs_14_2.0'],
                    mode='lines', fill='tonexty', line=dict(width=0), fillcolor='rgba(0,255,0,0.2)', showlegend=False
                ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=b_positions, y=df.loc[b_positions, 'SUPERTl_14_2.0']*0.995, 
            mode='markers', name='买入', 
            marker=dict(symbol='triangle-up-dot', color='orangered', size=10)
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=s_positions, y=df.loc[s_positions, 'SUPERTs_14_2.0']*1.005, 
            mode='markers', name='卖出', 
            marker=dict(symbol='triangle-down-dot', color='green', size=10)
        ), row=1, col=1)

        #family是名称而不是路径
        fig.update_layout(
            width=960, height=600,
            title={'text': '超级趋势指标', 'font': dict(family="SmileySans-Oblique", size=32, color="#222222")}, 
            title_x=0.5, 
            legend_title='图例',
            xaxis_rangeslider_visible=False
        )
        fig.update_yaxes(title_text='价格', row=1, col=1)
        fig.update_yaxes(title_text='交易量', row=2, col=1)
        fig.update_xaxes(showgrid=False)

        """首先使用 io.BytesIO 和 fig.write_image 将 Plotly 图表转换为 PNG 格式的图像，并存储在内存中。然后，使用 Image.open 将这个内存中的图像转换为 PIL 图像对象。"""
        # 创建一个 BytesIO 对象来保存图像数据
        fig_bytes = io.BytesIO() #这是一张RGBA的png
        fig.write_image(fig_bytes, format='png')
        fig_bytes.seek(0)

        image = Image.open(fig_bytes).convert("RGB")
        #print("Image size:", image.size)  # 打印图像尺寸进行检查，输出 Image size: (960, 600)

        transform = transforms.ToTensor()
        image_tensor = transform(image)
        #print("Tensor shape before unsqueeze:", image_tensor.shape)  # 检查张量形状，实际是CHW，torch.Size([3, 600, 960])
        
        # 调整张量形状以匹配 ComfyUI 的期望格式，从 (C, H, W) 转换为 (1, H, W, C) 格式
        image_tensor = image_tensor.unsqueeze(0).permute(0, 2, 3, 1)
        #print("Tensor shape after unsqueeze and permute:", image_tensor.shape)  # 再次检查张量形状，torch.Size([1, 600, 960, 3])

        return (image_tensor,) #元组（tuple）。在 Python 中，元组是一种不可变的序列类型，可以包含多个值。元组的元素由逗号分隔，当元组只有一个元素时，需要在该元素后面加上逗号 , 来表示它是一个元组，而不是单纯的括号表达式。