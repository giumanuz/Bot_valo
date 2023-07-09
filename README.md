
<div align="center">
<h1 align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/NewTux.svg/1707px-NewTux.svg.png" width="100" />
<br>
Botvalo
</h1>
<h3 align="center">📍 Block out the Ordinary with Botvalo!</h3>
<h3 align="center">⚙️ Developed with the software and tools below:</h3>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white" alt="Python" />

</p>
</div>

---

## 📚 Table of Contents
- [📚 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [💫 Features](#-features)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---


## 📍 Overview

The GitHub repository is dedicated to a Telegram bot named Botvalo, which is designed to provide entertainment and fun interactions in chat. It offers a variety of features aimed at playfully insulting and making jokes with friends. The bot responds when specific phrases or words are used in chat, replying with humorous messages, photos, or triggering certain actions.
---

## 💫 Features

1. Entertainment: Botvalo is one of the best bots for entertainment purposes, offering numerous features that aim to bring joy and fun to chat interactions.

2. Insulting and Joking: The bot playfully insults and makes fun of friends in a light-hearted manner, creating an enjoyable and humorous atmosphere.

3. Phrase and Word Triggering: By activating specific phrases or words, Botvalo responds with witty messages, funny phrases, photos, or other amusing content.

4. University Classroom Booking: Botvalo implements a practical feature for university students, allowing them to book classrooms. This functionality is developed using HTTP requests, analyzed through black box analysis techniques. The bot generates a PDF of the reservation using the FPDF and QRCODE libraries.

5. Inter-chat Messaging: Botvalo enables users to send messages between different chats. Users can register specific chat IDs to facilitate communication and interaction.

6. Games: The bot offers engaging games such as Snake and Tic-Tac-Toe, providing users with additional entertainment options.

7. Google Firebase Integration: Botvalo is interfaced with the Google Firebase database, making it easy to modify and manage various parameters without the need for manual code changes.

8. Heroku Hosting: The bot is hosted on the Heroku server, ensuring reliable and continuous availability for users.

The Botvalo repository encompasses the source code and configurations required to deploy and operate the bot successfully.

---

## 📂 Project Structure


```bash
repo
├── Procfile
├── README.md
├── bot_components
│   ├── anti_cioppy_policy.py
│   ├── commands
│   │   └── bancioppy_command.py
│   ├── commands_registration.py
│   ├── db
│   │   ├── db_manager.py
│   │   └── firebase_manager.py
│   ├── foto.py
│   ├── games
│   │   ├── snake.py
│   │   └── tris.py
│   ├── gestore.py
│   ├── insulti.py
│   ├── menu.py
│   ├── prenotazioni.py
│   ├── risposte.py
│   └── settings
│       ├── cross_chat_messaging_setting.py
│       ├── menu_setting.py
│       ├── photo_removal_setting.py
│       └── settings.py
├── botvalo_tests
│   ├── components_tests.py
│   ├── conftest.py
│   ├── conversation_tests.py
│   ├── flowmatrix_tests.py
│   ├── framework
│   │   ├── mockbot.py
│   │   ├── mockcallbackquery.py
│   │   ├── mockchat.py
│   │   ├── mockcontext.py
│   │   ├── mockdatabase.py
│   │   ├── mockdispatcher.py
│   │   ├── mockmessage.py
│   │   ├── mockupdate.py
│   │   ├── mockupdater.py
│   │   └── mockuser.py
│   ├── test_utilities
│   │   ├── common_tests_utils.py
│   │   └── tris_tests_utils.py
│   └── tris_tests.py
├── main.py
├── pytest.ini
├── requirements.txt
├── resources
│   └── prenotazioni
│       ├── dichiarazione.json
│       └── settings_prenotazioni.json
├── runtime.txt
└── utils
    ├── db_utils.py
    ├── lib_utils.py
    ├── os_utils.py
    ├── regex_parser.py
    └── telegram_utils.py

12 directories, 47 files
```

---

## 🧩 Modules

<details closed><summary>Bot_components</summary>

| File                     | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Module                                  |
|:-------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------|
| commands_registration.py | This code snippet defines a class called CommandRegister that facilitates the registration and updating of commands in a Telegram bot. The class keeps track of a list of command names and their descriptions, allows for the addition of new commands, initialization of a dispatcher object, and updating the registered commands with the bot. By using this class, developers can easily manage and update the available commands in their Telegram bots.                                                                       | bot_components/commands_registration.py |
| foto.py                  | The provided code snippet defines a class called "Foto" that handles processing and sending photos in a chatbot. It initializes and updates keyword filters and schedule blacklists from a database, checks if the current hour is within the blacklist timeframe to prevent message handling, sends a randomly selected photo based on specified keywords from the database, and sets a timer to delete the sent message after a certain number of seconds.                                                                         | bot_components/foto.py                  |
| insulti.py               | The provided code snippet is for a class called `Insulti` that handles insult-related functionalities in a Telegram bot. It uses the `Database` class from `bot_components.db.db_manager` to get a list of insults, and then listens for messages that match the pattern "insulta <word>". If a matching message is received, it randomly selects an insult from the list, substitutes `<word>` in the insult with the captured word from the message, and sends it as a response to the chat.                                       | bot_components/insulti.py               |
| menu.py                  | This code snippet defines a Menu class that represents a chat menu in a Telegram bot. It uses the python-telegram-bot library to handle interactions. The class provides a method to initialize the menu and register a command handler for "/menu" command. It also allows adding buttons to the menu, which are stored in a flow matrix, and when the menu is shown, it sends a message with the menu text and buttons to the chat.                                                                                                | bot_components/menu.py                  |
| risposte.py              | The provided code snippet defines a class called Risposte that handles messages and responses in a chat bot. It keeps a dictionary of trigger words and corresponding responses, which can be fetched from a database. The handle_message method checks if the received message contains any triggers and sends the corresponding response back to the chat. This class also supports alternative responses if a trigger has a special prefix.                                                                                       | bot_components/risposte.py              |
| anti_cioppy_policy.py    | This code snippet is a part of a chatbot that implements an anti-coppier policy. It identifies a specific user called "cioppy", flags their messages for containing certain forbidden words, alerts the group if the user exceeds a maximum number of alerts, and ultimately bans the user for a progressively longer duration with each offense. The code also includes functions to adjust the banned words list, handle timeouts, and maintain a count of bans. It is integrated with a database for storing and retrieving data. | bot_components/anti_cioppy_policy.py    |
| gestore.py               | The provided code snippet defines several message handlers for a Telegram bot. These handlers filter incoming messages based on their content and source, and then perform various actions based on the filtered messages. These actions include handling certain types of messages, such as insults or photos, and enforcing an anti-copy policy. The code uses the Telegram API and related libraries to accomplish these functionalities.                                                                                         | bot_components/gestore.py               |
| prenotazioni.py          | The code snippet provided is a Python script that contains a class called "Prenotazione" and the necessary functions to handle the prenotazione-related functionalities. It includes methods for generating PDFs with QR codes, inserting text into PDFs, formatting text, and handling user inputs for creating prenotazioni. The code also integrates with the Telegram API to send prenotazione PDF documents to users.                                                                                                           | bot_components/prenotazioni.py          |

</details>

<details closed><summary>Botvalo_tests</summary>

| File                  | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Module                              |
|:----------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------|
| conftest.py           | This code snippet provides three test fixtures:                                                                                                                                                                                                                                                                                                                                                                                                                                                     | botvalo_tests/conftest.py           |
|                       | 1. The `simple_setup` fixture resets the data of a common bot instance.                                                                                                                                                                                                                                                                                                                                                                                                                             |                                     |
|                       | 2. The `full_blacklist` fixture resets the data of the common bot instance, calls a method in the'Foto' class to update a full blacklist, and then resets the blacklist after test completion.                                                                                                                                                                                                                                                                                                      |                                     |
|                       | 3. The `empty_blacklist` fixture also resets the data of the common bot instance, calls a method in the'Foto' class to clear the blacklist, and then resets the blacklist after test completion. These fixtures can be used to set up specific conditions before running tests.                                                                                                                                                                                                                     |                                     |
| tris_tests.py         | The provided code snippet is a collection of unit tests for a Tris (tic-tac-toe) game component in a bot framework. The tests cover various scenarios such as displaying the game board, handling player moves, determining win/draw conditions, and sending appropriate messages based on the game outcome. The code uses fixtures to set up the game state and provides test cases for different player actions and inputs.                                                                       | botvalo_tests/tris_tests.py         |
| components_tests.py   | The code snippet includes pytest test cases for different functionalities.                                                                                                                                                                                                                                                                                                                                                                                                                          | botvalo_tests/components_tests.py   |
|                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                     |
|                       | 1. The first test case checks if the Menu class properly adds a command handler to the message dispatcher.                                                                                                                                                                                                                                                                                                                                                                                          |                                     |
|                       | 2. The second test case verifies that the Foto class throws a TypeError when trying to set the chat removal timer with invalid parameters.                                                                                                                                                                                                                                                                                                                                                          |                                     |
|                       | 3. The third test case ensures that the Foto class correctly identifies if a given text exists in a list.                                                                                                                                                                                                                                                                                                                                                                                           |                                     |
|                       | 4. The last test case validates that the Foto class does not raise an error when attempting to delete a message that cannot be deleted due to exceptions like BadRequest or TimedOut.                                                                                                                                                                                                                                                                                                               |                                     |
| flowmatrix_tests.py   | The provided code snippet contains a set of test cases for the functionality of the FlowMatrix class from the utils.lib_utils module. The tests ensure that the class behaves as expected-adding elements to the matrix in the correct rows based on their row length, raising errors for invalid row lengths, and converting a list into a matrix with specified row lengths. The test cases cover different scenarios and provide comprehensive coverage for the key functionalities of the code. | botvalo_tests/flowmatrix_tests.py   |
| conversation_tests.py | The provided code snippet is written in Python and includes multiple test functions. These functions test various functionalities of a chatbot, including insult replies, sending photos, responding with specific messages, and displaying a menu. The tests use a mock bot and mock context to simulate interactions with the bot. The code also sets up a mock database and initializes certain components before running the tests.                                                             | botvalo_tests/conversation_tests.py |

</details>

<details closed><summary>Commands</summary>

| File                 | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Module                                       |
|:---------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------|
| bancioppy_command.py | The provided code snippet is a Python class called "BanCioppyCommand" that implements the functionality of a voting system to ban a user named "Cioppy" from a chat group. It uses the Telegram API to interact with the chat and manage the voting process. The class keeps track of the current voters, sets a required number of voters to ban Cioppy, sends messages to the chat about the voting status, and has a built-in timer to reset the voters after a specified time. | bot_components/commands/bancioppy_command.py |

</details>

<details closed><summary>Db</summary>

| File                | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Module                                |
|:--------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------|
| db_manager.py       | The code snippet defines a class called Database, which serves as an abstract base class for different types of databases. It includes class methods for setting and retrieving the current database type, as well as an instance method for registering callbacks to handle configuration changes. Additionally, it provides several abstract methods for retrieving and modifying various database-specific attributes such as insult lists, chat aliases, keywords for photos, and more.                                                                                                             | bot_components/db/db_manager.py       |
| firebase_manager.py | The provided code snippet is a Python class called `FirebaseStorage` that extends the `Database` class. It initializes the Firebase admin SDK and provides various methods to interact with Firestore, Firebase Storage, and retrieve data from Firestore documents. These methods include fetching insult lists, chat aliases, keywords for photos, nicknames, responses, schedule blacklist, chat removal seconds, chat alias settings, CIOPPY (an abbreviation) timeout settings, and more. Overall, the class serves as a wrapper for Firebase functionality to manage data and storage operations. | bot_components/db/firebase_manager.py |

</details>

<details closed><summary>Framework</summary>

| File                 | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Module                                       |
|:---------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------|
| mockupdate.py        | The provided code snippet defines a class called "MockUpdate" which mimics the behavior of an update object in the Telegram Bot API. It contains properties like "effective_message", "effective_chat", and "effective_user" that provide access to the message, chat, and user related information. It also includes methods for creating instances of the class with different sets of parameters. The class is primarily used for testing purposes in a Telegram bot environment. Overall, it provides a way to simulate and manipulate update objects for testing bot functionality. | botvalo_tests/framework/mockupdate.py        |
| mockcontext.py       | The code defines a class called "MockContext" that takes in a "dispatcher" object as a parameter during initialization. It has a property method called "bot" which returns the bot object associated with the dispatcher. The purpose of this class is to provide a context for handling requests and interactions with the bot.                                                                                                                                                                                                                                                        | botvalo_tests/framework/mockcontext.py       |
| mockdatabase.py      | The provided code snippet defines a class called `MockDatabase` that inherits from a `Database` superclass. This class serves as a mock implementation of a database, containing several attributes and methods. Some of the core functionalities include loading default values, getting and setting various data such as insults, photo keywords, nicknames, responses, blacklist settings, and chat aliases. Additionally, there are methods related to retrieving and manipulating data related to a fictional "Cioppy" entity.                                                      | botvalo_tests/framework/mockdatabase.py      |
| mockchat.py          | The provided code snippet defines a class called `MockChat` that represents a chat in a messaging application. It has attributes to store the chat ID and chat type, along with methods to send messages and photos. It also has a class level method to set a common bot instance and a class level method to retrieve a common chat instance. The code snippet offers a convenient way to interact with chats in a simplified manner.                                                                                                                                                  | botvalo_tests/framework/mockchat.py          |
| mockbot.py           | This code snippet defines the `MockBot` class, which represents a mock implementation of a Bot. It has methods such as `send_photo` and `send_message` to simulate sending photos and messages. It also has a `result` property to retrieve the data of the sent messages. Additionally, it has methods like `reset_data` and `set_my_commands` for managing the bot's data. Overall, this code snippet provides a way to simulate bot actions and retrieve information about them.                                                                                                      | botvalo_tests/framework/mockbot.py           |
| mockmessage.py       | The provided code snippet defines a `MockMessage` class that represents a mock message in a messaging platform (e.g., Telegram). This class encapsulates properties and methods to handle text, message ID, reply markup, caption, and chat ID. It has functionality to edit reply markup, reply with text or photo, delete the message, and set an exception to be thrown when deleting. Additionally, it has a class-level variable to store a common bot instance.                                                                                                                    | botvalo_tests/framework/mockmessage.py       |
| mockdispatcher.py    | The provided code snippet defines a MockDispatcher class that is used for handling communication between a bot and its handlers. It has a bot property that returns the bot it is associated with, and a list of handlers that can be added to it using the add_handler() method. This class is part of the Telegram package and extends the Handler class.                                                                                                                                                                                                                              | botvalo_tests/framework/mockdispatcher.py    |
| mockupdater.py       | The provided code snippet defines a class called "MockUpdater" that takes a "dispatcher" parameter in its constructor. The class has a method called "start_polling()" that currently does nothing. The purpose of this class is to handle updating some sort of data or information through the "dispatcher" object. The "start_polling()" method likely needs to be implemented to perform the necessary actions for updating the data.                                                                                                                                                | botvalo_tests/framework/mockupdater.py       |
| mockuser.py          | The code snippet defines a class called MockUser, which represents a user with an ID and a first name. The class has attributes for ID and first name, as well as getter methods (using Python property decorators) to access these attributes. The default values for ID and first name are-1 and an empty string, respectively.                                                                                                                                                                                                                                                        | botvalo_tests/framework/mockuser.py          |
| mockcallbackquery.py | The code snippet defines a class called "MockCallbackQuery" that represents a callback query object. It has a constructor that initializes the "answered" attribute to False and takes in a string argument called "data". It also has a property called "data" that returns the value of the "data" attribute. Additionally, there are methods to mark the query as answered and check if it has been answered.                                                                                                                                                                         | botvalo_tests/framework/mockcallbackquery.py |

</details>

<details closed><summary>Games</summary>

| File     | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Module                        |
|:---------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------|
| snake.py | This code snippet is a Python implementation of the classic game Snake using the Telegram Bot API.                                                                                                                                                                                                                                                                                                                                                                                                                                                          | bot_components/games/snake.py |
|          | The `Snake` class represents the game, and it handles the creation of a game instance, movement of the snake, responding to user commands, and updating the game grid.                                                                                                                                                                                                                                                                                                                                                                                      |                               |
|          | The game supports both private chats and group chats with different grid sizes and update intervals.                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                               |
|          | The game can be started by clicking on an inline button, and the player must navigate the snake using arrow buttons. The game ends when the snake hits a boundary or itself.                                                                                                                                                                                                                                                                                                                                                                                |                               |
| tris.py  | This code snippet is a complete implementation of a tic-tac-toe game (tris) using the Telegram Bot API. It allows users to play against each other by selecting cells on a game board, and determines the winner or declares a tie based on the game's rules. The active game instances are stored in a dictionary, and the game state is updated by handling callback queries and editing the message accordingly. The code also includes functionality to load player nicknames from a database, and buttons to access the game are registered in a menu. | bot_components/games/tris.py  |

</details>

<details closed><summary>Root</summary>

| File        | Summary                                                                                                                                                                                                                                                                                                                                                                              | Module      |
|:------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------|
| .env_sample | The code snippet provides environment variables for authentication and configuration of a Firebase project, including project ID, credentials key ID and private key, client email, client ID, and bucket name. Additionally, it includes a BOT_TOKEN variable, which is likely used for authentication in a bot application.                                                        | .env_sample |
| Procfile    | The provided code snippet is a terminal command that runs a Python file called `main.py` using Python version 3. It is likely used to start a Python web application or server.                                                                                                                                                                                                      | Procfile    |
| main.py     | The provided code snippet is for a Telegram bot. It imports necessary libraries, sets up environment variables, initializes database and bot components, creates an updater, and starts the bot as either a server or for local testing based on the environment variables. The functionality is encapsulated in various functions and classes for easy management and organization. | main.py     |

</details>

<details closed><summary>Settings</summary>

| File                            | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Module                                                  |
|:--------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------|
| photo_removal_setting.py        | The provided code snippet is a class called `PhotoRemovalSetting` that is a subclass of `MenuSetting`. It handles the setting of an automatic photo removal timer in a Telegram bot. It creates a menu with preset options for the timer duration, allows the user to select a duration, and handles the logic to set the timer and display a confirmation message accordingly.                                                                                                                                                                                                                      | bot_components/settings/photo_removal_setting.py        |
| menu_setting.py                 | The code snippet defines a base class called MenuSetting that provides functionality for creating menu settings in a Telegram bot. It is an abstract class with abstract methods for implementing the name, id, and callback functions. It also provides methods for adding a callback query handler and generating a button with a callback pattern. The code utilizes the telegram library for receiving updates and handling callbacks.                                                                                                                                                           | bot_components/settings/menu_setting.py                 |
| settings.py                     | This code snippet represents a class called "ChatSettings" that provides functionality for managing settings in a chat application using the Telegram bot API. It utilizes the "telegram" and "telegram.ext" libraries for creating inline keyboard buttons and handling callback queries.                                                                                                                                                                                                                                                                                                           | bot_components/settings/settings.py                     |
|                                 | The class initializes the settings matrix, adds a callback handler for displaying the settings, and initializes a few predefined settings. It also provides a method to show the current settings in an inline keyboard format when invoked.                                                                                                                                                                                                                                                                                                                                                         |                                                         |
| cross_chat_messaging_setting.py | This code snippet defines a class called CrossChatMessagingSetting, which is a menu setting implementation for a Telegram bot. It handles cross-chat messaging functionalities such as registering and removing chats, sending messages to other chats, and canceling actions. The class utilizes the Telegram and python-telegram libraries and includes methods for setting up inline buttons, adding event handlers, and managing conversations using a ConversationHandler. Overall, it provides a convenient way to configure and perform cross-chat messaging actions within the Telegram bot. | bot_components/settings/cross_chat_messaging_setting.py |

</details>

<details closed><summary>Test_utilities</summary>

| File                  | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Module                                             |
|:----------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------|
| common_tests_utils.py | The code snippet provides functions for setting and getting a global variable called COMMON_BOT, which represents a common bot object used in tests. There are also functions for sending fake messages to a class and checking if a response has a valid photo. The code is part of a testing framework and aims to facilitate testing functionalities related to bots and messages.                                                                                                                                  | botvalo_tests/test_utilities/common_tests_utils.py |
| tris_tests_utils.py   | This code snippet provides several helper functions for creating and manipulating a virtual tic-tac-toe board used in a Telegram bot game. The "is_empty_tris" function checks if all cells on the board are empty, "make_cells" creates a keyboard markup for the buttons representing the board cells with corresponding labels and callback data, and "are_cells_equal" compares two sets of cells to check for equality. These functions facilitate the functionality of the tic-tac-toe game in the Telegram bot. | botvalo_tests/test_utilities/tris_tests_utils.py   |

</details>

<details closed><summary>Utils</summary>

| File              | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Module                  |
|:------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------|
| os_utils.py       | The provided code snippet includes three functions:                                                                                                                                                                                                                                                                                                                                                                                                      | utils/os_utils.py       |
|                   | 1. "get_absolute_path" takes a string representing a file path starting from the main directory, and returns the absolute path by appending it to the main directory path.                                                                                                                                                                                                                                                                               |                         |
|                   | 2. "get_current_local_datetime" returns the current date and time in the Italian timezone using the "datetime" and "pytz" libraries.                                                                                                                                                                                                                                                                                                                     |                         |
|                   | 3. "get_current_weekday_name" returns the lowercase English name of the current day of the week by using the "datetime" library and formatting the current date accordingly. If a specific "local_datetime" is provided, it uses that instead of the current time.                                                                                                                                                                                       |                         |
| telegram_utils.py | The provided code defines a function called "get_effective_text" that takes an "update" object as its parameter. This function checks if the "update" object has a caption or a text attribute and, if present, returns the lowercase version of the caption or text as a string. It is used to retrieve and process the actual text message from the update object.                                                                                     | utils/telegram_utils.py |
| regex_parser.py   | The provided code snippet defines a class called `WordParser` with a single class method called `contains`. This method checks if a given phrase is present in a given text string as a separate word. It uses a regular expression to find a match by surrounding the phrase with non-word characters or the start/end of the text. If a match is found, the method returns True, otherwise False.                                                      | utils/regex_parser.py   |
| lib_utils.py      | The provided code snippet defines a class called FlowMatrix. This class is designed to create 2-dimensional matrices with a specific row length. The class has methods to append elements to the matrix, check if the matrix is empty, and create a new row if the current row is full. It also provides a class method to create a FlowMatrix object from a given list, automatically calculating the number of rows based on the specified row length. | utils/lib_utils.py      |
| db_utils.py       | The provided code snippet is structured using the JavaScript Promise API. It creates a new Promise object and defines success and error handlers. Inside the promise, an asynchronous task is performed, making an API call. If the API call is successful, the promise is resolved with the result, otherwise it is rejected with an error. The code also includes a utility function for delaying execution of the promise.                            | utils/db_utils.py       |

</details>

---

## 🚀 Getting Started

### ✅ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:
> - APScheduler==3.6.3
> - cachetools==4.2.2
> - certifi==2021.10.8
> - fpdf==1.7.2
> - Pillow==9.0.1
> - python-telegram-bot 
>=13.11, ==13.*
> - pytz==2021.3
> - pytz-deprecation-shim==0.1.0.post0
> - qrcode==7.3.1
> - six==1.16.0
> - tornado==6.1
> - tzdata==2021.5
> - tzlocal==4.1
> - firebase-admin 
>=5.2.0, ==5.2.*
> - python-dotenv

### 🖥 Installation

1. Clone the  repository:
```sh
git clone https://github.com/giumanuz/Bot_valo
```

2. Change to the project directory:
```sh
cd Bot_valo
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🚀 Setup

Questo readme è temporaneo, verranno scritte delle pagine wiki dettagliate appena sarà disponibile.

Per setuppare il bot dopo il merge `edotm/firebase-integration` è necessario avere un file `.env` con dentro tutte le
informazioni necessarie per far partire il bot. Guarda, per riferimento, il file `.env_sample`.

Il file `.env` che va usato per il testing si trova sul server discord comune, nella chat `#botvalo-shit`. **
Importante:** discord lo fa scaricare come "env", senza il punto davanti, ma deve essere rinominato in "**.env**" per
funzionare.

## 🖥 Configurazione del bot

Per configurare il bot, vai nella [**console di
firebase**](https://console.firebase.google.com/u/0/project/botvalodatabase). Se non hai accesso a firebase come editor,
chiedi a [@EdoTM](https://github.com/EdoTM) o a [@giumanuz](https://github.com/giumanuz) di fornirtelo. Il bot usa
principalmente due servizi di firebase:

+ Il [firestore database](https://console.firebase.google.com/u/0/project/botvalodatabase/firestore/), usato per i file
  di configurazione. **Non modificare file se non sai quello che stai facendo.** Prima di modificare un file, nota come
  è strutturato e modificalo seguendo quella struttura, altrimenti il bot potrebbe non funzionare correttamente.



+ Lo [storage](https://console.firebase.google.com/u/0/project/botvalodatabase/storage), che viene usato per le foto. Si
  trovano tutte dentro la cartella `images/categoria/`, dove `categoria` è una delle sottocartelle. **Attenzione:** il
  nome delle categorie
  (quindi, delle sottocartelle) deve corrispondere alle rispettive voci dentro il file
  `keyword_foto` nel firestore database. Se vuoi aggiungere categorie e non sai come fare, chiedi
  a [@EdoTM](https://github.com/EdoTM) o a [@giumanuz](https://github.com/giumanuz).





---


## 🤝 Contributing

Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a pull request to the original repository.
Open a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.

---

## 📄 License

This project is licensed under the `MIT` License.
---

