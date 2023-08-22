# AIoT-FML Learning Tools Software

# Supported by
# Ministry of Science and Technology (MOST), Taiwan
# AI-FML Agent with Machine Learning Tools for AloT Future Applications
# MOST 109-2622-E-024-001-CC1, MOST 110-2622-E-024-003-CC1, and MOST 111-2622-E-024-001

# Copyright (c) 2023
# KWS Center/OASE Lab. of NUTN, Taiwan
# Zsystem Technology Co., Taiwan
# Mediawave Intelligent Communication Limited., Taiwan
# All rights reserved.


from gpb import sdcard as sdc
import uos
import image

class SDModule():
    def __init__(self):
        self.vfs = uos.VfsFat(sdc())
        #mount to current directory
        uos.mount(self.vfs, '/')
        uos.chdir('/')
        
    def WriteFile(self, filename, data, mode):
        '''
        Function: Write data to a file and store in SD card
        Input:
        (1) filename: name of the file
        (2) data: content which will be written into the file
        '''
        # write file (You can see the file after clicking on reset button on the board
        f = self.vfs.open(filename, mode)
        # separate each other using '\n
        data_str = ''
        for item in data:
            data_str = data_str + item + '\n'
            #print('data_str=', data_str)
        #write data to the file
        len = f.write(data_str)
        #print("Finish writing file and length is ", len)
        #close file
        f.close()
       

    def ReadFile(self, filename):
        '''
        Function: Read file from SD card
        '''
        f = self.vfs.open(filename, 'r')
        #print(f.read()) #read all contents
        #read file line by line
        data = []
        for line in f.readlines():                          
            line = line.strip()                              
            #print('line=', line)
            data.append(line)
        f.close()
        return data
        
    def file_or_dir_exists(self, filename):
        '''
        Function: Check data exists or not
        Output:
        True: exist
        False: not exist
        '''
        try:
            uos.stat(filename)
            return True
        except OSError:
            return False
            
    def DeleteFile(self, filename):
        '''
        Function: Delete a file from SD card
        '''
        if self.file_or_dir_exists(filename):   
            uos.remove(filename)
            print('Delete {}'.format(filename) + ' successfully.')
        else:
            print('{}'.format(filename) + ' does not exist.')

    def WriteImage(self, filename, img):
        '''
        Function: Write data to a file and store in SD card
        Input:
        (1) filename: name of the file
        (2) data: content which will be written into the file
        '''
        # write file (You can see the file after clicking on reset button on the board
        
        #compress img to a jpeg file
        new_img = img.compressed()
        
        #save new_img to the SD
        f = self.vfs.open(filename, 'wb')
        len = f.write(new_img)
        print("Finish writing image and length is ", len)
        #close file
        f.close()
    