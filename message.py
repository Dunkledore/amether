import regex
import emoji
import datetime

class Message:

	def __init__(self, message_string):
		message_string = message_string.replace(u"\u200E", "")
		self.author = self.get_author(message_string)
		self.timestamp = self.get_timestamp(message_string)
		self.content = self.get_content(message_string)
		self.emojis = self.get_emojis(message_string)

	def __str__(self):
		return f"{self.timestamp.date()}:{self.author}:{self.content}"

	def __repr__(self):
		return f"{self.timestamp.date()}:{self.author}:{self.content}"

	@staticmethod
	def get_author(message_string):
		try:
			removed_timestamp = message_string[message_string.index("] ")+2:]
			if ":" not in removed_timestamp:  # No Author
				return None
			else:
				return removed_timestamp[:removed_timestamp.index(":")]
		except:
			return None

	@staticmethod
	def get_timestamp(message_string):
		try:
			date_string = message_string[1:message_string.index("]")]
			stripped = "".join(date_string.split())
			datetimeobj = datetime.datetime.strptime(stripped, "%d/%m/%Y,%I:%M:%S%p")
			return datetimeobj
		except Exception as e:
			raise

	@staticmethod
	def get_content(message_string):
		try:
			removed_timestamp = message_string[message_string.index("] ")+2:]
			if ":" not in removed_timestamp:
				return None
			else:
				return removed_timestamp[removed_timestamp.index(":")+2:]
		except:
			return None

	@staticmethod
	def get_emojis(message_string):
		try:
			emoji_list = []
			content = Message.get_content(message_string)
			graphemes = regex.findall(r'\X', content)
			for chars in graphemes:
				if any(char in emoji.UNICODE_EMOJI for char in chars):
					emoji_list.append(chars)
			flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', content)

			return emoji_list+flags
		except:
			return []


