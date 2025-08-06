# ☁️ Cloud Infra Automation Suite

This project is my no-nonsense take on building a complete cloud automation pipeline — fully deployed, tested, and pushed without over-engineering anything.

### 🔧 What it Does

- **Daily Cloud Reports** sent via **AWS Lambda + SES**
- Reports include:
  - 💸 AWS Billing cost
  - 📈 Log event size (CloudWatch)
  - 🌤️ Weather from OpenWeather API (because why not)
- Runs on a schedule (EventBridge)
- All infra is built and deployed using **Terraform**
- Includes a working **EC2 + Load Balancer setup**

### 📦 What's Inside

- `terraform/`: All infrastructure code
- `lambda/`: Python function to send the daily email report
- `.gitignore`: Cleaned up to avoid committing heavy junk like provider binaries & zip files

### 🧪 Tested & Working

I deployed and tested this whole setup myself. Everything runs automatically, sends daily updates, and the whole thing can be torn down and rebuilt from scratch.

### 🧠 Why I Did This

No fluff, no tutorials copied. I wanted to:
- Actually *build something real* with AWS
- Make sure I understand how infra-as-code, Lambda, email alerts, and cost analysis works
- Prove that I can ship — fast and clean

And I did.

---

## 🚀 Next Up

Might extend this with:
- S3 logs analysis
- Multi-region failover setup
- Dashboard UI for viewing reports

But honestly? This version does the job damn well.

---

## 💬 Final Words

If you're reading this and you're a recruiter or engineer — I’m just getting started.  
Give me tools, give me specs, I’ll build fast and I’ll build right.

