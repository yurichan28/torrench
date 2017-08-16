## Module to select which website to fetch data from

import platform

def main(title, page, site): ## site means which site to use
	title = title.replace(" ", "+")
	
	if platform.system() == 'Windows': # Determine platform
		import os
		import ctypes
		ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 3)
		os.system("mode CON: COLS=180 LINES=350") 	# Expand windows console window so output does not overlap (font==default).
													# Change accordingly if necessary.
	
	if site == 1: ## For TPB
		import torrench.tpb.main as tpb
		tpb.main(title, page)
		
	elif site == 2: ## For KAT
		import torrench.kat.main as kat
		kat.main(title, page)
	elif site == 3: ## For Distrowatch
		import torrench.distrowatch.main as distrowatch
		distrowatch.main(title)
	else:
		import torrench.linuxtracker.main as LTracker
		LTracker.main(title)

	if __name__ == "__main__":
		print("Its a module to be called with __main__")
