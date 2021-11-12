import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import boto3
import os
import random
client=boto3.client('s3')
s3 = boto3.resource('s3')

my_bucket = s3.Bucket("hot-dog-images")
#----------------------------------
#Fonction effacement d'ecran 
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'

    os.system(command)

while True:
    clearConsole()
    #----------------------------------
    #--------------------- Menu --------------------------
    print("                 -------                      ")
    print("                   Menu                       ")
    print("                 -------                      ")
    print("----------------------------------------------")
    print(" Load random images                        <1>")
    print(" Upload images Hot-Dog                     <2>")
    print(" Quit                                      <3>")
    print("----------------------------------------------")
    #Entrer le choix compris entre [1-3]
    while True:
        try:
            choice=int(input(">> "))
            if choice >= 1 and choice <= 3: 
                break
            else:
                print('Error choice')
        except:
            print('\n Invalid choice')
    #choix donwload
    if choice == 1:
        #create folder download
        folder='./download_client'
        if not os.path.exists(folder):
            os.makedirs(folder)
        local_download_directory = r"./download_client/"
        #-------------------------------------------
        #resp = my_bucket.objects.filter(Prefix="images/")
        resp=client.list_objects_v2(Bucket='hot-dog-images')
        keys = []
        for obj in resp['Contents']:
            if obj['Key'].endswith(".jpg"):
                keys.append(obj['Key'])
        length = len(keys)
        liste=[]
        i=0
        while True:
            id=random.randint(0,length)
            if keys[id].endswith(".jpg") and id not in liste:
                liste.append(id)
                s3.meta.client.download_file('hot-dog-images', keys[id] , 'download_client/'+keys[id])
                #---------------------------------------------------
                plt.figure('Hot-Dogs Apps')
                plt.title(keys[id])
                plt.axis('off')
                img = mpimg.imread('download_client/'+keys[id])
                imgplot = plt.imshow(img)
                plt.show()
                #------------------------------------------------------
                while True:
                    try:
                        valide=int(input("1. Hot-Dog | 0. other\n>> "))
                        if valide >= 0 and valide <= 1: break
                    except:
                        print('\n Invalid label')
                basename_without_ext = os.path.splitext(os.path.basename(keys[id]))[0]
                file_txt=basename_without_ext+'.txt'
                s3.meta.client.download_file('hot-dog-images', 'files/'+basename_without_ext+'.txt', 'download_client/'+basename_without_ext+'.txt')
                with open('download_client/'+basename_without_ext+'.txt', "a") as file:
                    file.write(str(valide)+"\n")
                my_bucket.upload_file('download_client/'+basename_without_ext+'.txt', f"files/{file_txt}")

                if os.path.exists("./download_client/"+keys[id]):
                    os.remove("./download_client/"+keys[id])
                    os.remove("./download_client/"+file_txt)
                else:
                    print("The file does not exist")
                i=i+1
                if i>3: break
    elif choice == 2:
        local_upload_directory = r"./upload_client/"
        for image in os.listdir(local_upload_directory):
            full_upload_path = os.path.join(local_upload_directory, image)
            print(f"uploading {full_upload_path} to {image}")
            my_bucket.upload_file(full_upload_path, f"{image}")
            image_without_ext = os.path.splitext(os.path.basename(image))[0]
            s3.Object("hot-dog-images", 'files/'+image_without_ext+'.txt').put(Body=b'')
            print(f"done uploading {full_upload_path} to {image}\n")
    else:
        print('end of Apps AWS')
        break
    input("press any key to continue")
