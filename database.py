from supabase import create_client

SUPABASE_URL = "https://ffltpgscsnmkyaicmzfq.supabase.co"
SUPABASE_KEY = "sb_publishable_PAq1AjM6ZgELFDQAyE_GpQ_VhONO1CX"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)