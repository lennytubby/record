# This code is based on tutorial by slicktechies modified as needed to use oauth token from Twitch.
# You can read more details at: https://www.junian.net/2017/01/how-to-record-twitch-streams.html
# original code is from https://slicktechies.com/how-to-watchrecord-twitch-streams-using-livestreamer/

import requests
import os
import time
import json
import sys
import subprocess
import datetime
import getopt
import datetime



class TwitchRecorder:
    def __init__(self):
        # global configuration
        self.client_id = "cy4qphxbgh6ef74tuvpdzcgk2eat5p" # don't change this
        # get oauth token value by typing `streamlink --twitch-oauth-authenticate` in terminal
        self.oauth_token ="x7jqesfq2pc3mn3mh4ddrkbxhc9i6z"
        self.ffmpeg_path = 'ffmpeg'
        self.refresh = 30.0
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.upload_path = os.path.join(self.root_path, "onedriveupload")
        
        # user configuration
        self.username = "lennytubby"
        self.twitchid = "109929194"
        self.subtoken = "zzh7207rnaqwj4c9ubvrtbkkenviw7"
        self.quality = "best"
        self.channels = ["ukoethe","arturandrzejak"]

    def run(self):
        # path to recorded stream
        self.recorded_path = os.path.join(self.root_path, "recorded", self.username)

        # path to finished video, errors removed
        self.processed_path = os.path.join(self.root_path, "processed", self.username)

        # create directory for recordedPath and processedPath if not exist
        if(os.path.isdir(self.recorded_path) is False):
            os.makedirs(self.recorded_path)
        if(os.path.isdir(self.processed_path) is False):
            os.makedirs(self.processed_path)

        # make sure the interval to check user availability is not less than 15 seconds
        if(self.refresh < 15):
            print("Check interval should not be lower than 15 seconds.")
            self.refresh = 15
            print("System set check interval to 15 seconds.")
        
        # fix videos from previous recording session
        try:
            video_list = [f for f in os.listdir(self.recorded_path) if os.path.isfile(os.path.join(self.recorded_path, f))]
            if(len(video_list) > 0):
                print('Fixing previously recorded files.')
            for f in video_list:
                recorded_filename = os.path.join(self.recorded_path, f)
                print('Fixing ' + recorded_filename + '.')
                try:
                    subprocess.call([self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy', os.path.join(self.processed_path,f)])
                    os.remove(recorded_filename)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

        print("Checking for", self.username, "every", self.refresh, "seconds. Record with", self.quality, "quality.")
        self.loopcheck()

    def check_user(self):
        # 0: online, 
        # 1: offline, 
        # 2: not found, 
        # 3: error 
        '''
        url = 'https://api.twitch.tv/kraken/streams/' + self.username
        info = None
        status = 3
        try:
            r = requests.get(url, headers = {"Client-ID" : self.client_id}, timeout = 15)
            r.raise_for_status()
            info = r.json()
            if info['stream'] == None:
                status = 1
            else:
                status = 0
        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.reason == 'Not Found' or e.response.reason == 'Unprocessable Entity':
                    status = 2

        return status, info
        '''

        url2 = 'https://api.twitch.tv/helix/streams?user_login='+ self.channels[0]
        for i in range(len(self.channels)-1):
            url2 = url2 + "&user_login=" + self.channels[i+1]
        try:
            r = requests.get(url2, headers = {"Client-ID" : self.client_id}, timeout = 15)
            r.raise_for_status()
            info = r.json()
            if len(info['data']) == 0:
                status = 1
            else:
                status = 0
                logins = []
                for obj in info['data']:
                    logins.append(obj["user_name"])
                return status, logins
        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.reason == 'Not Found' or e.response.reason == 'Unprocessable Entity':
                    status = 2

        return status, logins

    def loopcheck(self):
        while True:
            
            status, logins = self.check_user()
            if status == 2:
                print("Username not found. Invalid username or typo.")
                time.sleep(self.refresh)
            elif status == 3:
                print(datetime.datetime.now().strftime("%Hh%Mm%Ss")," ","unexpected error. will try again in 5 minutes.")
                time.sleep(300)
            elif status == 1:
                print(self.username, "currently offline, checking again in", self.refresh, "seconds.")
                time.sleep(self.refresh)
            elif status == 0:

                print(self.username, "online. Stream recording in session.")
                '''
                
                # start streamlink process
                subprocess.call(["streamlink", "--twitch-oauth-token", self.oauth_token, "twitch.tv/" + self.username, self.quality, "-o", recorded_filename])

                print("Recording stream is done. Fixing video file.")
                if(os.path.exists(recorded_filename) is True):
                    try:
                        filename_path = os.path.join(self.processed_path, filename)
                        subprocess.call([self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy', filename_path])
                        os.remove(recorded_filename)
                        uploadname = filename + datetime.date.today()
                        if ((info['stream']).get("channel") == "some"):
                            uploadlocation = "Uni/Info/Alda"
                        subprocess.call([self.upload_path, filename_path, uploadlocation, uploadname])
                    except Exception as e:
                        print(e)
                else:
                    print("Skip fixing. File not found.")
                    
                print("Fixing is done. Going back to checking..")
            '''
                processes = []
                for login in logins:
                    filename = login + " - " + datetime.datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss") + ".mp4"

                    # clean filename from unecessary characters
                    filename = "".join(x for x in filename if x.isalnum() or x in [" ", "-", "_", "."])
                    
                    recorded_filename = os.path.join(self.recorded_path, filename)
                    processes.append(subprocess.Popen(["streamlink", "--twitch-oauth-token", self.oauth_token, "twitch.tv/" + login, self.quality, "-o", recorded_filename]))

                while processes:
                    for i in range(len(processes)):
                        process = processes[i]
                        retcode = process.poll()
                        if retcode is not None: # Process finished.
                            processes.remove(process)
                            filename_path = os.path.join(self.processed_path, filename)
                            subprocess.call([self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy', filename_path])
                            os.remove(recorded_filename)
                            uploadname = filename
                            if (logins[i] == "ukoethe"):
                                uploadlocation = "Uni/Info/Alda"
                            if (logins[i] == "arturandrzejak"):
                                uploadlocation = "Uni/Info/Betriebssys - Net"
                            subprocess.call([self.upload_path, filename_path, uploadlocation, uploadname])
                            break
                        else: # No process is done, wait a bit and check again.
                            time.sleep(5)
                            continue


                time.sleep(self.refresh)

def main(argv):
    twitch_recorder = TwitchRecorder()
    usage_message = 'twitch-recorder.py -u <username> -q <quality>'

    try:
        opts, args = getopt.getopt(argv,"hu:q:",["username=","quality="])
    except getopt.GetoptError:
        print (usage_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage_message)
            sys.exit()
        elif opt in ("-u", "--username"):
            twitch_recorder.username = arg
        elif opt in ("-q", "--quality"):
            twitch_recorder.quality = arg

    twitch_recorder.run()

if __name__ == "__main__":
    main(sys.argv[1:])
