import os
import asyncio
from datetime import datetime
from typing import Final
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

# Custom Imports
import discordResponses
import discordDatabase

# STEP 0: LOAD ENVIRONMENT VARIABLES
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

TARGET_HOUR = 0
TARGET_MINUTE = 30

# STEP 1: BOT SETUP
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# STEP 2: HANDLING STARTUP & SYNCING COMMANDS
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')
    
    # CRITICAL: This "registers" your slash commands with Discord's servers.
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s) globally!")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")
        
    #check_menu_time.start()


# STEP 3: CREATING THE SLASH COMMANDS ("Fill in the blanks")

# Example 1: A simple /ping command
@bot.tree.command(name="ping", description="Check if the food bot is alive!")
async def ping(interaction: discord.Interaction):
    # Instead of message.channel.send(), slash commands use interaction responses
    await interaction.response.send_message(f"Pong! Bot latency is {round(bot.latency * 1000)}ms", ephemeral=True)

"""
# STEP 4: BACKGROUND TIME TASK (Kept from your original setup)
@tasks.loop(minutes=1)
async def check_menu_time():
    now = datetime.now()
    if now.hour == TARGET_HOUR and now.minute == TARGET_MINUTE:
        channel = bot.get_channel(1291094574617595928)
        if channel:
            await channel.send("Hello World! It's time for menus!")
            
        guild = bot.get_guild(1291094573950566444)
        role = get(guild.roles, name="Friley") if guild else None
        
        if guild and role:
            for member in guild.members:
                if role in member.roles:
                    try:
                        menu_data = databasingattempt1.dataBasing()
                        await member.send(f"Hello {member.display_name}, the food at Friley today is: {menu_data[0]}")
                    except Exception as e:
                        print(f"Could not send DM to {member.display_name}: {e}")
"""

"""
@check_menu_time.before_loop
async def before_check_menu_time():
    await bot.wait_until_ready()
"""

"""
# 2. THE MENU COMMAND: Upgraded to make the location option strictly optional
@bot.tree.command(name="menu", description="Check what's cooking! Defaults to your saved location.")
@app_commands.describe(location="Optional: Look up a specific hall instead of your default choice")
@app_commands.choices(location=[
    app_commands.Choice(name="Friley Windows", value="Friley"),
    app_commands.Choice(name="Conversations", value="Conversations"),
    app_commands.Choice(name="Union Drive Marketplace (UDCC)", value="UDCC")
])
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def menu(interaction: discord.Interaction, location: str = None): # Default location to None
    user_id = interaction.user.id
    
    # If the user left the fill-in-the-blank empty, look them up in the DB!
    if location is None:
        # Fetch the preference (Change this to a SQL SELECT query later)
        location = USER_PREFERENCES_DB.get(user_id)
        
        # If they haven't set a default yet, gently push them to fix it
        if location is None:
            await interaction.response.send_message(
                "❌ You haven't set a favorite location yet! "
                "Please specify one in the command box or set your default using `/set_location`.",
                ephemeral=True
            )
            return
            
    # If we made it here, we have a valid location! Let's pull the data.
    await interaction.response.defer(ephemeral=False)
"""


"""
Selecting Dining Halls Menu
"""

class MenuSelectInterface(discord.ui.View):
    def __init__(self):
        # don't time out the interface
        super().__init__(timeout=None)
        # store the user's selection temporary inside the view instance state
        self.selected_locations = []

    @discord.ui.select(
        placeholder="Select an ISU dining location...",
        min_values=1,
        max_values=3,
        options=[
            discord.SelectOption(label="Friley Windows", value="Friley"),
            discord.SelectOption(label="Seasons Marketplace", value="Seasons"),
            discord.SelectOption(label="Union Drive Marketplace (UDCC)", value="UDCC")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        # Save the current selection to our view state
        self.selected_locations = select.values
        
        # Turn the array into a pretty comma-separated string for the text preview
        readable_locations = ", ".join([f"**{location}**" for location in self.selected_locations])
        
        # Subtly update the chat message to show what is currently checked
        await interaction.response.edit_message(
            content=f"📍 Currently Checked: {readable_locations}\nClick 'Confirm Selection' below to submit them all!",
            view=self
        )

    # 2. The Accept/Submit Button (Processes the whole batch)
    @discord.ui.button(label="✅ Confirm Selection", style=discord.ButtonStyle.success)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Safety Check: Did they click submit before actually checking any boxes?
        if not self.selected_locations:
            await interaction.response.send_message(
                "❌ Please check at least one dining location from the dropdown first!", 
                ephemeral=True
            )
            return

        # Tell Discord to wait while we process multiple lookups
        await interaction.response.defer(ephemeral=True)

        discordDatabase.save_user_data(interaction.user.id, interaction.user.name, self.selected_locations)

        """
        await interaction.response.edit_message(
            content="✅ Your dining preferences have been saved! This menu is now closed.", 
            view=None  # Setting view to None completely deletes the components
        )

        self.stop()
        """

        try:
            # --- YOUR MULTI-FETCH BACKEND LOGIC HERE ---
            # You can now loop over every hall they selected!
            results = []
            for hall in self.selected_locations:
                # Example: menu_data = your_backend_lookup_function(hall)
                results.append(f"• **{hall}**: (Data loaded successfully)")
            
            final_payload = "\n".join(results)
            
            # Send the collective payload back to the user
            await interaction.followup.send(
                f"🚀 Here are the requested menus:\n{final_payload}", 
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while retrieving data: {e}", 
                ephemeral=True
            )

# 3. The Slash Command setup to call it
@bot.tree.command(name="set_dining_halls", description="Select multiple dining halls to receive.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_menus(interaction: discord.Interaction):
    view = MenuSelectInterface()
    await interaction.response.send_message(
        "Please open the dropdown selection box below, check up to 3 dining halls, then click Confirm.",
        view=view,
        ephemeral=True
    )

"""
Selecting Food Types Menu
"""

class DietSelectInferface(discord.ui.View):
    def __init__(self):
        # don't time out the interface
        super().__init__(timeout=None)
        # store the user's selection temporary inside the view instance state
        self.selected_diets = []

    @discord.ui.select(
        placeholder="Select your diet preferences...",
        min_values=0,
        max_values=3,
        options=[
            discord.SelectOption(label="Halal", value="Halal"),
            discord.SelectOption(label="Vegan", value="Vegan"),
            discord.SelectOption(label="Vegetarian", value="Vegetarian")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        # Save the current selection to our view state
        self.selected_diets = select.values
        
        # Turn the array into a pretty comma-separated string for the text preview
        readable_diets = ", ".join([f"**{diet}**" for diet in self.selected_diets])
        
        # Subtly update the chat message to show what is currently checked
        await interaction.response.edit_message(
            content=f"📍 Currently Checked: {readable_diets}\nClick 'Confirm Selection' below to submit them all!",
            view=self
        )

    # 2. The Accept/Submit Button (Processes the whole batch)
    @discord.ui.button(label="✅ Confirm Selection", style=discord.ButtonStyle.success)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        # Safety Check: Did they click submit before actually checking any boxes?
        if not self.selected_locations:
            await interaction.response.send_message(
                "❌ Please check at least one dining location from the dropdown first!", 
                ephemeral=True
            )
            return
        """

        # Tell Discord to wait while we process multiple lookups
        await interaction.response.defer(ephemeral=True)

        discordDatabase.save_user_diets(interaction.user.id, interaction.user.name, self.selected_diets)

        """
        await interaction.response.edit_message(
            content="✅ Your dining preferences have been saved! This menu is now closed.", 
            view=None  # Setting view to None completely deletes the components
        )

        self.stop()
        """

        try:
            # --- YOUR MULTI-FETCH BACKEND LOGIC HERE ---
            # You can now loop over every hall they selected!
            results = []
            for diet in self.selected_diets:
                # Example: menu_data = your_backend_lookup_function(hall)
                results.append(f"• **{diet}**: (Data loaded successfully)")
            
            final_payload = "\n".join(results)
            
            # Send the collective payload back to the user
            await interaction.followup.send(
                f"🚀 Here are the requested menus:\n{final_payload}", 
                ephemeral=True
            )
                
        except Exception as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while retrieving data: {e}", 
                ephemeral=True
            )

# 3. The Slash Command setup to call it
@bot.tree.command(name="set_diet_preferences", description="Select your diet preferences.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_menus(interaction: discord.Interaction):
    view = DietSelectInferface()
    await interaction.response.send_message(
        "Please open the dropdown selection box below, your diet preferences, then click Confirm.",
        view=view,
        ephemeral=True
    )

"""
Select Allergy Types Menu
"""

class AllergySelectInterface(discord.ui.View):
    def __init__(self):
        # don't time out the interface
        super().__init__(timeout=None)
        # store the user's selection temporary inside the view instance state
        self.selected_allergens = []

    @discord.ui.select(
        placeholder="Select your allergies...",
        min_values=0,
        max_values=9,
        options=[
            discord.SelectOption(label="Dairy", value="dairy"),
            discord.SelectOption(label="Eggs", value="egg"),
            discord.SelectOption(label="Fish", value="fish"),
            discord.SelectOption(label="Peanuts", value="peanuts"),
            discord.SelectOption(label="Shellfish", value="shellfish"),
            discord.SelectOption(label="Soy", value="soy"),
            discord.SelectOption(label="Sesame/Tahini", value="sesame_tahini"),
            discord.SelectOption(label="Wheat Gluten", value="wheat_gluten"),
            discord.SelectOption(label="Tree Nuts", value="tree_nuts")
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        # Save the current selection to our view state
        self.selected_allergens = select.values
        
        # Turn the array into a pretty comma-separated string for the text preview
        readable_allergens = ", ".join([f"**{allergen}**" for allergen in self.selected_allergens])
        
        # Subtly update the chat message to show what is currently checked
        await interaction.response.edit_message(
            content=f"📍 Currently Checked: {readable_allergens}\nClick 'Confirm Selection' below to submit them all!",
            view=self
        )

    # 2. The Accept/Submit Button (Processes the whole batch)
    @discord.ui.button(label="✅ Confirm Selection", style=discord.ButtonStyle.success)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        # Tell Discord to wait while we process multiple lookups
        await interaction.response.defer(ephemeral=True)

        discordDatabase.save_user_allergens(interaction.user.id, interaction.user.name, self.selected_allergens)

        """
        await interaction.response.edit_message(
            content="✅ Your dining preferences have been saved! This menu is now closed.", 
            view=None  # Setting view to None completely deletes the components
        )

        self.stop()
        """

        try:
            # --- YOUR MULTI-FETCH BACKEND LOGIC HERE ---
            # You can now loop over every hall they selected!
            results = []
            for allergen in self.selected_allergens:
                # Example: menu_data = your_backend_lookup_function(hall)
                results.append(f"• **{allergen}**: (Data loaded successfully)")
            
            final_payload = "\n".join(results)
            
            # Send the collective payload back to the user
            await interaction.followup.send(
                f"🚀 Here are the requested menus:\n{final_payload}", 
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.followup.send(
                f"⚠️ An error occurred while retrieving data: {e}", 
                ephemeral=True
            )

# 3. The Slash Command setup to call it
@bot.tree.command(name="set_allergies", description="Select your diet preferences.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_menus(interaction: discord.Interaction):
    view = AllergySelectInterface()
    await interaction.response.send_message(
        "Please open the dropdown selection box below, your allergies, then click Confirm.",
        view=view,
        ephemeral=True
    )

"""
Paginator
"""

class MenuPaginator(discord.ui.View):
    def __init__(self, items: list, items_per_page: int = 5):
        super().__init__(timeout=180) # Timeout after 3 minutes of inactivity
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 0
        
        # Calculate total pages dynamically
        self.total_pages = (len(items) + items_per_page - 1) // items_per_page
        
        # Update button visual states on initialization
        self.update_button_states()

    def get_page_content(self) -> str:
        """Slices the main list to get only the items for the current page."""
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page
        page_items = self.items[start_index:end_index]
        
        # Format the items into a clean string layout
        content = f"**📋 Dining Menu (Page {self.current_page + 1}/{self.total_pages})**\n\n"
        for idx, item in enumerate(page_items, start=start_index + 1):
            content += f"{idx}. {item}\n"
            
        return content

    def update_button_states(self):
        """Disables buttons if there are no more pages in that direction."""
        # Disable "Previous" if on the first page
        self.prev_button.disabled = self.current_page == 0
        
        # Disable "Next" if on the last page
        self.next_button.disabled = self.current_page >= self.total_pages - 1

    @discord.ui.button(label="⬅️ Previous", style=discord.ButtonStyle.blurple)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            
        self.update_button_states()
        # Edit the existing message with new slice of data and updated buttons
        await interaction.response.edit_message(content=self.get_page_content(), view=self)

    @discord.ui.button(label="Next ➡️", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            
        self.update_button_states()
        # Edit the existing message with new slice of data and updated buttons
        await interaction.response.edit_message(content=self.get_page_content(), view=self)

    async def on_timeout(self):
        """Fires automatically when the timeout expires to clean up UI artifacts."""
        # Optional: Disable all buttons when the command expires so users can't click dead buttons
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True
        # Note: You'll need to save the original message object to edit it on timeout, 
        # or leave it as-is (they will just be unclickable grey buttons).

@bot.tree.command(name="show_menu", description="Browse items across multiple pages!")
async def show_menu(interaction: discord.Interaction):
    await interaction.response.defer() # Prevent 3-second timeouts while database reads happen
    
    # --- Example Database Call Simulation ---
    # raw_db_rows = cursor.execute("SELECT item_name FROM menu_items WHERE ...").fetchall()
    # items_list = [row[0] for row in raw_db_rows]

    discordDatabase.findFirstPlace(interaction.user.id)

    discordDatabase.findData_forUser(interaction.user.id, interaction.user.name)

    # For testing, let's pretend your database returned 30 food entries:
    items_list = [f"Food Item ABC #{i}" for i in range(1, 31)] 
    
    if not items_list:
        await interaction.followup.send("No items found in the database.")
        return

    # Instantiate our view class handler
    paginator_view = MenuPaginator(items=items_list, items_per_page=5)
    
    # Grab the initial page text string setup
    initial_text = paginator_view.get_page_content()
    
    # Send the final response attaching the UI buttons view!
    await interaction.followup.send(content=initial_text, view=paginator_view)       

# STEP 5: MAIN ENTRY POINT
def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()