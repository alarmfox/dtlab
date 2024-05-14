# Webex Chatbot Lab

## Introduction
Welcome to the Webex Chatbot Lab! In this lab, you will create a simple chatbot using the Webex API. You will start with a starter file that provides basic functionality, and your task will be to extend it by adding new commands.

## Prerequisites
Before you begin, make sure you have the following:
- Basic knowledge of Python programming language
- Familiarity with Flask framework
- A Webex account and access to the Webex API
- Python and Flask installed on your computer

## Installing Dependencies

Before you start working on the lab tasks, you need to install the required Python dependencies. These dependencies are listed in a `requirements.txt` file. Follow the instructions below to install the dependencies:

1. **Navigate to the Project Directory**: Open a terminal or command prompt and navigate to the directory where your project files are located.

2. **Install Dependencies**: Run the following command to install the dependencies using pip:

```bash
   pip install -r requirements.txt
```

## Lab Tasks

Your main task is to extend the functionality of the chatbot by adding new commands. You can refer to the provided functions and existing commands as examples.

### Task 1: Add Command to Send Cat Images
Your first task is to add a command that allows the chatbot to send cat images to users. You can use the [Cataas API](https://cataas.com/cat) to fetch cat images.
With this simple script you can save the image as a `png`:
```python
r = requests.get("https://cataas.com/cat")
with open("out.png", "wb") as f:
    f.write(r.content)
```
Use [this article](https://developer.webex.com/docs/basics), to understand how to send attachments to a Webex message.
### Task 2: Add More Commands (Optional)
If you finish Task 1 quickly and want to further enhance your chatbot, you can add more commands of your choice. For example, you can add commands to fetch jokes, weather updates, or news articles.

webhook: Y2lzY29zcGFyazovL3VzL1dFQkhPT0svZWExNGI1ZWQtMjQ1Ni00ZDNkLTk0ZDAtOTZhYjY1ZWRkNTEx
