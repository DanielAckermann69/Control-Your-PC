# Control-Your-PC: Empowering Remote PC Control via Discord

## Introduction

Control-Your-PC is a powerful program designed to grant you remote control over your computer through Discord, providing convenience and flexibility like never before. This markdown file serves as a guide to understanding and utilizing the various functions and capabilities of this remarkable tool. From capturing screenshots and webcam pictures to executing commands and managing tasks, Control-Your-PC puts the power of your PC at your fingertips, regardless of your physical location.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Reactions](#reactions)
3. [Commands](#commands)


## Getting Started <a name="getting-started"></a>

To begin using Control-Your-PC, follow these simple steps:

1. Install Control-Your-PC on your computer.
2. Create a Discord bot and obtain its token.
3. Add the bot to your Discord server.
4. Grab the token and a channel id and change them in the settings
![image](https://github.com/DanielAckermann69/Control-Your-PC/assets/86055452/b8a03ad2-5a44-438e-8738-79eba70e9ad0)
5. Once you start the .py programm you should see something like this:
![image](https://github.com/DanielAckermann69/Control-Your-PC/assets/86055452/adda18dc-255d-4bb5-9e01-78e6bef173ff)


## Reactions <a name="reactions"></a>

You will have 5 reactions:
1. 💻 --> this will send screenshots
2. 📴 --> this will turn off the computer
3. 🔄 --> this will restart the computer
4. 🛏 --> this will set the computer in sleep mode
5. ☢ --> this will stop the programm


## Commands <a name="commands"></a>

The Programm has 18 commands you can use.

1.  download --> Downloads a file from the internet and saves it on your pc (cwd)
2.  shutdown --> shuts down the pc
3.  restart --> restarts the pc
4.  deepsleep --> Set Pc in deepsleep
5.  screenshot --> Takes screenshot
6.  taskkill --> kills a task <task>
7.  status --> Status
8.  saveFile --> Saves attached file to CWD
9.  commands --> Shows this message
10. tasks --> lists all tasks
11. clear --> clears the discord chat
12. terminate --> terminates Discord_Control
13. cd --> change dir to <path>
14. dir --> lists dir
15. cwd --> prints current working dir
16. exec --> Executes the command <cmd>
17. get --> Downloads a file from your pc <file/file_path>
18. getAll --> Downloads all files in cwd from your pc


## Autostart - setup

1. Press win+ r to open the run window.
2. Enter 'shell:startup'
![image](https://github.com/DanielAckermann69/Control-Your-PC/assets/86055452/01a453c1-6a10-4168-b797-823ca2754620)
3. Copy the .py file with the correct setup (Token/channelid) into the startup folder, and rename it to .pyw (no consol)
![image](https://github.com/DanielAckermann69/Control-Your-PC/assets/86055452/0685f981-02aa-4f5d-9f8a-8a8b9adf7682)

Congreats! your programm is set up and will start on every system start.



