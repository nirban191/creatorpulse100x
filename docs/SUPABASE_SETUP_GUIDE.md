# Supabase Database Setup Guide 🗄️

## Why Supabase?

- **FREE**: Generous free tier (500MB database, 50K monthly users)
- **POSTGRESQL**: Full-featured relational database
- **REAL-TIME**: Instant updates across clients
- **ROW LEVEL SECURITY**: Built-in data protection
- **EASY**: Simple setup, great developer experience

## Quick Setup (5 minutes)

### Step 1: Create Supabase Project

1. Go to **https://supabase.com/**
2. Sign up with GitHub (takes 30 seconds)
3. Click **"New Project"**
4. Fill in details:
   - **Name**: `creatorpulse`
   - **Database Password**: Generate strong password (save it!)
   - **Region**: Choose closest to you
5. Wait 2 minutes for project to be created

### Step 2: Get API Credentials

1. Go to **Settings** > **API**
2. Copy these values:
   - **Project URL**: `https://xxx.supabase.co`
   - **anon/public key**: Long key starting with `eyJ...`

### Step 3: Run Database Schema

1. Go to **SQL Editor** in Supabase dashboard
2. Click **"New Query"**
3. Copy entire contents of `database/schema.sql`
4. Paste and click **"Run"**
5. Wait for success message ✅

### Step 4: Add to Your App

```bash
cd /Users/nirbanbiswas/Desktop/100x/code/creatorpulse

# Add to .env file
echo "SUPABASE_URL=https://your-project.supabase.co" >> .env
echo "SUPABASE_KEY=your_anon_key_here" >> .env
```

Or edit `.env` manually:
```
SUPABASE_URL=https://xxxproject.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Step 5: Install & Test

```bash
# Install supabase package
pip install supabase postgrest

# Test connection
python3 -c "from utils.supabase_client import get_db; db = get_db(); print('✅ Connected!' if db.is_configured() else '❌ Not configured')"
```

## Database Schema Overview

### Tables Created:

1. **profiles** - User profiles (extends auth.users)
2. **sources** - Connected content sources (Twitter/YouTube/RSS)
3. **drafts** - Generated newsletters
4. **feedback** - User feedback on drafts
5. **style_training** - Writing style training data
6. **email_sends** - Email delivery tracking
7. **analytics** - Usage analytics

### Key Features:

✅ **Row Level Security (RLS)** - Users can only access their own data
✅ **Automatic Timestamps** - Created/updated at tracking
✅ **Foreign Key Constraints** - Data integrity
✅ **Indexes** - Fast queries
✅ **Views** - Pre-computed statistics

## Using the Database

### In Your App:

The app automatically uses Supabase when configured:

```python
from utils.supabase_client import get_db

db = get_db()

# Add a source
db.add_source(user_id="xxx", source_type="twitter", identifier="elonmusk")

# Save a draft
db.save_draft(user_id="xxx", title="Weekly Digest", content="...", llm_provider="groq")

# Get user stats
stats = db.get_user_stats(user_id="xxx")
print(stats)  # {'total_drafts': 5, 'acceptance_rate': 75.0, ...}
```

### Benefits Over Session State:

| Feature | Session State | Supabase |
|---------|---------------|----------|
| Persistence | Lost on refresh | Permanent |
| Multi-device | No | Yes |
| Collaboration | No | Yes |
| Analytics | Limited | Full history |
| Backup | No | Automatic |

## Testing Without Supabase

The app works without Supabase:
- Falls back to session state
- All features still work
- Data lost on refresh
- Add Supabase when ready for production

## Database Schema Details

### profiles Table
```sql
- id (UUID, primary key)
- email (text, unique)
- full_name (text)
- avatar_url (text)
- preferred_llm_provider (text, default: 'groq')
- created_at, updated_at (timestamps)
```

### sources Table
```sql
- id (UUID, primary key)
- user_id (UUID, foreign key)
- source_type (text: 'twitter', 'youtube', 'newsletter')
- identifier (text: handle/channel/URL)
- is_active (boolean)
- last_fetched_at (timestamp)
- created_at, updated_at (timestamps)
```

### drafts Table
```sql
- id (UUID, primary key)
- user_id (UUID, foreign key)
- title (text)
- content (text)
- llm_provider (text)
- generation_time_ms (integer)
- status (text: 'draft', 'sent', 'scheduled', 'archived')
- sent_at (timestamp)
- recipient_count (integer)
- created_at, updated_at (timestamps)
```

### feedback Table
```sql
- id (UUID, primary key)
- user_id (UUID, foreign key)
- draft_id (UUID, foreign key)
- feedback_type (text: 'positive', 'negative')
- notes (text)
- created_at (timestamp)
```

## Advanced Features

### Real-Time Subscriptions

Listen to changes in real-time:

```python
# In future versions
db.client.table('drafts').on('INSERT', callback).subscribe()
```

### Custom Queries

```python
# Complex analytics
response = db.client.rpc('custom_analytics_function', {
    'user_id': user_id,
    'start_date': '2024-01-01'
}).execute()
```

### Backup & Export

In Supabase dashboard:
1. Go to **Database** > **Backups**
2. Download backup anytime
3. Restore if needed

## Security & Privacy

### Row Level Security (RLS)

Every table has RLS enabled:
- Users can ONLY see their own data
- Automatic user_id filtering
- PostgreSQL enforces at database level

### Data Privacy

- Passwords hashed by Supabase Auth
- API keys never stored in database
- HTTPS encryption for all requests
- EU/US data residency options

## Monitoring & Maintenance

### Dashboard Features:

1. **Table Editor** - View/edit data visually
2. **SQL Editor** - Run custom queries
3. **Logs** - See all database operations
4. **API Logs** - Debug API calls
5. **Database** > **Roles** - Manage permissions

### Common Queries:

```sql
-- View all users
SELECT * FROM profiles;

-- Draft count by provider
SELECT llm_provider, COUNT(*) FROM drafts GROUP BY llm_provider;

-- Acceptance rate per user
SELECT * FROM user_stats;

-- Recent activity
SELECT * FROM analytics ORDER BY created_at DESC LIMIT 100;
```

## Troubleshooting

### "relation does not exist"
- Run the schema.sql in SQL Editor
- Check that all tables were created
- Refresh SQL Editor

### "permission denied"
- RLS is blocking access
- Ensure user_id matches auth.uid()
- Check RLS policies in Table Editor

### "invalid API key"
- Use the **anon** public key (not service_role)
- Copy full key from Settings > API
- Check no extra spaces in .env

### Connection timeout
- Check SUPABASE_URL is correct
- Verify internet connection
- Try from Supabase dashboard first

## Supabase Free Tier Limits

| Resource | Free Tier | Paid |
|----------|-----------|------|
| Database | 500 MB | Unlimited |
| Storage | 1 GB | Unlimited |
| Bandwidth | 2 GB/mo | Unlimited |
| Monthly Users | 50,000 | Unlimited |
| API Requests | Unlimited | Unlimited |
| Backups | 7 days | 30 days |

**Perfect for CreatorPulse!**

## Migration from Session State

Already using the app? Migrate your data:

```python
# Export from session state
import json
with open('backup.json', 'w') as f:
    json.dump(st.session_state, f)

# Import to Supabase
db = get_db()
# ... add migration logic
```

## Production Best Practices

### 1. Use Environment Variables
Never commit `.env` to git:
```bash
echo ".env" >> .gitignore
```

### 2. Monitor Usage
Check dashboard weekly:
- Database size
- API requests
- Active users

### 3. Regular Backups
Set up automatic backups:
- Settings > Database > Backup schedule
- Download monthly snapshots

### 4. Optimize Queries
Use indexes for common queries:
```sql
CREATE INDEX idx_custom ON table_name(column_name);
```

## Next Steps

1. ✅ Create Supabase project (2 min)
2. ✅ Run schema.sql (1 min)
3. ✅ Add credentials to `.env`
4. ✅ Test connection
5. ✅ Use app normally - data now persists!
6. 🎉 Enjoy permanent storage!

## Resources

- **Supabase Docs**: https://supabase.com/docs
- **SQL Reference**: https://supabase.com/docs/guides/database
- **Dashboard**: https://supabase.com/dashboard
- **Status**: https://status.supabase.com/

## Pro Tips

1. **Use Table Editor** for quick data viewing
2. **Test queries in SQL Editor** before code
3. **Monitor logs** to debug issues
4. **Set up email auth** for production
5. **Use database functions** for complex logic

---

**Questions?**
- Supabase Discord: https://discord.supabase.com
- Supabase Support: support@supabase.io
- CreatorPulse Issues: See main README.md

**Fun Fact**: Supabase is open source! You can self-host if needed.
