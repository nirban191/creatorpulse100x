# Fix: "Database not configured. Source not saved."

## The Problem

You're seeing this warning because Row Level Security (RLS) is enabled on your Supabase tables. RLS requires authentication, but the app is currently using a demo user without auth.

## Quick 2-Minute Fix

### Step 1: Open Supabase SQL Editor

Go to: https://supabase.com/dashboard/project/htqwegnixlhdhrdbjkgp/editor

### Step 2: Run This SQL

1. Click "+ New query" (top right)
2. Copy and paste this entire code block:

```sql
-- Disable RLS for Development Mode
-- This allows the app to work without authentication

ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.sources DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.drafts DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.style_training DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.email_sends DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.analytics DISABLE ROW LEVEL SECURITY;

SELECT 'RLS disabled - app will now work!' AS status;
```

3. Click **"Run"** (bottom right) or press Cmd/Ctrl + Enter
4. You should see: "RLS disabled - app will now work!"

### Step 3: Refresh Your Browser

- Go back to http://localhost:8501
- Refresh the page (Cmd/Ctrl + R)
- Try adding "elonmusk" as a Twitter source again
- Should now see: ✅ "Added @elonmusk" instead of the warning!

## What This Does

- **Disables authentication requirement** for development
- Allows the app to save data to your database
- All your sources, drafts, and emails will persist permanently

## ⚠️  For Production Later

When you're ready to deploy publicly, you should:
1. Re-enable RLS for security
2. Implement Supabase Auth for real user accounts
3. Each user will only see their own data

But for development and personal use, disabling RLS is perfectly fine!

---

## Alternative: Use SQL File

If you prefer, you can also run the file:
- In Supabase SQL Editor, copy contents of: `database/disable_rls_for_dev.sql`
- Paste and run

---

## After This Fix Works

Once RLS is disabled, your app will be fully functional:

✅ **Sources** saved to database
✅ **Drafts** persisted
✅ **Email logs** tracked
✅ **Style training** stored
✅ **Stats** updated in real-time

All data will survive app restarts and page refreshes!

---

## Test It

After disabling RLS, run this to verify:

```bash
python test_database.py
```

You should see all green checkmarks! ✅
