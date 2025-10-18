
# BloomBank 🌱  
**Grow good habits. Watch your finances flourish.**

BloomBank turns personal finance into a living, growing experience. Every smart decision plants seeds that grow into a digital garden — a visual reflection of your financial wellbeing.

---

## 📖 Overview
Managing money shouldn't feel like punishment. BloomBank rewards healthy financial habits with visual growth: trees, plants, and habitats that evolve as you spend responsibly and save consistently.  
The goal is simple: make financial literacy *visible, calming, and rewarding.*

---

## 💡 Inspiration
Apps like *Flora* and *Forest* make productivity feel rewarding. We thought — what if budgeting felt the same way?  
Instead of guilt-tripping people with charts, BloomBank gives emotional reinforcement for good money choices.

---

## 🌿 Core Features
- **Grow your garden:** Save money, hit goals, and watch your world bloom.  
- **Habit tracking:** Automatically turns actions (like meeting a savings goal or skipping impulse buys) into growth points.  
- **Mood-linked spending:** Reflect your emotions in the environment — e.g. overspending triggers “wilting” visuals.  
- **Plain English summaries:** “You saved £50 this week — that’s one new oak tree!”  
- **Community forest (optional):** Connect with friends and grow a shared ecosystem of healthy habits.

---

## 🧠 How It Works
1. **Data Input:** Users import demo data or connect a bank sandbox (like Plaid).  
2. **Analysis:** Python backend categorizes spending and calculates “health scores.”  
3. **Growth Engine:** Each score increment generates plant growth animations using procedural generation.  
4. **Frontend Visualization:** React + Canvas/WebGL render the live garden scene.  

---

## 🛠️ Tech Stack
| Layer | Tech |
|-------|------|
| Frontend | Unity + C# for garden rendering |
| Backend | Python |
| Database | SQLite? |
| APIs | Plaid Sandbox (fake financial data), OpenAI API (text summaries) |
| Styling | TailwindCSS |

---

## 🚀 Running Locally
```bash
git clone https://github.com/yourusername/bloombank.git
cd bloombank
pip install -r requirements.txt
npm install
npm run dev