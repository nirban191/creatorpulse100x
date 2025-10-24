-- Fix Row Level Security for trending_content and trend_settings tables
-- Run this in Supabase SQL Editor AFTER creating the tables

-- ========================================
-- TRENDING_CONTENT TABLE RLS POLICIES
-- ========================================

-- First, drop any existing policies that might conflict
DROP POLICY IF EXISTS "Users can insert own trending content" ON trending_content;
DROP POLICY IF EXISTS "Users can read own trending content" ON trending_content;
DROP POLICY IF EXISTS "Users can update own trending content" ON trending_content;
DROP POLICY IF EXISTS "Users can delete own trending content" ON trending_content;

-- Ensure RLS is enabled
ALTER TABLE trending_content ENABLE ROW LEVEL SECURITY;

-- CREATE: Allow authenticated users to INSERT their own trending content
CREATE POLICY "Users can insert own trending content"
ON trending_content
FOR INSERT
TO authenticated
WITH CHECK (auth.uid()::text = user_id::text);

-- READ: Allow authenticated users to SELECT their own trending content
CREATE POLICY "Users can read own trending content"
ON trending_content
FOR SELECT
TO authenticated
USING (auth.uid()::text = user_id::text);

-- UPDATE: Allow authenticated users to UPDATE their own trending content
CREATE POLICY "Users can update own trending content"
ON trending_content
FOR UPDATE
TO authenticated
USING (auth.uid()::text = user_id::text)
WITH CHECK (auth.uid()::text = user_id::text);

-- DELETE: Allow authenticated users to DELETE their own trending content
CREATE POLICY "Users can delete own trending content"
ON trending_content
FOR DELETE
TO authenticated
USING (auth.uid()::text = user_id::text);


-- ========================================
-- TREND_SETTINGS TABLE RLS POLICIES
-- ========================================

-- First, drop any existing policies that might conflict
DROP POLICY IF EXISTS "Users can insert own trend settings" ON trend_settings;
DROP POLICY IF EXISTS "Users can read own trend settings" ON trend_settings;
DROP POLICY IF EXISTS "Users can update own trend settings" ON trend_settings;
DROP POLICY IF EXISTS "Users can delete own trend settings" ON trend_settings;

-- Ensure RLS is enabled
ALTER TABLE trend_settings ENABLE ROW LEVEL SECURITY;

-- CREATE: Allow authenticated users to INSERT their own trend settings
CREATE POLICY "Users can insert own trend settings"
ON trend_settings
FOR INSERT
TO authenticated
WITH CHECK (auth.uid()::text = user_id::text);

-- READ: Allow authenticated users to SELECT their own trend settings
CREATE POLICY "Users can read own trend settings"
ON trend_settings
FOR SELECT
TO authenticated
USING (auth.uid()::text = user_id::text);

-- UPDATE: Allow authenticated users to UPDATE their own trend settings
CREATE POLICY "Users can update own trend settings"
ON trend_settings
FOR UPDATE
TO authenticated
USING (auth.uid()::text = user_id::text)
WITH CHECK (auth.uid()::text = user_id::text);

-- DELETE: Allow authenticated users to DELETE their own trend settings
CREATE POLICY "Users can delete own trend settings"
ON trend_settings
FOR DELETE
TO authenticated
USING (auth.uid()::text = user_id::text);

-- Verify policies are created
SELECT tablename, policyname FROM pg_policies WHERE tablename IN ('trending_content', 'trend_settings');
