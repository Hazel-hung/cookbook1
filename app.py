from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Google AI Studio API 設定
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    try:
        data = request.json
        mode = data.get('mode', 'dish')
        dish_name = data.get('dishName', '')
        ingredients = data.get('ingredients', '')
        dietary = data.get('dietary', '')
        cuisine = data.get('cuisine', '')
        cooking_time = data.get('cookingTime', '')
        servings = data.get('servings', '2')
        difficulty = data.get('difficulty', '')
        
        # 構建 prompt
        if mode == 'dish':
            prompt = f"""請為「{dish_name}」生成一份完整的食譜。請務必提供具體的數值，不要使用「___」placeholder。

{f'飲食限制：{dietary}' if dietary else ''}
{f'料理風格：{cuisine}' if cuisine else ''}
{f'烹飪時間：{cooking_time}' if cooking_time else ''}
{f'難度：{difficulty}' if difficulty else ''}
份量：{servings}人份

請以以下格式詳細提供：

# {dish_name}

## 📝 料理簡介
（簡單介紹這道料理的特色和由來）

## 🥘 食材清單
（列出所有需要的食材和精確份量）

## 👨‍🍳 烹飪步驟
（提供詳細的步驟說明，每個步驟清楚標號，包含溫度和時間）

## 💡 烹飪技巧與注意事項
（提供專業的烹飪建議和常見錯誤提醒）

## 🍽️ 營養資訊（每人份）
請提供具體數值：
- 熱量：[具體數字]大卡
- 蛋白質：[具體數字]克
- 碳水化合物：[具體數字]克
- 脂肪：[具體數字]克
- 膳食纖維：[具體數字]克
- 鈉：[具體數字]毫克

## ⏱️ 時間分配
- 準備時間：[具體數字]分鐘
- 烹飪時間：[具體數字]分鐘
- 總時間：[具體數字]分鐘"""
        else:
            prompt = f"""請根據以下食材創作一道料理的完整食譜。請務必提供具體的數值，不要使用「___」placeholder。

現有食材：{ingredients}
{f'飲食限制：{dietary}' if dietary else ''}
{f'料理風格：{cuisine}' if cuisine else ''}
{f'烹飪時間：{cooking_time}' if cooking_time else ''}
{f'難度：{difficulty}' if difficulty else ''}
份量：{servings}人份

請以以下格式詳細提供：

# [建議的料理名稱]

## 📝 料理簡介
（簡單介紹這道料理的特色）

## 🥘 食材清單
（列出所有需要的食材和精確份量，包含現有食材和需要補充的食材）

## 👨‍🍳 烹飪步驟
（提供詳細的步驟說明，每個步驟清楚標號，包含溫度和時間）

## 💡 烹飪技巧與注意事項
（提供專業的烹飪建議）

## 🍽️ 營養資訊（每人份）
請提供具體數值：
- 熱量：[具體數字]大卡
- 蛋白質：[具體數字]克
- 碳水化合物：[具體數字]克
- 脂肪：[具體數字]克
- 膳食纖維：[具體數字]克
- 鈉：[具體數字]毫克

## ⏱️ 時間分配
- 準備時間：[具體數字]分鐘
- 烹飪時間：[具體數字]分鐘
- 總時間：[具體數字]分鐘"""
        
        # 調用 Gemini API
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        recipe_text = response.text
        
        return jsonify({
            'success': True,
            'recipe': recipe_text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)