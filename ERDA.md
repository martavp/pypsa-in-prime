# Moving files between ERDA and PRIME
-----------------

ERDA or Electronic Research Data Archive at Aarhus University (AU) is meant for storing, sharing, analyzing and archiving research data. You can upload your files from PRIME directly into ERDA to save disc space on the cluster. 

----------------

## Setting up ERDA


#### 1. Get access to ERDA
Go to https://erda.au.dk/ and sign up with your AU account. Read the manuals to familiarize yourself with ERDA.

#### 2. Set up SFTP
The easiest way to upload files to ERDA from the PRIME cluster is using the SFTP protocol. On your homepage, click on the profile icon (bottom left) and go to 'setup'. Choose 'SFTP' option from the top row and choose a password for connecting to ERDA, then save the SFTP settings.


#### 3. Connect to ERDA from PRIME
log on to PRIME from your terminal and connect to ERDA with the below command :

  sftp -P 2222 (your user name here)@io.erda.au.dk
  
Port number is usually 2222. You can find your port number and username under 'login details' on the SFTP setup page on ERDA. The username is usually your email address, i.e. : pr@mpe.au.dk  
  
#### 4. Moving files to ERDA
To navigate PRIME and ERDA after connecting with SFTP, use cd for changing directory on ERDA, and 'lcd' for changing directory on PRIME. The 'l' can be added to al commands to indicate that they must be run on the local directory.
Let's say you want to move files from the /home/com/meenergy/data/pypsa_networks folder on PRIME to a new folder we call "private" on ERDA:

  connected to io.erda.au.dk
  
  sftp> lpwd
  
  Local working directory: /home 
  
  sftp> lcd com/meenergy
  
  sftp> lpwd
  
  Local working directory: /home/com/meenergy/data/pypsa_networks
  
  sftp> mkdir private # create folder on ERDA
  
  sftp> cd private # access folder on ERDA in which data from PRIME will be located
  

#### 5. Upload/download files
You can use the 'put' command to upload files or whole directories directly to ERDA :

   put postnetworks_Base/postnetwork-go_TYNDP_2020.nc # upload single file to ERDA from PRIME
   
   put -r postnetworks_Base/ # upload repository to ERDA from PRIME
   
You can also download files from ERDA to PRIME using the 'get' command.
#### Close the connection
Type 'bye' or 'quit' in the terminal to quit the SFTP.
#### Further reading
Read this guide on SFTP for more information : https://linuxize.com/post/how-to-use-linux-sftp-command-to-transfer-files/?utm_content=cmp-true
