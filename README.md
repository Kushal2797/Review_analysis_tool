# Review_analysis_tool
# CLI Review Analysis Tool

## 📌 Overview
This tool extracts customer delight attributes from product reviews and ranks them. It helps businesses understand what customers love about their products by analyzing customer feedback.

## 🛠️ Installation
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/repository-name.git
cd repository-name
```

### 2️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Set Up API Key**
#### **Option 1: Use a `.env` File (Recommended)**
1. Create a `.env` file in the same directory as the script.
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
3. The script will automatically read this key.

#### **Option 2: Set API Key as an Environment Variable**
##### **Linux/Mac**
```bash
export OPENAI_API_KEY="your-api-key-here"
```
##### **Windows (Command Prompt)**
```cmd
set OPENAI_API_KEY=your-api-key-here
```
##### **Windows (PowerShell)**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

---

## 🚀 Usage
To run the CLI tool, use:
```bash
python cli_review_analysis.py reviews.json output.json output.csv
```
### **Arguments:**
- `reviews.json` → Input file containing customer reviews.
- `output.json` → Output file storing extracted attributes.
- `output.csv` → Output file storing ranked attributes.

### **Example Command:**
```bash
python cli_review_analysis.py sample_reviews.json extracted_reviews.json delight_attributes.csv
```

---

## ✅ Evaluation
This tool includes an evaluation module to compare extracted vs. expected attributes.

### **Running Evaluation**
```bash
python evaluate.py ground_truth.csv output.json
```

### **Expected Files:**
- **Ground Truth (`ground_truth.csv`)** → Contains manually labeled delight attributes.
- **Extracted Output (`output.json`)** → The extracted attributes from the script.

### **Evaluation Metrics Used:**
- **Precision, Recall, and F1-score** to measure accuracy.

---

## 📂 File Structure
```
├── cli_review_analysis.py  # Main script for extracting delight attributes
├── evaluate.py             # Evaluation script
├── reviews.json            # Sample input file
├── output.json             # Extracted attributes
├── output.csv              # Ranked delight attributes
├── requirements.txt        # Dependencies list
├── .env                    # API key (ignored in Git)
├── README.md               # Documentation
```

---

## 🛠️ Assumptions & Known Issues
### **Assumptions**
- Input JSON file contains a `body` field with customer reviews.
- OpenAI API is available and responsive.

### **Potential Issues**
- Large files might cause **rate limits** with OpenAI API.
- Some extracted attributes might be **too broad or generic**.
- Clustering might **group unrelated attributes together** due to embedding similarities.

---

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing
Feel free to submit pull requests or report issues on [GitHub](https://github.com/your-username/repository-name/issues).

---

## 📞 Contact
For support, please contact [your-email@example.com](mailto:your-email@example.com).

