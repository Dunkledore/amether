from zipfile import ZipFile
from message import Message
import matplotlib.dates as dates
import matplotlib.pyplot
from scipy.interpolate import spline
import numpy as np
from datetime import timedelta, datetime

def create_chart(filename):

	with ZipFile(f"chats/{filename}", 'r') as zip:
		raw_data = zip.read("_chat.txt").decode()
	raw_message_list = raw_data.split("\r\n")

	message_objects = []
	for message_string in raw_message_list[:-1]:  #End message is blank line
		message_object = Message(message_string)
		if message_object.author:
			if message_object.content != "Messages to this group are now secured with end-to-end encryption.":
				message_objects.append(message_object)

	group_members = {}
	master_emojis = {}
	for message in message_objects:
		if message.author not in group_members:
			group_members[message.author] = {}

	for message in message_objects:
		for member in group_members.keys():
			if message.timestamp.replace(hour=0, minute=0, second=0, microsecond=0) not in group_members[member]:
				group_members[member][message.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)] = 0
		group_members[message.author][message.timestamp.replace(hour=0, minute=0, second=0, microsecond=0)] += 1


		for emoji in message.emojis:
			if emoji not in master_emojis:
				master_emojis[emoji] = 1
			else:
				master_emojis[emoji] +=1
	xaxis = dates.date2num(list(group_members[list(group_members.keys())[0]].keys()))
	xsmooth = np.linspace(xaxis.min(),xaxis.max(),1000000)
	fig , ax = matplotlib.pyplot.subplots(figsize=[20,5])
	to_plot = []
	for member in group_members.keys():
		yaxis = list(group_members[member].values())
		ysmooth = spline(xaxis,yaxis,xsmooth)
		to_plot.append((ysmooth,member))

	for item, member in to_plot:
		ax.plot_date(xsmooth, item, '-', linewidth=2, label=member)
	ax.xaxis.set_major_locator(dates.DayLocator(None,5))
	ax.xaxis.set_major_formatter(dates.DateFormatter("%d/%m/%y"))
	matplotlib.pyplot.xticks(rotation="vertical")
	matplotlib.pyplot.legend()
	matplotlib.pyplot.title("😮")
	matplotlib.pyplot.savefig(f"outputs/{filename}.png",bbox_inches='tight')





