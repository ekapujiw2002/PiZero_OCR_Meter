# Gas Meter Reading Recognition Project

## Raspberry Pi Zero Configuration

### OpenCV setup
Initial project included the use of OpenCV 3 with Python3 bindings on Raspian OS. A detailed tutorial for installing can be found [here](http://www.pyimagesearch.com/2015/10/26/how-to-install-opencv-3-on-raspbian-jessie/).

### Other dependencies
- [Numpy](http://www.numpy.org/) (should be installed together with the OpenCV python bindings)
- [scikit-learn](http://scikit-learn.org/stable/) for machine learning algorithms
- [MNIST dataset](http://yann.lecun.com/exdb/mnist/)
- [Python Image Library (PIL)](https://python-pillow.org/)

### Wi-fi setup
The wifi connection can be set up from the Raspian GUI while the device is running.

Alternatively, SSID and password pairs can be manually introduced into the WPA supplicant configuration file (located at "/etc/wpa_supplicant/wpa_supplicant.conf"). Note that any password of less than 8 characters will break this file (making it unable to be parsed).

## Obtaining a reading
Note that as work focused on finding a suitable digit classification algorithms, the following approaches have not been tested on the Raspberry Pi Zero. The scripts were created and tested on macOS Sierra.

### Digit classifiers

Trained on the MNIST dataset (or subsets thereof), these 3 approaches require the user to individually select the digits using the web interface. Based on the selected areas of the image, each individual digit is pre-processed and classified by the three models. Is it worth nothing that all classification methods are very sensible to noise.

The command to loop over the dataset using pre-defined configuration files is show below. The digitRecog.py program shows the accuracy of the following 3 approaches to classification, when given a file containing labels for the dataset.

The script looks for 2 configuration files (examples configured for the dataset are included in the PyMeterReader directory):
- config.txt
  - containing the 4 points used to determine the region of interest
- digitConfigs/digit\_config\_[number of digit].txt
  - containing the 4 points used to determine an individual digit in the warped image

```
python3 digitRecog.py -d ../../Datasets/30JulyDistinct/ --label ../../Datasets/30JulyDistinct/labels.txt  --flip
```

Output for the final image and the overall accuracy for the dataset can be seen in the screenshow below:
![Output](https://i.imgur.com/3sO4kdU.png)


#### kNN (k nearest neighbours)

Uses [sklearn's implementation](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html) of a kNN classifier. The MNISTclassif class contains code adapted from [this pyimagesearch tutorial](https://gurus.pyimagesearch.com/lesson-sample-k-nearest-neighbor-classification/).

The class looks for a trained model (in the file "digits_model_knn.pkl") during its initialisation and will otherwise train one using the MNIST dataset and, in the process, chose the k-value yielding the best accuracy.

#### SVM (support vector machine)

Uses sklearn's [linear SVM implementation trained](http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html) on the MNIST dataset. Code is based on the above-mentioned tutorial.

Similar to the previous approach, the class looks for a pre-trained model (in the file "digits_model_linearSVC.pkl"). If this is not found, a new model is trained. The training process is longer than that of the kNN classifier.

#### ANN (artificial neural network)

The implemented classifier is based on the [tutorial](https://www.tensorflow.org/get_started/mnist/pros) given on tensorFlow website, that uses the MNIST dataset for training. Using the resulting model, each image is fed in and the resulting prediction used, based on another [tutorial](https://niektemme.com/2016/02/21/tensorflow-handwriting/) for obtaining predictions on new data.

### Tesseract OCR Recognition

Work done using this can be found under the TesseractOCR directory. Based on the  TensorFlow [deep neural network tutorial](https://www.tensorflow.org/get_started/mnist/pros) that is trained on the MNIST dataset, this approach yields a higher accuracy. Further improvements could focus on better image pre-processing (to better mimic that of the MNIST dataset)

Available parameters are described by the help menu
```
python3 tesseractRecog.py -h
```

Example command to run the recognition software on the dataset and measure its accuracy based on predefined labels
```
python3 tesseractRecog.py -d ../Datasets/30JulyDistinct/ --label ../Datasets/30JulyDistinct/labels.txt --f -bs 81 -c 5
```
Similar to the other approaches, the script looks for 2 configuration files, however as TesseractOCR reads a whole line, individual digits need not be separated (examples configured for the dataset are included in the script's directory):
- config.txt
  - containing the 4 points used to determine the region of interest
- lineConfigs/line\_config\_[line number].txt
  - containing the 4 points used to determine an individual line


![Output](https://i.imgur.com/zBESZzt.png)

Directory structure of the project for reference (as example commands used with relative paths)
```
.
├── Datasets
│   ├── 30JulyClean
│   ├── 30JulyDistinct
│   ├── Raw-Images
│   └── curated
├── meterReader
│   ├── CharIoT
│   ├── MeterPictures
│   ├── PyMeterReader
│   ├── TesseractOCR
│   ├── tutorials
│   └── utils
├── sensors
│   └── TestInfluxDB
├── webInterface
│   └── WebInt
└── website
    ├── Bootstrapped
    └── CharIoT-Reference
```

### Hardware setup

- [Raspberry Pi Zero W](https://shop.pimoroni.com/products/raspberry-pi-zero-w)
	- Running Raspian OS as included on the [NOOBS](https://www.raspberrypi.org/documentation/installation/noobs.md) starter memory card
- [Camera Module for Pi Zero](https://shop.pimoroni.com/products/raspberry-pi-zero-camera-module)
 - LED lights were used to light the gas meter in the included dataset. The version without the IR filter could be used in conjunction with IR lights.
 - Camera specification is identical to that of the [Raspberry Pi Camera Module V1](https://www.raspberrypi.org/documentation/hardware/camera/)

## Web interface

As the device would be static when taking pictures, and as detecting digits in the unprocessed image proved to be too difficult, a barebones web interface was made. It allows the user to select the area of the image in which the meter is present, as well as each individual digit.

The web page uses forms to trigger PHP script, that, in turn, use system calls to take images or python3 scripts to perform operations on images with OpenCV. (if they don't seem to work on Apache2, make sure the [server executes php scripts](https://askubuntu.com/questions/451708/php-script-not-executing-on-apache-server); also check the folder permissions)


## Dataset
In order to capture images from the camera, the [raspistill](https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md) utility was used within the "capture.sh" script, which was executed every 5 minutes by use of cron. The images are saved with the format ""<timestamp>.png" in the "/home/pi/webcam/" directory

The dataset contains range of images captured between 12:10 24.07.2017 and 10:15 27.07.2017 at 5 minute intervals using the Raspberry Pi Zero's camera and the LED light board.

![Image before move](https://i.imgur.com/n933ZiV.jpg)

Images showing distinct meter readings have been manually selected and can be found, together with labels, in the 30JulyDistinct directory. This is further split into images captured before and after a small movement of the device at ~5:30 on 25.07.2017, as the scripts below assume the sensor has a static location and cannot currently correct for movement.

![Image after move](https://i.imgur.com/cZGuzLr.jpg)

Dataset can be downloaded from [this link](https://www.dropbox.com/s/w3qr1bwl98g4s4t/Dataset-Curated.zip?dl=0).

## Misc links

##### TensorFlow
[MNIST convolutional classifier tutorial](https://www.tensorflow.org/get_started/mnist/pros)
<br>
[How to extract prediction from trained model](	https://stackoverflow.com/questions/33711556/making-predictions-with-a-tensorflow-model)
<br>
[Saving and restoring variables](https://www.tensorflow.org/programmers_guide/variables)

##### Raspberry Pi Zero Tweaks
[Remote Control Windows]( https://askubuntu.com/questions/405916/open-a-window-in-a-remote-machine)
<br>
[Boot time scripts](	https://www.cyberciti.biz/tips/linux-how-to-run-a-command-when-boots-up.html)
<br>
[SSH over USB](	https://www.thepolyglotdeveloper.com/2016/06/connect-raspberry-pi-zero-usb-cable-ssh/)
<br>
[Cron webcam tutorial](https://www.raspberrypi.org/documentation/usage/webcams/)
<br>

##### Possible troubleshooting links:

[Give php access to directory](https://stackoverflow.com/questions/2900690/how-do-i-give-php-write-access-to-a-directory) <br>
[Copy files without confirmation]( https://stackoverflow.com/questions/8488253/how-to-force-cp-to-overwrite-without-confirmation) <br>
[Fix for failing to open vchiq instance](https://digitalchild.info/raspberry-pi-failed-open-vchiq-instance-solved/)<br>
[Setup as AP](	https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/overview) <br>
[Let sudo script run w/o password:]( https://askubuntu.com/questions/167847/how-to-run-bash-script-as-root-with-no-password)

To open windows on remote session:
	xhost + (on remote machine)
	export DISPLAY=:0 (on current shell)
