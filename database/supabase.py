from supabase import create_client, Client

from config.load_config import init

config = init()
url = config["SUPABASE_URL"]
key = config["SUPABASE_KEY"]

supabase: Client = create_client(url, key)

class Supabase:
    def check_guild(self, guild_id):
        response = supabase.table("settings").select("*").eq("guild_id", guild_id).execute()
        if response.data == []:
            return False
        return True

    def check_channel(self, channel_id):
        response = supabase.table("settings").select("*").eq("channel_id", channel_id).execute()
        if response.data == []:
            return False
        return True
    
    def check_role(self, channel_id):
        response = supabase.table("settings").select("role_id").eq("channel_id", channel_id).execute()
        if response.data[0]["role_id"] == None:
            return False
        return True

    def add(self, guild_id, channel_id, role_id = None):
        if role_id:
            data = supabase.table("settings").insert({"guild_id": guild_id, "channel_id": channel_id, "role_id": role_id}).execute()
        else:
            data = supabase.table("settings").insert({"guild_id": guild_id, "channel_id": channel_id}).execute()
        return data.data

    def insert_post_id(self, id):
        supabase.table("ids").insert({"id": id}).execute()

    def remove_old_posts_ids(self, ids_list):
        data = self.select_post_ids()
        for id in data:
            if id["id"] not in ids_list:
                supabase.table("ids").delete().eq("id", id["id"]).execute()

    def add_role(self, guild_id, role_id):
        data = supabase.table("settings").update({"role_id": role_id}).eq("guild_id", guild_id).execute()
        return data.data
    
    def delete(self, guild_id):
        data = supabase.table("settings").delete().eq("guild_id", guild_id).execute()
        return data.data

    def delete_role(self, guild_id):
        data = supabase.table("settings").update({"role_id": None}).eq("guild_id", guild_id).execute()
        return data.data

    def select(self):
        data = supabase.table("settings").select("*").execute()
        return data.data
    
    def select_role(self, guild_id):
        data = supabase.table("settings").select("role_id").eq("guild_id", guild_id).execute()
        return data.data

    def select_post_ids(self):
        data = supabase.table("ids").select("*").execute()
        return data.data
