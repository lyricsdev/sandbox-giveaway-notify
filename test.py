
import logging
from posixpath import split
import time
import datetime
from turtle import color
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from discord_webhook import DiscordWebhook, DiscordEmbed

import asyncio
from selenium.webdriver.remote.remote_connection import LOGGER
url = "your webhook here"
webhook = DiscordWebhook(url=url,content='@everyone',avatar_url='https://files.facepunch.com/s/43d4ef6a46eb.jpg',username='Garry')


togller = False

def close_driver():
	print("[/] Closing driver...")
	driver.close()
	driver.quit()
def main():
	global togller
	global driver
	LOGGER.setLevel(logging.WARNING)

	print("[/] Opening driver...")
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	options.headless = True
	options.add_experimental_option("excludeSwitches", ["enable-logging"])
	driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
	driver.get("https://asset.party/get/developer/preview")
	try:
		print("[/] Parsing buttons...")
		while True:
			time.sleep(5)
			try:
				driver.find_element(By.CSS_SELECTOR, "div.components-reconnect-rejected")
				driver.refresh()
			except selenium.common.exceptions.NoSuchElementException:
				pass
			try:
				key_value = driver.find_element(By.CLASS_NAME, "tag").text.replace("key", " ").replace("\n", "").strip()
				if key_value.isdigit():
					key_value = int(key_value)
					print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keys: {key_value}")
					if key_value > 0:
						if not togller:
							embed = DiscordEmbed(title="Slots have been detected", description=":wave:",color='03b2f8')
							embed.description = "Use this link to claim them https://asset.party/get/developer/preview"
							embed.add_embed_field(name="keys", value=key_value, inline=False)
							embed.add_embed_field(name="Status", value="Available", inline=False)
							webhook.add_embed(embed)
							webhook.execute()
							togller = True
					else:
						togller = False
				
			except selenium.common.exceptions.NoSuchElementException as e:
				print("[-] " + e)
	except KeyboardInterrupt:
		pass

	close_driver()
loop = asyncio.get_event_loop()
if __name__ == '__main__':
	loop.create_task(main())