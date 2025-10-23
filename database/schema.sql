-- CreatorPulse Database Schema for Supabase
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    preferred_llm_provider TEXT DEFAULT 'groq',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" 
    ON public.profiles FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" 
    ON public.profiles FOR UPDATE 
    USING (auth.uid() = id);

-- Content Sources table
CREATE TABLE IF NOT EXISTS public.sources (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL CHECK (source_type IN ('twitter', 'youtube', 'newsletter')),
    identifier TEXT NOT NULL, -- handle, channel, or RSS URL
    is_active BOOLEAN DEFAULT true,
    last_fetched_at TIMESTAMP WITH TIME ZONE,
    fetch_frequency_hours INTEGER DEFAULT 24,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, source_type, identifier)
);

ALTER TABLE public.sources ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own sources" 
    ON public.sources FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sources" 
    ON public.sources FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sources" 
    ON public.sources FOR UPDATE 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sources" 
    ON public.sources FOR DELETE 
    USING (auth.uid() = user_id);

-- Style Training Data table
CREATE TABLE IF NOT EXISTS public.style_training (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    training_text TEXT NOT NULL,
    analysis_result JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE public.style_training ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own style training" 
    ON public.style_training FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own style training" 
    ON public.style_training FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own style training" 
    ON public.style_training FOR DELETE 
    USING (auth.uid() = user_id);

-- Newsletter Drafts table
CREATE TABLE IF NOT EXISTS public.drafts (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    llm_provider TEXT,
    generation_time_ms INTEGER,
    status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'sent', 'scheduled', 'archived')),
    sent_at TIMESTAMP WITH TIME ZONE,
    recipient_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE public.drafts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own drafts" 
    ON public.drafts FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own drafts" 
    ON public.drafts FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own drafts" 
    ON public.drafts FOR UPDATE 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own drafts" 
    ON public.drafts FOR DELETE 
    USING (auth.uid() = user_id);

-- Feedback table
CREATE TABLE IF NOT EXISTS public.feedback (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    draft_id UUID REFERENCES public.drafts(id) ON DELETE CASCADE,
    feedback_type TEXT CHECK (feedback_type IN ('positive', 'negative')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE public.feedback ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own feedback" 
    ON public.feedback FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own feedback" 
    ON public.feedback FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Email Sends table (track email deliveries)
CREATE TABLE IF NOT EXISTS public.email_sends (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    draft_id UUID REFERENCES public.drafts(id) ON DELETE SET NULL,
    recipient_emails TEXT[] NOT NULL,
    subject TEXT NOT NULL,
    send_status TEXT DEFAULT 'pending' CHECK (send_status IN ('pending', 'sent', 'failed')),
    resend_email_id TEXT,
    error_message TEXT,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE public.email_sends ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own email sends" 
    ON public.email_sends FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own email sends" 
    ON public.email_sends FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Analytics table
CREATE TABLE IF NOT EXISTS public.analytics (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE public.analytics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own analytics" 
    ON public.analytics FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own analytics" 
    ON public.analytics FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sources_user_id ON public.sources(user_id);
CREATE INDEX IF NOT EXISTS idx_sources_type ON public.sources(source_type);
CREATE INDEX IF NOT EXISTS idx_drafts_user_id ON public.drafts(user_id);
CREATE INDEX IF NOT EXISTS idx_drafts_created ON public.drafts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_feedback_draft ON public.feedback(draft_id);
CREATE INDEX IF NOT EXISTS idx_analytics_user ON public.analytics(user_id, created_at DESC);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sources_updated_at BEFORE UPDATE ON public.sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_drafts_updated_at BEFORE UPDATE ON public.drafts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create view for user stats
CREATE OR REPLACE VIEW public.user_stats AS
SELECT 
    p.id as user_id,
    COUNT(DISTINCT s.id) as total_sources,
    COUNT(DISTINCT d.id) as total_drafts,
    COUNT(DISTINCT CASE WHEN f.feedback_type = 'positive' THEN f.id END) as positive_feedback,
    COUNT(DISTINCT f.id) as total_feedback,
    ROUND(
        COUNT(DISTINCT CASE WHEN f.feedback_type = 'positive' THEN f.id END)::numeric / 
        NULLIF(COUNT(DISTINCT f.id), 0) * 100, 
        2
    ) as acceptance_rate,
    COUNT(DISTINCT d.id) * 2.5 as estimated_hours_saved
FROM public.profiles p
LEFT JOIN public.sources s ON s.user_id = p.id
LEFT JOIN public.drafts d ON d.user_id = p.id
LEFT JOIN public.feedback f ON f.user_id = p.id
GROUP BY p.id;

-- Grant permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT SELECT ON public.user_stats TO authenticated;
