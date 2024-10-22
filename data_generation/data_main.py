import subprocess
import concurrent.futures

def run_script(script):
    """Function to run a Python script."""
    subprocess.run(['python', script])

if __name__ == '__main__':
    # List your visualization scripts
    scripts = ['isobar.py', 'isotherm.py', 'isotach.py', 'isohume.py', 'isohyet.py', 'isodrosotherm.py', 'isoneph.py', 'isogon.py' ]  # Add all your scripts here

    # Run scripts in parallel
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(run_script, scripts)
