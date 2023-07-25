import sys
from upload import uploadfile



# process_file('april/me')   
if __name__ == '__main__':
    folder = sys.argv[1]
    uploadfile(folder)