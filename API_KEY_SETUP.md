# OpenAI API Key Setup Guide

## 🔑 Setting Up OpenAI API Key

The Resume Evaluation System uses OpenAI's GPT models for generating intelligent feedback and analysis. Follow these steps to set up your API key.

## 📋 Prerequisites

1. **OpenAI Account**: Create an account at [OpenAI](https://platform.openai.com/)
2. **API Access**: Ensure you have access to OpenAI's API
3. **Billing**: Set up billing information for API usage

## 🚀 Setup Steps

### **Step 1: Get Your API Key**

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign in to your account
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy the generated API key (starts with `sk-`)

### **Step 2: Configure the API Key**

#### **Option A: Using .env file (Recommended)**

1. Create a `.env` file in the project root directory
2. Add your API key:

```bash
# .env file
OPENAI_API_KEY=sk-your-actual-api-key-here
```

#### **Option B: Environment Variable**

Set the environment variable in your system:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Linux/macOS:**
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
```

### **Step 3: Verify Configuration**

1. Run the system: `python run_system.py`
2. Check the console for any API key warnings
3. Test an evaluation to see if LLM feedback is generated

## 🔧 Configuration Files

### **env.example**
```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
```

### **app/config.py**
```python
class Settings(BaseSettings):
    openai_api_key: str = "your-openai-api-key-here"
    # ... other settings
```

## 🎯 Features That Require API Key

### **With API Key (Full Features):**
- ✅ **AI-Generated Feedback**: Intelligent analysis and suggestions
- ✅ **Strengths Analysis**: AI-identified candidate strengths
- ✅ **Weaknesses Analysis**: AI-identified areas for improvement
- ✅ **Improvement Suggestions**: Personalized recommendations
- ✅ **Overall Assessment**: Comprehensive AI evaluation

### **Without API Key (Fallback Mode):**
- ✅ **Basic Feedback**: Rule-based analysis
- ✅ **Skill Matching**: Hard skill comparison
- ✅ **Score Calculation**: Relevance scoring
- ⚠️ **Limited Analysis**: Basic feedback without AI insights

## 🛠️ Troubleshooting

### **Issue: "LLM analysis not available"**

**Cause**: API key not configured or invalid

**Solution**:
1. Check if `.env` file exists and contains valid API key
2. Verify API key format (starts with `sk-`)
3. Ensure API key has sufficient credits
4. Check OpenAI service status

### **Issue: "Error generating LLM feedback"**

**Cause**: API connection issues or rate limits

**Solution**:
1. Check internet connection
2. Verify API key validity
3. Check OpenAI service status
4. Wait if rate limited

### **Issue: Empty feedback arrays**

**Cause**: LLM response parsing failed

**Solution**:
1. System automatically falls back to rule-based feedback
2. Check console for error messages
3. Verify API key permissions

## 💰 Cost Considerations

### **API Usage Costs**
- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Typical evaluation**: ~500-1000 tokens
- **Cost per evaluation**: ~$0.001-0.002

### **Cost Optimization**
- System uses efficient prompts
- Token limits prevent excessive usage
- Fallback mode available if needed

## 🔒 Security Best Practices

### **API Key Security**
1. **Never commit API keys to version control**
2. **Use environment variables**
3. **Rotate keys regularly**
4. **Monitor usage and costs**

### **File Permissions**
```bash
# Make .env file readable only by owner
chmod 600 .env
```

## 📊 Monitoring Usage

### **OpenAI Dashboard**
1. Go to [OpenAI Usage Dashboard](https://platform.openai.com/usage)
2. Monitor API usage and costs
3. Set up usage alerts if needed

### **System Logs**
Check console output for:
- API key validation messages
- LLM request/response logs
- Error messages and fallbacks

## 🎉 Success Indicators

### **When API Key is Working:**
- Console shows: "OpenAI API key loaded successfully"
- Evaluations show detailed AI feedback
- Strengths, weaknesses, and suggestions are populated
- Overall assessment contains intelligent analysis

### **When Using Fallback Mode:**
- Console shows: "Warning: OPENAI_API_KEY not found"
- Evaluations show basic rule-based feedback
- Still functional but with limited AI insights

## 🚀 Next Steps

1. **Set up your API key** using the steps above
2. **Test the system** with sample resumes and job descriptions
3. **Monitor usage** through OpenAI dashboard
4. **Enjoy AI-powered resume evaluation!**

---

**Need Help?** Check the troubleshooting section or review the console output for specific error messages.
