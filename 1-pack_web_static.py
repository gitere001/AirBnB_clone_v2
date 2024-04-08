from fabric import task
from datetime import datetime
import os


@task
def do_pack(c):
    """Generate a .tgz archive from the contents of the web_static folder."""
    # Define the current date and time
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")

    # Name of the archive
    archive_name = "web_static_{}.tgz".format(date_time)

    # Path of the archive
    archive_path = "versions/{}".format(archive_name)

    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Compress the contents of the web_static folder into the archive
    result = c.local("tar -cvzf {} web_static".format(archive_path))

    # Check if the compression was successful
    if result.failed:
        return None
    else:
        return archive_path
