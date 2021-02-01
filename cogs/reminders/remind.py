import discord
from discord.ext import commands, tasks
import datetime
import pytz


class Reminder(commands.Cog):

    def __init__(self, client):
        self.client = client
            
    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()

    @commands.command()
    async def remind(self,ctx,action):

        async def get_days():
            message = ''
            await ctx.channel.send('What days would You like this reminder to occur on? `M/Tu/W/Th/F/Sa/Su`')
            days = await self.client.wait_for('message')
            if "M" in days.content:
                message = message + ' Mon'
            if "Tu" in days.content:
                message = message + ' Tue'
            if "W" in days.content:
                message = message + ' Wed'
            if "Th" in days.content:
                message = message + ' Thur'
            if "F" in days.content:
                message = message + ' Fri'
            if "Sa" in days.content:
                message = message + ' Sat'
            if "Su" in days.content:
                message = message + ' Sun'
            await get_time(message)

        async def get_time(days):
            await ctx.channel.send('What time of day would you like to be reminded on?`Example: 01:30 PM`')
            time = await self.client.wait_for('message')
            await ctx.channel.send('You would like to be reminded on' + days + ' at ' + time.content)
            await ctx.channel.send('is this correct? (Y/N)')
            confirm = await self.client.wait_for('message')
            if confirm.content == 'Y':
                await correct_input(days,f'{time.content}')
            elif confirm.content == 'N':
                await get_days()

        async def get_message():
            await ctx.channel.send('What would you like to be reminded of?')
            reminder = await self.client.wait_for('message')
            return reminder.content

        async def correct_input(days,time):
            message = await get_message()
            await ctx.channel.send('Remind me to ' + message + ' on'+days+' '+time)
            my_file = open('./cogs/reminders/reminders.txt', 'a')
            my_file.write('\n>'+days)
            my_file.write('\n` '+time + " `")
            my_file.write('\n'+message)
            my_file.close()
            
        if action == 'new':
            await get_days()
            #await ctx.channel.send(await send_days(days))

        if action == 'edit':
            reminders = open('./cogs/reminders/reminders.txt')
            content = reminders.read()
            await ctx.channel.send(content)
            reminders.close()
            await ctx.channel.send('**Which line would you like to edit? (Int)**')
            choice = await self.client.wait_for('message')
            selection = int(choice.content) - 1
            #print(selection)

            a_file = open('./cogs/reminders/reminders.txt', "r")
            list_of_lines = a_file.readlines()
            await ctx.send(f'{list_of_lines[selection]}')
            await ctx.send(f'Input the updated info as shown above')
            new_info = await self.client.wait_for('message')
            list_of_lines[selection] = new_info.content + '\n'
            await ctx.send('confirmed')
            a_file = open('./cogs/reminders/reminders.txt', "w")
            a_file.writelines(list_of_lines)
            a_file.close()



        if action == 'list':
            reminders = open('./cogs/reminders/reminders.txt')
            content = reminders.read()
            await ctx.channel.send(content)
            reminders.close()

    @commands.command()
    async def time(self,ctx):
        def get_curr_time():   
            tz_NY = pytz.timezone('America/New_York') 

            day_week = datetime.datetime.now().strftime('%a')
        
            hour = datetime.datetime.now(tz_NY).strftime('%I')
            minute = datetime.datetime.now(tz_NY).strftime('%M')
            suffix = datetime.datetime.now(tz_NY).strftime('%p')

            curr_time = (f'{day_week} {hour}:{minute} {suffix}')
        
            return curr_time
        
        time = get_curr_time()
        await ctx.channel.send(f'Current Time: {time}')
            
    @tasks.loop(seconds= 60)
    async def check(self):
        channel_id = 805620694456860714
        channel = self.client.get_channel(channel_id)

        async def check_time(curr_time,list):
            if curr_time in list[place]:
                await channel.send(list[place+1])

        reminders = open('./cogs/reminders/reminders.txt')
        list_reminders = reminders.readlines()

        # current time info
        today_day = datetime.datetime.now().strftime('%a')
        tz_NY = pytz.timezone('America/New_York') 
        hour = datetime.datetime.now(tz_NY).strftime('%I')
        minute = datetime.datetime.now(tz_NY).strftime('%M')
        suffix = datetime.datetime.now(tz_NY).strftime('%p')

        curr_time = (f'{hour}:{minute} {suffix}')

        place = 0
        for lines in list_reminders:
            place += 1
            if today_day in lines:
                #print(place)
                await check_time(curr_time,list_reminders)

        #await ctx.channel.send(list_reminders[0])
            


def setup(client):
    client.add_cog(Reminder(client))
