#INSTRUCTIONS
#  * You need to make a txt file called "SubName.txt" in the same folder as this file with the subreddit name inside it (just the plain subreddit name so use "wallpaper" NOT "r/wallpaper")
#  * You need to make another txt called "FolderLocation.txt" also in the same folder as this file with the place you wan't this program to create the folder where all your wallpapers will
#    be stored (it should look like this: "C:\Users\(username)\Desktop\") if you want it on the desktop for example

#LIBRARIES
LOUD = True
try:
    from playsound import playsound
except ModuleNotFoundError:
    LOUD = False
import praw
import urllib.request
import ctypes
from datetime import date
today = date.today()
today = str(today)


#GETTING THE SUBNAME AND SETTINGS FROM THE TXT FILES
f = open("SubName.txt","r")
f2 = open("Settings.txt","r")

subName = f.read()
f.close()
settings = f2.read()
f2.close()
sortMode = settings.split(',')[0]
if sortMode == 'top':
    sortMode = 'top/all'
trial = int(settings.split(',')[1])

#CRASH PROGRAM IF DISABLED
if len(settings.split(',')) > 2:
    if settings.split(',')[2] == "disable" or settings.split(',')[2] == "disabled":
        raise Exception("DISABLED")


#NEW API BIT
def urlIsAnImage(imgurl): #checks whether the URL is an image or not
    if ('.png' in imgurl) or ('.jpg' in imgurl) or ('.jpeg' in imgurl):
        return True
    else:
        return False

def findURL(subreddit, sortMode, trial): #function that finds url of image
    global imgURL
    imgurls = []
    
    if sortMode == 'hot':
        for submission in subreddit.hot(limit=trial+1):
            imgurl = submission.url
            imgurls.append(imgurl)
        if not urlIsAnImage(imgurls[trial]):
            findURL(subreddit, sortMode, trial+1)
        else:
            imgURL = imgurls[trial]
            return
    if sortMode == 'new':
        for submission in subreddit.new(limit=trial+1):
            imgurl = submission.url
            imgurls.append(imgurl)
        if not urlIsAnImage(imgurls[trial]):
            findURL(subreddit, sortMode, trial+1)
        else:
            imgURL = imgurls[trial]
            return
    if 'top' in sortMode:
        for submission in subreddit.top(sortMode.split('/')[1], limit=trial+1):
            imgurl = submission.url
            imgurls.append(imgurl)
        if not urlIsAnImage(imgurls[trial]):
            findURL(subreddit, sortMode, trial+1)
        else:
            imgURL = imgurls[trial]
            return
    if sortMode == 'rising':
        for submission in subreddit.rising(limit=trial+1):
            imgurl = submission.url
            imgurls.append(imgurl)
        if not urlIsAnImage(imgurls[trial]):
            findURL(subreddit, sortMode, trial+1)
        else:
            imgURL = imgurls[trial]
            return

reddit = praw.Reddit(client_id="Wey4vljRS_7EVg",client_secret="et5ySN69hvMC5FFBXrWtY_sAb0k",user_agent="<Windows>:<Wey4vljRS_7EVg>:<4.1> (by u/Omaro_IB")
subreddit = reddit.subreddit(subName)
imgURL = ''
findURL(subreddit, sortMode, trial)


#DOWNLOADS PIC FROM URL
imgName = "Backgrounds\\"+today+".jpg"
urllib.request.urlretrieve(imgURL, imgName)


#SETTING WALLPAPER
f = open("FolderLocation.txt","r")
wallpaperFolderLocation = f.read()
f.close()

src = r"%s\%s" %(wallpaperFolderLocation, imgName,)
SPIF_UPDATEINIFILE = 0x2
SPI_SETDESKWALLPAPER = 0x14
print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE))

if LOUD and len(settings.split(',')) == 2:
    playsound("Ding.wav")
if len(settings.split(',')) == 3:
    if LOUD and settings.split(',')[2] != "mute":
        playsound("Ding.wav")


