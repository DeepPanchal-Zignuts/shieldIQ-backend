from supabase import create_client
from config.settings import (
    SUPABASE_PROJECT_URL,
    SUPABASE_SECRET_KEY,
)

# Supabase client
supabase = create_client(SUPABASE_PROJECT_URL, SUPABASE_SECRET_KEY)
