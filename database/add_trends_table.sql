-- Add Trends Table for CreatorPulse
-- Run this in your Supabase SQL Editor to enable trend tracking

-- Trends tracking table
CREATE TABLE IF NOT EXISTS public.trends (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    mention_count INTEGER DEFAULT 1,
    spike_detected BOOLEAN DEFAULT false,
    spike_factor DECIMAL(10, 2),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Index for faster queries
    CONSTRAINT unique_user_keyword_per_day UNIQUE (user_id, keyword, DATE(detected_at))
);

-- Create index for faster trend queries
CREATE INDEX IF NOT EXISTS idx_trends_user_id ON public.trends(user_id);
CREATE INDEX IF NOT EXISTS idx_trends_detected_at ON public.trends(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_trends_keyword ON public.trends(keyword);

-- Enable Row Level Security
ALTER TABLE public.trends ENABLE ROW LEVEL SECURITY;

-- RLS Policies for trends
CREATE POLICY "Users can view own trends"
    ON public.trends FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own trends"
    ON public.trends FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own trends"
    ON public.trends FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own trends"
    ON public.trends FOR DELETE
    USING (auth.uid() = user_id);

-- Create a function to clean up old trend data (optional - keeps last 30 days)
CREATE OR REPLACE FUNCTION cleanup_old_trends()
RETURNS void AS $$
BEGIN
    DELETE FROM public.trends
    WHERE detected_at < NOW() - INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Optionally schedule cleanup (requires pg_cron extension)
-- SELECT cron.schedule('cleanup-trends', '0 0 * * *', 'SELECT cleanup_old_trends()');

COMMENT ON TABLE public.trends IS 'Stores trending keyword data for spike detection and historical analysis';
COMMENT ON COLUMN public.trends.keyword IS 'Trending keyword extracted from content';
COMMENT ON COLUMN public.trends.mention_count IS 'Number of times keyword appeared in content';
COMMENT ON COLUMN public.trends.spike_detected IS 'Whether this was detected as a spike';
COMMENT ON COLUMN public.trends.spike_factor IS 'Multiplier compared to baseline (e.g., 2.5x)';
