# Ibislayer
Welcome to the ReadMe file for our Git repo

This file will act as a guideline for how to access/edit/update/etc files for our project

IMPORTANT NOTE

When some projects are created they may be initialised with the SIMULATOR instead of the ICD3 for debugging. Please check this (project settings) before spending an hour trying to debug nothing

Also, during testing we're using the PIC18F452 boards so don't worry too much at the moment about how the PIC18F4520 differs, we'll deal with this a little later - so when creating projects and choosing which board to use, make sure to select the PIC18F452 (at least for now - this will be updated as any changes come through)

Intro to Git

Download the terminal

Download and install Git

Run a terminal (eg. iterm for Mac or git bash for Windows) after Git is installed and then continue

Navigate

Navigate to the directory on your computer that you want to store a copy of the repository on

If you're using a terminal, navigate to the directory by using:

cd <directory>
You can use ls to show the contents of the current directory

Initialise Git

Initialise an empty Git repo with the command:

git init
Cloning

Cloning is making a local copy of the Git repo

You can make changes to this copy and they remain "local" until they are "pushed/synced" to the remote repository (pushed using git bash terminal or synced using the git gui)

In order to clone you need the URL of the main repo (given below)

Clone the repo with the command:

git clone https://github.com/taklpw/Ibislayer

If you get any errors at this stage it means you haven't been added as a collaborator to the repo yet - send Jason your Github account name and he will add you to the repo as a collaborator

Go into the local repo (the clone you just made)

Enter the following command:

cd Ibislayer
Branching

Go to Atlassian's Git Branches Tutorial and checkout their tutorial on how to branch before you continue (for your own benefit)

A branch is an independent line of development; we will use them to test and write our modules in parallel before merging them back into the master

To list all of the branches in the repo, enter:

git branch
We'll use a naming convention to ensure we know who created the branch

Try and keep the branch name clear and simple so we know what it's for without it being a novel

Eg. "taylor/desktop" is the branch Marty has created to work on the RF module

To create a new branch called , enter:

git branch <branch name>
At any point in time you can check which branch you're currently on with the command:

git status
This will also tell you if there's anything waiting to be committed (more on that later)

At this stage, even though you have created a new branch you're still on the 'master' branch

To navigate to your newly created branch (or any other branch), enter:

git checkout <branch name>
Notice your local repo (the clone) will change to show what is in your current branch

Your branch will initialise to the state of the master at the time the branch was created

Now you can work on your branch

Committing changes

Committing a change is the act of locking it in at a local level

This is a two-step process; staging and committing

To stage all your changes, enter:

git add *
To commit these changes, enter:

git commit -m "<your name>: <A brief message about the changes>"
At the moment these changes are only local

Syncing local and remote repos

The changes you have made so far are only local to your machine

In order to update the online repo we have to "push" these changes

(the term 'push' may sometimes be replaced with 'sync' but they mean the same thing - the terminal uses the command push whereas the git gui uses a clickable sync option)

To push your changes to the online repo using the terminal, enter:

git push origin <branch name>
It is important to include the correct branch name here to ensure your changes don't overwrite a different branch

Check the online repo

Log into Github and navigate to the repo

Select your branch from just above and to the left of the file list

The files should be updated to reflect any changes you have made and the message you wrote in Step 6 is displayed next to any updated files, as well as the time of the most recent commit for each updated file/folder

Buy Marty and Jason a beer

It's just a nice thing to do

CODING CONVENTIONS

For the purposes of clarity and simplicity, each module is given an abbreviation to use for the conventions listed below. You can create your own abbreviation or use the recommended ones from below:

RF module: "rf"

UI module: "ui"

Control module: "ctl"

Path planning module: "pp"

All examples below are for the RF module

Filenames:

<module>.c or <module>.h

eg.

rf.c or rf.h

Functions:

<module>UpperCaseFirstLetters();
eg.

rfTransmit();
Defines:

UPPER_CASE_WORDS
eg.

CLEAR_PORTB
Variables:

lower_case_words
eg.

transmit_buffer
Parentheses:

rfSomeFunction(param) {

	// code goes here

}

DOXYGEN REQUIREMENTS

All code found in the master must be Doxygen commented

A doxygen template can be found on the master, 'doxygen_c.h' read through this sometime and integrate it with all of your code as you go

Any merges will be rejected until the code in them has been Doxygen commented inline with the Doxygen template

The Doxygen template won't be active until Friday - if you have code ready before then, please update it after Friday to bring it up to standard, do not use the Doxygen template there currently as it will be replaced and updated so your commenting will be out-of-date

Top Secret Password

If you're reading this, let Jason or Marty know by saying the word "BANANARAMA"

Check for updates over time as the file is updated on occasion
