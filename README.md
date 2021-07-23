# BGTracker
BGTracker scrapes boardgame data from online retailer Miniature Market(MM) and stores that data in files.

The program will first discover what board games are already being tracked by reading the files, then allow the user to input the MM product number for a new board game to track. After this, it will scrape the data for the appropriate board games, compare that data to the last entry written to the file, and if the newly scraped data is the same as the file nothing happens, otherwise the new data is appended to the file. 