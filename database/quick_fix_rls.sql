-- Quick Fix: Disable RLS and Remove Foreign Key Constraint Check for Development
-- Run this in Supabase SQL Editor to fix the error

-- Step 1: Disable RLS on all tables
ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.sources DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.drafts DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.style_training DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.email_sends DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.analytics DISABLE ROW LEVEL SECURITY;

-- Step 2: Make foreign key constraint deferrable (allows insert without immediate check)
ALTER TABLE public.sources
DROP CONSTRAINT IF EXISTS sources_user_id_fkey;

ALTER TABLE public.sources
ADD CONSTRAINT sources_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES public.profiles(id)
ON DELETE CASCADE
DEFERRABLE INITIALLY DEFERRED;

-- Step 3: Same for other tables
ALTER TABLE public.drafts
DROP CONSTRAINT IF EXISTS drafts_user_id_fkey;

ALTER TABLE public.drafts
ADD CONSTRAINT drafts_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES public.profiles(id)
ON DELETE CASCADE
DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE public.feedback
DROP CONSTRAINT IF EXISTS feedback_user_id_fkey;

ALTER TABLE public.feedback
ADD CONSTRAINT feedback_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES public.profiles(id)
ON DELETE CASCADE
DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE public.style_training
DROP CONSTRAINT IF EXISTS style_training_user_id_fkey;

ALTER TABLE public.style_training
ADD CONSTRAINT style_training_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES public.profiles(id)
ON DELETE CASCADE
DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE public.email_sends
DROP CONSTRAINT IF EXISTS email_sends_user_id_fkey;

ALTER TABLE public.email_sends
ADD CONSTRAINT email_sends_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES public.profiles(id)
ON DELETE CASCADE
DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE public.analytics
DROP CONSTRAINT IF EXISTS analytics_user_id_fkey;

ALTER TABLE public.analytics
ADD CONSTRAINT analytics_user_id_fkey
FOREIGN KEY (user_id)
REFERENCES public.profiles(id)
ON DELETE CASCADE
DEFERRABLE INITIALLY DEFERRED;

-- Success message
SELECT 'RLS disabled and constraints fixed! App should work now.' AS status;
