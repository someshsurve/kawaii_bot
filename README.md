Kawaii Discord Bot Documentation
=========================

Introduction
------------

This Discord bot is designed to enhance server functionality by providing various features and commands. It offers the following capabilities:

-   Member Data: Retrieves a list of all members in the Discord channel along with their roles.
-   Message Counter: Calculates the number of messages sent in the past 12 hours.
-   Endorsements: Allows users to give endorsements or express gratitude to other members.
-   Endorsement Leaderboard: Displays a sorted list of users based on the number of endorsements they received.
-   Points System: Tracks the total number of endorsement points received by specific user.

### bot link
``` https://discord.com/api/oauth2/authorize?client_id=1129299200081928282&permissions=8&scope=bot```

Commands and Usage
------------------
### prefix based commands
### `$members_data`

Retrieves a list of all members in the Discord channel along with their roles.

### `$messages_counter`

Calculates and displays the total number of messages sent in the past hour.

### slash commands

### `/help`

instructions to use kawaii bot.

### `/thanks @username`

Allows users to give endorsements or express gratitude to other members.

### `/endorsements`

Generates a sorted list of users based on the number of endorsements received.


### `/endorsement_points @username`

Displays the total number of endorsement points received by a user.

Installation
------------

To run the Discord bot locally or on your server, follow these steps:

1.  Clone the repository:

    `git clone https://github.com/someshsurve/kawaii_bot`

2.  Install the required dependencies:

    required: discord.py library, datetime, sqlite3

    `pip install discord.py`

3.  please recheck for bot token in script. ```MTEyOTI5OTIwMDA4MTkyODI4Mg.GW2V5Z.njBau_i_0U2L4l36L0OuYOmJSoGePhaOkGOvHA```

4. Run the bot script:

    `kawaii_bot.py`

5. The bot is now active and ready to respond to commands in your Discord server.

