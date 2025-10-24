-- Fix Row Level Security for style_training table
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/htqwegnixlhdhrdbjkgp/sql

-- First, drop any existing policies that might conflict
DROP POLICY IF EXISTS "Users can insert own style training" ON style_training;
DROP POLICY IF EXISTS "Users can read own style training" ON style_training;
DROP POLICY IF EXISTS "Users can update own style training" ON style_training;
DROP POLICY IF EXISTS "Users can delete own style training" ON style_training;

-- Enable RLS on the table
ALTER TABLE style_training ENABLE ROW LEVEL SECURITY;

-- CREATE: Allow authenticated users to INSERT their own style training
CREATE POLICY "Users can insert own style training"
ON style_training
FOR INSERT
TO authenticated
WITH CHECK (auth.uid() = user_id);

-- READ: Allow authenticated users to SELECT their own style training
CREATE POLICY "Users can read own style training"
ON style_training
FOR SELECT
TO authenticated
USING (auth.uid() = user_id);

-- UPDATE: Allow authenticated users to UPDATE their own style training
CREATE POLICY "Users can update own style training"
ON style_training
FOR UPDATE
TO authenticated
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- DELETE: Allow authenticated users to DELETE their own style training
CREATE POLICY "Users can delete own style training"
ON style_training
FOR DELETE
TO authenticated
USING (auth.uid() = user_id);

-- Test the policies (should return your user ID)
SELECT auth.uid() as my_user_id;

-- Check if you have any existing style training
SELECT * FROM style_training WHERE user_id = auth.uid();

-- Test insert (comment out after first run)
-- INSERT INTO style_training (user_id, training_text, is_active)
-- VALUES (auth.uid(), 'Test style training data', true);
