# BowVision

# Description: 
Program that uses the webcam and draws out a line representing bow movement, ultimately helping musicians to visualize their their bow placement. This not only helps with artistry, as we are better able to see the different angles and dips that we make with the string, but also helps with releasing tension in the arm (a major problem in bow technique), as we can concentrate on creating a certain shape rather than trying to relax taught muscles.

# How It Works:
This program uses the webcam as a medium to take in the "pixels" reflected from the image and transfer into the model, where the bow is then detected. After this is done, I locate the position of the bow and draw a line that connects the bow detected in the previous frame to the bow in the current frame. This creates a continous line that reflects bow movement.

# Difficulties Faced
My first model was created from 100 random internet pictures of the bow. This model later proved to not only have an insufficient amount of picture to have an accurate recognition of the bow, but that the "random" images weren't of good quality and thus, encroached upon the quality of the model. With this I tripled the number of pictures and raised my bar of "quality" for the pictures. The quality I'm talking about refers to the blurriness, hue, lighting, angle and position of the bow. With this new set of photos, my updated model was able to detect the bow with relatively good acccuracy (ex: 0.89, 0.91 etc) and draw a line.


