# 📧 Resend Email Setup Guide

## Understanding Resend's Email Restrictions

### Free Tier Limitations:
- ✅ Can send test emails to **your own verified email** only
- ❌ Cannot send to other recipients without domain verification
- ✅ 100 emails/day for free
- ✅ 3,000 emails/month for free

### To Send to Other Recipients:
You **must verify a custom domain** (e.g., `newsletter.yourcompany.com`)

---

## Option 1: Testing Mode (Current Setup)

**What works:**
- Generate newsletters with AI ✅
- Preview newsletters in the app ✅
- Copy/download newsletter content ✅
- Send test emails to **nirban.biswas595@gmail.com** ✅

**What doesn't work:**
- Sending to other email addresses ❌ (requires domain verification)

**How to use:**
1. Generate your newsletter
2. Use the "Send Test Email" button
3. Email will be sent to: `nirban.biswas595@gmail.com`
4. Check your inbox to see the formatted newsletter

---

## Option 2: Verify a Domain (Production Setup)

### Step 1: Get a Domain

You need to own a domain name. Options:
- **Free**: Use a subdomain from Cloudflare, Netlify, or Vercel
- **Paid**: Buy from Namecheap, GoDaddy (~$10/year)
- **Recommended for newsletters**: Use your existing website domain

### Step 2: Add Domain to Resend

1. Go to: https://resend.com/domains
2. Click **"Add Domain"**
3. Enter your domain (e.g., `yourcompany.com`)
4. Or use a subdomain (e.g., `mail.yourcompany.com`)

### Step 3: Add DNS Records

Resend will provide DNS records to add:

**Example DNS Records:**
```
Type: TXT
Name: @
Value: resend-verify-abc123xyz456...

Type: MX
Name: @
Priority: 10
Value: mx1.resend.com

Type: MX
Name: @
Priority: 20
Value: mx2.resend.com

Type: TXT
Name: resend._domainkey
Value: p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQ...
```

**Where to add these:**
- If using Cloudflare: Dashboard → DNS → Add Record
- If using Namecheap: Domain List → Manage → Advanced DNS
- If using GoDaddy: Domain Settings → DNS Management

### Step 4: Verify Domain

1. After adding DNS records (wait 5-60 minutes for propagation)
2. Go back to Resend dashboard
3. Click **"Verify Domain"**
4. Wait for green checkmark ✅

### Step 5: Update From Address

Once verified, update your `.env` file:

```bash
# Change from:
RESEND_FROM_EMAIL=CreatorPulse <newsletter@resend.dev>

# To your verified domain:
RESEND_FROM_EMAIL=CreatorPulse <newsletter@yourcompany.com>
```

### Step 6: Test Sending

Now you can send to any email address!

---

## Option 3: Use Alternative Email Service (No Domain Required)

If you don't want to verify a domain, consider these alternatives:

### A. Gmail SMTP (Free)
- Use Gmail's SMTP server
- Limit: 500 emails/day
- Setup: Enable "App Password" in Gmail settings

### B. SendGrid Free Tier
- 100 emails/day free (no domain required for testing)
- Easier for beginners

### C. Mailgun Free Tier
- 5,000 emails/month free
- Requires credit card

### D. Just Use the App UI
- Generate newsletters in CreatorPulse
- Copy the content
- Paste into your existing email platform (Substack, Beehiiv, etc.)

---

## Current Workaround for CreatorPulse

Until you verify a domain, here's how to use the app:

### Method 1: Test Email to Yourself
```
1. Generate newsletter with AI
2. Click "Send Test Email"
3. Check nirban.biswas595@gmail.com inbox
4. Forward it manually to subscribers
```

### Method 2: Copy & Paste
```
1. Generate newsletter with AI
2. Click "Copy to Clipboard" or "Download as Markdown"
3. Paste into:
   - Substack editor
   - Beehiiv editor
   - Gmail compose
   - Any email platform
```

### Method 3: Export & Use Your Platform
```
1. Generate newsletter
2. Export as HTML or Markdown
3. Import to your existing newsletter tool
4. Send through their verified system
```

---

## Recommended Setup for Production

**Best approach:**

1. **Use a subdomain** (e.g., `mail.yoursite.com`)
   - Keeps your main domain separate
   - Easier to manage email reputation

2. **Verify with Resend**
   - Fast email delivery
   - Great API
   - Good free tier

3. **Update app configuration**
   - Set `RESEND_FROM_EMAIL` to your verified domain
   - Add domain to environment variables

4. **Test thoroughly**
   - Send test emails first
   - Check spam folders
   - Monitor delivery rates

---

## FAQ

### Q: Do I need a domain to use CreatorPulse?
**A:** No! You can still:
- Generate AI newsletters ✅
- Preview content ✅
- Export/copy content ✅
- Send test emails to yourself ✅

You only need a domain to send to multiple recipients automatically.

### Q: Can I use a free domain?
**A:** Not really. Free domains (like `.tk`, `.ml`) are often blocked by email providers. You need a real domain (~$10/year).

### Q: What if I already have Substack/Beehiiv?
**A:** Perfect! Just:
1. Generate newsletter in CreatorPulse
2. Copy the content
3. Paste into Substack/Beehiiv editor
4. Send through their platform (they handle email delivery)

### Q: How long does domain verification take?
**A:** Usually 5-30 minutes, sometimes up to 24 hours for DNS propagation.

### Q: Can I verify a subdomain?
**A:** Yes! Use `mail.yoursite.com` or `newsletter.yoursite.com`

---

## Quick Setup Checklist

- [ ] Have a domain name
- [ ] Access to DNS settings
- [ ] Add domain to Resend dashboard
- [ ] Copy DNS records from Resend
- [ ] Add DNS records to your domain provider
- [ ] Wait for DNS propagation (5-60 minutes)
- [ ] Verify domain in Resend
- [ ] Update `.env` with verified from address
- [ ] Test sending to different email addresses
- [ ] Check spam folders
- [ ] Monitor delivery rates

---

## Support Resources

- **Resend Docs**: https://resend.com/docs
- **Resend Domains**: https://resend.com/domains
- **DNS Checker**: https://dnschecker.org
- **Email Test Tool**: https://www.mail-tester.com

---

## Summary

**Current Status:**
- ✅ CreatorPulse AI newsletter generation works perfectly
- ✅ You can send test emails to `nirban.biswas595@gmail.com`
- ❌ Cannot send to other emails yet (need domain verification)

**To send to anyone:**
1. Get/use a domain
2. Verify it with Resend
3. Update from address
4. Start sending! 📧

**Or just:**
- Use CreatorPulse for AI generation
- Copy/paste content to your existing newsletter platform
- They handle the email sending

**CreatorPulse's main value is AI-powered content curation and newsletter generation - email delivery is optional!** 🚀
