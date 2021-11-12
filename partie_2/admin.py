import boto3
import os
client=boto3.client('s3')
s3 = boto3.resource('s3')
my_bucket = s3.Bucket("hot-dog-images")
local_upload_directory = r"./upload_server/"
local_download_directory = r"./download_server/"

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
    print("            ----------------                  ")
    print("              Menu Serveur                    ")
    print("            ----------------                  ")
    print("----------------------------------------------")
    print(" Upload images                             <1>")
    print(" Statistiques (Hot-Dogs)                   <2>")
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

    #choice upload
    if choice == 1:
        #upload all images that are in the local folder named the upload-server
        for image in os.listdir(local_upload_directory):
            full_upload_path = os.path.join(local_upload_directory, image)
            print(f"uploading {full_upload_path} to {image}")
            my_bucket.upload_file(full_upload_path, f"{image}")
            image_without_ext = os.path.splitext(os.path.basename(image))[0]
            s3.Object("hot-dog-images", 'files/'+image_without_ext+'.txt').put(Body=b'')
            print(f"done uploading {full_upload_path} to {image}\n")
    #choice statistics
    elif choice == 2:
        #download all text files that are in the s3 bucket and calculate the statistics of user's choices
       for file in my_bucket.objects.filter(Prefix="files/"):
           if file.key.endswith(".txt"):
                local_file_name = os.path.join(local_download_directory, file.key.split("/")[1])
                my_bucket.download_file(file.key, local_file_name)
                file = open(local_file_name, 'r')
                Lines = file.readlines()
                #sum the 0 label
                p0=0
                #sum the 1 label
                p1=0
                #count the number of lines
                count = 0
                for line in Lines:
                    count += 1
                    if int(line.strip()) == 0:
                        p0+=1
                    else:
                        p1+=1
                #show the statistics in the command line
                print('-------------------------------------')
                print("Images: "+local_file_name.split("/")[2].split(".")[0]+".jpg")    
                if count != 0:
                    percent0=round(((100*p0)/count),2)
                    percent1=round(((100*p1)/count),2)                    
                    print("Hot-Dogs: "+str(percent0)+" % | Others: "+str(percent1)+" %")
                else:
                    print("File empty!")
                print('-------------------------------------')

    #choice quit
    else:
        print("3")
        break
    input("press any key to continue")        