# Python-AOI-UI
In this repository you will find this solution I developed to replace an AOI, is very generic so you could modify the method of inspection and where you want to inspect what, initially was build to inspect glue but you could use it for your own purposes.

This can also be used to sort certain images located in a folder or subfolders of a location.
as includes the "offline" option this means we go through all the folder looking for the pictures or "online" meaning it will keep constant monitoring a given folder for new images to inspect.

<img width="2200" height="1463" alt="image" src="https://github.com/user-attachments/assets/1412e280-b86c-498d-9094-3306e67e486d" />
<img width="2202" height="1459" alt="image" src="https://github.com/user-attachments/assets/30709af1-8047-471a-9739-4af3b25c8c5f" />

I included a configuration tab to:
Modify the path where the main configuration is found(this means the threshold for inspection, model equivalences and other configurations required to read the json where the coordinates of the ROI are)
Assign a folder where all the logs will be saved (the main.py saves the picture when detects an annomaly )
Select the path where all the ROI coordinates are found
Select the path where all the pictures to inspect will be

<img width="2204" height="1459" alt="image" src="https://github.com/user-attachments/assets/a67338ee-bb64-4830-a10a-155bfa898b60" />







