-- Create trend_settings table for user preferences on trend discovery
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS trend_settings (
    user_id UUID PRIMARY KEY NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    categories TEXT[] DEFAULT ARRAY['tech', 'ai', 'business'],
    custom_keywords TEXT[] DEFAULT ARRAY[]::TEXT[],
    schedule_time TIME DEFAULT '09:00:00',
    last_run_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add index for finding users with enabled trend discovery
CREATE INDEX IF NOT EXISTS idx_trend_settings_enabled ON trend_settings(enabled) WHERE enabled = TRUE;

-- Enable Row Level Security
ALTER TABLE trend_settings ENABLE ROW LEVEL SECURITY;

-- Note: RLS policies will be created in a separate file (fix_trending_content_rls.sql)

-- Add trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_trend_settings_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_trend_settings_updated_at
    BEFORE UPDATE ON trend_settings
    FOR EACH ROW
    EXECUTE FUNCTION update_trend_settings_updated_at();
