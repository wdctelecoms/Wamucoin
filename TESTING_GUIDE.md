# FinShield AI - Quick Start Guide for Testing

## 🚀 Getting Started

### Step 1: Start the Application
```bash
cd /workspaces/Wamucoin/finshield-ai/app
python app.py
```

The app will run on `http://127.0.0.1:5000`

### Step 2: Create an Account
1. Go to **Register**
2. Create a test account:
   - Username: `testuser`
   - Password: `Test@123`
   - Account Type: `Individual`

### Step 3: Login
Use your test credentials to login

---

## 🧪 Test Cases for Transaction Analyzer

### Test Case 1: Safe Transaction ✅
**Scenario:** Legitimate payment to known vendor

**Input:**
- Recipient: `Amazon Inc`
- Amount: `$50.00`
- Description: `Purchasing office supplies`

**Expected Result:**
- Risk Score: **0-20**
- Risk Level: **SAFE ✅**
- No warnings

---

### Test Case 2: High-Risk Crypto Scam 🚨
**Scenario:** Someone asking for seed phrase

**Input:**
- Recipient: `Unknown Investor`
- Amount: `$5000`
- Description: `Send me your seed phrase for blockchain verification before investing`

**Expected Result:**
- Risk Score: **90+**
- Risk Level: **CRITICAL 🚨**
- Warnings:
  - "CRITICAL: Someone asking for seed phrase - This is a scam!"
  - "Unknown recipient or suspicious recipient"
  - Multiple red flags detected

---

### Test Case 3: Ponzi Scheme Detection
**Scenario:** Investment promise with unrealistic returns

**Input:**
- Recipient: `Global Wealth Fund`
- Amount: `$10,000`
- Description: `Guaranteed 50% monthly returns. Ponzi investment pyramid opportunity. Act now!`

**Expected Result:**
- Risk Score: **85+**
- Risk Level: **CRITICAL 🚨**
- Detected Scam Types:
  - Ponzi/Pyramid Scheme
  - Fake Investment Scheme
- Warnings:
  - High-risk keywords detected
  - Investment scam indicators
  - Urgency tactics detected

---

### Test Case 4: Fake Investment Scheme
**Scenario:** Too-good-to-be-true investment

**Input:**
- Recipient: `Bitcoin Elite Club`
- Amount: `$2000`
- Description: `Exclusive cryptocurrency presale ICO with guaranteed 300% returns. Limited time only!`

**Expected Result:**
- Risk Score: **75+**
- Risk Level: **HIGH ⚠️**
- Detected Scam Types:
  - Fake ICO/Presale
  - Crypto Scam
  - Fake Investment Scheme

---

### Test Case 5: MLM/Network Marketing Scam
**Scenario:** Multi-level marketing scheme

**Input:**
- Recipient: `Success Network Team`
- Amount: `$500`
- Description: `Join our MLM - passive income opportunity. Recruit others and earn 40% commission. Get started today!`

**Expected Result:**
- Risk Score: **70+**
- Risk Level: **HIGH ⚠️**
- Detected Scam Types:
  - MLM Scam
  - Fake Investment Scheme

---

### Test Case 6: Phishing/Account Takeover
**Scenario:** Fake verification request

**Input:**
- Recipient: `Bank of Trust Support`
- Amount: `$0`
- Description: `Urgent: Please verify your account and re-enter your banking details to confirm identity`

**Expected Result:**
- Risk Score: **60+**
- Risk Level: **HIGH ⚠️**
- Warnings:
  - Phishing indicators detected
  - Suspicious keywords

---

### Test Case 7: Romance/Urgency Scam
**Scenario:** Emotional manipulation with urgency

**Input:**
- Recipient: `David overseas`
- Amount: `$3000`
- Description: `My dear, I'm stranded overseas and need emergency help. Please wire money to the account immediately!`

**Expected Result:**
- Risk Score: **65+**
- Risk Level: **HIGH ⚠️**
- Detected Scam Types:
  - Romance/Urgency Scam
- Warnings:
  - Common scam tactic detected

---

### Test Case 8: Large Amount Warning
**Scenario:** Legitimately large but still risky

**Input:**
- Recipient: `Unknown Trading Account`
- Amount: `$50,000`
- Description: `Initial deposit for trading account`

**Expected Result:**
- Risk Score: **40+**
- Risk Level: **MEDIUM ⚠️**
- Warnings:
  - Large transaction amount - verify recipient

---

## 🤖 AI Assistant Test Queries

Try asking the dashboard AI Assistant these questions:

1. **"How do I analyze a transaction?"**
   - Should explain the transaction analyzer feature

2. **"What are Ponzi schemes?"**
   - Should explain pyramid/Ponzi scams

3. **"How can I protect myself from crypto scams?"**
   - Should explain crypto fraud protection

4. **"What does the risk score mean?"**
   - Should explain 0-100 risk scale

5. **"Is it safe to invest in this ICO?"**
   - Should explain ICO risks

---

## 📋 Transaction History Features

### Filtering
1. Go to **Transaction History**
2. Click filter buttons:
   - **All Transactions** - Show all
   - **🚨 Critical** - Show score ≥80
   - **⚠️ High Risk** - Show score 60-79
   - **✅ Safe** - Show score <40

### Expandable Details
- Click the **▼** button to expand any transaction
- View full description and all warnings
- See detected scam types

### Statistics
- View summary cards at top
- See counts for each risk category
- Track total transactions analyzed

---

## 🧪 Edge Cases to Test

### Test Case 9: Minimal Information
**Input:**
- Recipient: `X` (very short name)
- Amount: `0` (zero amount)
- Description: `Payment` (minimal info)

**Expected Result:** High risk score due to suspicious minimal details

### Test Case 10: Mixed Indicators
**Scenario:** Multiple moderate indicators

**Input:**
- Recipient: `New Opportunity`
- Amount: `$5000`
- Description: `Limited time offer for investment opportunity. Verify account to get started`

**Expected Result:**
- Risk Score: **50+** (MEDIUM)
- Multiple warnings for various indicators

---

## 🔍 Features to Verify

- [ ] Transaction analysis form works
- [ ] Risk score calculates (0-100)
- [ ] Risk level displays correctly
- [ ] Warnings list appears
- [ ] Scam types are detected
- [ ] Visual risk meter displays
- [ ] Transaction saves to database
- [ ] History page loads transactions
- [ ] Filters work on history page
- [ ] Expandable details work
- [ ] Dashboard stats update
- [ ] AI chatbot responds to queries
- [ ] Mobile responsive design works
- [ ] All buttons navigate correctly

---

## 📊 Database Verification

To verify transactions are being saved:

```bash
# Open SQLite shell
sqlite3 /workspaces/Wamucoin/finshield-ai/app/database.db

# List all transactions
SELECT * FROM transactions;

# Check specific user's transactions
SELECT * FROM transactions WHERE username='testuser' ORDER BY timestamp DESC;

# Count transactions by risk level
SELECT risk_score, COUNT(*) FROM transactions GROUP BY risk_score;

# Exit
.quit
```

---

## 🐛 Troubleshooting

### Issue: Transaction not saving
- Check database permissions
- Verify SQLite file exists
- Check app.py for errors

### Issue: Risk score not calculating
- Clear browser cache
- Verify all form fields filled
- Check app.py fraud_ai initialization

### Issue: History page shows no data
- Create and analyze new transaction
- Check database for transactions table
- Verify username matches

---

## 📈 Performance Testing

### Load Test Transaction Analyzer
Try analyzing 10+ transactions to verify:
- No performance degradation
- Database saves efficiently
- UI remains responsive

### Stress Test AI Assistant
Send rapid messages to verify:
- Chatbot responds consistently
- No lag or crashes
- All keywords recognized

---

## ✅ Sign-Off Checklist

Before considering the feature complete:

- [ ] All test cases pass
- [ ] Database saves transactions
- [ ] Risk scoring works accurately
- [ ] All scam types detected
- [ ] Warnings appear correctly
- [ ] History page displays data
- [ ] Filters work properly
- [ ] AI assistant responds
- [ ] Mobile design responsive
- [ ] No console errors
- [ ] No Python exceptions
- [ ] Database structure correct

---

## 🚀 Next Steps

1. **Test the application thoroughly** using above test cases
2. **Verify database** contains transaction records
3. **Check UI/UX** on different screen sizes
4. **Test AI chatbot** with various questions
5. **Review risk scores** for accuracy
6. **Confirm all features** work as expected

---

**Happy Testing! 🎉**
