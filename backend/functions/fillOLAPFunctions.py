import subprocess

from clearing_dbs import clearDB

async def fill_oltp_using_pan():
    # Example command
    command = 'C:\\Users\\Alex\\Desktop\\pentaho\\data-integration\\.\\Kitchen.bat /file="C:\\Users\\Alex\\kettle\\Main_Job.kjb" /logfile="C:\\Users\\Alex\\Desktop\\logfile.txt" /loglevel=Detailed'  # This command lists files and directories in the current directory

    # Execute the command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        # Print the output of the command
        return result.stdout
    else:
        # Print the error message if the command failed
        return "Error:", result.stderr
    

async def clear_OLAP(conn):
    clearDB.execute_delete(conn)