-- Add Delivery Schedule Fields to CreatorPulse
-- Run this in your Supabase SQL Editor to enable scheduled delivery

-- Add delivery preferences columns to profiles table
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS auto_delivery_enabled BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS delivery_time TIME DEFAULT '08:00:00',
ADD COLUMN IF NOT EXISTS delivery_timezone TEXT DEFAULT 'UTC',
ADD COLUMN IF NOT EXISTS delivery_frequency TEXT DEFAULT 'daily',
ADD COLUMN IF NOT EXISTS delivery_recipients JSONB DEFAULT '[]'::jsonb,
ADD COLUMN IF NOT EXISTS last_delivery_at TIMESTAMP WITH TIME ZONE;

-- Add check constraint for delivery frequency
ALTER TABLE public.profiles
ADD CONSTRAINT check_delivery_frequency
CHECK (delivery_frequency IN ('daily', 'weekdays', 'weekly', 'custom'));

-- Add index for faster queries on scheduled deliveries
CREATE INDEX IF NOT EXISTS idx_profiles_auto_delivery
ON public.profiles(auto_delivery_enabled, delivery_time)
WHERE auto_delivery_enabled = true;

-- Create scheduled_newsletters table for tracking pending deliveries
CREATE TABLE IF NOT EXISTS public.scheduled_newsletters (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    draft_id UUID REFERENCES public.drafts(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    scheduled_for TIMESTAMP WITH TIME ZONE NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'sending', 'sent', 'failed')),
    recipient_emails JSONB DEFAULT '[]'::jsonb,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for querying pending deliveries
CREATE INDEX IF NOT EXISTS idx_scheduled_newsletters_status
ON public.scheduled_newsletters(status, scheduled_for)
WHERE status IN ('pending', 'sending');

CREATE INDEX IF NOT EXISTS idx_scheduled_newsletters_user
ON public.scheduled_newsletters(user_id, scheduled_for DESC);

-- Enable Row Level Security
ALTER TABLE public.scheduled_newsletters ENABLE ROW LEVEL SECURITY;

-- RLS Policies for scheduled_newsletters
CREATE POLICY "Users can view own scheduled newsletters"
    ON public.scheduled_newsletters FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own scheduled newsletters"
    ON public.scheduled_newsletters FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own scheduled newsletters"
    ON public.scheduled_newsletters FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own scheduled newsletters"
    ON public.scheduled_newsletters FOR DELETE
    USING (auth.uid() = user_id);

-- Create a function to get users due for delivery
CREATE OR REPLACE FUNCTION get_users_due_for_delivery()
RETURNS TABLE (
    user_id UUID,
    delivery_time TIME,
    delivery_timezone TEXT,
    delivery_frequency TEXT,
    delivery_recipients JSONB,
    last_delivery_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id as user_id,
        p.delivery_time,
        p.delivery_timezone,
        p.delivery_frequency,
        p.delivery_recipients,
        p.last_delivery_at
    FROM public.profiles p
    WHERE p.auto_delivery_enabled = true
    AND p.delivery_time IS NOT NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function to update last delivery timestamp
CREATE OR REPLACE FUNCTION update_last_delivery(p_user_id UUID)
RETURNS void AS $$
BEGIN
    UPDATE public.profiles
    SET last_delivery_at = NOW()
    WHERE id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create function to cleanup old scheduled newsletters (optional)
CREATE OR REPLACE FUNCTION cleanup_old_scheduled_newsletters()
RETURNS void AS $$
BEGIN
    DELETE FROM public.scheduled_newsletters
    WHERE status = 'sent'
    AND sent_at < NOW() - INTERVAL '30 days';

    DELETE FROM public.scheduled_newsletters
    WHERE status = 'failed'
    AND created_at < NOW() - INTERVAL '7 days';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Add helpful comments
COMMENT ON COLUMN public.profiles.auto_delivery_enabled IS 'Whether automatic delivery is enabled';
COMMENT ON COLUMN public.profiles.delivery_time IS 'Time of day to deliver newsletter (local time)';
COMMENT ON COLUMN public.profiles.delivery_timezone IS 'User''s timezone (e.g., America/New_York)';
COMMENT ON COLUMN public.profiles.delivery_frequency IS 'How often to deliver (daily, weekdays, weekly)';
COMMENT ON COLUMN public.profiles.delivery_recipients IS 'Array of email addresses to send to';
COMMENT ON COLUMN public.profiles.last_delivery_at IS 'Timestamp of last successful delivery';

COMMENT ON TABLE public.scheduled_newsletters IS 'Tracks scheduled newsletter deliveries';
COMMENT ON COLUMN public.scheduled_newsletters.scheduled_for IS 'When to send the newsletter (UTC)';
COMMENT ON COLUMN public.scheduled_newsletters.status IS 'Delivery status (pending, sending, sent, failed)';

-- Grant necessary permissions
GRANT EXECUTE ON FUNCTION get_users_due_for_delivery() TO authenticated;
GRANT EXECUTE ON FUNCTION update_last_delivery(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION cleanup_old_scheduled_newsletters() TO authenticated;
