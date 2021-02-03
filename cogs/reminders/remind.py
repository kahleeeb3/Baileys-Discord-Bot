import discord
from discord.ext import commands, tasks
import datetime
import pytz
from time import sleep


class Reminder(commands.Cog):

    def __init__(self, client):
        self.client = client
            
    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()

    @commands.command()
    async def remind(self,ctx,action):
            
        if action == 'new':

            async def get_days(menu):
                await menu.edit(content = 'What days would you like this reminder to occur on?')
                days = await self.client.wait_for('message')
                await days.delete()
                return days.content

            async def get_time(menu):
                await menu.edit(content = 'What time of day would you like to be reminded on?`Example: 01:30 PM`')
                time = await self.client.wait_for('message')
                await time.delete()
                return time.content

            async def get_message(menu):
                await menu.edit(content = 'What would you like to be reminded of?')
                message = await self.client.wait_for('message')
                await message.delete()
                return message.content

            async def confirm(menu, days, time, message):
                await menu.edit(content = 'Remind me to ' + message + ' on '+days+' at '+time + '\n is this correct? (Y/N)')
                confirm = await self.client.wait_for('message')
                if confirm.content == 'Y':
                    await confirm.delete()
                    correct(days, time, message)
                    await menu.edit(content = 'Confirmed!')
                    await menu.delete()
                elif confirm.content == 'N':
                    await confirm.delete()
                    await change(menu, days, time, message)

            async def change(menu, days, time, message):
                await menu.edit(content = menu.content + '\nWhat would you like to change? (days/time/message)')
                answer = await self.client.wait_for('message')
                await answer.delete()
                if answer.content == 'days':
                    days = await get_days(menu)
                elif answer.content == 'time':
                    time = await get_time(menu)
                elif answer.content == 'message':
                    message = await get_message(menu)
                await confirm(menu, days, time, message)

            def correct(days, time, message):
                my_file = open('./cogs/reminders/reminders.txt', 'a')
                my_file.write('\n'+days)
                my_file.write('\n'+time)
                my_file.write('\n'+message+'\n')
                my_file.close()

            menu = await ctx.channel.send('Creating New Reminder...')
            sleep(1)
            days = await get_days(menu)
            time = await get_time(menu)
            message = await get_message(menu)
            await confirm(menu, days, time, message)
            action = 'list'
            print(action)
            
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
        channel_id = 768896234810245141
        channel = self.client.get_channel(channel_id)

        async def check_time(curr_time,list):
            if curr_time in list[place]:
                await channel.send(list[place+1])

        reminders = open('./cogs/reminders/reminders.txt')
        list_reminders = reminders.readlines()

        # current time info
        tz_NY = pytz.timezone('America/New_York') 
        today_day = datetime.datetime.now(tz_NY).strftime('%a')
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

