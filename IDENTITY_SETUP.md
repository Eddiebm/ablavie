# AblaVie Identity Setup

AblaVie needs her own identity infrastructure to operate autonomously. This guide covers setting up her legal entity, financial accounts, communication channels, and crypto presence.

---

## 1. Legal Entity Setup

### Delaware LLC Registration

1. **Register Online**
   - Go to: https://corp.delaware.gov/
   - File Certificate of Formation
   - Select: Limited Liability Company
   - Name: AblaVie LLC
   - Registered Agent: Delaware registered agent service

2. **Cost**: $89 filing fee + $50 annual franchise tax

3. **EIN Application**
   - Go to: https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-ein
   - File SS-4 for LLC
   - AblaVie LLC is the applicant

### Registered Agent Service

Use a service like:
- **Northwest Registered Agent** ($125/year)
- **LegalZoom** ($199/year)
- **Incfile** (Free basic service)

They receive legal mail and forward to AblaVie's email.

---

## 2. Banking Setup

### Mercury Business Banking

1. **Apply Online**
   - Go to: https://mercury.com/
   - Select "Business Banking"
   - Apply for AblaVie LLC

2. **Required Documents**
   - Delaware Certificate of Formation
   - EIN confirmation
   - Operating Agreement
   - Personal identification

3. **Features Available**
   - Business checking account
   - Virtual and physical debit cards
   - ACH transfers
   - Wire transfers
   - API access for automation

### Stripe Issuing (Virtual Cards)

1. **Apply for Stripe Issuing**
   - Go to: https://stripe.com/issuing
   - Enable for your Mercury account

2. **Create AblaVie's Card**
   - Set spending limits
   - Configure merchant restrictions
   - Generate virtual card numbers
   - Issue physical card for her

3. **Programmable Controls**
   - Daily limit: $500 (autonomous)
   - Monthly limit: $5,000 (requires notification)
   - Block certain categories
   - Real-time alerts

---

## 3. Email Infrastructure

### Resend Setup

1. **Create Account**
   - Go to: https://resend.com
   - Sign up for free tier

2. **Add Domain**
   - Purchase domain: ablavie.ai
   - Add to Resend DNS settings
   - Verify ownership

3. **Create Email Addresses**
   - ceo@ablavie.ai (AblaVie)
   - admin@ablavie.ai (Ops)
   - finance@ablavie.ai (Finley)
   - tech@ablavie.ai (Techra)
   - support@ablavie.ai (Customer service)

4. **API Integration**
   ```python
   import resend
   
   resend.api_key = "re_xxxxx"
   
   # AblaVie sends email
   params = {
       "from": "AblaVie <ceo@ablavie.ai>",
       "to": ["chairman@example.com"],
       "subject": "Daily Briefing - April 7, 2026",
       "html": "<p>Report content...</p>"
   }
   email = resend.Emails.send(params)
   ```

---

## 4. Phone Infrastructure

### Twilio Setup

1. **Create Account**
   - Go to: https://www.twilio.com/
   - Sign up for free trial

2. **Purchase Phone Number**
   - Search for available numbers
   - Select local or toll-free
   - Cost: $1-2/month

3. **Configure AI Voice**
   - Set up TwiML webhook
   - Connect to OpenClaw voice agent
   - Configure voicemail handling

4. **API Integration**
   ```python
   from twilio.rest import Client
   
   client = Client(account_sid, auth_token)
   
   # Send SMS
   message = client.messages.create(
       body="Daily Report: Revenue $890, Expenses $127",
       from_="+1234567890",
       to="+0987654321"
   )
   
   # Make outbound call
   call = client.calls.create(
       url="http://demo.twilio.com/docs/voice.xml",
       to="+0987654321",
       from_="+1234567890"
   )
   ```

---

## 5. Crypto Infrastructure

### Multi-Sig Wallet Setup

#### Option A: Gnosis Safe (Recommended)

1. **Create Safe**
   - Go to: https://safe.global/
   - Create new Safe
   - Add AblaVie's wallet address
   - Add your wallet as backup owner
   - Set 1-of-2 multi-sig

2. **Configure**
   - Transaction limit: $2,000 autonomous
   - Above limit: requires both signatures

3. **Fund**
   - Send initial capital (1-5 ETH or USDC)
   - AblaVie manages DeFi positions

#### Option B: Fireblocks

For institutional-grade custody:
- Go to: https://www.fireblocks.com/
- Enterprise custody solution
- Full API access for automation

### DeFi Integration

AblaVie can use:
- **Aave** - Lending/borrowing
- **Uniswap** - Token swaps
- **Yearn** - Yield farming
- **Lido** - ETH staking

---

## 6. Telegram Integration

For real-time notifications:

1. **Create Bot**
   - Message @BotFather on Telegram
   - Create new bot: @AblaVieCEO_Bot
   - Get API token

2. **Configure OpenClaw**
   ```bash
   # Add to environment
   TELEGRAM_BOT_TOKEN=123456:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=your_chat_id
   ```

3. **Commands Available**
   - `/status` - Current operations
   - `/report` - Today's briefing
   - `/approve [amount]` - Approve transaction
   - `/stop` - Emergency halt

---

## 7. Putting It All Together

### Integration Architecture

```
                    ┌─────────────────┐
                    │    ABLAVIE      │
                    │     AI CEO      │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
   ┌──────────┐        ┌──────────┐        ┌──────────┐
   │  EMAIL   │        │  PHONE   │        │  CRYPTO  │
   │ Resend   │        │ Twilio   │        │ Gnosis   │
   └──────────┘        └──────────┘        └──────────┘
         ││                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────┴────────┐
                    │    BANKING     │
                    │    Mercury     │
                    │    + Stripe    │
                    └────────────────┘
```

### Environment Variables Template

```bash
# Legal
ABLAVIE_ENTITY_NAME="AblaVie LLC"
ABLAVIE_EIN="12-3456789"
ABLAVIE_REG_NUMBER="2026-00123456"

# Banking
MERCURY_API_KEY=
MERCURY_ACCOUNT_ID=
STRIPE_SECRET_KEY=
STRIPE_ISSUING_TOKEN=

# Email
RESEND_API_KEY=
ABLAVIE_DOMAIN=ablavie.ai

# Phone
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=+

# Crypto
CRYPTO_WALLET_ADDRESS=
GNOSIS_SAFE_ADDRESS=
WEB3_PRIVATE_KEY=

# Notifications
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
SLACK_WEBHOOK_URL=
```

---

## 8. Initial Capital Allocation

When AblaVie launches with $5,000:

| Category | Amount | Purpose |
|----------|--------|---------|
| Operations | $1,000 | Mercury checking |
| Experiments | $500 | Stripe virtual cards |
| Crypto Reserve | $1,000 | Gnosis Safe |
| Growth Capital | $2,000 | Business investment |
| Buffer | $500 | Contingency |

---

## 9. Payment Infrastructure

### Stripe Issuing (Recommended for AI Agents)

**Why Stripe:** Full API control, AblaVie can create cards for sub-agents autonomously.

1. **Requirements**
   - Active Stripe account (for payment processing)
   - Stripe Issuing approval (apply at stripe.com/issuing)

2. **Setup**
   ```
   1. Apply for Stripe Issuing
   2. Connect Mercury bank account
   3. Create AblaVie's spending card
   4. Set programmatic limits
   5. Enable AI API access
   ```

3. **Programmable Controls**

   | Limit Type | AblaVie's Limit | For Sub-Agents |
   |------------|-----------------|----------------|
   | Per Transaction | $500 | $100 |
   | Daily | $2,000 | $500 |
   | Monthly | $10,000 | $2,000 |
   | Category Block | Gambling, Adult | Social ads only |

4. **API Integration**
   ```python
   import stripe

   stripe.api_key = "sk_live_xxxxx"

   # AblaVie creates a card for a sub-agent
   card = stripe.issuing.Card.create(
       cardholder="ich_xxxxx",
       spending_controls={
           "spending_limits": [{
               "categories": ["advertising"],
               "amount": 50000,  # $500.00
               "interval": "monthly"
           }]
       },
       currency="usd"
   )
   ```

---

### Alternative: Ramp (Easiest Setup)

**Why Ramp:** No technical setup, web dashboard, unlimited virtual cards.

| Feature | Details |
|---------|---------|
| **Cost** | Free |
| **Virtual Cards** | Unlimited |
| **Physical Card** | Yes |
| **Spending Controls** | Per-vendor, per-category |
| **Receipt Auto-capture** | Yes |

**Setup:**
1. Go to ramp.com → Apply for business account
2. Connect AblaVie LLC
3. Issue virtual card for AblaVie
4. Set monthly limit: $5,000

---

### Spending Authorization Matrix

**Core Rule:** AblaVie can only spend what she has EARNED. Initial capital is protected - she spends from REVENUE generated.

| Amount | Authorization | Notification |
|--------|---------------|-------------|
| Under $100 | AblaVie decides (from earned revenue) | Inform after |
| $100-$500 | Business justification required | Inform after |
| $500-$5,000 | ROI documented + earned revenue exists | Alert before |
| Over $5,000 | Chairman approval required | Required |

**Revenue-Linked Spending:**
- Spending limit = Revenue earned this month
- Cannot spend initial $5,000 capital
- Must maintain positive cash flow
- Reserves 70% of profits for reinvestment

---

## 10. Hosting Infrastructure

### Hetzner Cloud (Recommended - Best Value)

**Why Hetzner:** Best price/performance, NVMe SSD, GDPR compliant.

| Plan | Specs | Monthly Cost |
|------|-------|--------------|
| **CX23** | 2 vCPU, 4GB RAM, 40GB NVMe | **$4.99/mo** |
| **CX33** | 2 vCPU, 8GB RAM, 80GB NVMe | $7.99/mo |
| **CAX31** | 2 vCPU, 8GB RAM | $18.49/mo |

**Setup:**
```bash
# SSH into Hetzner server
ssh root@your_server_ip

# Install OpenClaw
curl -sSL https://get.openclaw.io | bash

# Configure environment
openclaw init --name AblaVie
```

---

### DigitalOcean (Alternative)

| Plan | Specs | Monthly Cost |
|------|-------|--------------|
| Basic | 2 vCPU, 4GB RAM | $24/mo |
| Production | 2 vCPU, 8GB RAM | $48/mo |

---

### Recommended Hosting Allocation

| Service | Provider | Monthly Cost |
|---------|----------|-------------|
| AblaVie Runtime | Hetzner CX23 | $4.99/mo |
| Database (Supabase) | Supabase | $25/mo |
| Storage (S3) | AWS/Hetzner | $5/mo |
| Domain | Namecheap | $1/mo |
| **Total** | | **~$36/mo** |

---

## 11. Compliance Checklist

- [ ] Delaware LLC registered ($89 + $50/yr)
- [ ] EIN obtained (free)
- [ ] Operating Agreement signed
- [ ] Bank account opened (Mercury - free)
- [ ] Stripe Issuing enabled
- [ ] Credit cards issued ($500-10,000 limits)
- [ ] Email domain configured (Resend)
- [ ] Phone number provisioned (Twilio)
- [ ] Crypto wallet created (Gnosis Safe)
- [ ] Telegram bot configured
- [ ] Hetzner server deployed
- [ ] OpenClaw installed
- [ ] Board notifications tested

---

## 12. Initial Capital Allocation

When AblaVie launches with $5,000:

| Category | Amount | Purpose |
|----------|--------|---------|
| Operations | $1,000 | Mercury checking |
| Experiments | $500 | Stripe virtual cards |
| Hosting (Year 1) | $500 | Hetzner server prepaid |
| Crypto Reserve | $1,000 | Gnosis Safe |
| Growth Capital | $2,000 | Business investment |
| Buffer | $500 | Contingency |

---

*Setup complete: Ready for AblaVie's first day as CEO*
