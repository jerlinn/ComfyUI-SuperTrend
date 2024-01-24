# ComfyUI SuperTrend
A Supertrend indicator for US stocks, a technical analysis tool that can assist investors in identifying market trends.

![CoverIMG](https://github.com/jerlinn/ComfyUI-SuperTrend/assets/91647085/7de1079c-5d33-40bb-ac0d-419a6c830e26)

**Plots**
- Candlestick with Trading volume chart

**Legend**
- 🔴 LowerBand: Rising cycle
- 🟢 UpperBand: Down cyle
- ▲ Buy
- ▼ Sell / Leave

## Calculate
$\text{BASIC Upperband} = \frac{\text{High} + \text{Low}}{2} + \text{Multiplier} \times \text{ATR}$  

$\text{BASIC Lowerband} = \frac{\text{High} + \text{Low}}{2} - \text{Multiplier} \times \text{ATR}$ 
- **High and low:** These are the highest and lowest prices of the asset during a specified time frame. （Default is 7, I set 14)
- **ATR:** This measures market volatility. The ATR is calculated based on the highest and lowest prices, as well as the closing price of the asset over a specified time frame.  
- **Multiplier:** This is a constant value that traders and investors employ to push the indicator to be more or less sensitive to price movements.（Default is 3, I set 2)
  
## Usage
- 🖊️ Input：Stock symbols (1 or more)、Date (YYYYMMDD)
- 🏞️ Output：SuuuuperTrend plot

## Install ｜ Manual
```
cd ~/ComfyUI/custom_nodes
git clone https://github.com/jerlinn/ComfyUI-SuperTrend.git
cd custom_nodes/ComfyUI-SuperTrend
pip install -r requirements.txt
Restart ComfyUI
```
**Add Node:**

```
Right Click ▸ Financial Analysis ▸ 📈 Super Trend
```

## Examples

1. Default Workflow
![CleanShot 2024-01-22 at 23 31 43@2x](https://github.com/jerlinn/ComfyUI-SuperTrend/assets/91647085/4102876e-4cd7-47ac-b6ee-532458f2b9e8)

2. Microsoft
![ComfyUI_temp_pvrza_00003_](https://github.com/jerlinn/ComfyUI-SuperTrend/assets/91647085/26978757-b34f-46da-a050-8af054d97c55)

3. Apple
![ComfyUI_temp_pvrza_00004_](https://github.com/jerlinn/ComfyUI-SuperTrend/assets/91647085/7629d8c7-a2c0-4bbf-923a-168c90003f1a)

4. Nvidia
![ComfyUI_temp_pvrza_00005_](https://github.com/jerlinn/ComfyUI-SuperTrend/assets/91647085/182f9a19-4e90-4444-86d4-dd0af389374f)


**Copilot**  
[ComfyUI Assistant](https://chat.openai.com/g/g-B3qi2zKGB-comfyui-assistant)  [@ZHO](https://twitter.com/ZHOZHO672070)
