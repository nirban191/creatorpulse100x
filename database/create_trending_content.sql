-- Create trending_content table for storing discovered trends from Google Trends
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS trending_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    source_type TEXT NOT NULL CHECK (source_type IN ('google_trends', 'google_alerts')),
    title TEXT NOT NULL,
    description TEXT,
    keywords TEXT[], -- Array of related keywords
    url TEXT,
    metadata JSONB, -- Store raw trend data (search interest, related queries, etc.)
    search_volume INTEGER,
    category TEXT, -- 'tech', 'ai', 'business', 'science', etc.
    discovered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_trending_content_user_id ON trending_content(user_id);
CREATE INDEX IF NOT EXISTS idx_trending_content_discovered_at ON trending_content(discovered_at DESC);
CREATE INDEX IF NOT EXISTS idx_trending_content_category ON trending_content(category);
CREATE INDEX IF NOT EXISTS idx_trending_content_source_type ON trending_content(source_type);
CREATE INDEX IF NOT EXISTS idx_trending_content_is_active ON trending_content(is_active);

-- Add composite index for common query pattern (user + active + recent)
CREATE INDEX IF NOT EXISTS idx_trending_content_user_active_recent
ON trending_content(user_id, is_active, discovered_at DESC);

-- Enable Row Level Security
ALTER TABLE trending_content ENABLE ROW LEVEL SECURITY;

-- Note: RLS policies will be created in a separate file (fix_trending_content_rls.sql)
