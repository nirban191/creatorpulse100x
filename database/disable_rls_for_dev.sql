-- Disable RLS for Development Mode
-- WARNING: Only use this in development! Re-enable RLS for production.

-- This allows the app to work without authentication during development

-- Disable RLS on all tables
ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.sources DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.drafts DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedback DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.style_training DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.email_sends DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.analytics DISABLE ROW LEVEL SECURITY;

-- Success message
SELECT 'RLS disabled for development mode. Remember to re-enable for production!' AS status;
