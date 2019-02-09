### This tooling is inactive at the moment, please don't work on or send any data.

> Once we have finished more work on InstaPy, we will come back to this.

---

# instapy-gender-classification

In order to be able to add a general gender classification to InstaPy (even if you don't have a Business Account), we are evaluating some machine learning techniques to test if there is a possibility that we can classify profiles by their gender only given their way of writing a bio, the descriptions on their posts and some other features.    
Therefore we need a lot of data, this tool gives you an easy way to browse profiles based on tags.   
For every profile the tool will ask you whether you know if it is a male, female or not defineble person (like business pages, e.g. Bike shops)

> There will be a part about the tested approaches added once we have more data and can get some insights.

### Getting Started
```bash
1. git clone https://github.com/timgrossmann/instapy-gender-classification.git
2. cd instapy-gender-classification
3. pip install .
or
3. python setup.py install
```
4. Download ```chromedriver``` for your system [from here](https://sites.google.com/a/chromium.org/chromedriver/downloads). And put it in ```/assets``` folder (create the folder if not there).

### Starting the tool
> Please make sure to use python2

Once you've installed the dependencies and put the chromedriver in the assets folder you can simply start the tool by moving there with the command line. (After you've installed everything, you should already be in the right directory)

```bash
python classify_profiles.py <list_of_tags>
```

e.g.
```bash
python classify_profiles.py fun good car shoes nature food
```

### How to classify?
There are 3 classes:
- `m` (male)
- `f` (female)
- `x` (third gender)
- `-` (none - company, products etc.)

When the script asks you to enter the gender of the profile, choose one of the above mentioned letters.

> Note: the letter `x` is meant to be used for e.g. shops and other business that definitely don't have any gender.
I came across a bike shop. This definitely is profile that should be classified with an `x`.

### Contributing your classifications
Your gathered data is important! This is the key outcome of this tool which will help us build a AI model that can predict the gender of a person based on it's profile page.

**If you have a gmail account** you can run:
```bash
python sendData.py
```
To speed up the process, type your email and password in the file sendData.py

If you **do not** have a gmail account:  
The content of the `logs` folder represents the by you classified profiles.
Please send me an email to contact.timgrossmann@gmail.com with all of the json files you have in your `logs` folder.

##### Thank you very much for contributing to InstaPy!
