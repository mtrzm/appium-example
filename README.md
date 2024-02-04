# Running the project

## Requirements
* MacOS >=11
* Python 3.12
* [Appium driver](https://github.com/appium/appium-mac2-driver)
* [Allure](https://allurereport.org/docs/gettingstarted-installation/)

# Task

## Task
Create a Test script:
1. Start any Image Editing application for desktop that can import & export images with different formats (ex. Paint)
2. Import Image: IMAGE_1
3. Verify with image comparison that the imported Image looks correctly in the Image Editor
4. Export the Image in JPG format to a local drive
5. Verify that the exported image exists
6. Verify with image comparison whether the exported image is equal to IMAGE_2 (to be failed)
7. Generate an error report 

> Optional: Visually represent the differences between the images in the error report

## Requirements
* Use Python, Pytest, and any automation tool for desktop applications
