import os
import subprocess

def get_python_interpreter():
    # Check if 'python' command exists
    try:
        subprocess.run(['python', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return 'python'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Check if 'python3' command exists
    try:
        subprocess.run(['python3', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return 'python3'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    raise EnvironmentError("Neither 'python' nor 'python3' command is available")

python_interpreter = get_python_interpreter()

# Create driver results
subprocess.run([python_interpreter, 'Pys/driver_results.py'])

# Create drivers
subprocess.run([python_interpreter, 'Pys/drivers.py'])

# Create fastest_lap results
subprocess.run([python_interpreter, 'Pys/fastest_lap_results.py'])

# Create race results
subprocess.run([python_interpreter, 'Pys/race_results.py'])

# Create Teams
subprocess.run([python_interpreter, 'Pys/teams.py'])

# Create Team results
subprocess.run([python_interpreter, 'Pys/team_results.py'])
