#! python3

# Manar Naboulsi - 04 March, 2018
#
# Backup to Zip - Copies folder and its contents of a specified type into a ZIP 
#                 file. Backups older than a specified number of days are 
#                 deleted. Log messages are saved in same folder as ZIP file.

# Arguments:
#   - folder = folder to backup
#   - zipLocation = backup file location
#   - ext = extension of files to backup
#           if all types should be backed up, set to 'all'
#   - days = number of days before deleting a file 


import zipfile, os, time, sys, logging
from datetime import datetime

# backs up the entire contents of "folder" into a ZIP file
def backupToZip(folder, zipLocation, ext, days):
    now = datetime.now()  # obtains date and time when this backup started

    # initiates logging file saved in zipLocation
    logging.basicConfig(level=logging.INFO, filename=os.path.join(zipLocation, 'backup_log.log'))
    logging.info('-----------------------------------------------------------------------------') 
    logging.info('Starting at ' + str(now))

	
    # checks that paths provided exist
    # if not, program stops
    while True:
        if os.path.exists(folder) is False:
            logging.warning('"' + folder.rsplit(os.sep,1)[-1] + '"' + ' does not exist.\n\n')
            sys.exit()
        elif os.path.exists(zipLocation) is False:
            logging.warning('"'+ zipLocation.rsplit(os.sep,1)[-1] + '"' + ' does not exist.\n\n')
            sys.exit()
        else:
            break
                
				
    # names ZIP file with today's date and time
    zipFilename = str(now.strftime('%Y%m%d_%H%M%S')) + '_' + folder.rsplit(os.sep,1)[-1] + '.zip'  


    # creates the ZIP file
    logging.info('Creating %s...' % (zipFilename))
    backupZip = zipfile.ZipFile(os.path.join(zipLocation, zipFilename), 'w')

	
    # walks the entire folder tree and compresses the files in each folder
    logging.info('Backing up files...')
    for foldername, subfolders, filenames in os.walk(folder):
        # adds the current folder to the ZIP file
        backupZip.write(foldername)
         
        # adds files in this folder to the ZIP file    
        for filename in filenames:
            # backs up all files if ext provided is 'all'
            if ext == 'all':
                backupZip.write(os.path.join(foldername, filename))
            # backs up files of the ext provided
            elif filename.endswith(ext): 
                backupZip.write(os.path.join(foldername, filename))
    backupZip.close()
    logging.info('Done.\n')


    # deletes back up files older than 4 days
    old = 0  # initalizes deleted files counter
    now1 = time.time()  # obtains date and time when this backup ended
    
    logging.info('Deleting back-up files older than %s days...' % str(days))
    for file in os.listdir(zipLocation):
        filePath = os.path.join(zipLocation, file)
        if os.stat(filePath).st_mtime < now1 - days * 86400:
            logging.info('  - Deleting ' +  file)
            os.remove(os.path.join(zipLocation, file))
            old += 1
    if old == 0:
        logging.info('  - No old files found.')
   
   
    # ends logger
    now = datetime.now()  
    logging.info('Done at ' + str(now.strftime('%Y%m%d_%H%M%S')) + '\n\n')
    logging.shutdown()

# end of backupToZip
	
	
# run program 
#backupToZip('', '', '', )
