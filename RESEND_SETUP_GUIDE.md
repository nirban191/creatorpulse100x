# Resend Email Setup Guide 📧

## Why Resend?

- **FREE**: 100 emails/day, 3,000 emails/month on free tier
- **SIMPLE**: Clean API, easy integration
- **FAST**: Email delivery in seconds
- **MODERN**: Built for developers
- **NO SPAM**: High deliverability rates

## Quick Setup (3 minutes)

### Step 1: Get Your Free API Key

1. Go to **https://resend.com/**
2. Sign up with Google/GitHub (takes 30 seconds)
3. Click **"API Keys"** in the sidebar
4. Click **"Create API Key"**
5. Give it a name like "CreatorPulse"
6. Copy the key (starts with `re_...`)

### Step 2: Add to Your App

```bash
cd /Users/nirbanbiswas/Desktop/100x/code/creatorpulse
echo "RESEND_API_KEY=re_YOUR_KEY_HERE" >> .env
```

Or edit `.env` manually:
```
RESEND_API_KEY=re_your_key_here
```

### Step 3: Verify Domain (Optional but Recommended)

For production use, verify your domain:

1. Go to **Domains** in Resend dashboard
2. Click **"Add Domain"**
3. Enter your domain (e.g., `mydomain.com`)
4. Add the DNS records Resend provides
5. Wait for verification (usually < 5 minutes)

**For testing**: Use `newsletter@resend.dev` (no verification needed!)

### Step 4: Install & Restart

```bash
# Install resend package
pip install resend

# Restart the app
pkill -f "streamlit run"
streamlit run app_enhanced.py
```

## Using Email Feature

### In the App:

1. **Generate a newsletter** in "Generate Newsletter" page
2. Click **"📧 Send Email"** button on any draft
3. Fill in the form:
   - **Recipients**: One email per line
   - **From**: Use `newsletter@resend.dev` for testing
   - **Subject**: Auto-filled from newsletter title
   - **Test mode**: Check for test emails
4. Click **"📤 Send Now"**
5. Watch it send! 🎉

### Email Features:

✅ **Beautiful HTML formatting** - Markdown converted to styled HTML
✅ **Mobile responsive** - Looks great on all devices
✅ **Multiple recipients** - Send to entire list at once
✅ **Test mode** - Send test emails before going live
✅ **Custom branding** - Use your verified domain
✅ **Unsubscribe links** - Built into footer

## Resend Free Tier Limits

| Feature | Free Tier | Paid |
|---------|-----------|------|
| Emails/day | 100 | Unlimited |
| Emails/month | 3,000 | Unlimited |
| Recipients | Unlimited | Unlimited |
| Domains | 1 | Unlimited |
| API Keys | Unlimited | Unlimited |
| Support | Community | Priority |

**Perfect for testing and small newsletters!**

## Email Template Preview

Your newsletters will be sent with:
- Clean, professional design
- Purple accent colors (brand colors)
- Mobile-responsive layout
- Proper typography
- Code syntax highlighting
- Clickable links
- Unsubscribe footer

## Testing Without API Key

The app works without Resend API key:
- "Send Email" button will show configuration warning
- You can still download and copy newsletters
- Add key when ready to actually send emails

## Production Best Practices

### 1. Verify Your Domain
```
# Instead of newsletter@resend.dev use:
newsletter@yourdomain.com
```

Benefits:
- Better deliverability
- Custom branding
- Professional appearance
- Higher trust from email clients

### 2. Warm Up Your Domain

Start small:
- Day 1: Send to 10-20 people
- Day 2: Send to 50 people
- Week 1: Send to 200 people
- After 2 weeks: Send to your full list

This improves deliverability!

### 3. Monitor Bounces

In Resend dashboard:
- Check delivery rates
- Monitor bounces
- Review spam complaints
- Track opens (optional)

### 4. Use Reply-To Address

Add this to the code:
```python
reply_to="youremail@domain.com"
```

So recipients can respond to you directly.

## Troubleshooting

### "Invalid API Key"
- Check that key starts with `re_`
- Verify no extra spaces in `.env`
- Make sure `.env` is in project root
- Try creating a new key

### "Domain Not Verified"
- For testing, use `newsletter@resend.dev`
- For production, add DNS records
- Wait 5-10 minutes for DNS propagation
- Check verification status in dashboard

### "Rate Limit Exceeded"
- Free tier: 100/day, 3,000/month
- Wait until next day/month
- Or upgrade to paid plan
- Consider batching emails

### "Email Not Received"
- Check spam folder
- Verify recipient email is correct
- Look at Resend dashboard for delivery status
- Check domain verification
- Test with different email provider

## Advanced: Programmatic Usage

```python
from utils.email_sender import NewsletterEmailSender

# Initialize
sender = NewsletterEmailSender()

# Send newsletter
result = sender.send_newsletter(
    to_emails=["subscriber1@example.com", "subscriber2@example.com"],
    subject="Weekly Tech Digest",
    content="# Your Newsletter\n\nContent goes here...",
    from_email="newsletter@yourdomain.com"
)

# Check result
if result['success']:
    print(f"Sent to {result['recipients']} recipients!")
else:
    print(f"Error: {result['error']}")
```

## Email Template Customization

Edit `utils/email_sender.py` to customize:

```python
def _markdown_to_html(self, markdown_content: str) -> str:
    # Modify HTML template here
    # Change colors, fonts, layout, etc.
    pass
```

## Scheduling Emails

For automated sending:

```python
import schedule
import time

def send_daily_newsletter():
    # Your newsletter generation code
    # Then call send_newsletter()
    pass

# Schedule for 8 AM daily
schedule.every().day.at("08:00").do(send_daily_newsletter)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Comparison with Alternatives

| Feature | Resend | SendGrid | Mailchimp | Postmark |
|---------|--------|----------|-----------|----------|
| Free Tier | 3K/mo | 100/day | 500 contacts | Trial only |
| Easy Setup | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Developer UX | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Price | Best | High | High | Medium |
| Deliverability | Great | Great | Good | Great |

## Resend API Models

### Available Endpoints:
- `Emails.send()` - Send single/multiple emails
- `Emails.get()` - Retrieve email status
- `Domains.list()` - List verified domains
- `Domains.create()` - Add new domain
- `ApiKeys.list()` - List API keys

## Rate Limits (Free Tier)

- **Emails**: 100 per day, 3,000 per month
- **API Calls**: No hard limit
- **Recipients**: Unlimited per email
- **Attachment Size**: 40MB total

## Next Steps

1. ✅ Get Resend API key (3 min)
2. ✅ Add to `.env` file
3. ✅ Restart app
4. ✅ Generate a newsletter
5. ✅ Click "Send Email"
6. ✅ Test with your email
7. 🎉 Go live!

## Resources

- **Resend Docs**: https://resend.com/docs
- **API Reference**: https://resend.com/docs/api-reference
- **Dashboard**: https://resend.com/emails
- **Status Page**: https://status.resend.com/

## Pro Tips

1. **Start with tests**: Always send test emails first
2. **Check spam score**: Use mail-tester.com
3. **Monitor metrics**: Track opens and clicks
4. **Build slowly**: Warm up your domain properly
5. **Use templates**: Consistent branding improves trust

---

**Questions?**
- Resend Support: support@resend.com
- Resend Discord: https://resend.com/discord
- CreatorPulse Issues: See main README.md

**Fun Fact**: Resend was built by the team behind React Email - so emails look beautiful by default!
