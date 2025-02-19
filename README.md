# Customer Review Analysis Tool

## 📌 Overview
This tool extracts customer delight attributes from product reviews and ranks them. It helps businesses understand what customers love about their products by analyzing customer feedback.

## 🛠️ Installation
### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/Kushal2797/Review_analysis_tool.git
cd Review_analysis_tool
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

---

## 🚀 Usage
To run the CLI tool, use:
```bash
python review_analysis.py reviews.json output.json output.csv
```
### **Arguments:**
- `reviews.json` → Input file containing customer reviews.
- `output.json` → Output file storing extracted attributes.
- `output.csv` → Output file storing ranked attributes.

### **Example Command:**
```bash
python review_analysis.py sample_reviews.json extracted_reviews.json delight_attributes.csv
```
---
## 📜 Logging Information

The tool generates a **log file (`script.log`)** that records processing details and errors. If something goes wrong, check the log for debugging:

```bash
cat script.log
```
---

## 📂 File Structure
```
├── review_analysis.py      # Main script for extracting delight attributes
├── reviews.json            # Sample input file
├── output.json             # Extracted attributes
├── output.csv              # Ranked delight attributes
├── script.log              # Log file for debuggi
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

## 📞 Contact
For support, please contact [kushalshah662@example.com](mailto:your-email@example.com).
