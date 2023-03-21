

## Synapse Team

Our app-"EduKare" aims to solve this issue, by providing  interactive MCQ quizzes  based on vast variety and sea of educational YouTube content, along with a personal recommendation model, along with focus on inclusivity for deaf and dumb students, to make learning more interesting and engaging. 

This allows users to learn from YouTube content as well as assess their learning and maintain their attention in learning content, instead of just wandering off from their minds.while watching non-interactive educational content from YouTube.  We have also trained a deaf sign language website to curate content for education of both signers nad non-signers, and reducing communication gap among students so as to achieve an inclusive for environment in classes
## Implementation Details:

The current version of personalised app is implemented using youtube-dl library to generate YouTube video transcript,qnd then BERT's model for text summarization, some NLP preprocessing that involves tokenizing, removing stopwords, lemmatization, etc, then then using transformers to generate questions based on the text contexts, The questions are then used to generate MCQ options using wordsense. The current implementation of app is generating quizzes, and shown in the react app as a separate entity, but can also be implememted to add the questions after specific timestamps as popups. We have also trained  a personalised video recommendation model based on average ratings of user, which can be integrated inside the app.
The sign language video api translates real time sign language content for non signers, and the second api, text to video api will be helpful for curating content for deaf and dumb students, so that they can have more learning content. The current MVP of app also restricts harmful or distractive/ sensitive content based on tags based search mechanism in home page of app


## Usage


1. Clone this dictionary.
2. Activate VIRTUAL ENV BY ./venv/Scripts/activate
```python
pip install -r requirements.txt

```

To activate the frontend, follow these steps:

Node
Node is really easy to install & now include NPM. You should be able to run the following command after the installation procedure below.

$ node --version
v0.10.24

$ npm --version
1.3.21
Node installation on OS X
You will need to use a Terminal. On OS X, you can find the default terminal in /Applications/Utilities/Terminal.app.

Please install Homebrew if it's not already done with the following command.

$ ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
If everything when fine, you should run

brew install node
Node installation on Linux
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
Node installation on Windows
Just go on official Node.js website & grab the installer. Also, be sure to have git available in your PATH, npm might need it.

Install
$ git clone https://github.com/ORG/PROJECT.git
$ cd PROJECT
$ npm install


Start & watch
$ npm start
Simple build for production
$ npm run build