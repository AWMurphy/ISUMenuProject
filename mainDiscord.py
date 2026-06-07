# region Imports
from operator import index
import os
import asyncio
from datetime import datetime
from typing import Final
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
import collections

# Custom Imports
import discordResponses
import discordDatabase
import jsonRequests
# endregion

# region Original Setup
# STEP 0: LOAD ENVIRONMENT VARIABLES < imported in
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

TARGET_HOUR = 0
TARGET_MINUTE = 30

# default bot set up
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
# endregion

# region On Ready
# handles the bot when its ready (if it wasn't obvious from the name) and ensures the slash commands sync with the server
@bot.event
async def on_ready() -> None:

    #region Starting Code
    # tells us the server is running
    print(f'{bot.user} is now running!')

    # ensures the daily script is running
    if not daily_menu_blast.is_running():

        # starts the daily menu & lets us know its running
        daily_menu_blast.start()
        print("Daily menu blast task has been started successfully!")
    #endregion
    
    #region Syncing Commands
    # this registers your slash commands with Discord's servers.
    try:

        # syncs and returns the amount of slash commands we have made to the server
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s) globally!")

        # on failure, give the reason it has failed here
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")
    #endregion

#endregion

# region Ping
# a ping command to make sure the bot is still alive
@bot.tree.command(name="ping", description="Check if the food bot is alive!")
async def ping(interaction: discord.Interaction):

    # send back the bot latency
    await interaction.response.send_message(f"Pong! Bot latency is {round(bot.latency * 1000)}ms", ephemeral=True)
#endregion

# region Daily Menu Burst
@tasks.loop(count=1) # Run this loop logic once on startup
async def daily_menu_blast():
    """
    while True:

        now = datetime.now()
        # Target today at 8:00 AM
        target = now.replace(hour=8, minute=0, second=0, microsecond=0)
        
        # If it's already past 8:00 AM today, target 8:00 AM tomorrow
        if now >= target:
            target += datetime.timedelta(days=1)
            
        # Calculate exactly how many seconds to wait
        seconds_to_wait = (target - now).total_seconds()
        
        # Sleep until the exact target time
        await asyncio.sleep(10)
        
        # --- RUN YOUR MENU CODE HERE ---
        print("It's 8:00 AM! Fetching menus...")
    """
#endregion

# region Location Selection Menu

    # region actual menu code
class LocationSelectInterface(discord.ui.View):

        # region Initialization
    def __init__(self, wantList):

        # don't time out the interface
        super().__init__(timeout=180)

        # store the user's location selection (0 = not selected, 1 = selected) [Friley, Seasons, Union]
        self.selected_locations = [0] * 3

        # set the list of places the person wants to see
        self.wantList = wantList

        # update the selected_locations based on wantList
        if self.wantList[0] == 1:
            self.selected_locations[0] = 1
        if self.wantList[1] == 1:
            self.selected_locations[1] = 1
        if self.wantList[2] == 1:
            self.selected_locations[2] = 1

        self.changeButtonColors()

        # endregion

        # region Embed Generation

            # region normal embed generation
    def get_page_embed(self) -> discord.Embed:

        # this function updates the embed panel to reflect the current location selection state
        description_lines = []
        description_lines.append("---**Selected Locations**---")
        index = 1
        for i in range(len(self.selected_locations)):
            item = self.selected_locations[i]
            match item:
                case 1:
                    if i == 0:
                        item = "Friley Windows"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 1:
                        item = "Seasons Marketplace"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 2:
                        item = "Union Drive Marketplace"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                case 0:
                    pass

        # if no locations are selected, add a placeholder line to the description
        if not description_lines:
            description_lines.append("*No locations selected.*")

        # set up the embed with the description and title
        embed = discord.Embed(
            title=f"Select up to 3 dining halls using the buttons or dropdown below.",
            description="\n".join(description_lines),
            color=0xD51007
        )

        # add a footer to show how many locations are selected out of the total available
        embed.set_footer(
            text=f"{index - 1} out of {len(self.wantList)}"
        )
        return embed

            # endregion

            # region submission embed generation
    def get_page_embed_sub(self) -> discord.Embed:

        # this function updates the embed panel to reflect the current location selection state
        description_lines = []
        description_lines.append("---**LOCATION CHOICES SAVED**---")

        # set up the embed with the description and title
        embed = discord.Embed(
            title=f"SAVED!",
            description="\n".join(description_lines),
            color=0xD51007
        )

        # add a footer to show how many locations are selected out of the total available
        embed.set_footer(
            text=f"Properly Saved"
        )
        return embed
            # endregion

        # endregion

        # region Button Logic
    def changeButtonColors(self):

        # Reset all meal buttons to a default secondary (gray)
        self.friley_button.style = discord.ButtonStyle.grey
        self.seasons_button.style = discord.ButtonStyle.grey
        self.union_button.style = discord.ButtonStyle.grey

        if self.selected_locations[0] == 1:
            self.friley_button.style = discord.ButtonStyle.green
        if self.selected_locations[1] == 1:
            self.seasons_button.style = discord.ButtonStyle.green
        if self.selected_locations[2] == 1:
            self.union_button.style = discord.ButtonStyle.green

        # endregion

        # region Dropdown Logic
    @discord.ui.select(
        placeholder="Select an ISU dining location...",
        min_values=1,
        max_values=3,
        options=[
            discord.SelectOption(label="Friley Windows", value="Friley"),
            discord.SelectOption(label="Seasons Marketplace", value="Seasons"),
            discord.SelectOption(label="Union Drive Marketplace (UDCC)", value="UDCC")
        ],
        row=0
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):

        # set according to what they selected in the dropdown
        if "Friley" in select.values:
            self.selected_locations[0] = 1
        else:
            self.selected_locations[0] = 0
        if "Seasons" in select.values:
            self.selected_locations[1] = 1
        else:
            self.selected_locations[1] = 0
        if "UDCC" in select.values:
            self.selected_locations[2] = 1
        else:            
            self.selected_locations[2] = 0
        
        # update the button colors to reflect the dropdown selection as well
        self.changeButtonColors()

        # update the embed to reflect the new selection state as well
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
        # endregion

        # region Buttons

            # region Location Buttons
    @discord.ui.button(label="Friley Windows 🖼️", style=discord.ButtonStyle.grey, row=1)
    async def friley_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.selected_locations[0] == 0:
            self.selected_locations[0] = 1
        else:
            self.selected_locations[0] = 0
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Seasons Marketplace 🍂", style=discord.ButtonStyle.grey, row=1)
    async def seasons_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.selected_locations[1] == 0:
            self.selected_locations[1] = 1
        else:
            self.selected_locations[1] = 0
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Union Drive Marketplace 🚗", style=discord.ButtonStyle.grey, row=1)
    async def union_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.selected_locations[2] == 0:
            self.selected_locations[2] = 1
        else:
            self.selected_locations[2] = 0
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
            # endregion

            # region Reset Button
    @discord.ui.button(label="⟲ Reset All", style=discord.ButtonStyle.blurple, row=2)
    async def reset_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.selected_locations = [0, 0, 0]
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
            # endregion

            # region Submit Button
    @discord.ui.button(label="✅ Confirm Selection", style=discord.ButtonStyle.green, row=2)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        # make sure they selected at least one location before submitting
        if not any(self.selected_locations):
            await interaction.response.send_message(
                "❌ Please check at least one dining location from the dropdown first!", 
                ephemeral=True
            )
            return

        # defer it
        await interaction.response.defer(ephemeral=True)

        # ensure no errors with the saving occur
        try:
            discordDatabase.save_user_data(interaction.user.id, interaction.user.name, self.selected_locations)
        except Exception as e:
            await interaction.response.send_message(
                "❌ An error occurred while saving your selection.",
                ephemeral=True
            )
            print(f"Error saving user data: {e}")
            return

        # edit the original message for confirmation of the submission
        await interaction.followup.send(embed=self.get_page_embed_sub(), view=self)
            # endregion

        # endregion

    # endregion

    # region slash command set up
@bot.tree.command(name="set_dining_halls", description="Select multiple dining halls to receive.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_menus(interaction: discord.Interaction):
    view = LocationSelectInterface(wantList=discordDatabase.listofPlaces(interaction.user.id))
    await interaction.response.send_message(
        "Please open the dropdown selection box below, check up to 3 dining halls, then click Confirm.",
        embed=view.get_page_embed(),
        view=view,
        ephemeral=True
    ) 
    # endregion

# endregion

# region Food Diet Selection Menu

    # region actual menu code
class DietSelectInterface(discord.ui.View):

        # region Initialization
    def __init__(self, wantList):

        # don't time out the interface
        super().__init__(timeout=180)

        # store the user's diet selection (0 = not selected, 1 = selected) [Halal, Vegan, Vegetarian]
        self.selected_diets = [0] * 3

        # set the list of diets the person wants to see
        self.wantList = wantList

        # update the selected_diets based on wantList
        if self.wantList[0] == 1:
            self.selected_diets[0] = 1
        if self.wantList[1] == 1:
            self.selected_diets[1] = 1
        if self.wantList[2] == 1:
            self.selected_diets[2] = 1

        self.changeButtonColors()

        # endregion

        # region Embed Generation

            # region normal embed generation
    def get_page_embed(self) -> discord.Embed:

        # this function updates the embed panel to reflect the current location selection state
        description_lines = []
        description_lines.append("---**Selected Diets**---")
        index = 1
        for i in range(len(self.selected_diets)):
            item = self.selected_diets[i]
            match item:
                case 1:
                    if i == 0:
                        item = "Halal"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 1:
                        item = "Vegan"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 2:
                        item = "Vegetarian"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                case 0:
                    pass

        # if no locations are selected, add a placeholder line to the description
        if not description_lines:
            description_lines.append("*No diets selected.*")

        # set up the embed with the description and title
        embed = discord.Embed(
            title=f"Select up to 3 diets using the buttons or dropdown below.",
            description="\n".join(description_lines),
            color=0xD51007
        )

        # add a footer to show how many locations are selected out of the total available
        embed.set_footer(
            text=f"{index - 1} out of {len(self.wantList)}"
        )
        return embed

            # endregion

            # region submission embed generation
    def get_page_embed_sub(self) -> discord.Embed:

        # this function updates the embed panel to reflect the current diet selection state
        description_lines = []
        description_lines.append("---**DIET CHOICES SAVED**---")

        # set up the embed with the description and title
        embed = discord.Embed(
            title=f"SAVED!",
            description="\n".join(description_lines),
            color=0xD51007
        )

        # add a footer to show how many diets are selected out of the total available
        embed.set_footer(
            text=f"Properly Saved"
        )
        return embed
            # endregion

        # endregion

        # region Button Logic
    def changeButtonColors(self):

        # Reset all meal buttons to a default secondary (gray)
        self.friley_button.style = discord.ButtonStyle.grey
        self.seasons_button.style = discord.ButtonStyle.grey
        self.union_button.style = discord.ButtonStyle.grey

        if self.selected_diets[0] == 1:
            self.friley_button.style = discord.ButtonStyle.green
        if self.selected_diets[1] == 1:
            self.seasons_button.style = discord.ButtonStyle.green
        if self.selected_diets[2] == 1:
            self.union_button.style = discord.ButtonStyle.green
        # endregion

        # region Dropdown Logic
    @discord.ui.select(
        placeholder="Select an ISU dining location...",
        min_values=1,
        max_values=3,
        options=[
            discord.SelectOption(label="Friley Windows", value="Friley"),
            discord.SelectOption(label="Seasons Marketplace", value="Seasons"),
            discord.SelectOption(label="Union Drive Marketplace (UDCC)", value="UDCC")
        ],
        row=0
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):

        # set according to what they selected in the dropdown
        if "Friley" in select.values:
            self.selected_locations[0] = 1
        else:
            self.selected_locations[0] = 0
        if "Seasons" in select.values:
            self.selected_locations[1] = 1
        else:
            self.selected_locations[1] = 0
        if "UDCC" in select.values:
            self.selected_locations[2] = 1
        else:            
            self.selected_locations[2] = 0
        
        # update the button colors to reflect the dropdown selection as well
        self.changeButtonColors()

        # update the embed to reflect the new selection state as well
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
        # endregion

        # region Buttons

            # region Location Buttons
    @discord.ui.button(label="Halal", style=discord.ButtonStyle.grey, row=1)
    async def friley_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.selected_diets[0] == 0:
            self.selected_diets[0] = 1
        else:
            self.selected_diets[0] = 0
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Vegan", style=discord.ButtonStyle.grey, row=1)
    async def seasons_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.selected_diets[1] == 0:
            self.selected_diets[1] = 1
        else:
            self.selected_diets[1] = 0
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Vegetarian", style=discord.ButtonStyle.grey, row=1)
    async def union_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.selected_diets[2] == 0:
            self.selected_diets[2] = 1
        else:
            self.selected_diets[2] = 0
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
            # endregion

            # region Reset Button
    @discord.ui.button(label="⟲ Reset All", style=discord.ButtonStyle.blurple, row=2)
    async def reset_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.selected_diets = [0, 0, 0]
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
            # endregion

            # region Submit Button
    @discord.ui.button(label="✅ Confirm Selection", style=discord.ButtonStyle.green, row=2)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        # defer it
        await interaction.response.defer(ephemeral=True)

        # ensure no errors with the saving occur
        try:
            discordDatabase.save_user_diets(interaction.user.id, interaction.user.name, self.selected_diets)
        except Exception as e:
            await interaction.response.send_message(
                "❌ An error occurred while saving your selection.",
                ephemeral=True
            )
            print(f"Error saving user data: {e}")
            return

        # edit the original message for confirmation of the submission
        await interaction.followup.send(embed=self.get_page_embed_sub(), view=self)
            # endregion

        # endregion

    # endregion

    # region slash command set up
@bot.tree.command(name="set_diet_preferences", description="Select your diet preferences.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_menus(interaction: discord.Interaction):
    view = DietSelectInterface(wantList=discordDatabase.listofDiets(interaction.user.id))
    await interaction.response.send_message(
        "Please open the dropdown selection box below, your diet preferences, then click Confirm.",
        embed=view.get_page_embed(),
        view=view,
        ephemeral=True
    )
    # endregion

# endregion

# region Allergy Selection Menu

class AllergySelectInterface(discord.ui.View):

    # region Initialization
    def __init__(self, wantList):

        # don't time out the interface
        super().__init__(timeout=180)

        # store the user's allergy selection (0 = not selected, 1 = selected) [Dairy, Eggs, Fish, Peanuts, Shellfish, Soy, Sesame/Tahini, Wheat Gluten, Tree Nuts]
        self.selected_allergens = [0] * 9

        # set the list of allergies the person wants to see
        self.wantList = wantList

        # update the selected_allergens based on wantList
        if self.wantList[0] == 1:
            self.selected_allergens[0] = 1
        if self.wantList[1] == 1:
            self.selected_allergens[1] = 1
        if self.wantList[2] == 1:
            self.selected_allergens[2] = 1
        if self.wantList[3] == 1:
            self.selected_allergens[3] = 1
        if self.wantList[4] == 1:
            self.selected_allergens[4] = 1
        if self.wantList[5] == 1:
            self.selected_allergens[5] = 1
        if self.wantList[6] == 1:  
            self.selected_allergens[6] = 1
        if self.wantList[7] == 1:
            self.selected_allergens[7] = 1
        if self.wantList[8] == 1:
            self.selected_allergens[8] = 1

        self.changeButtonColors()
    # endregion

    # region Dropdown Logic
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
        if "dairy" in select.values:
            self.selected_allergens[0] = 1
        else:
            self.selected_allergens[0] = 0
        if "egg" in select.values:
            self.selected_allergens[1] = 1
        else:
            self.selected_allergens[1] = 0
        if "fish" in select.values:
            self.selected_allergens[2] = 1
        else:            
            self.selected_allergens[2] = 0
        if "peanuts" in select.values:
            self.selected_allergens[3] = 1
        else:
            self.selected_allergens[3] = 0
        if "shellfish" in select.values:
            self.selected_allergens[4] = 1
        else:
            self.selected_allergens[4] = 0
        if "soy" in select.values:
            self.selected_allergens[5] = 1
        else:
            self.selected_allergens[5] = 0
        if "sesame_tahini" in select.values:
            self.selected_allergens[6] = 1
        else:
            self.selected_allergens[6] = 0
        if "wheat_gluten" in select.values:
            self.selected_allergens[7] = 1
        else:
            self.selected_allergens[7] = 0
        if "tree_nuts" in select.values:
            self.selected_allergens[8] = 1
        else:
            self.selected_allergens[8] = 0
        
        # update the button colors to reflect the dropdown selection as well
        self.changeButtonColors()

        # update the embed to reflect the new selection state as well
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    # endregion

    # region Embed Generation

        # region normal embed generation
    def get_page_embed(self) -> discord.Embed:

        # this function updates the embed panel to reflect the current location selection state
        description_lines = []
        description_lines.append("---**Selected Allergens**---")
        index = 1
        for i in range(len(self.selected_allergens)):
            item = self.selected_allergens[i]
            match item:
                case 1:
                    if i == 0:
                        item = "Dairy"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 1:
                        item = "Eggs"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 2:
                        item = "Fish"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 3:
                        item = "Peanuts"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 4:
                        item = "Shellfish"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 5:
                        item = "Soy"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 6:
                        item = "Sesame/Tahini"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 7:
                        item = "Wheat Gluten"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                    elif i == 8:
                        item = "Tree Nuts"
                        line = f"`{index:02d}.` **{item}**"
                        description_lines.append(line)
                        index += 1
                case 0:
                    pass

        # if no locations are selected, add a placeholder line to the description
        if not description_lines:
            description_lines.append("*No allergens selected.*")

        # set up the embed with the description and title
        embed = discord.Embed(
            title=f"Select up to 9 allergens using the buttons or dropdown below.",
            description="\n".join(description_lines),
            color=0xD51007
        )

        # add a footer to show how many locations are selected out of the total available
        embed.set_footer(
            text=f"{index - 1} out of {len(self.wantList)}"
        )
        return embed

            # endregion

        # region submission embed generation
    def get_page_embed_sub(self) -> discord.Embed:

        # this function updates the embed panel to reflect the current diet selection state
        description_lines = []
        description_lines.append("---**ALLERGEN CHOICES SAVED**---")

        # set up the embed with the description and title
        embed = discord.Embed(
            title=f"SAVED!",
            description="\n".join(description_lines),
            color=0xD51007
        )

        # add a footer to show how many allergens are selected out of the total available
        embed.set_footer(
            text=f"Properly Saved"
        )
        return embed
            # endregion

    # endregion

    # region Buttons

        # region Reset Button
    @discord.ui.button(label="⟲ Reset All", style=discord.ButtonStyle.blurple, row=2)
    async def reset_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.selected_allergens = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.changeButtonColors()
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
        # endregion

        # region Submit Button
    @discord.ui.button(label="✅ Confirm Selection", style=discord.ButtonStyle.green, row=2)
    async def submit_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        # defer it
        await interaction.response.defer(ephemeral=True)

        # ensure no errors with the saving occur
        try:
            discordDatabase.save_user_allergens(interaction.user.id, interaction.user.name, self.selected_allergens)
        except Exception as e:
            await interaction.response.send_message(
                "❌ An error occurred while saving your selection.",
                ephemeral=True
            )
            print(f"Error saving user data: {e}")
            return

        # edit the original message for confirmation of the submission
        await interaction.followup.send(embed=self.get_page_embed_sub(), view=self)
        # endregion

    # endregion

    # region slash command set up
@bot.tree.command(name="set_allergies", description="Select your allergies.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def get_menus(interaction: discord.Interaction):
    view = AllergySelectInterface(wantList=discordDatabase.listofAllergens(interaction.user.id))
    await interaction.response.send_message(
        "Please open the dropdown selection box below, your allergies, then click Confirm.",
        view=view,
        embed=view.get_page_embed(),
        ephemeral=True
    )
    # endregion

# endregion

# region Show Menus well... Menu (Paginator Logic)

    #region main code
class MenuPaginator(discord.ui.View):
    
        #region Initialization
    # initialization unit for the embed
    def __init__(self, items, givenTime, firstPlace, mainUser, openLocations, openTimes, wantList, items_per_page=10):

        # Timeout after 3 minutes of inactivity
        super().__init__(timeout=180)

        # holds full list of items for the location
        self.fullitems = dict(items)

        # hold the current station of the original array
        self.currentStation = next(iter(items))

        # holds the items for the current station
        self.items = items[self.currentStation]

        # sets the time of day (breakfast, lunch, dinner) according to the selection
        self.timeOfDay = givenTime

        # holds the current selected location | sets it to the first place this person can see
        self.currentLocation = firstPlace

        # the user_id (int) of the user who called the interaction
        self.mainUser = mainUser.id

        # the username of the user who called the interaction
        self.mainUsername = mainUser.name

        # holds the main user that called the interaction
        self.ogUser = mainUser

        # holds the array for open locations
        self.openLocations = openLocations

        # holds the 2d array for open times depending on locations
        self.openTimes = openTimes

        # the list of places the person wants to see
        self.wantList = wantList

        # set the maximum number of items per page
        self.items_per_page = items_per_page

        # current page value of the group
        self.current_page = 0

        # calculate the total number of pages for the range of all items the place
        self.total_pages = len(self.fullitems)

        self.changeButtonColors()

        self.update_button_states()
        #endregion

        #region Update States & Embed
    def reget_data(self, user_id):

        foodList = discordDatabase.findData_forUser(user_id, self.currentLocation, self.timeOfDay)

        station_dict = collections.defaultdict(list)
    
        # go through all food acquired in foodList
        for food in foodList:

            # extract fields for readability
            food_name = food[1]
            calories = food[2]
            calorieError = food[3]
            station_name = food[6]

            # format the food string based on calorie error variable
            if calorieError == 0:
                food_string = f"{food_name} | Cals Per Serving: {calories}"
            else:
                food_string = f"{food_name} | No Calories Given"

            # add a formatted string directly to that station's list
            station_dict[station_name].append(food_string)

        # convert back to a standard dict
        final_menu_dict = dict(station_dict)

        self.fullitems = final_menu_dict
        self.current_page = 0
        self.total_pages = len(self.fullitems)
        self.currentStation = self.getKeyAtIndex(self.fullitems, self.current_page)

    def get_page_embed(self) -> discord.Embed:
        """Generates a Last.fm-style clean embed layout for the current page."""
        # 1. Slice the items for our specific page range
        self.items = self.fullitems[self.currentStation]

        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_items = self.items[start:end]

        start = 0

        # 2. Build the structured Last.fm-style markdown list
        description_lines = []
        description_lines.append(f"----------**{self.currentStation}**----------")
        for index, item in enumerate(self.items, start=start + 1):
            # Formats single digits cleanly like '01.', '02.' to keep the grid perfectly vertical
            line = f"`{index:02d}.` **{item}**"
            description_lines.append(line)

        match self.currentLocation:
            case "Friley":
                locationFix = "Friley Windows"
            case "Seasons":
                locationFix = "Seasons Marketplace"
            case "Union":
                locationFix = "Union Drive Marketplace"

        # 3. Create a clean, focused embed panel
        # Setting a nice title referencing the location and meal period
        embed = discord.Embed(
            title=f"{locationFix.upper()} — {self.timeOfDay.capitalize()} Menu",
            description="\n".join(description_lines) if description_lines else "*No items listed for this meal.*",
            color=0xD51007  # Iconic Last.fm signature red
        )

        embed.set_author(
            name=f"{self.ogUser.display_name}'s Request", 
            icon_url=self.ogUser.display_avatar.url
        )

        # 4. Inject matching structured metadata at the footer (tracking page numbers)
        embed.set_footer(
            text=f"Page {self.current_page + 1} of {self.total_pages} • Total Items: {len(self.items)}"
        )
        return embed

    def update_button_states(self):

        # dynamically adds or removes buttons based page status

        if self.next_button not in self.children:
            self.add_item(self.next_button)

        if self.total_pages <= 1:
            self.remove_item(self.prev_button)
            self.remove_item(self.next_button)
        elif self.current_page == self.total_pages - 1:
            self.remove_item(self.next_button)
        elif self.current_page == 0:
            self.remove_item(self.prev_button)
        else:
            # ONLY add if they aren't already visible in children
            if self.prev_button not in self.children:
                self.remove_item(self.next_button)
                self.add_item(self.prev_button)
                self.add_item(self.next_button)
            if self.next_button not in self.children:
                self.add_item(self.next_button)

            self.prev_button.disabled = self.current_page == 0
            self.next_button.disabled = self.current_page >= self.total_pages - 1
                
        
        self.remove_item(self.close_button)
        self.add_item(self.close_button)

        match self.currentLocation:
            case "Friley":
                openArray = self.openTimes[0]
            case "Seasons":
                openArray = self.openTimes[1]
            case "Union":
                openArray = self.openTimes[2]
        
        # Breakfast
        if openArray[0] == 0:
            self.remove_item(self.breakfast_button)
        elif self.breakfast_button not in self.children:
            self.add_item(self.breakfast_button)

        # Lunch
        if openArray[1] == 0:
            self.remove_item(self.lunch_button)
        elif self.lunch_button not in self.children:
            self.add_item(self.lunch_button)

        # Dinner
        if openArray[2] == 0:
            self.remove_item(self.dinner_button)
        elif self.dinner_button not in self.children:
            self.add_item(self.dinner_button)

        # Friley
        if self.openLocations[0] == 0 or self.wantList[0] == 0:
            self.remove_item(self.friley_button)
        elif self.friley_button not in self.children:
            self.add_item(self.friley_button)

        # Seasons
        if self.openLocations[1] == 0 or self.wantList[1] == 0:
            self.remove_item(self.seasons_button)
        elif self.seasons_button not in self.children:
            self.add_item(self.seasons_button)

        # Union
        if self.openLocations[2] == 0 or self.wantList[2] == 0:
            self.remove_item(self.union_button)
        elif self.union_button not in self.children:
            self.add_item(self.union_button)

    def changeButtonColors(self):
        # Reset all meal buttons to a default secondary (gray)
        self.breakfast_button.style = discord.ButtonStyle.grey
        self.lunch_button.style = discord.ButtonStyle.grey
        self.dinner_button.style = discord.ButtonStyle.grey

        self.friley_button.style = discord.ButtonStyle.grey
        self.seasons_button.style = discord.ButtonStyle.grey
        self.union_button.style = discord.ButtonStyle.grey

        match self.timeOfDay:
            case "breakfast":
                self.breakfast_button.style = discord.ButtonStyle.green
            case "lunch":
                self.lunch_button.style = discord.ButtonStyle.green
            case "dinner":
                self.dinner_button.style = discord.ButtonStyle.green

        match self.currentLocation:
            case "Friley":
                self.friley_button.style = discord.ButtonStyle.green
            case "Seasons":
                self.seasons_button.style = discord.ButtonStyle.green
            case "Union":
                self.union_button.style = discord.ButtonStyle.green
        #endregion

        #region Dictionary Index/Key
    def getValueAtIndex(self, dictionary, index, default=None):
        iterator = iter(dictionary.values())
        for _ in range(index):
            next(iterator, None) # Skip preceding items
        return next(iterator, default)
        
    def getKeyAtIndex(self, dictionary, index, default=None):
        iterator = iter(dictionary)
        for _ in range(index):
            next(iterator, None) # Skip preceding items
        return next(iterator, default)
        #endregion

        #region Button Methods

    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.secondary, row=2)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Security: Check if the person clicking the button is the one who ran the slash command
        if self.current_page > 0:
            self.current_page -= 1
            self.currentStation = self.getKeyAtIndex(self.fullitems, self.current_page)
            self.update_button_states()
            # Edit the message directly with the updated embed panel
            await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.secondary, row=2)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Security check
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.currentStation = self.getKeyAtIndex(self.fullitems, self.current_page)
            self.update_button_states()
            # Edit the message directly with the updated embed panel
            await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="🗑️ Close", style=discord.ButtonStyle.danger, row=2)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.mainUser:
            await interaction.response.send_message("You cannot close this menu.", ephemeral=True)
            return
        # Clean up the UI components entirely so buttons can't be spammed later
        await interaction.response.edit_message(view=None)

    @discord.ui.button(label="Breakfast🥞", style=discord.ButtonStyle.gray, row=1)
    async def breakfast_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.timeOfDay = "breakfast"
        self.reget_data(self.mainUser)
        self.update_button_states()
        self.changeButtonColors()
        # Edit the existing message with new slice of data and updated buttons
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Lunch🍔", style=discord.ButtonStyle.gray, row=1)
    async def lunch_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.timeOfDay = "lunch"
        self.reget_data(self.mainUser)
        self.update_button_states()
        self.changeButtonColors()
        # Edit the existing message with new slice of data and updated buttons
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Dinner🍗", style=discord.ButtonStyle.gray, row=1)
    async def dinner_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.timeOfDay = "dinner"
        self.reget_data(self.mainUser)
        self.update_button_states()
        self.changeButtonColors()
        # Edit the existing message with new slice of data and updated buttons
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Friley Windows 🖼️", style=discord.ButtonStyle.gray, row=0)
    async def friley_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentLocation = "Friley"
        self.timeOfDay = "breakfast"
        self.reget_data(self.mainUser)
        self.update_button_states()
        self.changeButtonColors()
        # Edit the existing message with new slice of data and updated buttons
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Seasons Marketplace 🍂", style=discord.ButtonStyle.gray, row=0)
    async def seasons_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentLocation = "Seasons"
        self.timeOfDay = "breakfast"
        self.reget_data(self.mainUser)
        self.update_button_states()
        self.changeButtonColors()
        # Edit the existing message with new slice of data and updated buttons
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)

    @discord.ui.button(label="Union Drive Marketplace 🚗", style=discord.ButtonStyle.gray, row=0)
    async def union_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.currentLocation = "Union"
        self.timeOfDay = "breakfast"
        self.reget_data(self.mainUser)
        self.update_button_states()
        self.changeButtonColors()
        # Edit the existing message with new slice of data and updated buttons
        await interaction.response.edit_message(embed=self.get_page_embed(), view=self)
    
        #endregion
    
    #endregion
    
    #region slash command logic and startup
@bot.tree.command(name="show_menu", description="Browse items across multiple pages!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def show_menu(interaction: discord.Interaction):

    # Prevent 3-second timeouts while database reads happen < this line is currently broken, figure out why it is and what is happening
    await interaction.response.defer()

    # in case you are in a server and it doesn't want to break the code (has you as a member instead of a user) do this
    user_id = int(interaction.user.id)

    # if the person isn't in the database, don't allow them to use the part of the code, send back the line below and exit the function
    if not discordDatabase.isInDatabase(user_id):
        await interaction.followup.send("You are not in the database, run one of the other set commands first to establish a connection.", ephemeral=True)
        return

    # find the first place they can look at [if any] according to their set up dining hall requirements (accounts for closed locations)
    firstPlace = discordDatabase.findFirstPlace(interaction.user.id)

    # if you don't find anything in first place, tell them and exit the function
    if firstPlace == "":
        await interaction.followup.send("No items found in the database for your selected dining halls (they might be closed).", ephemeral=True)
        return

    # get the associated list of food from the place for the time selected (need to replace "breakfast" with a variable from another function later)
    foodList = discordDatabase.findData_forUser(interaction.user.id, firstPlace, "breakfast")

    # make a dictionary list object using collections for easier appending for each station
    station_dict = collections.defaultdict(list)
    
    # go through all food acquired in foodList
    for food in foodList:

        # extract fields for readability
        food_name = food[1]
        calories = food[2]
        calorieError = food[3]
        station_name = food[6]

        # format the food string based on calorie error variable
        if calorieError == 0:
            food_string = f"{food_name} | Calories Per Serving: {calories}"
        else:
            food_string = f"{food_name} | No Calories Given"

        # add a formatted string directly to that station's list
        station_dict[station_name].append(food_string)

    # convert back to a standard dict
    final_menu_dict = dict(station_dict)
    
    # if final menu dict is empty then tell that and end the function
    if not final_menu_dict:
        await interaction.followup.send("No items found in the database.", ephemeral=True)
        return
    
    # get a list of places wanted from the user
    wantList = discordDatabase.listofPlaces(interaction.user.id)

    # get a list of places that are open
    otherArray = discordDatabase.openLocations()

    # get a list of times that each place is open (a 2d array) arranged [friley array, seasons array, union array]
    timeList = [None] * 3
    timeList[0] = discordDatabase.openTimes("Friley")
    timeList[1] = discordDatabase.openTimes("Seasons")
    timeList[2] = discordDatabase.openTimes("Union")

    # instantiate our embed view handler
    paginator_view = MenuPaginator(items=final_menu_dict, givenTime="breakfast", firstPlace=firstPlace, mainUser=interaction.user, openLocations=otherArray, openTimes=timeList, wantList=wantList, items_per_page=10)
    
    # run the update button states to update the green and grey ones
    # paginator_view.update_button_states() # < we might no need this (put in init?)
    
    # send using the embed= and not content= since we are doing an embed & not just text
    await interaction.followup.send(embed=paginator_view.get_page_embed(), view=paginator_view)

    # endregion

# endregion

# region Database Emergency Reset Command
@bot.tree.command(name="reset_menudb", description="Send json requests and reset the daily data for the dining halls.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def reset_dininghalls(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    if interaction.user.id != 466679296417595403:
        await interaction.followup.send(f"yeah lil bro don't even try to use this if you ain't me", ephemeral=True)
        return

    jsonRequests.refresh_DiningHalls()

    await interaction.followup.send(f"Finished, all done.", ephemeral=True)
# endregion

# region Finalization & Startup
# STEP 5: MAIN ENTRY POINT
def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
# endregion